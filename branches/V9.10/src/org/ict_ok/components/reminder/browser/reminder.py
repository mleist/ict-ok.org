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
"""implementation of browser class of Reminder"""

__version__ = "$Id: template.py_cog 529 2009-05-14 17:46:43Z markusleist $"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field
from z3c.form.browser import checkbox

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory, fieldsForInterface
from org.ict_ok.components.reminder.interfaces import \
    IReminder, IAddReminder
from org.ict_ok.components.reminder.reminder import Reminder
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


class MSubAddReminder(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Reminder')
    viewURL = 'add_reminder.html'
    weight = 50


# --------------- object details ---------------------------


class ReminderDetails(ComponentDetails):
    """ Class for Reminder details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []


class ReminderFolderDetails(ComponentDetails):
    """ Class for Reminder details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []
    attrInterface = IReminder
    factory = Reminder
    omitFields = ReminderDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)

# --------------- forms ------------------------------------


class DetailsReminderForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Reminder')
    factory = Reminder
    omitFields = ReminderDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class AddReminderForm(AddComponentForm):
    """Add Reminder form"""
    label = _(u'Add Reminder')
    factory = Reminder
    attrInterface = IReminder
    addInterface = IAddReminder
    omitFields = ReminderDetails.omit_addfields
    allFields = fieldsForFactory(factory, omitFields)
    addFields = fieldsForInterface(addInterface, [])
    _session_key = 'org.ict_ok.components.reminder'
    allFields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget


class EditReminderForm(EditForm):
    """ Edit for Reminder """
    label = _(u'Reminder Edit Form')
    factory = Reminder
    omitFields = ReminderDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)


class DeleteReminderForm(DeleteForm):
    """ Delete the Reminder """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this Reminder: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportCsvDataForm(ImportCsvDataComponentForm):
    pass


class ImportXlsDataForm(ImportXlsDataComponentForm):
    factory = Reminder
    attrInterface = IReminder
    omitFields = ReminderDetails.omit_viewfields
    factoryId = u'org.ict_ok.components.reminder.reminder.Reminder'
    allFields = fieldsForInterface(attrInterface, [])
