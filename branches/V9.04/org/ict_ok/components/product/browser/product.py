# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: template.py_cog 465 2009-03-05 02:34:02Z markusleist $
#
# pylint: disable-msg=W0232,W0142
#
"""implementation of browser class of Product"""

__version__ = "$Id: template.py_cog 465 2009-03-05 02:34:02Z markusleist $"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field
from z3c.form.browser import checkbox

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory, fieldsForInterface
from org.ict_ok.components.product.interfaces import IProduct, IAddProduct
from org.ict_ok.components.product.product import Product
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditForm
from org.ict_ok.components.browser.component import AddComponentForm
from org.ict_ok.components.browser.component import ImportCsvDataComponentForm
from org.ict_ok.components.browser.component import ImportXlsDataComponentForm

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddProduct(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Product')
    viewURL = 'add_product.html'

    weight = 50

# --------------- object details ---------------------------


class ProductDetails(ComponentDetails):
    """ Class for Product details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []


class ProductFolderDetails(ComponentDetails):
    """ Class for Product details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []
    attrInterface = IProduct
    factory = Product
    omitFields = ProductDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)

# --------------- forms ------------------------------------


class DetailsProductForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Product')
    factory = Product
    omitFields = ProductDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class AddProductForm(AddComponentForm):
    """Add Product form"""
    label = _(u'Add Product')
    factory = Product
    attrInterface = IProduct
    addInterface = IAddProduct
    omitFields = ProductDetails.omit_addfields
    allFields = fieldsForFactory(factory, omitFields)
    addFields = fieldsForInterface(addInterface, [])
    _session_key = 'org.ict_ok.components.product'
    allFields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget


class EditProductForm(EditForm):
    """ Edit for Product """
    label = _(u'Product Edit Form')
    factory = Product
    omitFields = ProductDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)


class DeleteProductForm(DeleteForm):
    """ Delete the Product """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this Product: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportCsvDataForm(ImportCsvDataComponentForm):
    pass


class ImportXlsDataForm(ImportXlsDataComponentForm):
    factory = Product
    attrInterface = IProduct
    omitFields = ProductDetails.omit_viewfields
    factoryId = u'org.ict_ok.components.product.product.Product'
    allFields = fieldsForInterface(attrInterface, [])
