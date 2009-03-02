# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: template.py_cog 396 2009-01-08 00:21:51Z markusleist $
#
# pylint: disable-msg=W0232,W0142
#
"""implementation of browser class of PhysicalConnector"""

__version__ = "$Id: template.py_cog 396 2009-01-08 00:21:51Z markusleist $"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# ict_ok.org imports
from org.ict_ok.components.physical_connector.interfaces import IPhysicalConnector, IAddPhysicalConnector
from org.ict_ok.components.physical_connector.physical_connector import PhysicalConnector
from org.ict_ok.components.browser.component import ComponentDetails

_ = MessageFactory('org.ict_ok')


# --------------- object details ---------------------------


class PhysicalConnectorDetails(ComponentDetails):
    """ Class for PhysicalConnector details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []


class PhysicalConnectorFolderDetails(ComponentDetails):
    """ Class for MobilePhone details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + ['requirement']
    omit_addfields = ComponentDetails.omit_addfields + ['requirement']
    omit_editfields = ComponentDetails.omit_editfields + ['requirement']
