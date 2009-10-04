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
"""implementation of browser class of SoftwareComponent"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# ict_ok.org imports
from org.ict_ok.components.logical_component.browser.logical_component import \
    LogicalComponentDetails, LogicalComponentFolderDetails
from org.ict_ok.components.software_component.interfaces import ISoftwareComponent
from org.ict_ok.components.software_component.software_component import SoftwareComponent
from org.ict_ok.components.browser.component import ComponentDetails

_ = MessageFactory('org.ict_ok')


# --------------- object details ---------------------------


class SoftwareComponentDetails(LogicalComponentDetails):
    """ Class for SoftwareComponent details
    """
    omit_viewfields = LogicalComponentDetails.omit_viewfields + []
    omit_addfields = LogicalComponentDetails.omit_addfields + []
    omit_editfields = LogicalComponentDetails.omit_editfields + []


class SoftwareComponentFolderDetails(LogicalComponentFolderDetails):
    """ Class for MobilePhone details
    """
    omit_viewfields = LogicalComponentFolderDetails.omit_viewfields + ['requirement']
    omit_addfields = LogicalComponentFolderDetails.omit_addfields + ['requirement']
    omit_editfields = LogicalComponentFolderDetails.omit_editfields + ['requirement']
