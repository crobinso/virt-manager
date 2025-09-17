#
# XML API wrappers
#
# This work is licensed under the GNU GPLv2 or later.
# See the COPYING file in the top-level directory.

import os

from .logger import log
from .xmllibxml2 import Libxml2API

_backend = os.environ.get("VIRTINST_XML_BACKEND")
log.debug("VIRTINST_XML_BACKEND=%s", _backend)

if _backend == "libxml2":
    XMLAPI = Libxml2API
else:
    # Default
    XMLAPI = Libxml2API
log.debug("Using XMLAPI=%s", XMLAPI)
