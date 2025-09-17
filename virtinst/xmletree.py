#
# XML API wrappers
#
# This work is licensed under the GNU GPLv2 or later.
# See the COPYING file in the top-level directory.

import xml.etree.ElementTree as ET

from .xmlbase import XMLBase, XPath


class ETreeAPI(XMLBase):
    def __init__(self, parsexml):
        XMLBase.__init__(self)
        self._et = ET.ElementTree(ET.fromstring(parsexml))

        for _k, _v in XMLBase.NAMESPACES.items():
            ET.register_namespace(_k, _v)

    #######################
    # Private helper APIs #
    #######################

    def _sanitize_xml(self, xml):
        return xml.replace(" />", "/>")

    def _node_tostring(self, node):
        return ET.tostring(node, encoding="unicode")

    def _node_from_xml(self, xml):
        return ET.fromstring(xml)

    def _node_get_name(self, node):
        return node.tag

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
        xpath = XPath(fullxpath).xpath
        node = self._et.find(xpath, self.NAMESPACES)
        if node is None:
            return None
        return node

    ###############
    # Simple APIs #
    ###############

    def copy_api(self):
        return ETreeAPI(self._node_tostring(self._et.getroot()))

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
        xpathobj = XPath(parentxpath)

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
        return len(node) or node.attrib or re.search(r"\w+", (node.text or ""))

    def _node_remove_child(self, parentnode, childnode):
        idx = list(parentnode).index(childnode)

        if idx != 0 and idx == (len(list(parentnode)) - 1):
            prevsibling = list(parentnode)[idx - 1]
            prevsibling.tail = prevsibling.tail[:-2]
        elif idx == 0 and len(list(parentnode)) == 1:
            parentnode.text = None

        parentnode.remove(childnode)

    def _node_new(self, xpathseg, _parentnode):
        newname = xpathseg.nodename
        if xpathseg.nsname:
            newname = "{%s}%s" % (self.NAMESPACES[xpathseg.nsname], newname)
        return ET.Element(newname)

    def _node_replace_child(self, xpath, newnode):
        raise NotImplementedError()

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
