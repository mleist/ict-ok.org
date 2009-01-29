# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0232,W0142
#
"""implementation of browser class of Location object
"""

__version__ = "$Id$"

# python imports
import time
import rrdtool

# zope imports
from zope.app import zapi
from zope.proxy import removeAllProxies
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field
from z3c.form.browser import checkbox

# ict_ok.org imports
from org.ict_ok.components.location.interfaces import ILocation, IAddLocation
from org.ict_ok.components.location.location import Location
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


class MSubAddLocation(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Location')
    viewURL = 'add_location.html'
    weight = 50


# --------------- object details ---------------------------


class LocationDetails(ComponentDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []
    

class LocationFolderDetails(ComponentDetails):
    """ Class for MobilePhone details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + ['requirement']
    omit_addfields = ComponentDetails.omit_addfields + ['requirement']
    omit_editfields = ComponentDetails.omit_editfields + ['requirement']
    fields = field.Fields(ILocation).omit(*LocationDetails.omit_viewfields)
    attrInterface = ILocation

# --------------- forms ------------------------------------


class DetailsLocationForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of location')
    fields = field.Fields(ILocation).omit(*LocationDetails.omit_viewfields)


#class AddLocationForm(AddForm):
#    """Add form."""
#    label = _(u'Add Location')
#    fields = field.Fields(ILocation).omit(*LocationDetails.omit_addfields)
#    factory = Location
    
    
class AddLocationForm(AddComponentForm):
    label = _(u'Add Location')
    addFields = field.Fields(IAddLocation)
    allFields = field.Fields(ILocation).omit(*LocationDetails.omit_addfields)
    allFields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget
    factory = Location
    attrInterface = ILocation
    _session_key = 'org.ict_ok.components.location'


class EditLocationForm(EditForm):
    """ Edit for for net """
    label = _(u'Location Edit Form')
    fields = field.Fields(ILocation).omit(*LocationDetails.omit_editfields)
    fields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget


class DeleteLocationForm(DeleteForm):
    """ Delete the net """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this location: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportCsvDataForm(ImportCsvDataComponentForm):
    pass


class ImportXlsDataForm(ImportXlsDataComponentForm):
    allFields = field.Fields(ILocation)
    attrInterface = ILocation
    factoryId = u'org.ict_ok.components.location.location.Location'

