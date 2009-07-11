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
"""implementation of Contract"""

__version__ = "$Id: template.py_cog 465 2009-03-05 02:34:02Z markusleist $"

# python imports

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.app.intid.interfaces import IIntIds
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds
from zope.app.folder import Folder
from zope.i18nmessageid import MessageFactory

# lovely imports
from lovely.relation.property import RelationPropertyIn
from lovely.relation.property import RelationPropertyOut
from lovely.relation.property import FieldRelationManager

# ict_ok.org imports
from org.ict_ok.libs.lib import getRefAttributeNames
from org.ict_ok.components.superclass.superclass import Superclass
from org.ict_ok.components.contract.interfaces import IContract
from org.ict_ok.components.contract.interfaces import IContractFolder
from org.ict_ok.components.contract.interfaces import IAddContract
from org.ict_ok.components.interfaces import \
    IImportCsvData, IImportXlsData
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents
from org.ict_ok.components.interfaces import IComponent
from org.ict_ok.components.component import Component, Contracts_Component_RelManager
from org.ict_ok.components.contact_item.interfaces import IContactItem

def AllContractTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IContract)

def AllContracts(dummy_context):
    return AllComponents(dummy_context, IContract)

def AllUnusedOrUsedComponentContracts(dummy_context):
    return AllUnusedOrSelfComponents(dummy_context, IContract, 'component')


_ = MessageFactory('org.ict_ok')

def ContractTypes(dummy_context):
    terms = []
    for (gkey, gname) in {
        'Contract of sale': _(u'Contract of sale'),
        }.items():
        terms.append(SimpleTerm(gkey, str(gkey), gname))
    return SimpleVocabulary(terms)

def ContractState(dummy_context):
    terms = []
    for (gkey, gname) in {
        'draft': _(u'Draft'),
        'approved': _(u'Approved'),
        }.items():
        terms.append(SimpleTerm(gkey, str(gkey), gname))
    return SimpleVocabulary(terms)

ClosedContracts_ContactItems_RelManager = \
       FieldRelationManager(IContract['contractors'],
                            IContactItem['closedContracts'],
                            relType='closedContracts:contractors')

Responsible4Contracts_ContactItems_RelManager = \
       FieldRelationManager(IContract['responsibles'],
                            IContactItem['responsible4Contracts'],
                            relType='responsible4Contracts:responsibles')



class Contract(Component):
    """
    the template instance
    """
    implements(IContract)
    shortName = "contract"
    # for ..Contained we have to:
    __name__ = __parent__ = None

    type = FieldProperty(IContract['type'])
    startDate = FieldProperty(IContract['startDate'])
    state = FieldProperty(IContract['state'])
    expirationDate = FieldProperty(IContract['expirationDate'])
    annualCharges = FieldProperty(IContract['annualCharges'])
    internalContractNumber = FieldProperty(IContract['internalContractNumber'])
    externalContractNumber = FieldProperty(IContract['externalContractNumber'])
    periodOfNotice = FieldProperty(IContract['periodOfNotice'])
    minimumTerm = FieldProperty(IContract['minimumTerm'])
    responsibles = RelationPropertyOut(Responsible4Contracts_ContactItems_RelManager)
    contractors = RelationPropertyOut(ClosedContracts_ContactItems_RelManager)
    component = RelationPropertyOut(Contracts_Component_RelManager)

    fullTextSearchFields = []
    fullTextSearchFields.extend(Component.fullTextSearchFields)
        


    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(Contract)
        for (name, value) in data.items():
            if name in IContract.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        self.ikRevision = __version__

    def store_refs(self, **data):
        Component.store_refs(self, **data)
        refAttributeNames = getRefAttributeNames(Contract)
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class ContractFolder(Superclass, Folder):
    implements(IContractFolder,
               IImportCsvData,
               IImportXlsData,
               IAddContract)
    def __init__(self, **data):
        """
        constructor of the object
        """
        Superclass.__init__(self, **data)
        Folder.__init__(self)
