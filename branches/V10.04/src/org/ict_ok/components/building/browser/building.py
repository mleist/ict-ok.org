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
"""implementation of browser class of Building object
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
from org.ict_ok.libs.lib import fieldsForFactory, fieldsForInterface
from org.ict_ok.components.building.interfaces import \
    IBuilding, IAddBuilding, IBuildingFolder
from org.ict_ok.components.building.building import Building
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.skin.menu import GlobalMenuSubItem, GlobalMenuAddItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditForm
from org.ict_ok.components.browser.component import AddComponentForm
from org.ict_ok.components.browser.component import ImportXlsDataComponentForm

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddBuilding(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Building')
    viewURL = 'add_building.html'
    weight = 50


class MGlobalAddBuilding(GlobalMenuAddItem):
    """ Menu Item """
    title = _(u'Add Building')
    viewURL = 'add_building.html'
    weight = 50
    folderInterface = IBuildingFolder


# --------------- object details ---------------------------


class BuildingDetails(ComponentDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []


class BuildingFolderDetails(ComponentDetails):
    """ Class for MobilePhone details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + ['requirement']
    omit_addfields = ComponentDetails.omit_addfields + ['requirement']
    omit_editfields = ComponentDetails.omit_editfields + ['requirement']
    fields = field.Fields(IBuilding).omit(*BuildingDetails.omit_viewfields)
    attrInterface = IBuilding
    factory = Building
    fields = fieldsForFactory(factory, omit_editfields)

# --------------- forms ------------------------------------


class DetailsBuildingForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of building')
    factory = Building
    omitFields = BuildingDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


#class AddBuildingForm(AddForm):
#    """Add form."""
#    label = _(u'Add Building')
#    fields = field.Fields(IBuilding).omit(*BuildingDetails.omit_addfields)
#    factory = Building
    
    
class AddBuildingForm(AddComponentForm):
    label = _(u'Add Building')
    factory = Building
    attrInterface = IBuilding
    addInterface = IAddBuilding
    omitFields = BuildingDetails.omit_addfields
    _session_key = 'org.ict_ok.components.building'
    allFields = fieldsForFactory(factory, omitFields)
    addFields = fieldsForInterface(addInterface, [])
    allFields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget


class EditBuildingForm(EditForm):
    """ Edit for for net """
    label = _(u'Building Edit Form')
    factory = Building
    omitFields = BuildingDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)
    fields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget


class DeleteBuildingForm(DeleteForm):
    """ Delete the net """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this building: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportXlsDataForm(ImportXlsDataComponentForm):
    attrInterface = IBuilding
    factory = Building
    factoryId = u'org.ict_ok.components.building.building.Building'
    allFields = fieldsForInterface(attrInterface, [])
