# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
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

# phython imports

# zope imports
from zope.app import zapi
from zope.interface import implements
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

# ict_ok.org imports
from org.ict_ok.components.component import Component
from org.ict_ok.components.location.interfaces import ILocation



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


class Location(Component):
    """
    the template instance
    """

    implements(ILocation)
    # for ..Contained we have to:
    __name__ = __parent__ = None
    #ikAttr = FieldProperty(ILocation['ikAttr'])

    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        # find our correct factory, is there a better solution?
        for (fact_name, fact_obj) in zapi.getFactoriesFor(ILocation):
            if (len(fact_name) > 11) and (fact_name[:11]=='org.ict_ok.'):
                self.myFactory = unicode(fact_name)
        for (name, value) in data.items():
            if name in ILocation.names():
                setattr(self, name, value)
        self.ikRevision = __version__
