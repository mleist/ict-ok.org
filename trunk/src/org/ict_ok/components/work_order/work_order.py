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
"""implementation of WorkOrder"""

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

# lovely imports
from lovely.relation.property import RelationPropertyIn
from lovely.relation.property import RelationPropertyOut
from lovely.relation.property import FieldRelationManager

# ict_ok.org imports
from org.ict_ok.components.component import getRefAttributeNames
from org.ict_ok.components.superclass.superclass import Superclass
from org.ict_ok.components.work_order.interfaces import IWorkOrder
from org.ict_ok.components.work_order.interfaces import IWorkOrderFolder
from org.ict_ok.components.work_order.interfaces import IAddWorkOrder
from org.ict_ok.components.component import Component, ComponentFolder
from org.ict_ok.components.interfaces import \
    IImportCsvData, IImportXlsData
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents
from org.ict_ok.components.product.interfaces import IProduct
from org.ict_ok.components.contact.interfaces import IContact
from org.ict_ok.components.contact_item.interfaces import IContactItem

def AllWorkOrderTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IWorkOrder)

def AllWorkOrders(dummy_context):
    return AllComponents(dummy_context, IWorkOrder)

def AllUnusedOrUsedWorkOrderWorkOrders(dummy_context):
    return AllUnusedOrSelfComponents(dummy_context, IWorkOrder, 'mainWorkOrder')


WorkOrder_Products_RelManager = \
       FieldRelationManager(IWorkOrder['products'],
                            IProduct['workOrder'],
                            relType='workOrder:products')
WorkOrder_ContactItems_RelManager = \
       FieldRelationManager(IWorkOrder['contactItems'],
                            IContactItem['workOrder'],
                            relType='workOrder:contactItems')
WorkOrder_Contacts_RelManager = \
       FieldRelationManager(IWorkOrder['contacts'],
                            IContact['workOrder'],
                            relType='workOrder:contacts')
WorkOrder_WorkOrders_RelManager = \
       FieldRelationManager(IWorkOrder['subWorkOrders'],
                            IWorkOrder['mainWorkOrder'],
                            relType='mainWorkOrder:subWorkOrders')




class WorkOrder(Component):
    """
    the template instance
    """
    implements(IWorkOrder)
    shortName = "work_order"
    # for ..Contained we have to:
    __name__ = __parent__ = None

    mainWorkOrder = RelationPropertyIn(WorkOrder_WorkOrders_RelManager)
    products = RelationPropertyOut(WorkOrder_Products_RelManager)
    contactItems = RelationPropertyOut(WorkOrder_ContactItems_RelManager)
    contacts = RelationPropertyOut(WorkOrder_Contacts_RelManager)
    subWorkOrders = RelationPropertyOut(WorkOrder_WorkOrders_RelManager)

    fullTextSearchFields = []
    fullTextSearchFields.extend(Component.fullTextSearchFields)
        


    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(WorkOrder)
        for (name, value) in data.items():
            if name in IWorkOrder.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        self.ikRevision = __version__

    def getRefAttributeNames(self):
        return getRefAttributeNames(WorkOrder)

    def store_refs(self, **data):
        Component.store_refs(self, **data)
        refAttributeNames = self.getRefAttributeNames()
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class WorkOrderFolder(ComponentFolder):
    implements(IWorkOrderFolder,
               IAddWorkOrder)
    contentFactory = WorkOrder

    def __init__(self, **data):
        """
        constructor of the object
        """
        ComponentFolder.__init__(self, **data)
