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
"""implementation of Outlet"""

__version__ = "$Id: template.py_cog 399 2009-01-08 14:00:17Z markusleist $"

# python imports

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.app.intid.interfaces import IIntIds
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds
from zope.app.folder import Folder

# lovely imports
from lovely.relation.property import RelationPropertyIn
from lovely.relation.property import RelationPropertyOut
from lovely.relation.property import FieldRelationManager

# ict_ok.org imports
from org.ict_ok.libs.lib import getRefAttributeNames
from org.ict_ok.components.superclass.superclass import Superclass
from org.ict_ok.components.outlet.interfaces import \
    IOutlet, IOutletFolder, IAddOutlet
from org.ict_ok.components.interfaces import \
    IImportCsvData, IImportXlsData
from org.ict_ok.components.component import Component

def AllOutlets(dummy_context):
    """Which Outlet are there
    """
    terms = []
    uidutil = getUtility(IIntIds)
    for (oid, oobj) in uidutil.items():
        if IOutlet.providedBy(oobj.object):
            myString = u"%s" % (oobj.object.getDcTitle())
            terms.append(                SimpleTerm(oobj.object,
                          token=oid,
                          title=myString))
    return SimpleVocabulary(terms)

def AllOutletTemplates(dummy_context):
    """Which Outlet templates exists
    """
    terms = []
    uidutil = getUtility(IIntIds)
    for (oid, oobj) in uidutil.items():
        if IOutlet.providedBy(oobj.object) and \
        oobj.object.isTemplate:
            myString = u"%s [T]" % (oobj.object.getDcTitle())
            terms.append(SimpleTerm(oobj.object,
                                    token=oid,
                                    title=myString))
    return SimpleVocabulary(terms)



Outlet_Conns_RelManager = FieldRelationManager(IOutlet['conns'],
                                                 IOutlet['conn'],
                                                 relType='outlet:conns')

class Outlet(Component):
    """
    the template instance
    """
    implements(IOutlet)
    shortName = "outlet"
    # for ..Contained we have to:
    __name__ = __parent__ = None
    attrFoo = FieldProperty(IOutlet['attrFoo'])

    conns = RelationPropertyOut(Outlet_Conns_RelManager)
    conn = RelationPropertyIn(Outlet_Conns_RelManager)

    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(Outlet)
        for (name, value) in data.items():
            if name in IOutlet.names():
                if name not in refAttributeNames:
                    setattr(self, name, value)
        self.ikRevision = __version__

    def store_refs(self, **data):
        refAttributeNames = getRefAttributeNames(Outlet)
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class OutletFolder(Superclass, Folder):
    implements(IOutletFolder, 
               IImportCsvData,
               IImportXlsData,
               IAddOutlet)
    def __init__(self, **data):
        """
        constructor of the object
        """
        Superclass.__init__(self, **data)
        Folder.__init__(self)
