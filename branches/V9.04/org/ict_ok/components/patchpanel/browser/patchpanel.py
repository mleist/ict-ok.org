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
"""implementation of browser class of PatchPanel"""

__version__ = "$Id: template.py_cog 411 2009-01-29 16:16:51Z markusleist $"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field
from z3c.form.browser import checkbox

# ict_ok.org imports
from org.ict_ok.components.patchpanel.interfaces import IPatchPanel, IAddPatchPanel
from org.ict_ok.components.patchpanel.patchpanel import PatchPanel
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


class MSubAddPatchPanel(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Patch panel')
    viewURL = 'add_patchpanel.html'

    weight = 50

# --------------- object details ---------------------------


class PatchPanelDetails(ComponentDetails):
    """ Class for PatchPanel details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []


class PatchPanelFolderDetails(ComponentDetails):
    """ Class for PatchPanel details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []
    fields = field.Fields(IPatchPanel).omit(*PatchPanelDetails.omit_viewfields)
    attrInterface = IPatchPanel

# --------------- forms ------------------------------------


class DetailsPatchPanelForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Patch panel')
    fields = field.Fields(IPatchPanel).omit(*PatchPanelDetails.omit_viewfields)


class AddPatchPanelForm(AddComponentForm):
    """Add Patch panel form"""
    label = _(u'Add Patch panel')
    addFields = field.Fields(IAddPatchPanel)
    allFields = field.Fields(IPatchPanel).omit(*PatchPanelDetails.omit_addfields)
    allFields['isTemplate'].widgetFactory =         checkbox.SingleCheckBoxFieldWidget
    factory = PatchPanel
    attrInterface = IPatchPanel
    _session_key = 'org.ict_ok.components.patchpanel'


class EditPatchPanelForm(EditForm):
    """ Edit for Patch panel """
    label = _(u'Patch panel Edit Form')
    fields = field.Fields(IPatchPanel).omit(*PatchPanelDetails.omit_editfields)


class DeletePatchPanelForm(DeleteForm):
    """ Delete the Patch panel """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this PatchPanel: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportCsvDataForm(ImportCsvDataComponentForm):
    pass


class ImportXlsDataForm(ImportXlsDataComponentForm):
    allFields = field.Fields(IPatchPanel)
    attrInterface = IPatchPanel
    factory = PatchPanel
    factoryId = u'org.ict_ok.components.patchpanel.patchpanel.PatchPanel'
