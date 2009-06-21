# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: template.py_cog 529 2009-05-14 17:46:43Z markusleist $
#
# pylint: disable-msg=W0232,W0142
#
"""implementation of browser class of Contract"""

__version__ = "$Id: template.py_cog 529 2009-05-14 17:46:43Z markusleist $"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field
from z3c.form.browser import checkbox

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory, fieldsForInterface
from org.ict_ok.components.contract.interfaces import \
    IContract, IAddContract, IContractFolder
from org.ict_ok.components.contract.contract import Contract
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.skin.menu import GlobalMenuSubItem, GlobalMenuAddItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditForm
from org.ict_ok.components.browser.component import AddComponentForm
from org.ict_ok.components.browser.component import ImportCsvDataComponentForm
from org.ict_ok.components.browser.component import ImportXlsDataComponentForm

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddContract(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Contract')
    viewURL = 'add_contract.html'
    weight = 50


class MGlobalAddContract(GlobalMenuAddItem):
    """ Menu Item """
    title = _(u'Add Contract')
    viewURL = 'add_contract.html'
    weight = 50
    folderInterface = IContractFolder

# --------------- object details ---------------------------


class ContractDetails(ComponentDetails):
    """ Class for Contract details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []


class ContractFolderDetails(ComponentDetails):
    """ Class for Contract details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []
    attrInterface = IContract
    factory = Contract
    omitFields = ContractDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)

# --------------- forms ------------------------------------


class DetailsContractForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Contract')
    factory = Contract
    omitFields = ContractDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class AddContractForm(AddComponentForm):
    """Add Contract form"""
    label = _(u'Add Contract')
    factory = Contract
    attrInterface = IContract
    addInterface = IAddContract
    omitFields = ContractDetails.omit_addfields
    allFields = fieldsForFactory(factory, omitFields)
    addFields = fieldsForInterface(addInterface, [])
    _session_key = 'org.ict_ok.components.contract'
    allFields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget


class EditContractForm(EditForm):
    """ Edit for Contract """
    label = _(u'Contract Edit Form')
    factory = Contract
    omitFields = ContractDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)


class DeleteContractForm(DeleteForm):
    """ Delete the Contract """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this Contract: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportCsvDataForm(ImportCsvDataComponentForm):
    pass


class ImportXlsDataForm(ImportXlsDataComponentForm):
    factory = Contract
    attrInterface = IContract
    omitFields = ContractDetails.omit_viewfields
    factoryId = u'org.ict_ok.components.contract.contract.Contract'
    allFields = fieldsForInterface(attrInterface, [])
