# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: template.py_cog 411 2009-01-29 16:16:51Z markusleist $
#
# pylint: disable-msg=W0232,W0142
#
"""implementation of browser class of PersonalComputer"""

__version__ = "$Id: template.py_cog 411 2009-01-29 16:16:51Z markusleist $"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field
from z3c.form.browser import checkbox

# ict_ok.org imports
from org.ict_ok.components.pc.interfaces import IPersonalComputer, IAddPersonalComputer
from org.ict_ok.components.pc.pc import PersonalComputer
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


class MSubAddPersonalComputer(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Personal Computer')
    viewURL = 'add_pc.html'

    weight = 50

# --------------- object details ---------------------------


class PersonalComputerDetails(ComponentDetails):
    """ Class for PersonalComputer details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []


class PersonalComputerFolderDetails(ComponentDetails):
    """ Class for PersonalComputer details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []
    fields = field.Fields(IPersonalComputer).omit(*PersonalComputerDetails.omit_viewfields)
    attrInterface = IPersonalComputer

# --------------- forms ------------------------------------


class DetailsPersonalComputerForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Personal Computer')
    fields = field.Fields(IPersonalComputer).omit(*PersonalComputerDetails.omit_viewfields)


class AddPersonalComputerForm(AddComponentForm):
    """Add Personal Computer form"""
    label = _(u'Add Personal Computer')
    addFields = field.Fields(IAddPersonalComputer)
    allFields = field.Fields(IPersonalComputer).omit(*PersonalComputerDetails.omit_addfields)
    allFields['isTemplate'].widgetFactory =         checkbox.SingleCheckBoxFieldWidget
    factory = PersonalComputer
    attrInterface = IPersonalComputer
    _session_key = 'org.ict_ok.components.pc'


class EditPersonalComputerForm(EditForm):
    """ Edit for Personal Computer """
    label = _(u'Personal Computer Edit Form')
    fields = field.Fields(IPersonalComputer).omit(*PersonalComputerDetails.omit_editfields)


class DeletePersonalComputerForm(DeleteForm):
    """ Delete the Personal Computer """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this PersonalComputer: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportCsvDataForm(ImportCsvDataComponentForm):
    pass


class ImportXlsDataForm(ImportXlsDataComponentForm):
    allFields = field.Fields(IPersonalComputer)
    attrInterface = IPersonalComputer
    factory = PersonalComputer
    factoryId = u'org.ict_ok.components.pc.pc.PersonalComputer'
