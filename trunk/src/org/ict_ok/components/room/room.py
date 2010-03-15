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
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

# lovely imports
from lovely.relation.property import RelationPropertyIn
from lovely.relation.property import RelationPropertyOut
from lovely.relation.property import FieldRelationManager

# ict_ok.org imports
from org.ict_ok.components.component import getRefAttributeNames
from org.ict_ok.components.component import Component, ComponentFolder
from org.ict_ok.components.room.interfaces import \
    IRoom, IAddRoom, IRoomFolder
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents
from org.ict_ok.components.building.building import Building_Rooms_RelManager
from org.ict_ok.components.physical_component.interfaces import IPhysicalComponent

def AllRoomTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IRoom)

def AllRooms(dummy_context):
    return AllComponents(dummy_context, IRoom, 'building')

def AllUnusedOrUsedBuildingRooms(dummy_context):
    return AllUnusedOrSelfComponents(dummy_context, IRoom,
                                     'building', 'building')

Room_Devices_RelManager = FieldRelationManager(IRoom['physicalComponents'],
                                               IPhysicalComponent['room'],
                                               relType='room:devices')

Room_PhysicalComponents_RelManager = FieldRelationManager(IRoom['physicalComponents'],
                                                          IPhysicalComponent['room'],
                                                          relType='room:physicalcomponents')


class Room(Component):
    """
    the template instance
    """

    implements(IRoom)
    shortName = "room"
    containerIface = IRoomFolder
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


class RoomFolder(ComponentFolder):
    implements(IRoomFolder,
               IAddRoom)
    contentFactory = Room
    shortName = "room folder"

    def __init__(self, **data):
        """
        constructor of the object
        """
        ComponentFolder.__init__(self, **data)
