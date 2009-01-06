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

# ict_ok.org imports
from org.ict_ok.components.location.interfaces import ILocation
from org.ict_ok.components.location.location import Location
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditForm

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

# --------------- forms ------------------------------------


class DetailsLocationForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of location')
    fields = field.Fields(ILocation).omit(*LocationDetails.omit_viewfields)


class AddLocationForm(AddForm):
    """Add form."""
    label = _(u'Add Location')
    fields = field.Fields(ILocation).omit(*LocationDetails.omit_addfields)
    factory = Location


class EditLocationForm(EditForm):
    """ Edit for for net """
    label = _(u'Location Edit Form')
    fields = field.Fields(ILocation).omit(*LocationDetails.omit_editfields)


class DeleteLocationForm(DeleteForm):
    """ Delete the net """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this location: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


