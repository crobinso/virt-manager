#
# XML API wrappers
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA.

import builtins
import functools
import logging
import re
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

# lxml is a drop in replacement for ElementTree that is widely used.
# However it uses libxml2 behind the scenes, and if distro versions
# are compiled against a system libxml2, lxml usage collides with
# libvirt usage and results in segfaults:
# https://bugzilla.redhat.com/show_bug.cgi?id=1544019
# import lxml.etree as ET
import libxml2

from . import util

# pylint: disable=protected-access

if "lxml.etree" not in str(ET):
    # Hackery to make stock python ElementTree not alphabetize XML
    # attributed. We basically stub out the global 'sorted' method
    # when ElementTree is serializing XML.
    _origsorted = builtins.sorted
    def _fake_sorted(obj, **kwargs):
        ignore = kwargs
        return obj

    _origserialize = ET._serialize_xml
    @functools.wraps(_origserialize)
    def _fake_serialize(*args, **kwargs):
        try:
            ET.__builtins__["sorted"] = _fake_sorted
            return _origserialize(*args, **kwargs)
        except Exception:
            ET.__builtins__["sorted"] = builtins.sorted
            logging.debug("Error with ElementTree hackery, "
                    "attempting fallback", exc_info=True)
            return _origserialize(*args, **kwargs)
    ET._serialize_xml = _fake_serialize

    _origwritexml = minidom.Element.writexml
    @functools.wraps(_origwritexml)
    def _fake_writexml(*args, **kwargs):
        try:
            ET.__builtins__["sorted"] = _fake_sorted
            return _origwritexml(*args, **kwargs)
        except Exception:
            ET.__builtins__["sorted"] = builtins.sorted
            logging.debug("Error with minidom hackery, "
                    "attempting fallback", exc_info=True)
            return _origwritexml(*args, **kwargs)
    minidom.Element.writexml = _fake_writexml


class _XPathSegment(object):
    """
    Class representing a single 'segment' of an xpath string. For example,
    the xpath:

        ./qemu:foo/bar[1]/baz[@somepro='someval']/@finalprop

    will be split into the following segments:

        #1: nodename=., fullsegment=.
        #2: nodename=foo, nsname=qemu, fullsegment=qemu:foo
        #3: nodename=bar, condition_num=1, fullsegment=bar[1]
        #4: nodename=baz, condition_prop=somepro, condition_val=someval,
                fullsegment=baz[@somepro='somval']
        #5: nodename=finalprop, is_prop=True, fullsegment=@finalprop
    """
    def __init__(self, fullsegment):
        self.fullsegment = fullsegment
        self.nodename = fullsegment

        self.condition_prop = None
        self.condition_val = None
        self.condition_num = None
        if "[" in self.nodename:
            self.nodename, cond = self.nodename.strip("]").split("[")
            if "=" in cond:
                (cprop, cval) = cond.split("=")
                self.condition_prop = cprop.strip("@")
                self.condition_val = cval.strip("'")
            elif cond.isdigit():
                self.condition_num = int(cond)

        self.is_prop = self.nodename.startswith("@")
        if self.is_prop:
            self.nodename = self.nodename[1:]

        self.nsname = None
        if ":" in self.nodename:
            self.nsname, self.nodename = self.nodename.split(":")


class _XPath(object):
    """
    Helper class for performing manipulations of XPath strings. Splits
    the xpath into segments.
    """
    def __init__(self, fullxpath):
        self.fullxpath = fullxpath
        self.segments = [_XPathSegment(s) for s in self.fullxpath.split("/")]

        self.is_prop = self.segments[-1].is_prop
        self.propname = (self.is_prop and self.segments[-1].nodename or None)
        if self.is_prop:
            self.segments = self.segments[:-1]
        self.xpath = self.join(self.segments)

    @staticmethod
    def join(segments):
        return "/".join(s.fullsegment for s in segments)

    def parent_xpath(self):
        return self.join(self.segments[:-1])


class _XMLBase(object):
    NAMESPACES = {
        "qemu": "http://libvirt.org/schemas/domain/qemu/1.0",
    }

    def copy_api(self):
        raise NotImplementedError()
    def count(self, xpath):
        raise NotImplementedError()
    def _find(self, fullxpath):
        raise NotImplementedError()
    def _node_tostring(self, node):
        raise NotImplementedError()
    def _node_get_text(self, node):
        raise NotImplementedError()
    def _node_set_text(self, node, setval):
        raise NotImplementedError()
    def _node_get_property(self, node, propname):
        raise NotImplementedError()
    def _node_set_property(self, node, propname, setval):
        raise NotImplementedError()
    def _node_new(self, xpathseg):
        raise NotImplementedError()
    def _node_add_child(self, parentxpath, parentnode, newnode):
        raise NotImplementedError()
    def _node_remove_child(self, parentnode, childnode):
        raise NotImplementedError()
    def _node_from_xml(self, xml):
        raise NotImplementedError()
    def _node_has_content(self, node):
        raise NotImplementedError()
    def node_clear(self, xpath):
        raise NotImplementedError()
    def _sanitize_xml(self, xml):
        raise NotImplementedError()

    def get_xml(self, xpath):
        node = self._find(xpath)
        if node is None:
            return ""
        return self._sanitize_xml(self._node_tostring(node))

    def get_xpath_content(self, xpath, is_bool):
        node = self._find(xpath)
        if node is None:
            return None
        if is_bool:
            return True
        xpathobj = _XPath(xpath)
        if xpathobj.is_prop:
            return self._node_get_property(node, xpathobj.propname)
        return self._node_get_text(node)

    def set_xpath_content(self, xpath, setval):
        node = self._find(xpath)
        if setval is False:
            # Boolean False, means remove the node entirely
            self.node_force_remove(xpath)
        elif setval is None:
            if node is not None:
                self._node_set_content(xpath, node, None)
            self._node_remove_empty(xpath)
        else:
            if node is None:
                node = self._node_make_stub(xpath)

            if setval is True:
                # Boolean property, creating the node is enough
                return
            self._node_set_content(xpath, node, setval)

    def node_add_xml(self, xml, xpath):
        newnode = self._node_from_xml(xml)
        parentnode = self._node_make_stub(xpath)
        self._node_add_child(xpath, parentnode, newnode)

    def node_force_remove(self, fullxpath):
        """
        Remove the element referenced at the passed xpath, regardless
        of whether it has children or not, and then clean up the XML
        chain
        """
        xpathobj = _XPath(fullxpath)
        parentnode = self._find(xpathobj.parent_xpath())
        childnode = self._find(fullxpath)
        if parentnode is None or childnode is None:
            return
        self._node_remove_child(parentnode, childnode)

    def _node_set_content(self, xpath, node, setval):
        xpathobj = _XPath(xpath)
        if setval is not None:
            setval = str(setval)
        if xpathobj.is_prop:
            self._node_set_property(node, xpathobj.propname, setval)
        else:
            self._node_set_text(node, setval)

    def _node_make_stub(self, fullxpath):
        """
        Build all nodes for the passed xpath. For example, if XML is <foo/>,
        and xpath=./bar/@baz, after this function the XML will be:

          <foo>
            <bar baz=''/>
          </foo>

        And the node pointing to @baz will be returned, for the caller to
        do with as they please.

        There's also special handling to ensure that setting
        xpath=./bar[@baz='foo']/frob will create

          <bar baz='foo'>
            <frob></frob>
          </bar>

        Even if <bar> didn't exist before. So we fill in the dependent property
        expression values
        """
        xpathobj = _XPath(fullxpath)
        parentxpath = "."
        parentnode = self._find(parentxpath)
        if parentnode is None:
            raise RuntimeError("programming error: "
                "Did not find XML root node for xpath=%s" % fullxpath)

        for xpathseg in xpathobj.segments[1:]:
            oldxpath = parentxpath
            parentxpath += "/%s" % xpathseg.fullsegment
            tmpnode = self._find(parentxpath)
            if tmpnode is not None:
                # xpath node already exists, nothing to create yet
                parentnode = tmpnode
                continue

            newnode = self._node_new(xpathseg)
            self._node_add_child(oldxpath, parentnode, newnode)
            parentnode = newnode

            # For a conditional xpath like ./foo[@bar='baz'],
            # we also want to implicitly set <foo bar='baz'/>
            if xpathseg.condition_prop:
                self._node_set_property(parentnode, xpathseg.condition_prop,
                        xpathseg.condition_val)

        return parentnode

    def _node_remove_empty(self, fullxpath):
        """
        Walk backwards up the xpath chain, and remove each element
        if it doesn't have any children or attributes, so we don't
        leave stale elements in the XML
        """
        xpathobj = _XPath(fullxpath)
        segments = xpathobj.segments[:]
        parent = None
        while segments:
            xpath = _XPath.join(segments)
            segments.pop()
            child = parent
            parent = self._find(xpath)
            if parent is None:
                break
            if child is None:
                continue
            if self._node_has_content(child):
                break

            self._node_remove_child(parent, child)


class _Libxml2API(_XMLBase):
    def __init__(self, xml):
        _XMLBase.__init__(self)
        self._doc = libxml2.parseDoc(xml)
        self._ctx = self._doc.xpathNewContext()
        self._ctx.setContextNode(self._doc.children)
        for key, val in self.NAMESPACES.items():
            self._ctx.xpathRegisterNs(key, val)

    def __del__(self):
        self._doc.freeDoc()
        self._doc = None
        self._ctx.xpathFreeContext()
        self._ctx = None

    def _sanitize_xml(self, xml):
        # Strip starting <?...> line
        if xml.startswith("<?"):
            ignore, xml = xml.split("\n", 1)
        if not xml.endswith("\n") and "\n" in xml:
            xml += "\n"
        return xml

    def copy_api(self):
        return _Libxml2API(self._doc.children.serialize())

    def _find(self, fullxpath):
        xpath = _XPath(fullxpath).xpath
        node = self._ctx.xpathEval(xpath)
        return (node and node[0] or None)

    def count(self, xpath):
        return len(self._ctx.xpathEval(xpath))

    def _node_tostring(self, node):
        return node.serialize()
    def _node_from_xml(self, xml):
        return libxml2.parseDoc(xml).children

    def _node_get_text(self, node):
        return node.content
    def _node_set_text(self, node, setval):
        if setval is not None:
            setval = util.xml_escape(setval)
        node.setContent(setval)

    def _node_get_property(self, node, propname):
        prop = node.hasProp(propname)
        if prop:
            return prop.content
    def _node_set_property(self, node, propname, setval):
        if setval is None:
            prop = node.hasProp(propname)
            if prop:
                prop.unlinkNode()
                prop.freeNode()
        else:
            node.setProp(propname, util.xml_escape(setval))

    def _node_new(self, xpathseg):
        newnode = libxml2.newNode(xpathseg.nodename)
        if not xpathseg.nsname:
            return newnode

        ctxnode = self._ctx.contextNode()
        for ns in util.listify(ctxnode.nsDefs()):
            if ns.name == xpathseg.nsname:
                break
        else:
            ns = ctxnode.newNs(
                    self.NAMESPACES[xpathseg.nsname], xpathseg.nsname)
        newnode.setNs(ns)
        return newnode

    def node_clear(self, xpath):
        node = self._find(xpath)
        if node:
            propnames = [p.name for p in (node.properties or [])]
            for p in propnames:
                node.unsetProp(p)
            node.setContent(None)

    def _node_has_content(self, node):
        return node.type == "element" and (node.children or node.properties)

    def _node_remove_child(self, parentnode, childnode):
        node = childnode

        # Look for preceding whitespace and remove it
        white = node.get_prev()
        if white and white.type == "text":
            white.unlinkNode()
            white.freeNode()

        node.unlinkNode()
        node.freeNode()
        if all([n.type == "text" for n in parentnode.children]):
            parentnode.setContent(None)

    def _node_add_child(self, parentxpath, parentnode, newnode):
        ignore = parentxpath
        def node_is_text(n):
            return bool(n and n.type == "text")

        if not node_is_text(parentnode.get_last()):
            prevsib = parentnode.get_prev()
            if node_is_text(prevsib):
                newlast = libxml2.newText(prevsib.content)
            else:
                newlast = libxml2.newText("\n")
            parentnode.addChild(newlast)

        endtext = parentnode.get_last().content
        parentnode.addChild(libxml2.newText("  "))
        parentnode.addChild(newnode)
        parentnode.addChild(libxml2.newText(endtext))


class _ETreeAPI(_XMLBase):
    for _k, _v in _XMLBase.NAMESPACES.items():
        ET.register_namespace(_k, _v)

    def __init__(self, parsexml):
        _XMLBase.__init__(self)
        self._et = ET.ElementTree(ET.fromstring(parsexml))

    #######################
    # Private helper APIs #
    #######################

    def _sanitize_xml(self, xml):
        return xml.replace(" />", "/>")

    def _node_tostring(self, node):
        return ET.tostring(node, encoding="unicode")

    def _node_from_xml(self, xml):
        return ET.fromstring(xml)

    def _node_get_text(self, node):
        return node.text
    def _node_set_text(self, node, setval):
        node.text = setval

    def _node_get_property(self, node, propname):
        return node.attrib.get(propname)
    def _node_set_property(self, node, propname, setval):
        if setval is None:
            node.attrib.pop(propname, None)
        else:
            node.attrib[propname] = setval

    def _find(self, fullxpath):
        xpath = _XPath(fullxpath).xpath
        node = self._et.find(xpath, self.NAMESPACES)
        if node is None:
            return None
        return node


    ###############
    # Simple APIs #
    ###############

    def copy_api(self):
        return XMLAPI(ET.tostring(self._et.getroot(), encoding="unicode"))

    def count(self, xpath):
        return len(self._et.findall(xpath, self.NAMESPACES) or [])


    ####################
    # Private XML APIs #
    ####################

    def _node_add_child(self, parentxpath, parentnode, newnode):
        """
        Add 'newnode' as a child of 'parentnode', but try to preserve
        whitespace and nicely format the result.
        """
        xpathobj = _XPath(parentxpath)

        if bool(len(parentnode)):
            lastelem = list(parentnode)[-1]
            newnode.tail = lastelem.tail
            lastelem.tail = parentnode.text
        elif xpathobj.parent_xpath():
            grandparent = self._find(xpathobj.parent_xpath())
            idx = list(grandparent).index(parentnode)
            if idx == (len(list(grandparent)) - 1):
                parentnode.text = (grandparent.text or "\n") + "  "
                newnode.tail = (parentnode.tail or "\n") + "  "
            else:
                parentnode.text = list(grandparent)[0].tail + "  "
                newnode.tail = list(grandparent)[0].tail
        else:
            parentnode.text = "\n  "
            newnode.tail = "\n"

        parentnode.append(newnode)

    def _node_has_content(self, node):
        return (len(node) or node.attrib or
            re.search(r"\w+", (node.text or "")))

    def _node_remove_child(self, parentnode, childnode):
        idx = list(parentnode).index(childnode)

        if idx != 0 and idx == (len(list(parentnode)) - 1):
            prevsibling = list(parentnode)[idx - 1]
            prevsibling.tail = prevsibling.tail[:-2]
        elif idx == 0 and len(list(parentnode)) == 1:
            parentnode.text = None

        parentnode.remove(childnode)

    def _node_new(self, xpathseg):
        newname = xpathseg.nodename
        if xpathseg.nsname:
            newname = ("{%s}%s" %
                    (self.NAMESPACES[xpathseg.nsname], newname))
        return ET.Element(newname)


    #####################
    # XML editting APIs #
    #####################

    def node_clear(self, xpath):
        node = self._find(xpath)
        if node is not None:
            for c in list(node):
                node.remove(c)
            node.attrib.clear()
            node.text = None


class _MinidomAPI(_XMLBase):
    def __init__(self, xml):
        _XMLBase.__init__(xml)
        self._doc = minidom.parseString(xml)

    def _sanitize_xml(self, xml):
        return xml
    def _node_tostring(self, node):
        return node.toxml("utf-8").decode("utf-8")
    def copy_api(self):
        return _MinidomAPI(self._node_tostring(self._doc.documentElement))

    def _xpath_lookup(self, fullxpath):
        xpathobj = _XPath(fullxpath)
        parent = self._doc.documentElement
        segments = xpathobj.segments[1:]

        def _find_segment_match(children, xpathseg, match_once):
            ret = []
            nodename = ""
            if xpathseg.nsname:
                nodename = xpathseg.nsname + ":"
            nodename += xpathseg.nodename

            condnum = xpathseg.condition_num
            if condnum:
                match_once = False

            for child in children:
                if (child.nodeType == child.ELEMENT_NODE and
                    child.nodeName == nodename):
                    if xpathseg.condition_prop:
                        pval = self._node_get_property(child,
                                xpathseg.condition_prop)
                        if pval != xpathseg.condition_val:
                            continue

                    if match_once:
                        return child
                    ret.append(child)

            if condnum:
                if condnum not in range(len(ret) + 1):
                    return None
                return ret[condnum - 1]

            return ret

        while segments:
            seg = segments[0]
            segments = segments[1:]
            parent = _find_segment_match(
                    parent.childNodes, seg, bool(segments))
            if not parent:
                break

        return util.listify(parent)

    def count(self, xpath):
        return len(self._xpath_lookup(xpath))
    def _find(self, fullxpath):
        nodes = self._xpath_lookup(fullxpath)
        return (nodes and nodes[0] or None)

    def _node_get_text(self, node):
        if node.childNodes:
            return node.childNodes[0].nodeValue
    def _node_set_text(self, node, setval):
        if setval is None:
            if node.childNodes:
                node.removeChild(node.childNodes[0])
        else:
            if node.childNodes:
                node.childNodes[0].nodeValue = setval
            else:
                text = self._doc.createTextNode(setval)
                node.appendChild(text)

    def _node_get_property(self, node, propname):
        if node.hasAttribute(propname):
            return node.getAttribute(propname)
    def _node_set_property(self, node, propname, setval):
        if setval is None:
            if node.hasAttribute(propname):
                node.removeAttribute(propname)
        else:
            node.setAttribute(propname, setval)

    def _node_new(self, xpathseg):
        nsname = xpathseg.nsname
        nodename = xpathseg.nodename
        if not nsname:
            return self._doc.createElement(nodename)

        nsurl = self.NAMESPACES[nsname]
        self._doc.documentElement.setAttribute("xmlns:%s" % nsname, nsurl)
        return self._doc.createElementNS(nsurl, nsname + ":" + nodename)

    def _node_add_child(self, parentxpath, parentnode, newnode):
        ignore = parentxpath
        def node_is_text(n):
            return bool(n and n.nodeType == n.TEXT_NODE)

        if not node_is_text(parentnode.lastChild):
            prevsib = parentnode.previousSibling
            if node_is_text(prevsib):
                newlast = self._doc.createTextNode(prevsib.nodeValue)
            else:
                newlast = self._doc.createTextNode("\n")
            parentnode.appendChild(newlast)

        endtext = parentnode.lastChild.nodeValue
        parentnode.lastChild.nodeValue += "  "
        parentnode.appendChild(newnode)
        parentnode.appendChild(self._doc.createTextNode(endtext))


    def _node_remove_child(self, parentnode, childnode):
        white = childnode.previousSibling
        if white and white.nodeType == white.TEXT_NODE:
            parentnode.removeChild(white)
            white.unlink()

        parentnode.removeChild(childnode)
        childnode.unlink()

        if all([n.nodeType == n.TEXT_NODE for n in parentnode.childNodes]):
            for c in parentnode.childNodes[:]:
                parentnode.removeChild(c)
                c.unlink()

    def _node_from_xml(self, xml):
        return minidom.parseString(xml).documentElement

    def _node_has_content(self, node):
        if not node.nodeType == node.ELEMENT_NODE:
            return False
        return (node.hasChildNodes() or node.hasAttributes())

    def node_clear(self, xpath):
        node = self._find(xpath)
        if node:
            for c in (node.childNodes or [])[:]:
                node.removeChild(c)
            for c in list(node.attributes.keys()):
                node.removeAttribute(c)


XMLAPI = _Libxml2API
XMLAPI = _ETreeAPI
#XMLAPI = _MinidomAPI
