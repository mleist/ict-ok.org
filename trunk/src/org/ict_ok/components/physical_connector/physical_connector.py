# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0142
#
"""implementation of PhysicalConnector"""

__version__ = "$Id$"

# python imports

# zope imports

# lovely imports

# ict_ok.org imports
from org.ict_ok.components.physical_connector.interfaces import \
    IPhysicalConnector#, IPhysicalConnectorFolder, IAddPhysicalConnector
from org.ict_ok.components.component import \
    AllComponents, AllUnusedOrSelfComponents
#from org.ict_ok.components.room.room import Room_PhysicalConnectors_RelManager


def AllPhysicalConnectors(dummy_context):
    return AllComponents(dummy_context, IPhysicalConnector, additionalAttrNames=['device', 'room'])

def AllUnusedOrUsedPhysikalLinkPhysicalConnectors(dummy_context):
    return AllUnusedOrSelfComponents(dummy_context, IPhysicalConnector, 'links', additionalAttrNames=['device', 'room'])
