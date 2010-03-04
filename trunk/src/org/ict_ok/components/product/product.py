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
"""implementation of Product"""

__version__ = "$Id: template.py_cog 465 2009-03-05 02:34:02Z markusleist $"

# python imports

# zope imports
from zope.interface import implements
from zope.app.intid.interfaces import IIntIds
from zope.component import getUtility

# lovely imports
from lovely.relation.property import RelationPropertyIn
from lovely.relation.property import RelationPropertyOut
from lovely.relation.property import FieldRelationManager

# ict_ok.org imports
from org.ict_ok.components.component import getRefAttributeNames
from org.ict_ok.components.product.interfaces import IProduct
from org.ict_ok.components.product.interfaces import IProductFolder
from org.ict_ok.components.product.interfaces import IAddProduct
from org.ict_ok.components.component import Component, ComponentFolder
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents
from org.ict_ok.components.work_order.work_order import WorkOrder_Products_RelManager

def AllProductTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IProduct)

def AllProducts(dummy_context):
    return AllComponents(dummy_context, IProduct)

def AllUnusedOrUsedProductProducts(dummy_context):
    return AllUnusedOrSelfComponents(dummy_context, IProduct, 'mainProduct')
def AllUnusedOrUsedWorkOrderProducts(dummy_context):
    return AllUnusedOrSelfComponents(dummy_context, IProduct, 'workOrder')


Product_Products_RelManager = \
       FieldRelationManager(IProduct['subProducts'],
                            IProduct['mainProduct'],
                            relType='mainProduct:subProducts')


def getFirstLevelObjectList(foldername):
    uidutil = getUtility(IIntIds)
    i_list = [oobj.object for (oid, oobj) in uidutil.items() \
              if IProduct.providedBy(oobj.object) and \
              oobj.object.mainProduct is None]
    i_list.sort(cmp=lambda x,y: x.ikName < y.ikName)
    return (foldername, i_list)



class Product(Component):
    """
    the template instance
    """
    implements(IProduct)
    shortName = "product"
    # for ..Contained we have to:
    __name__ = __parent__ = None

    mainProduct = RelationPropertyIn(Product_Products_RelManager)
    workOrder = RelationPropertyIn(WorkOrder_Products_RelManager)
    subProducts = RelationPropertyOut(Product_Products_RelManager)

    fullTextSearchFields = []
    fullTextSearchFields.extend(Component.fullTextSearchFields)
        


    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(Product)
        for (name, value) in data.items():
            if name in IProduct.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        self.ikRevision = __version__

    def getRefAttributeNames(self):
        return getRefAttributeNames(Product)

    def store_refs(self, **data):
        Component.store_refs(self, **data)
        refAttributeNames = self.getRefAttributeNames()
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class ProductFolder(ComponentFolder):
    implements(IProductFolder,
               IAddProduct)
    contentFactory = Product
    shortName = "product folder"

    def __init__(self, **data):
        """
        constructor of the object
        """
        ComponentFolder.__init__(self, **data)
