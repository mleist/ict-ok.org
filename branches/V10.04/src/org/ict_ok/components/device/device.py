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
from lovely.relation.property import RelationPropertyOut
from lovely.relation.property import FieldRelationManager

# ict_ok.org imports
from org.ict_ok.components.component import getRefAttributeNames
from org.ict_ok.components.supernode.interfaces import IState
from org.ict_ok.components.device.wf.nagios import pd as WfPdNagios
from org.ict_ok.admin_utils.wfmc.wfmc import AdmUtilWFMC
from org.ict_ok.components.device.interfaces import IDevice, IDeviceFolder
from org.ict_ok.components.interface.interfaces import IInterface
from org.ict_ok.components.appsoftware.interfaces import IApplicationSoftware
from org.ict_ok.components.osoftware.interfaces import IOperatingSoftware
from org.ict_ok.components.logical_device.interfaces import ILogicalDevice
from org.ict_ok.components.physical_media.interfaces import IPhysicalMedia
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents
from org.ict_ok.components.physical_component.physical_component import \
    PhysicalComponent
from org.ict_ok.components.component import ComponentFolder
from org.ict_ok.admin_utils.generators.nagios.interfaces import INagiosCheck

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
Devices_PhysicalMedia_RelManager = \
    FieldRelationManager(IDevice['physicalMedia'],
                         IPhysicalMedia['device'],
                         relType='device:physicalMedia')


class Device(PhysicalComponent):
    """
    the template instance
    """
    implements(IDevice, INagiosCheck)
    shortName = "device"
    __name__ = __parent__ = None
    cpuType = FieldProperty(IDevice['cpuType'])
    memsize = FieldProperty(IDevice['memsize'])

#    room = RelationPropertyIn(Room_Devices_RelManager)
    interfaces = RelationPropertyOut(Device_Interface_RelManager)
    appsoftwares = RelationPropertyOut(Device_AppSoftware_RelManager)
    osoftwares = RelationPropertyOut(Device_OSoftware_RelManager)
#    logicalDevices = RelationPropertyOut(Device_LogicalDevices_RelManager)
    logicalDevices = RelationPropertyOut(Devices_LogicalDevices_RelManager)
    physicalMedia = RelationPropertyOut(Devices_PhysicalMedia_RelManager)

    fullTextSearchFields = ['cpuType']
    fullTextSearchFields.extend(PhysicalComponent.fullTextSearchFields)

    genNagios = FieldProperty(INagiosCheck['genNagios'])
    
    # Workflows
    wf_pd_dict = {}
    wf_pd_dict[WfPdNagios.id] = WfPdNagios
    AdmUtilWFMC.wf_pd_dict[WfPdNagios.id] = WfPdNagios

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
        self.workflows[WfPdNagios.id] = nagios_wf = WfPdNagios()
        setattr(nagios_wf.workflowRelevantData, "state", "-")
        setattr(nagios_wf.workflowRelevantData, "object", self)
        setattr(nagios_wf.workflowRelevantData, "new_state", "2_start")
        nagios_wf.start()

    def getRefAttributeNames(self):
        return getRefAttributeNames(Device)

    def store_refs(self, **data):
        PhysicalComponent.store_refs(self, **data)
        refAttributeNames = self.getRefAttributeNames()
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)

    def trigger_online(self):
        """
        trigger workflow
        """
#        print "trigger_online"
        lastWorkItem = list(self.wf_worklist)[-1]
        wfd = lastWorkItem.participant.activity.process.workflowRelevantData
        wfd.new_state = "online"
        lastWorkItem.change()

    def trigger_offline(self):
        """
        trigger workflow
        """
#        print "trigger_offline"
        lastWorkItem = list(self.wf_worklist)[-1]
        wfd = lastWorkItem.participant.activity.process.workflowRelevantData
        wfd.new_state = "offline"
        lastWorkItem.change()

    def trigger_not1(self):
        """
        trigger workflow
        """
#        print "trigger_not1"
        lastWorkItem = list(self.wf_worklist)[-1]
        wfd = lastWorkItem.participant.activity.process.workflowRelevantData
        wfd.new_state = "notification1"
        lastWorkItem.change()


class DeviceFolder(ComponentFolder):
    implements(IDeviceFolder)
    contentFactory = Device
    shortName = "device folder"

    def __init__(self, **data):
        """
        constructor of the object
        """
        ComponentFolder.__init__(self, **data)
