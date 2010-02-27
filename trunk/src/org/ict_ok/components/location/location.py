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
"""implementation of Location

Location does ....

"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.app import zapi
from zope.interface import implements
from zope.component import getUtility
from zope.schema.fieldproperty import FieldProperty
from zope.app.intid.interfaces import IIntIds
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.app.folder import Folder

# lovely imports
from lovely.relation.property import RelationPropertyIn
from lovely.relation.property import RelationPropertyOut
from lovely.relation.property import FieldRelationManager

# ict_ok.org imports
from org.ict_ok.components.component import getRefAttributeNames
from org.ict_ok.components.component import Component, ComponentFolder
from org.ict_ok.components.superclass.superclass import Superclass
from org.ict_ok.components.location.interfaces import \
    ILocation, IAddLocation, ILocationFolder
from org.ict_ok.components.interfaces import \
    IImportCsvData, IImportXlsData
from org.ict_ok.components.building.interfaces import IBuilding


def AllLocationsVocab(dummy_context):
    """Which locations are there
    """
    terms = []
    uidutil = getUtility(IIntIds)
    for (oid, oobj) in uidutil.items():
        if ILocation.providedBy(oobj.object):
            terms.append(\
                SimpleTerm(oobj.object.objectID,
                           str(oobj.object.objectID),
                           oobj.object.getDcTitle()))
    return SimpleVocabulary(terms)


def AllLocations(dummy_context):
    """In which production state a host may be
    """
    terms = []
    uidutil = getUtility(IIntIds)
    for (oid, oobj) in uidutil.items():
        if ILocation.providedBy(oobj.object):
            myString = u"%s" % (oobj.object.getDcTitle())
            terms.append(\
                SimpleTerm(oobj.object,
                           token=getattr(oobj.object, 'objectID', oid),
                           title=myString))
    return SimpleVocabulary(terms)
    
def AllLocationTemplates(dummy_context):
    """Which MobilePhone templates exists
    """
    terms = []
    uidutil = getUtility(IIntIds)
    for (oid, oobj) in uidutil.items():
        if ILocation.providedBy(oobj.object) and \
        oobj.object.isTemplate:
            myString = u"%s [T]" % (oobj.object.getDcTitle())
            terms.append(SimpleTerm(oobj.object,
                                    token=getattr(oobj.object, 'objectID', oid),
                                    title=myString))
    return SimpleVocabulary(terms)

Location_Buildings_RelManager = FieldRelationManager(ILocation['buildings'],
                                                 IBuilding['location'],
                                                 relType='location:buildings')


class Location(Component):
    """
    the template instance
    """

    implements(ILocation)
    shortName = "location"
    containerIface = ILocationFolder
    # for ..Contained we have to:
    __name__ = __parent__ = None
    #ikAttr = FieldProperty(ILocation['ikAttr'])
    coordinates = FieldProperty(ILocation['coordinates'])
    gmapsurl = FieldProperty(ILocation['gmapsurl'])
    gmapcode = FieldProperty(ILocation['gmapcode'])

    buildings = RelationPropertyOut(Location_Buildings_RelManager)

    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(Location)
        for (name, value) in data.items():
            if name in ILocation.names():
                if name not in refAttributeNames:
                    setattr(self, name, value)
        self.ikRevision = __version__

    def getRefAttributeNames(self):
        return getRefAttributeNames(Location)

    def store_refs(self, **data):
        Component.store_refs(self, **data)
        refAttributeNames = self.getRefAttributeNames()
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class LocationFolder(ComponentFolder):
    implements(ILocationFolder, 
               IAddLocation)
    contentFactory = Location

    def __init__(self, **data):
        """
        constructor of the object
        """
        ComponentFolder.__init__(self, **data)
