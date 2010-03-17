# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232,W0142
#
"""implementation of browser class of Notebook"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory
from zope.component import queryUtility
from zope.app.intid.interfaces import IIntIds

# z3c imports
from z3c.form import field
from z3c.form.browser import checkbox

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory, fieldsForInterface
from org.ict_ok.components.notebook.interfaces import \
    INotebook, IAddNotebook, INotebookFolder
from org.ict_ok.components.notebook.notebook import Notebook
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.components.superclass.superclass import objectsWithInterface
from org.ict_ok.skin.menu import GlobalMenuSubItem, GlobalMenuAddItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditForm
from org.ict_ok.components.superclass.browser.superclass import \
    Overview as SuperOverview
from org.ict_ok.components.browser.component import AddComponentForm
from org.ict_ok.components.browser.component import ImportCsvDataComponentForm
from org.ict_ok.components.browser.component import ImportXlsDataComponentForm
from org.ict_ok.components.superclass.browser.superclass import \
    GetterColumn, DateGetterColumn, getStateIcon, raw_cell_formatter, \
    getHealth, getTitle, getModifiedDate, link, getActionBottons, IctGetterColumn
from org.ict_ok.components.physical_component.browser.physical_component import \
    getUserName, fsearch_user_formatter

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddNotebook(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Notebook')
    viewURL = 'add_notebook.html'
    weight = 50


class MGlobalAddNotebook(GlobalMenuAddItem):
    """ Menu Item """
    title = _(u'Add Notebook')
    viewURL = 'add_notebook.html'
    weight = 50
    folderInterface = INotebookFolder


class MSubInvNotebook(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'All notebooks')
    viewURL = '/@@all_notebooks.html'
    weight = 100

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
    attrInterface = INotebook
    factory = Notebook
    fields = fieldsForFactory(factory, omit_editfields)

# --------------- forms ------------------------------------


class DetailsNotebookForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Notebook')
    factory = Notebook
    omitFields = NotebookDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class AddNotebookForm(AddComponentForm):
    """Add Notebook form"""
    label = _(u'Add Notebook')
    factory = Notebook
    omitFields = NotebookDetails.omit_addfields
    attrInterface = INotebook
    addInterface = IAddNotebook
    _session_key = 'org.ict_ok.components.notebook'
    allFields = fieldsForFactory(factory, omitFields)
    addFields = fieldsForInterface(addInterface, [])
    allFields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget


class EditNotebookForm(EditForm):
    """ Edit for Notebook """
    label = _(u'Notebook Edit Form')
    factory = Notebook
    omitFields = NotebookDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)


class DeleteNotebookForm(DeleteForm):
    """ Delete the Notebook """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        import pdb
        pdb.set_trace()
        return _(u"Delete this Notebook: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportCsvDataForm(ImportCsvDataComponentForm):
    pass


class ImportXlsDataForm(ImportXlsDataComponentForm):
    attrInterface = INotebook
    factory = Notebook
    factoryId = u'org.ict_ok.components.notebook.notebook.Notebook'
    allFields = fieldsForInterface(attrInterface, [])

#def getRoom(item, formatter):
#    if item.device is not None:
#        return item.device.room
#    return None


class Overview(SuperOverview):
    columns = (
        GetterColumn(title="",
                     getter=getStateIcon,
                     cell_formatter=raw_cell_formatter),
        GetterColumn(title=_('Health'),
                     getter=getHealth),
        IctGetterColumn(title=_('Title'),
                        getter=getTitle,
                        cell_formatter=link('overview.html')),
        IctGetterColumn(title=_('User'),
                        getter=getUserName,
                        cell_formatter=fsearch_user_formatter),
        IctGetterColumn(title=_('Room'),
                        getter=lambda i,f: i.room,
                        cell_formatter=link('details.html')),
        DateGetterColumn(title=_('Modified'),
                        getter=getModifiedDate,
                        subsort=True,
                        cell_formatter=raw_cell_formatter),
        GetterColumn(title=_('Actions'),
                     getter=getActionBottons,
                     cell_formatter=raw_cell_formatter),
        )
    pos_column_index = 1
    sort_columns = [1, 2, 3, 4, 5]

class AllNotebooks(Overview):
    objListInterface = INotebook
