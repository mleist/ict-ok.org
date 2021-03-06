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
"""implementation of Notebook"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

# lovely imports
from lovely.relation.property import RelationPropertyIn

# ict_ok.org imports
from org.ict_ok.components.component import getRefAttributeNames
from org.ict_ok.components.logical_device.interfaces import ILogicalDevice, ILogicalDeviceFolder
from org.ict_ok.components.component import ComponentFolder

from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents
from org.ict_ok.components.logical_component.logical_component import \
    LogicalComponent
from org.ict_ok.components.device.device import Devices_LogicalDevices_RelManager

def AllLogicalDeviceTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, ILogicalDevice)

def AllLogicalDevices(dummy_context):
    return AllComponents(dummy_context, ILogicalDevice)

def AllUnusedOrUsedDeviceLogicalDevices(dummy_context):
    return AllUnusedOrSelfComponents(dummy_context, ILogicalDevice, 'devices')

class LogicalDevice(LogicalComponent):
    """
    the template instance
    """
    implements(ILogicalDevice)
    __name__ = __parent__ = None
    powerManagementSupported = FieldProperty(ILogicalDevice['powerManagementSupported'])

    devices = RelationPropertyIn(Devices_LogicalDevices_RelManager)

    fullTextSearchFields = []
    fullTextSearchFields.extend(LogicalComponent.fullTextSearchFields)

    def __init__(self, **data):
        """
        constructor of the object
        """
        LogicalComponent.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(LogicalDevice)
        for (name, value) in data.items():
            if name in ILogicalDevice.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        self.ikRevision = __version__

    def getRefAttributeNames(self):
        return getRefAttributeNames(LogicalDevice)

    def store_refs(self, **data):
        LogicalComponent.store_refs(self, **data)
        refAttributeNames = self.getRefAttributeNames()
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class LogicalDeviceFolder(ComponentFolder):
    implements(ILogicalDeviceFolder)
    contentFactory = LogicalDevice

    def __init__(self, **data):
        """
        constructor of the object
        """
        ComponentFolder.__init__(self, **data)
