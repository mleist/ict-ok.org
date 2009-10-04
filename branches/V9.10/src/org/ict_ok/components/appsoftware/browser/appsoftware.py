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
"""implementation of browser class of ApplicationSoftware"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implementedBy
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field
from z3c.form.browser import checkbox

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory, fieldsForInterface
from org.ict_ok.components.appsoftware.interfaces import \
    IApplicationSoftware, IAddApplicationSoftware, IApplicationSoftwareFolder
from org.ict_ok.components.appsoftware.appsoftware import ApplicationSoftware
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
from org.ict_ok.components.software_component.browser.software_component import \
    SoftwareComponentDetails, SoftwareComponentFolderDetails


_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddApplicationSoftware(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Application Software')
    viewURL = 'add_appsoftware.html'
    weight = 50


class MGlobalAddApplicationSoftware(GlobalMenuAddItem):
    """ Menu Item """
    title = _(u'Add Application Software')
    viewURL = 'add_appsoftware.html'
    weight = 50
    folderInterface = IApplicationSoftwareFolder

# --------------- object details ---------------------------


class ApplicationSoftwareDetails(SoftwareComponentDetails):
    """ Class for ApplicationSoftware details
    """
    omit_viewfields = SoftwareComponentDetails.omit_viewfields + []
    omit_addfields = SoftwareComponentDetails.omit_addfields + []
    omit_editfields = SoftwareComponentDetails.omit_editfields + []


class ApplicationSoftwareFolderDetails(SoftwareComponentFolderDetails):
    """ Class for MobilePhone details
    """
    omit_viewfields = SoftwareComponentFolderDetails.omit_viewfields + ['requirement']
    omit_addfields = SoftwareComponentFolderDetails.omit_addfields + ['requirement']
    omit_editfields = SoftwareComponentFolderDetails.omit_editfields + ['requirement']
    
#    fields = field.Fields(IApplicationSoftware).omit(*ApplicationSoftwareDetails.omit_viewfields)
    factory = ApplicationSoftware
    omitFields = ApplicationSoftwareDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)
    attrInterface = IApplicationSoftware

# --------------- forms ------------------------------------


class DetailsApplicationSoftwareForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Application Software Instance')
    factory = ApplicationSoftware
    omitFields = ApplicationSoftwareDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class AddApplicationSoftwareForm(AddComponentForm):
    """Add Application Software Instance form"""
    label = _(u'Add Application Software Instance')
    factory = ApplicationSoftware
    attrInterface = IApplicationSoftware
    addInterface = IAddApplicationSoftware
    omitFields = ApplicationSoftwareDetails.omit_addfields
    _session_key = 'org.ict_ok.components.asoftware'
    allFields = fieldsForFactory(factory, omitFields)
    addFields = fieldsForInterface(addInterface, [])

class EditApplicationSoftwareForm(EditForm):
    """ Edit for Application Software Instance """
    label = _(u'Application Software Instance Edit Form')
    factory = ApplicationSoftware
    omitFields = ApplicationSoftwareDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)


class DeleteApplicationSoftwareForm(DeleteForm):
    """ Delete the Application Software Instance """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this ApplicationSoftware: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportCsvDataForm(ImportCsvDataComponentForm):
    pass


class ImportXlsDataForm(ImportXlsDataComponentForm):
    attrInterface = IApplicationSoftware
    factory = ApplicationSoftware
    factoryId = u'org.ict_ok.components.appsoftware.appsoftware.ApplicationSoftware'
    #allFields = fieldsForInterface(attrInterface, [])
    omitFields = ApplicationSoftwareDetails.omit_viewfields
    allFields = fieldsForFactory(factory, omitFields)


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
        IctGetterColumn(title=_('Device'),
                        getter=lambda i,f: i.device,
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
