# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232,W0142
#
"""implementation of browser class of Service object
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field
from z3c.form.browser import checkbox
from z3c.pagelet.browser import BrowserPagelet

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory, fieldsForInterface
from org.ict_ok.components.service.interfaces import \
    IService, IAddService, IServiceFolder
from org.ict_ok.components.service.service import Service, getAllServices
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.skin.menu import GlobalMenuSubItem, GlobalMenuAddItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditForm
from org.ict_ok.components.superclass.browser.superclass import \
     Overview
from org.ict_ok.components.browser.component import AddComponentForm
from org.ict_ok.components.browser.component import ImportCsvDataComponentForm
from org.ict_ok.components.browser.component import ImportXlsDataComponentForm

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddService(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Service')
    viewURL = 'add_service.html'
    weight = 50


class MGlobalAddService(GlobalMenuAddItem):
    """ Menu Item """
    title = _(u'Add Service')
    viewURL = 'add_service.html'
    weight = 50
    folderInterface = IServiceFolder


# --------------- object details ---------------------------


class ServiceDetails(ComponentDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []


class ServiceFolderDetails(ComponentDetails):
    """ Class for MobilePhone details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + ['requirement']
    omit_addfields = ComponentDetails.omit_addfields + ['requirement']
    omit_editfields = ComponentDetails.omit_editfields + ['requirement']
    attrInterface = IService
    factory = Service
    fields = fieldsForFactory(factory, omit_editfields)


class AddServiceClass(BrowserPagelet):
    def update(self):
        pass

# --------------- forms ------------------------------------


class DetailsServiceForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of service')
    factory = Service
    attrInterface = IService
    omitFields = ServiceDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


#class AddServiceForm(AddForm):
#    """Add form."""
#    label = _(u'Add Service')
#    fields = field.Fields(IService).omit(*ServiceDetails.omit_addfields)
#    factory = Service
    

class AddServiceForm(AddComponentForm):
    label = _(u'Add Service')
    factory = Service
    omitFields = ServiceDetails.omit_addfields
    attrInterface = IService
    addInterface = IAddService
    _session_key = 'org.ict_ok.components.service'
    allFields = fieldsForFactory(factory, omitFields, [])
    addFields = fieldsForInterface(addInterface, [])
    allFields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget


class EditServiceForm(EditForm):
    """ Edit for for net """
    label = _(u'Service Edit Form')
    factory = Service
    omitFields = ServiceDetails.omit_addfields
    fields = fieldsForFactory(factory, omitFields)
    fields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget


class DeleteServiceForm(DeleteForm):
    """ Delete the net """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this service: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class AllServices(Overview):
    """Overview Pagelet"""
    def objs(self):
        """List of Content objects"""
        return getAllServices()


class ImportCsvDataForm(ImportCsvDataComponentForm):
    pass


class ImportXlsDataForm(ImportXlsDataComponentForm):
    attrInterface = IService
    factory = Service
    factoryId = u'org.ict_ok.components.service.service.Service'
    allFields = fieldsForInterface(attrInterface, [])
