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
"""implementation of ApplicationSoftware"""

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
from org.ict_ok.components.appsoftware.interfaces import IApplicationSoftware
from org.ict_ok.components.appsoftware.interfaces import IApplicationSoftwareFolder
from org.ict_ok.components.component import Component
from org.ict_ok.components.notebook.notebook import Notebook_AppSoftware_RelManager
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents

#def AllApplicationSoftwares(dummy_context):
#    """Which ApplicationSoftware are there
#    """
#    terms = []
#    uidutil = getUtility(IIntIds)
#    for (oid, oobj) in uidutil.items():
#        if IApplicationSoftware.providedBy(oobj.object):
#            myString = u"%s" % (oobj.object.getDcTitle())
#            terms.append(                SimpleTerm(oobj.object,
#                          token=oid,
#                          title=myString))
#    return SimpleVocabulary(terms)
#
#
#def AllApplicationSoftwareTemplates(dummy_context):
#    """Which room templates exists
#    """
#    terms = []
#    uidutil = getUtility(IIntIds)
#    for (oid, oobj) in uidutil.items():
#        if IApplicationSoftware.providedBy(oobj.object) and \
#        oobj.object.isTemplate:
#            myString = u"%s [T]" % (oobj.object.getDcTitle())
#            terms.append(SimpleTerm(oobj.object,
#                                    token=oid,
#                                    title=myString))
#    return SimpleVocabulary(terms)
#
#def AllUnusedOrSelfApplicationSoftwares(dummy_context):
#    """In which production state a host may be
#    """
##    import pdb
##    pdb.set_trace()
#    terms = []
#    uidutil = getUtility(IIntIds)
#    for (oid, oobj) in uidutil.items():
#        if IApplicationSoftware.providedBy(oobj.object):
#            if not oobj.object.isTemplate:
##                if oobj.object.building is None:
#                myString = u"%s" % (oobj.object.getDcTitle())
#                terms.append(\
#                    SimpleTerm(oobj.object,
#                               token=oid,
#                               title=myString))
##                else:
###                    if oobj.object.building == dummy_context:
##                    myString = u"%s" % (oobj.object.getDcTitle())
##                    terms.append(\
##                        SimpleTerm(oobj.object,
##                                   token=oid,
##                                   title=myString))
#    return SimpleVocabulary(terms)

def AllApplicationSoftwareTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IApplicationSoftware)

def AllApplicationSoftwares(dummy_context):
    return AllComponents(dummy_context, IApplicationSoftware)

def AllUnusedOrSelfApplicationSoftwares(dummy_context):
    return AllUnusedOrSelfComponents(dummy_context, IApplicationSoftware, 'device')


class ApplicationSoftware(Component):
    """
    the template instance
    """
    implements(IApplicationSoftware)
    shortName = "appsoftware"
    # for ..Contained we have to:
    __name__ = __parent__ = None
    manufacturer = FieldProperty(IApplicationSoftware['manufacturer'])
    otherType = FieldProperty(IApplicationSoftware['otherType'])
    targetOperatingSystems = FieldProperty(IApplicationSoftware['targetOperatingSystems'])
    versionText = FieldProperty(IApplicationSoftware['versionText'])
    licenseKey = FieldProperty(IApplicationSoftware['licenseKey'])
    language = FieldProperty(IApplicationSoftware['language'])
    majorVersion = FieldProperty(IApplicationSoftware['majorVersion'])
    minorVersion = FieldProperty(IApplicationSoftware['minorVersion'])
    revisionNumber = FieldProperty(IApplicationSoftware['revisionNumber'])
    buildNumber = FieldProperty(IApplicationSoftware['buildNumber'])

    device = RelationPropertyIn(Notebook_AppSoftware_RelManager)

    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(ApplicationSoftware)
        for (name, value) in data.items():
            if name in IApplicationSoftware.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        self.ikRevision = __version__

    def store_refs(self, **data):
        refAttributeNames = getRefAttributeNames(ApplicationSoftware)
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class ApplicationSoftwareFolder(Superclass, Folder):
    implements(IApplicationSoftwareFolder)
    def __init__(self, **data):
        """
        constructor of the object
        """
        Superclass.__init__(self, **data)
        Folder.__init__(self)