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
"""implementation of browser class of IndustrialComputer"""

__version__ = "$Id: template.py_cog 411 2009-01-29 16:16:51Z markusleist $"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field
from z3c.form.browser import checkbox

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory, fieldsForInterface
from org.ict_ok.components.ipc.interfaces import IIndustrialComputer, IAddIndustrialComputer
from org.ict_ok.components.ipc.ipc import IndustrialComputer
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.skin.menu import GlobalMenuSubItem
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

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddIndustrialComputer(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Industrial Computer')
    viewURL = 'add_ipc.html'

    weight = 50

# --------------- object details ---------------------------


class IndustrialComputerDetails(ComponentDetails):
    """ Class for IndustrialComputer details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []


class IndustrialComputerFolderDetails(ComponentDetails):
    """ Class for IndustrialComputer details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []
    fields = field.Fields(IIndustrialComputer).omit(*IndustrialComputerDetails.omit_viewfields)
    attrInterface = IIndustrialComputer

# --------------- forms ------------------------------------


class DetailsIndustrialComputerForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Industrial Computer')
    factory = IndustrialComputer
    omitFields = IndustrialComputerDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class AddIndustrialComputerForm(AddComponentForm):
    """Add Industrial Computer form"""
    label = _(u'Add Industrial Computer')
    factory = IndustrialComputer
    attrInterface = IIndustrialComputer
    _session_key = 'org.ict_ok.components.ipc'
    addInterface = IAddIndustrialComputer
    omitFields = IndustrialComputerDetails.omit_addfields
    allFields = fieldsForFactory(factory, omitFields)
    addFields = fieldsForInterface(addInterface, [])
    allFields['isTemplate'].widgetFactory = checkbox.SingleCheckBoxFieldWidget


class EditIndustrialComputerForm(EditForm):
    """ Edit for Industrial Computer """
    label = _(u'Industrial Computer Edit Form')
    factory = IndustrialComputer
    omitFields = IndustrialComputerDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)


class DeleteIndustrialComputerForm(DeleteForm):
    """ Delete the Industrial Computer """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this IndustrialComputer: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportCsvDataForm(ImportCsvDataComponentForm):
    pass


class ImportXlsDataForm(ImportXlsDataComponentForm):
    attrInterface = IIndustrialComputer
    factory = IndustrialComputer
    factoryId = u'org.ict_ok.components.ipc.ipc.IndustrialComputer'
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
#        IctGetterColumn(title=_('Device'),
#                        getter=lambda i,f: i.device,
#                        cell_formatter=link('details.html')),
#        IctGetterColumn(title=_('Room'),
#                        getter=getRoom,
#                        cell_formatter=link('details.html')),
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
