# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0612,W0142
#
"""implementation of Room

Room does ....

"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.app import zapi
from zope.interface import implements
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.component.interfaces import ComponentLookupError
from zope.app.folder import Folder
from zope.schema.fieldproperty import FieldProperty

# lovely imports
from lovely.relation.property import RelationPropertyIn
from lovely.relation.property import RelationPropertyOut
from lovely.relation.property import FieldRelationManager

# ict_ok.org imports
from org.ict_ok.libs.lib import getRefAttributeNames
from org.ict_ok.components.component import Component
from org.ict_ok.components.superclass.superclass import Superclass
from org.ict_ok.components.location.interfaces import ILocation
from org.ict_ok.components.building.interfaces import IBuilding
from org.ict_ok.components.device.interfaces import IDevice
from org.ict_ok.components.rack.interfaces import IRack
from org.ict_ok.components.room.interfaces import \
    IRoom, IAddRoom, IRoomFolder
from org.ict_ok.components.physical_connector.interfaces import IPhysicalConnector
from org.ict_ok.components.interfaces import \
    IImportCsvData, IImportXlsData
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents
from org.ict_ok.components.building.building import Building_Rooms_RelManager
from org.ict_ok.components.physical_component.interfaces import IPhysicalComponent

def AllRoomTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IRoom)

def AllRooms(dummy_context):
    return AllComponents(dummy_context, IRoom, ['building'])

def AllUnusedOrUsedBuildingRooms(dummy_context):
    return AllUnusedOrSelfComponents(dummy_context, IRoom,
                                     'building', ['building'])


#Room_Devices_RelManager = FieldRelationManager(IRoom['devices'],
#                                               IPhysicalComponent['room'],
#                                               relType='room:devices')
Room_Devices_RelManager = FieldRelationManager(IRoom['physicalComponents'],
                                               IPhysicalComponent['room'],
                                               relType='room:devices')
#Room_PhysicalConnectors_RelManager = FieldRelationManager(IRoom['physicalConnectors'],
#                                                          IPhysicalConnector['room'],
#                                                          relType='room:physicalConnectors')
#Room_Racks_RelManager = FieldRelationManager(IRoom['racks'],
#                                             IPhysicalComponent['room'],
#                                             relType='room:racks')


Room_PhysicalComponents_RelManager = FieldRelationManager(IRoom['physicalComponents'],
                                                          IPhysicalComponent['room'],
                                                          relType='room:physicalcomponents')



class Room(Component):
    """
    the template instance
    """

    implements(IRoom)
    shortName = "room"
    # for ..Contained we have to:
    __name__ = __parent__ = None
    level = FieldProperty(IRoom['level'])
    coordinates = FieldProperty(IRoom['coordinates'])

    building = RelationPropertyIn(Building_Rooms_RelManager)
 #   devices = RelationPropertyOut(Room_Devices_RelManager)
#    physicalConnectors = RelationPropertyOut(Room_PhysicalConnectors_RelManager)
#    racks = RelationPropertyOut(Room_Racks_RelManager)
    physicalComponents = RelationPropertyOut(Room_PhysicalComponents_RelManager)

    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(Room)
        for (name, value) in data.items():
            if name in IRoom.names():
                if name not in refAttributeNames:
                    setattr(self, name, value)
        self.ikRevision = __version__

    def getRefAttributeNames(self):
        return getRefAttributeNames(Room)

    def store_refs(self, **data):
        Component.store_refs(self, **data)
        refAttributeNames = self.getRefAttributeNames()
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class RoomFolder(Superclass, Folder):
    implements(IRoomFolder, 
               IImportCsvData,
               IImportXlsData,
               IAddRoom)
    def __init__(self, **data):
        """
        constructor of the object
        """
        Superclass.__init__(self, **data)
        Folder.__init__(self)
