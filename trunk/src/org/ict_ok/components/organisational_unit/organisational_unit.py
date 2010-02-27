# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: template.py_cog 465 2009-03-05 02:34:02Z markusleist $
#
# pylint: disable-msg=E1101,W0142
#
"""implementation of OrganisationalUnit"""

__version__ = "$Id: template.py_cog 465 2009-03-05 02:34:02Z markusleist $"

# python imports

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema import vocabulary

# lovely imports
from lovely.relation.property import RelationPropertyIn
from lovely.relation.property import RelationPropertyOut
from lovely.relation.property import FieldRelationManager

# ict_ok.org imports
from org.ict_ok.components.component import getRefAttributeNames
from org.ict_ok.components.organisational_unit.interfaces import IOrganisationalUnit
from org.ict_ok.components.organisational_unit.interfaces import IOrganisationalUnitFolder
from org.ict_ok.components.organisational_unit.interfaces import IAddOrganisationalUnit
from org.ict_ok.components.component import ComponentFolder
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates
from org.ict_ok.components.contact_item.contact_item import ContactItem
#from org.ict_ok.components.organization.organization import AllOrganizations

def AllOrganisationalUnitTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IOrganisationalUnit)

def AllOrganisationalUnits(dummy_context):
    return AllComponents(dummy_context, IOrganisationalUnit)




def AllValidSubOrganisationalUnits(dummy_context):
    return AllComponents(dummy_context, IOrganisationalUnit,
                  additionalAttrNames=None, includeSelf=False)

def AllOrganisationsAndOrganisationalUnits(dummy_context):
    terms = []
    listOUs = AllValidSubOrganisationalUnits(dummy_context)
    for term in listOUs:
        terms.append(term)
#    listOs = AllOrganizations(dummy_context)
    vocabReg = vocabulary.getVocabularyRegistry()
    if vocabReg is not None:
        vocab = vocabReg.get(None, 'AllOrganizations')
        if vocab is not None:
            for term in vocab:
                terms.append(term)
    terms.sort(lambda l, r: cmp(l.title.lower(), r.title.lower()))
    return SimpleVocabulary(terms)


OrganisationalUnit_OrganisationalUnits_RelManager = \
       FieldRelationManager(IOrganisationalUnit['subOUs'],
                            IOrganisationalUnit['parent_O_OU'],
                            relType='parent_O_OU:subOUs')


class OrganisationalUnit(ContactItem):
    """
    the template instance
    """
    implements(IOrganisationalUnit)
    shortName = "organisational_unit"
    # for ..Contained we have to:
    __name__ = __parent__ = None

    name = FieldProperty(IOrganisationalUnit['name'])
    subOUs = RelationPropertyOut(\
         OrganisationalUnit_OrganisationalUnits_RelManager)
    parent_O_OU = RelationPropertyIn(\
         OrganisationalUnit_OrganisationalUnits_RelManager)

    fullTextSearchFields = ['name']
    fullTextSearchFields.extend(ContactItem.fullTextSearchFields)
        

    def __init__(self, **data):
        """
        constructor of the object
        """
        ContactItem.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(OrganisationalUnit)
        for (name, value) in data.items():
            if name in IOrganisationalUnit.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        self.ikRevision = __version__

    def getRefAttributeNames(self):
        return getRefAttributeNames(OrganisationalUnit)

    def store_refs(self, **data):
        ContactItem.store_refs(self, **data)
        refAttributeNames = self.getRefAttributeNames()
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class OrganisationalUnitFolder(ComponentFolder):
    implements(IOrganisationalUnitFolder,
               IAddOrganisationalUnit)
    contentFactory = OrganisationalUnit

    def __init__(self, **data):
        """
        constructor of the object
        """
        ComponentFolder.__init__(self, **data)
