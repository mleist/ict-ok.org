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
"""implementation of browser class of Address"""

__version__ = "$Id: template.py_cog 465 2009-03-05 02:34:02Z markusleist $"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field
from z3c.form.browser import checkbox

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory, fieldsForInterface
from org.ict_ok.components.address.interfaces import IAddress, IAddAddress
from org.ict_ok.components.address.address import Address
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


class MSubAddAddress(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Address')
    viewURL = 'add_address.html'

    weight = 50

# --------------- object details ---------------------------


class AddressDetails(ComponentDetails):
    """ Class for Address details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []


class AddressFolderDetails(ComponentDetails):
    """ Class for Address details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []
    attrInterface = IAddress
    factory = Address
    omitFields = AddressDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)

# --------------- forms ------------------------------------


class DetailsAddressForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Address')
    factory = Address
    omitFields = AddressDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class AddAddressForm(AddComponentForm):
    """Add Address form"""
    label = _(u'Add Address')
    factory = Address
    attrInterface = IAddress
    addInterface = IAddAddress
    omitFields = AddressDetails.omit_addfields
    allFields = fieldsForFactory(factory, omitFields)
    addFields = fieldsForInterface(addInterface, [])
    _session_key = 'org.ict_ok.components.address'
    allFields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget


class EditAddressForm(EditForm):
    """ Edit for Address """
    label = _(u'Address Edit Form')
    factory = Address
    omitFields = AddressDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)


class DeleteAddressForm(DeleteForm):
    """ Delete the Address """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this Address: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportCsvDataForm(ImportCsvDataComponentForm):
    pass


class ImportXlsDataForm(ImportXlsDataComponentForm):
    factory = Address
    attrInterface = IAddress
    omitFields = AddressDetails.omit_viewfields
    factoryId = u'org.ict_ok.components.address.address.Address'
    allFields = fieldsForInterface(attrInterface, [])
