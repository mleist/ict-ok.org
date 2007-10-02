# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
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

# phython imports

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field

# ict_ok.org imports
from org.ict_ok.components.service.interfaces import IService
from org.ict_ok.components.service.service import Service
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditForm

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddService(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Service')
    viewURL = 'add_service.html'
    weight = 50


# --------------- object details ---------------------------


class ServiceDetails(ComponentDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []

# --------------- forms ------------------------------------


class DetailsServiceForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of net')
    fields = field.Fields(IService).omit(*ServiceDetails.omit_viewfields)


class AddServiceForm(AddForm):
    """Add form."""
    label = _(u'Add Service')
    fields = field.Fields(IService).omit(*ServiceDetails.omit_addfields)
    factory = Service


class EditServiceForm(EditForm):
    """ Edit for for net """
    label = _(u'Hello Service Edit Form')
    fields = field.Fields(IService).omit(*ServiceDetails.omit_editfields)


class DeleteServiceForm(DeleteForm):
    """ Delete the net """
    
    def getTitel(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this net: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


