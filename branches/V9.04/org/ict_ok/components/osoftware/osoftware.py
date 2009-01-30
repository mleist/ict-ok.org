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
"""implementation of OperatingSoftware"""

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
from org.ict_ok.components.osoftware.interfaces import IOperatingSoftware
from org.ict_ok.components.osoftware.interfaces import IOperatingSoftwareFolder
from org.ict_ok.components.component import Component
from org.ict_ok.components.notebook.notebook import Notebook_OSoftware_RelManager
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents

#def AllOperatingSoftwares(dummy_context):
#    """Which OperatingSoftware are there
#    """
#    terms = []
#    uidutil = getUtility(IIntIds)
#    for (oid, oobj) in uidutil.items():
#        if IOperatingSoftware.providedBy(oobj.object):
#            myString = u"%s" % (oobj.object.getDcTitle())
#            terms.append(                SimpleTerm(oobj.object,
#                          token=oid,
#                          title=myString))
#    return SimpleVocabulary(terms)


def AllOperatingSoftwareTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IOperatingSoftware)

def AllOperatingSoftwares(dummy_context):
    return AllComponents(dummy_context, IOperatingSoftware)

def AllUnusedOrSelfOperatingSoftwares(dummy_context):
    return AllUnusedOrSelfComponents(dummy_context, IOperatingSoftware, 'device')


class OperatingSoftware(Component):
    """
    the template instance
    """
    implements(IOperatingSoftware)
    shortName = "osoftware"
    # for ..Contained we have to:
    __name__ = __parent__ = None
    
    manufacturer = FieldProperty(IOperatingSoftware['manufacturer'])
    osType = FieldProperty(IOperatingSoftware['osType'])
    otherType = FieldProperty(IOperatingSoftware['otherType'])
    versionText = FieldProperty(IOperatingSoftware['versionText'])
    licenseKey = FieldProperty(IOperatingSoftware['licenseKey'])
    language = FieldProperty(IOperatingSoftware['language'])
    majorVersion = FieldProperty(IOperatingSoftware['majorVersion'])
    minorVersion = FieldProperty(IOperatingSoftware['minorVersion'])
    revisionNumber = FieldProperty(IOperatingSoftware['revisionNumber'])
    buildNumber = FieldProperty(IOperatingSoftware['buildNumber'])

    device = RelationPropertyIn(Notebook_OSoftware_RelManager)
    

    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(OperatingSoftware)
        for (name, value) in data.items():
            if name in IOperatingSoftware.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        self.ikRevision = __version__

    def store_refs(self, **data):
        refAttributeNames = getRefAttributeNames(OperatingSoftware)
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class OperatingSoftwareFolder(Superclass, Folder):
    implements(IOperatingSoftwareFolder)
    def __init__(self, **data):
        """
        constructor of the object
        """
        Superclass.__init__(self, **data)
        Folder.__init__(self)
