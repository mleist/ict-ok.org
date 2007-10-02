# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232
#
"""implementation of browser class of Slave object
"""

__version__ = "$Id$"

# phython imports

# zope imports

# ict_ok.org imports
from org.ict_ok.components.browser.component import ComponentDetails


# --------------- menu entries -----------------------------


# --------------- forms ------------------------------------


# --------------- object details ---------------------------


class SlaveDetails(ComponentDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []
