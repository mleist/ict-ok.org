# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: template.py_cog 396 2009-01-08 00:21:51Z markusleist $
#
# pylint: disable-msg=W0232,W0142
#
"""implementation of browser class of Notebook"""

__version__ = "$Id: template.py_cog 396 2009-01-08 00:21:51Z markusleist $"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field
from z3c.form.browser import checkbox

# ict_ok.org imports
from org.ict_ok.components.notebook.interfaces import INotebook, IAddNotebook
from org.ict_ok.components.notebook.notebook import Notebook
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


class MSubAddNotebook(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Notebook')
    viewURL = 'add_notebook.html'

    weight = 50

# --------------- object details ---------------------------


class NotebookDetails(ComponentDetails):
    """ Class for Notebook details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []


class NotebookFolderDetails(ComponentDetails):
    """ Class for MobilePhone details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + ['requirement']
    omit_addfields = ComponentDetails.omit_addfields + ['requirement']
    omit_editfields = ComponentDetails.omit_editfields + ['requirement']
    fields = field.Fields(INotebook).omit(*NotebookDetails.omit_viewfields)
    attrInterface = INotebook

# --------------- forms ------------------------------------


class DetailsNotebookForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Notebook')
    fields = field.Fields(INotebook).omit(*NotebookDetails.omit_viewfields)


class AddNotebookForm(AddComponentForm):
    """Add Notebook form"""
    label = _(u'Add Notebook')
    addFields = field.Fields(IAddNotebook)
    allFields = field.Fields(INotebook).omit(*NotebookDetails.omit_addfields)
    allFields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget
    factory = Notebook
    attrInterface = INotebook
    _session_key = 'org.ict_ok.components.notebook'
    

class EditNotebookForm(EditForm):
    """ Edit for Notebook """
    label = _(u'Notebook Edit Form')
    fields = field.Fields(INotebook).omit(*NotebookDetails.omit_editfields)


class DeleteNotebookForm(DeleteForm):
    """ Delete the Notebook """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this Notebook: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportCsvDataForm(ImportCsvDataComponentForm):
    pass


class ImportXlsDataForm(ImportXlsDataComponentForm):
    allFields = field.Fields(INotebook)
#    allFields['isTemplate'].widgetFactory = \
#        checkbox.SingleCheckBoxFieldWidget
    attrInterface = INotebook
    factory = Notebook
    factoryId = u'org.ict_ok.components.notebook.notebook.Notebook'
