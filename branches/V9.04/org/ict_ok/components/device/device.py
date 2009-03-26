# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: template.py_cog 399 2009-01-08 14:00:17Z markusleist $
#
# pylint: disable-msg=E1101,W0142
#
"""implementation of Notebook"""

__version__ = "$Id: template.py_cog 399 2009-01-08 14:00:17Z markusleist $"

# python imports

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.app.folder import Folder

# lovely imports
from lovely.relation.property import RelationPropertyIn
from lovely.relation.property import RelationPropertyOut
from lovely.relation.property import FieldRelationManager

# ict_ok.org imports
from org.ict_ok.libs.lib import getRefAttributeNames
from org.ict_ok.components.device.interfaces import IDevice, IDeviceFolder
from org.ict_ok.components.superclass.superclass import Superclass
from org.ict_ok.components.interface.interfaces import IInterface
from org.ict_ok.components.appsoftware.interfaces import IApplicationSoftware
from org.ict_ok.components.osoftware.interfaces import IOperatingSoftware
from org.ict_ok.components.logical_device.interfaces import ILogicalDevice
from org.ict_ok.components.interfaces import \
    IImportCsvData, IImportXlsData
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents
from org.ict_ok.components.physical_component.physical_component import \
    PhysicalComponent

def AllDeviceTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IDevice)

def AllDevices(dummy_context):
    return AllComponents(dummy_context, IDevice)

def AllUnusedOrUsedRoomDevices(dummy_context):
    return AllUnusedOrSelfComponents(dummy_context, IDevice, 'room')

Device_Interface_RelManager = \
    FieldRelationManager(IDevice['interfaces'],
                         IInterface['device'],
                         relType='device:interfaces')
Device_AppSoftware_RelManager = \
    FieldRelationManager(IDevice['appsoftwares'],
                         IApplicationSoftware['device'],
                         relType='device:appsoftwares')
Device_OSoftware_RelManager = \
    FieldRelationManager(IDevice['osoftwares'],
                         IOperatingSoftware['device'],
                         relType='device:osoftwares')
#Device_LogicalDevices_RelManager = \
#    FieldRelationManager(IDevice['logicalDevices'],
#                         ILogicalDevice['device'],
#                         relType='device:logicalDevices')
Devices_LogicalDevices_RelManager = \
    FieldRelationManager(IDevice['logicalDevices'],
                         ILogicalDevice['devices'],
                         relType='devices:logicalDevices')


class Device(PhysicalComponent):
    """
    the template instance
    """
    implements(IDevice)
    __name__ = __parent__ = None
    cpuType = FieldProperty(IDevice['cpuType'])
    memsize = FieldProperty(IDevice['memsize'])

#    room = RelationPropertyIn(Room_Devices_RelManager)
    interfaces = RelationPropertyOut(Device_Interface_RelManager)
    appsoftwares = RelationPropertyOut(Device_AppSoftware_RelManager)
    osoftwares = RelationPropertyOut(Device_OSoftware_RelManager)
#    logicalDevices = RelationPropertyOut(Device_LogicalDevices_RelManager)
    logicalDevices = RelationPropertyOut(Devices_LogicalDevices_RelManager)

    fullTextSearchFields = ['cpuType']
    fullTextSearchFields.extend(PhysicalComponent.fullTextSearchFields)

    def __init__(self, **data):
        """
        constructor of the object
        """
        PhysicalComponent.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(Device)
        for (name, value) in data.items():
            if name in IDevice.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        self.ikRevision = __version__

    def store_refs(self, **data):
        PhysicalComponent.store_refs(self, **data)
        refAttributeNames = getRefAttributeNames(Device)
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class DeviceFolder(Superclass, Folder):
    implements(IDeviceFolder,
               IImportCsvData,
               IImportXlsData)
    def __init__(self, **data):
        """
        constructor of the object
        """
        Superclass.__init__(self, **data)
        Folder.__init__(self)
