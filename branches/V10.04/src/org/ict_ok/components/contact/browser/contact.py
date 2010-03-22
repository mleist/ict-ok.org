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
"""implementation of browser class of Contact"""

__version__ = "$Id: template.py_cog 465 2009-03-05 02:34:02Z markusleist $"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field
from z3c.form.browser import checkbox

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory, fieldsForInterface
from org.ict_ok.components.contact.interfaces import \
    IContact, IAddContact, IContactFolder
from org.ict_ok.components.contact.contact import Contact
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.skin.menu import GlobalMenuSubItem, GlobalMenuAddItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditForm
from org.ict_ok.components.browser.component import AddComponentForm
from org.ict_ok.components.browser.component import ImportXlsDataComponentForm

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddContact(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Contact')
    viewURL = 'add_contact.html'
    weight = 50


class MGlobalAddContact(GlobalMenuAddItem):
    """ Menu Item """
    title = _(u'Add Contact')
    viewURL = 'add_contact.html'
    weight = 50
    folderInterface = IContactFolder

# --------------- object details ---------------------------


class ContactDetails(ComponentDetails):
    """ Class for Contact details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []


class ContactFolderDetails(ComponentDetails):
    """ Class for Contact details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []
    attrInterface = IContact
    factory = Contact
    omitFields = ContactDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)

# --------------- forms ------------------------------------


class DetailsContactForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Contact')
    factory = Contact
    omitFields = ContactDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class AddContactForm(AddComponentForm):
    """Add Contact form"""
    label = _(u'Add Contact')
    factory = Contact
    attrInterface = IContact
    addInterface = IAddContact
    omitFields = ContactDetails.omit_addfields
    allFields = fieldsForFactory(factory, omitFields)
    addFields = fieldsForInterface(addInterface, [])
    _session_key = 'org.ict_ok.components.contact'
    allFields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget


class EditContactForm(EditForm):
    """ Edit for Contact """
    label = _(u'Contact Edit Form')
    factory = Contact
    omitFields = ContactDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)


class DeleteContactForm(DeleteForm):
    """ Delete the Contact """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this Contact: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportXlsDataForm(ImportXlsDataComponentForm):
    factory = Contact
    attrInterface = IContact
    omitFields = ContactDetails.omit_viewfields
    factoryId = u'org.ict_ok.components.contact.contact.Contact'
    allFields = fieldsForInterface(attrInterface, [])
