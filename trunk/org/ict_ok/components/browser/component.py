# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0232,W0142
#
"""implementation of browser class of Host object
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports

# ict_ok.org imports
from org.ict_ok.components.supernode.browser.supernode import SupernodeDetails

_ = MessageFactory('org.ict_ok')

# --------------- object details ---------------------------


class ComponentDetails(SupernodeDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = SupernodeDetails.omit_viewfields + []
    omit_addfields = SupernodeDetails.omit_addfields + []
    omit_editfields = SupernodeDetails.omit_editfields + []
