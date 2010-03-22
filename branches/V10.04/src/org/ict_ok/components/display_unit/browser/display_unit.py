# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232,W0142
#
"""implementation of browser class of DisplayUnit"""

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
from org.ict_ok.components.display_unit.interfaces import \
    IDisplayUnit, IAddDisplayUnit, IDisplayUnitFolder
from org.ict_ok.components.display_unit.display_unit import DisplayUnit
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.skin.menu import GlobalMenuSubItem, GlobalMenuAddItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditForm
from org.ict_ok.components.superclass.browser.superclass import \
    Overview as SuperOverview
from org.ict_ok.components.browser.component import AddComponentForm
from org.ict_ok.components.browser.component import ImportXlsDataComponentForm
from org.ict_ok.components.superclass.browser.superclass import \
    GetterColumn, DateGetterColumn, getStateIcon, raw_cell_formatter, \
    getHealth, getTitle, getModifiedDate, link, getActionBottons, IctGetterColumn
from org.ict_ok.components.physical_component.browser.physical_component import \
    getUserName, fsearch_user_formatter
from org.ict_ok.components.physical_component.browser.physical_component import \
    PhysicalComponentDetails
from org.ict_ok.osi.interfaces import IOSIModel
from org.ict_ok.osi.interfaces import IPhysicalLayer

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddDisplayUnit(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Display unit instance')
    viewURL = 'add_display_unit.html'
    weight = 50


class MGlobalAddDisplayUnit(GlobalMenuAddItem):
    """ Menu Item """
    title = _(u'Add Display unit instance')
    viewURL = 'add_display_unit.html'
    weight = 50
    folderInterface = IDisplayUnitFolder


class MSubInvDisplayUnit(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'All Display unit instances')
    viewURL = '/@@all_display_units.html'
    weight = 100

# --------------- object details ---------------------------


class DisplayUnitDetails(PhysicalComponentDetails):
    """ Class for DisplayUnit details
    """
    omit_viewfields = PhysicalComponentDetails.omit_viewfields + []
    omit_addfields = PhysicalComponentDetails.omit_addfields + []
    omit_editfields = PhysicalComponentDetails.omit_editfields + []


class DisplayUnitFolderDetails(ComponentDetails):
    """ Class for DisplayUnit details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []
    attrInterface = IDisplayUnit
    factory = DisplayUnit
    omitFields = DisplayUnitDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)

# --------------- forms ------------------------------------


class DetailsDisplayUnitForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Display unit instance')
    factory = DisplayUnit
    omitFields = DisplayUnitDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class AddDisplayUnitForm(AddComponentForm):
    """Add Display unit instance form"""
    label = _(u'Add Display unit instance')
    factory = DisplayUnit
    attrInterface = IDisplayUnit
    addInterface = IAddDisplayUnit
    omitFields = DisplayUnitDetails.omit_addfields
    allFields = fieldsForFactory(factory, omitFields)
    addFields = fieldsForInterface(addInterface, [])
    _session_key = 'org.ict_ok.components.display_unit'
    allFields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget


class EditDisplayUnitForm(EditForm):
    """ Edit for Display unit instance """
    label = _(u'Display unit instance Edit Form')
    factory = DisplayUnit
    omitFields = DisplayUnitDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)


class DeleteDisplayUnitForm(DeleteForm):
    """ Delete the Display unit instance """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this DisplayUnit: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportXlsDataForm(ImportXlsDataComponentForm):
    factory = DisplayUnit
    attrInterface = IDisplayUnit
    omitFields = DisplayUnitDetails.omit_viewfields
    factoryId = u'org.ict_ok.components.display_unit.display_unit.DisplayUnit'
    allFields = fieldsForInterface(attrInterface, [])


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


class AllDisplayUnits(Overview):
    objListInterface = IDisplayUnit
