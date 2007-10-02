# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
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

# phython imports
import time
import rrdtool

# zope imports
from zope.app import zapi
from zope.proxy import removeAllProxies
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field

# ict_ok.org imports
from org.ict_ok.components.building.interfaces import IBuilding
from org.ict_ok.components.building.building import Building
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditForm

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddBuilding(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Building')
    viewURL = 'add_building.html'
    weight = 50


# --------------- object details ---------------------------


class BuildingDetails(ComponentDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []

# --------------- forms ------------------------------------


class DetailsBuildingForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of building')
    fields = field.Fields(IBuilding).omit(*BuildingDetails.omit_viewfields)


class AddBuildingForm(AddForm):
    """Add form."""
    label = _(u'Add Building')
    fields = field.Fields(IBuilding).omit(*BuildingDetails.omit_addfields)
    factory = Building


class EditBuildingForm(EditForm):
    """ Edit for for net """
    label = _(u'Building Edit Form')
    fields = field.Fields(IBuilding).omit(*BuildingDetails.omit_editfields)


class DeleteBuildingForm(DeleteForm):
    """ Delete the net """
    
    def getTitel(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this building: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


