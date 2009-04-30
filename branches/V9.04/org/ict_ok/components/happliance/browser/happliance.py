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
"""implementation of browser class of HardwareAppliance"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field
from z3c.form.browser import checkbox

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory, fieldsForInterface
from org.ict_ok.components.happliance.interfaces import IHardwareAppliance, IAddHardwareAppliance
from org.ict_ok.components.happliance.happliance import HardwareAppliance
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


class MSubAddHardwareAppliance(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Hardware Appliance')
    viewURL = 'add_happliance.html'

    weight = 50

# --------------- object details ---------------------------


class HardwareApplianceDetails(ComponentDetails):
    """ Class for HardwareAppliance details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []


class HardwareApplianceFolderDetails(ComponentDetails):
    """ Class for HardwareAppliance details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []
    attrInterface = IHardwareAppliance
    factory = HardwareAppliance
    fields = fieldsForFactory(factory, omit_editfields)

# --------------- forms ------------------------------------


class DetailsHardwareApplianceForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Hardware Appliance')
    factory = HardwareAppliance
    omitFields = HardwareApplianceDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class AddHardwareApplianceForm(AddComponentForm):
    """Add Hardware Appliance form"""
    label = _(u'Add Hardware Appliance')
    factory = HardwareAppliance
    attrInterface = IHardwareAppliance
    addInterface = IAddHardwareAppliance
    omitFields = HardwareApplianceDetails.omit_addfields
    _session_key = 'org.ict_ok.components.happliance'
    allFields = fieldsForFactory(factory, omitFields)
    addFields = fieldsForInterface(addInterface, [])
    allFields['isTemplate'].widgetFactory = checkbox.SingleCheckBoxFieldWidget


class EditHardwareApplianceForm(EditForm):
    """ Edit for Hardware Appliance """
    label = _(u'Hardware Appliance Edit Form')
    factory = HardwareAppliance
    omitFields = HardwareApplianceDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)


class DeleteHardwareApplianceForm(DeleteForm):
    """ Delete the Hardware Appliance """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this HardwareAppliance: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportCsvDataForm(ImportCsvDataComponentForm):
    pass


class ImportXlsDataForm(ImportXlsDataComponentForm):
    attrInterface = IHardwareAppliance
    factory = HardwareAppliance
    factoryId = u'org.ict_ok.components.happliance.happliance.HardwareAppliance'
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
