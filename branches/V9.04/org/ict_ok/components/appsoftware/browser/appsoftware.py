# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: template.py_cog 396 2009-01-08 00:21:51Z markusleist $
#
# pylint: disable-msg=W0232,W0142
#
"""implementation of browser class of ApplicationSoftware"""

__version__ = "$Id: template.py_cog 396 2009-01-08 00:21:51Z markusleist $"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field
from z3c.form.browser import checkbox

# ict_ok.org imports
from org.ict_ok.components.appsoftware.interfaces import IApplicationSoftware, IAddApplicationSoftware
from org.ict_ok.components.appsoftware.appsoftware import ApplicationSoftware
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditForm
from org.ict_ok.components.browser.component import AddComponentForm
from org.ict_ok.components.browser.component import ImportCsvDataComponentForm
from org.ict_ok.components.browser.component import ImportXlsDataComponentForm

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddApplicationSoftware(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Application Software')
    viewURL = 'add_appsoftware.html'

    weight = 50

# --------------- object details ---------------------------


class ApplicationSoftwareDetails(ComponentDetails):
    """ Class for ApplicationSoftware details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []


class ApplicationSoftwareFolderDetails(ComponentDetails):
    """ Class for MobilePhone details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + ['requirement']
    omit_addfields = ComponentDetails.omit_addfields + ['requirement']
    omit_editfields = ComponentDetails.omit_editfields + ['requirement']
    fields = field.Fields(IApplicationSoftware).omit(*ApplicationSoftwareDetails.omit_viewfields)
    attrInterface = IApplicationSoftware

# --------------- forms ------------------------------------


class DetailsApplicationSoftwareForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Application Software Instance')
    fields = field.Fields(IApplicationSoftware).omit(*ApplicationSoftwareDetails.omit_viewfields)


class AddApplicationSoftwareForm(AddComponentForm):
    """Add Application Software Instance form"""
    label = _(u'Add Application Software Instance')
    addFields = field.Fields(IAddApplicationSoftware)
    allFields = field.Fields(IApplicationSoftware).omit(*ApplicationSoftwareDetails.omit_addfields)
    allFields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget
    factory = ApplicationSoftware
    attrInterface = IApplicationSoftware
    _session_key = 'org.ict_ok.components.asoftware'


class EditApplicationSoftwareForm(EditForm):
    """ Edit for Application Software Instance """
    label = _(u'Application Software Instance Edit Form')
    fields = field.Fields(IApplicationSoftware).omit(*ApplicationSoftwareDetails.omit_editfields)


class DeleteApplicationSoftwareForm(DeleteForm):
    """ Delete the Application Software Instance """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this ApplicationSoftware: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportCsvDataForm(ImportCsvDataComponentForm):
    pass


class ImportXlsDataForm(ImportXlsDataComponentForm):
    allFields = field.Fields(IApplicationSoftware)
#    allFields['isTemplate'].widgetFactory = \
#        checkbox.SingleCheckBoxFieldWidget
    attrInterface = IApplicationSoftware
    factory = ApplicationSoftware
    factoryId = u'org.ict_ok.components.appsoftware.appsoftware.ApplicationSoftware'
