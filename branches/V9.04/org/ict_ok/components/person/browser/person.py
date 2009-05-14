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
"""implementation of browser class of Person"""

__version__ = "$Id: template.py_cog 465 2009-03-05 02:34:02Z markusleist $"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field
from z3c.form.browser import checkbox

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory, fieldsForInterface
from org.ict_ok.components.person.interfaces import \
    IPerson, IAddPerson, IPersonFolder
from org.ict_ok.components.person.person import Person
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


class MSubAddPerson(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Person')
    viewURL = 'add_person.html'
    weight = 50


class MGlobalAddPerson(GlobalMenuAddItem):
    """ Menu Item """
    title = _(u'Add Person')
    viewURL = 'add_person.html'
    weight = 50
    folderInterface = IPersonFolder

# --------------- object details ---------------------------


class PersonDetails(ComponentDetails):
    """ Class for Person details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []


class PersonFolderDetails(ComponentDetails):
    """ Class for Person details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []
    attrInterface = IPerson
    factory = Person
    omitFields = PersonDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)

# --------------- forms ------------------------------------


class DetailsPersonForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Person')
    factory = Person
    omitFields = PersonDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class AddPersonForm(AddComponentForm):
    """Add Person form"""
    label = _(u'Add Person')
    factory = Person
    attrInterface = IPerson
    addInterface = IAddPerson
    omitFields = PersonDetails.omit_addfields
    allFields = fieldsForFactory(factory, omitFields)
    addFields = fieldsForInterface(addInterface, [])
    _session_key = 'org.ict_ok.components.person'
    allFields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget


class EditPersonForm(EditForm):
    """ Edit for Person """
    label = _(u'Person Edit Form')
    factory = Person
    omitFields = PersonDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)


class DeletePersonForm(DeleteForm):
    """ Delete the Person """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this Person: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportCsvDataForm(ImportCsvDataComponentForm):
    pass


class ImportXlsDataForm(ImportXlsDataComponentForm):
    factory = Person
    attrInterface = IPerson
    omitFields = PersonDetails.omit_viewfields
    factoryId = u'org.ict_ok.components.person.person.Person'
    allFields = fieldsForInterface(attrInterface, [])
