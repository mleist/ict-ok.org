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
"""implementation of browser class of ISDNPhone"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form.browser import checkbox

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory, fieldsForInterface
from org.ict_ok.components.isdnphone.interfaces import \
    IISDNPhone, IAddISDNPhone, IISDNPhoneFolder
from org.ict_ok.components.isdnphone.isdnphone import ISDNPhone
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
from org.ict_ok.components.physical_component.browser.physical_component import \
    PhysicalComponentDetails
from org.ict_ok.osi.interfaces import IOSIModel
from org.ict_ok.osi.interfaces import IPhysicalLayer
from org.ict_ok.components.physical_connector.interfaces import \
    IPhysicalConnector#, IPhysicalConnectorFolder, IAddPhysicalConnector

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddISDNPhone(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add ISDN Phone')
    viewURL = 'add_isdnphone.html'
    weight = 50


class MGlobalAddISDNPhone(GlobalMenuAddItem):
    """ Menu Item """
    title = _(u'Add ISDN Phone')
    viewURL = 'add_isdnphone.html'
    weight = 50
    folderInterface = IISDNPhoneFolder


class MSubInvISDNPhone(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'All ISDN Phones')
    viewURL = '/@@all_isdnphones.html'
    weight = 100

# --------------- object details ---------------------------


class ISDNPhoneDetails(PhysicalComponentDetails):
    """ Class for ISDNPhone details
    """
    omit_viewfields = PhysicalComponentDetails.omit_viewfields + []
    omit_addfields = PhysicalComponentDetails.omit_addfields + []
    omit_editfields = PhysicalComponentDetails.omit_editfields + []
    
    def otherConnectedInterfaces(self):
        return [i for i in self.connectedComponentsOnPhysicalLayer()
                if IISDNPhone.providedBy(i) and i is not self.context]


class ISDNPhoneFolderDetails(ComponentDetails):
    """ Class for ISDNPhone details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []
    attrInterface = IISDNPhone
    factory = ISDNPhone
    omitFields = ISDNPhoneDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)

# --------------- forms ------------------------------------


class DetailsISDNPhoneForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of ISDN Phone')
    factory = ISDNPhone
    omitFields = ISDNPhoneDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class AddISDNPhoneForm(AddComponentForm):
    """Add ISDN Phone form"""
    label = _(u'Add ISDN Phone')
    factory = ISDNPhone
    attrInterface = IISDNPhone
    addInterface = IAddISDNPhone
    omitFields = ISDNPhoneDetails.omit_addfields
    allFields = fieldsForFactory(factory, omitFields, [IPhysicalConnector])
    addFields = fieldsForInterface(addInterface, [])
    _session_key = 'org.ict_ok.components.isdnphone'
    allFields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget


class EditISDNPhoneForm(EditForm):
    """ Edit for ISDN Phone """
    label = _(u'ISDN Phone Edit Form')
    factory = ISDNPhone
    omitFields = ISDNPhoneDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields, [IPhysicalConnector])


class DeleteISDNPhoneForm(DeleteForm):
    """ Delete the ISDN Phone """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this ISDNPhone: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportCsvDataForm(ImportCsvDataComponentForm):
    pass


class ImportXlsDataForm(ImportXlsDataComponentForm):
    factory = ISDNPhone
    attrInterface = IISDNPhone
    omitFields = ISDNPhoneDetails.omit_viewfields
    factoryId = u'org.ict_ok.components.isdnphone.isdnphone.ISDNPhone'
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


class AllISDNPhones(Overview):
    objListInterface = IISDNPhone
