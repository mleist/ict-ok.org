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
"""implementation of Building

Building does ....

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

# ict_ok.org imports
from org.ict_ok.components.component import Component
from org.ict_ok.components.location.interfaces import ILocation
from org.ict_ok.components.building.interfaces import IBuilding


def AllBuildingsVocab(dummy_context):
    """Which locations are there
    """
    terms = []
    uidutil = getUtility(IIntIds)
    for (oid, oobj) in uidutil.items():
        if IBuilding.providedBy(oobj.object):
            locationObj = oobj.object.__parent__
            if ILocation.providedBy(locationObj):
                myString = u"%s / %s" % (locationObj.getDcTitle(),
                                      oobj.object.getDcTitle())
                terms.append(\
                    SimpleTerm(oobj.object.objectID,
                               str(oobj.object.objectID),
                               myString))
    return SimpleVocabulary(terms)


class Building(Component):
    """
    the template instance
    """

    implements(IBuilding)
    # for ..Contained we have to:
    __name__ = __parent__ = None
    #ikAttr = FieldProperty(IBuilding['ikAttr'])
    coordinates = FieldProperty(IBuilding['coordinates'])
    gmapsurl = FieldProperty(IBuilding['gmapsurl'])

    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        for (name, value) in data.items():
            if name in IBuilding.names():
                setattr(self, name, value)
        self.ikRevision = __version__
