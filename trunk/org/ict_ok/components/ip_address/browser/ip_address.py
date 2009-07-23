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
"""implementation of browser class of IpAddress"""

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
from org.ict_ok.components.ip_address.interfaces import \
    IIpAddress, IAddIpAddress, IIpAddressFolder
from org.ict_ok.components.ip_address.ip_address import IpAddress
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
from org.ict_ok.components.logical_component.browser.logical_component import \
    LogicalComponentDetails
from org.ict_ok.osi.interfaces import IOSIModel
from org.ict_ok.osi.interfaces import IPhysicalLayer

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddIpAddress(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add IP address')
    viewURL = 'add_ip_address.html'
    weight = 50


class MGlobalAddIpAddress(GlobalMenuAddItem):
    """ Menu Item """
    title = _(u'Add IP address')
    viewURL = 'add_ip_address.html'
    weight = 50
    folderInterface = IIpAddressFolder


class MSubInvIpAddress(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'All IP addresses')
    viewURL = '/@@all_ip_addresses.html'
    weight = 100

# --------------- object details ---------------------------


class IpAddressDetails(LogicalComponentDetails):
    """ Class for IpAddress details
    """
    omit_viewfields = LogicalComponentDetails.omit_viewfields + []
    omit_addfields = LogicalComponentDetails.omit_addfields + []
    omit_editfields = LogicalComponentDetails.omit_editfields + []


class IpAddressFolderDetails(ComponentDetails):
    """ Class for IpAddress details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []
    attrInterface = IIpAddress
    factory = IpAddress
    omitFields = IpAddressDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)

# --------------- forms ------------------------------------


class DetailsIpAddressForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of IP address')
    factory = IpAddress
    omitFields = IpAddressDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class AddIpAddressForm(AddComponentForm):
    """Add IP address form"""
    label = _(u'Add IP address')
    factory = IpAddress
    attrInterface = IIpAddress
    addInterface = IAddIpAddress
    omitFields = IpAddressDetails.omit_addfields
    allFields = fieldsForFactory(factory, omitFields)
    addFields = fieldsForInterface(addInterface, [])
    _session_key = 'org.ict_ok.components.ip_address'
    allFields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget


class EditIpAddressForm(EditForm):
    """ Edit for IP address """
    label = _(u'IP address Edit Form')
    factory = IpAddress
    omitFields = IpAddressDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)


class DeleteIpAddressForm(DeleteForm):
    """ Delete the IP address """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this IpAddress: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportCsvDataForm(ImportCsvDataComponentForm):
    pass


class ImportXlsDataForm(ImportXlsDataComponentForm):
    factory = IpAddress
    attrInterface = IIpAddress
    omitFields = IpAddressDetails.omit_viewfields
    factoryId = u'org.ict_ok.components.ip_address.ip_address.IpAddress'
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



class AllIpAddresses(Overview):
    def objs(self):
        """List of all objects with selected interface"""
        retList = []
        uidutil = queryUtility(IIntIds)
        for (oid, oobj) in uidutil.items():
            if IIpAddress.providedBy(oobj.object):
                retList.append(oobj.object)
        return retList


