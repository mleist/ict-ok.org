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
"""implementation of browser class of Printer"""

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
from org.ict_ok.components.printer.interfaces import \
    IPrinter, IAddPrinter, IPrinterFolder
from org.ict_ok.components.printer.printer import Printer
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
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
from org.ict_ok.components.device.browser.device import \
    DeviceDetails
from org.ict_ok.osi.interfaces import IOSIModel
from org.ict_ok.osi.interfaces import IPhysicalLayer

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddPrinter(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Printer')
    viewURL = 'add_printer.html'
    weight = 50


class MGlobalAddPrinter(GlobalMenuAddItem):
    """ Menu Item """
    title = _(u'Add Printer')
    viewURL = 'add_printer.html'
    weight = 50
    folderInterface = IPrinterFolder


class MSubInvPrinter(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'All Printers')
    viewURL = '/@@all_printers.html'
    weight = 100

class MSubSubInvPrinter(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'## All Printers')
    viewURL = '/@@all_printers.html'
    weight = 100

# --------------- object details ---------------------------


class PrinterDetails(DeviceDetails):
    """ Class for Printer details
    """
    omit_viewfields = DeviceDetails.omit_viewfields + []
    omit_addfields = DeviceDetails.omit_addfields + []
    omit_editfields = DeviceDetails.omit_editfields + []


class PrinterFolderDetails(ComponentDetails):
    """ Class for Printer details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []
    attrInterface = IPrinter
    factory = Printer
    omitFields = PrinterDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)

# --------------- forms ------------------------------------


class DetailsPrinterForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Printer')
    factory = Printer
    omitFields = PrinterDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class AddPrinterForm(AddComponentForm):
    """Add Printer form"""
    label = _(u'Add Printer')
    factory = Printer
    attrInterface = IPrinter
    addInterface = IAddPrinter
    omitFields = PrinterDetails.omit_addfields
    allFields = fieldsForFactory(factory, omitFields)
    addFields = fieldsForInterface(addInterface, [])
    _session_key = 'org.ict_ok.components.printer'
    allFields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget


class EditPrinterForm(EditForm):
    """ Edit for Printer """
    label = _(u'Printer Edit Form')
    factory = Printer
    omitFields = PrinterDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)


class DeletePrinterForm(DeleteForm):
    """ Delete the Printer """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this Printer: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportCsvDataForm(ImportCsvDataComponentForm):
    pass


class ImportXlsDataForm(ImportXlsDataComponentForm):
    factory = Printer
    attrInterface = IPrinter
    omitFields = PrinterDetails.omit_viewfields
    factoryId = u'org.ict_ok.components.printer.printer.Printer'
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


class AllPrinters(Overview):
    objListInterface = IPrinter
