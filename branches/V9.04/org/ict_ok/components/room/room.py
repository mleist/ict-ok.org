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
from org.ict_ok.components.room.interfaces import \
    IRoom, IAddRoom, IRoomFolder
from org.ict_ok.components.interfaces import \
    IImportCsvData, IImportXlsData
from org.ict_ok.components.building.building import Building_Rooms_RelManager

def AllRoomsVocab(dummy_context):
    """Which locations are there
    """
    terms = []
    try:
        uidutil = getUtility(IIntIds)
        for (oid, oobj) in uidutil.items():
            if IRoom.providedBy(oobj.object):
                buildingObj = oobj.object.__parent__
                if IBuilding.providedBy(buildingObj):
                    locationObj = buildingObj.__parent__
                    if ILocation.providedBy(locationObj):
                        myString = u"%s / %s / %s" % (locationObj.getDcTitle(),
                                              buildingObj.getDcTitle(),
                                              oobj.object.getDcTitle())
                        terms.append(\
                            SimpleTerm(oobj.object.objectID,
                                       str(oobj.object.objectID),
                                       myString))
        return SimpleVocabulary(terms)
    except ComponentLookupError:
        return SimpleVocabulary([])

def AllRoomTemplates(dummy_context):
    """Which room templates exists
    """
    terms = []
    uidutil = getUtility(IIntIds)
    for (oid, oobj) in uidutil.items():
        if IRoom.providedBy(oobj.object) and \
        oobj.object.isTemplate:
            myString = u"%s [T]" % (oobj.object.getDcTitle())
            terms.append(SimpleTerm(oobj.object,
                                    token=oid,
                                    title=myString))
    return SimpleVocabulary(terms)

def AllUnusedOrSelfRooms(dummy_context):
    """In which production state a host may be
    """
    terms = []
    uidutil = getUtility(IIntIds)
    for (oid, oobj) in uidutil.items():
        if IRoom.providedBy(oobj.object):
            if not oobj.object.isTemplate:
                if oobj.object.building is None:
                    myString = u"%s" % (oobj.object.getDcTitle())
                    terms.append(\
                        SimpleTerm(oobj.object,
                                   token=oid,
                                   title=myString))
                else:
                    if oobj.object.building == dummy_context:
                        myString = u"%s" % (oobj.object.getDcTitle())
                        terms.append(\
                            SimpleTerm(oobj.object,
                                       token=oid,
                                       title=myString))
    return SimpleVocabulary(terms)



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

    def store_refs(self, **data):
        refAttributeNames = getRefAttributeNames(Room)
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
