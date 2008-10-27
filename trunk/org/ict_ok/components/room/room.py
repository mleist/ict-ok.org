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

# ict_ok.org imports
from org.ict_ok.components.component import Component
from org.ict_ok.components.location.interfaces import ILocation
from org.ict_ok.components.building.interfaces import IBuilding
from org.ict_ok.components.room.interfaces import IRoom


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


class Room(Component):
    """
    the template instance
    """

    implements(IRoom)
    shortName = "room"
    # for ..Contained we have to:
    __name__ = __parent__ = None
    #ikAttr = FieldProperty(IRoom['ikAttr'])

    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        for (name, value) in data.items():
            if name in IRoom.names():
                setattr(self, name, value)
        self.ikRevision = __version__
