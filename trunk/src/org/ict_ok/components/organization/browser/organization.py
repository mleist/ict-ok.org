# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: template.py_cog 465 2009-03-05 02:34:02Z markusleist $
#
# pylint: disable-msg=W0232,W0142
#
"""implementation of browser class of Organization"""

__version__ = "$Id: template.py_cog 465 2009-03-05 02:34:02Z markusleist $"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form.browser import checkbox

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory, fieldsForInterface
from org.ict_ok.components.organization.interfaces import \
    IOrganization, IAddOrganization, IOrganizationFolder
from org.ict_ok.skin.menu import GlobalMenuSubItem, GlobalMenuAddItem
from org.ict_ok.components.organization.organization import Organization
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
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
from org.ict_ok.components.address.browser.address import getAddresses

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddOrganization(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Organization')
    viewURL = 'add_organization.html'
    weight = 50


class MGlobalAddOrganization(GlobalMenuAddItem):
    """ Menu Item """
    title = _(u'Add Organization')
    viewURL = 'add_organization.html'
    weight = 50
    folderInterface = IOrganizationFolder

class MSubInvOrganization(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'All Organizations')
    viewURL = '/@@all_organizations.html'
    weight = 100

# --------------- object details ---------------------------


class OrganizationDetails(ComponentDetails):
    """ Class for Organization details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []


class OrganizationFolderDetails(ComponentDetails):
    """ Class for Organization details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []
    attrInterface = IOrganization
    factory = Organization
    omitFields = OrganizationDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)

# --------------- forms ------------------------------------


class DetailsOrganizationForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Organization')
    factory = Organization
    omitFields = OrganizationDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class AddOrganizationForm(AddComponentForm):
    """Add Organization form"""
    label = _(u'Add Organization')
    factory = Organization
    attrInterface = IOrganization
    addInterface = IAddOrganization
    omitFields = OrganizationDetails.omit_addfields
    allFields = fieldsForFactory(factory, omitFields)
    addFields = fieldsForInterface(addInterface, [])
    _session_key = 'org.ict_ok.components.organization'
    allFields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget


class EditOrganizationForm(EditForm):
    """ Edit for Organization """
    label = _(u'Organization Edit Form')
    factory = Organization
    omitFields = OrganizationDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)


class DeleteOrganizationForm(DeleteForm):
    """ Delete the Organization """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this Organization: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportCsvDataForm(ImportCsvDataComponentForm):
    pass


class ImportXlsDataForm(ImportXlsDataComponentForm):
    factory = Organization
    attrInterface = IOrganization
    omitFields = OrganizationDetails.omit_viewfields
    factoryId = u'org.ict_ok.components.organization.organization.Organization'
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
        IctGetterColumn(title=_('Addresses'),
                        getter=getAddresses,
                        cell_formatter=raw_cell_formatter),
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

class AllOrganizations(Overview):
    objListInterface = IOrganization
