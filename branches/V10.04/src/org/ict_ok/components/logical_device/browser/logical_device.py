# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232,W0142
#
"""implementation of browser class of Notebook"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports

# ict_ok.org imports
from org.ict_ok.components.browser.component import ComponentDetails

_ = MessageFactory('org.ict_ok')

# --------------- object details ---------------------------


class LogicalDeviceDetails(ComponentDetails):
    """ Class for Notebook details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []


class LogicalDeviceFolderDetails(ComponentDetails):
    """ Class for MobilePhone details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + ['requirement']
    omit_addfields = ComponentDetails.omit_addfields + ['requirement']
    omit_editfields = ComponentDetails.omit_editfields + ['requirement']



