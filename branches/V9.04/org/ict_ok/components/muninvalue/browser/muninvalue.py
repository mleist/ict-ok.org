# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=F0401,E1101,E0611,W0612,W0232,W0201,W0142
#
"""implementation of browser class of Latency object
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory, fieldsForInterface
from org.ict_ok.components.latency.interfaces import ILatency, IAddLatency
from org.ict_ok.components.latency.latency import Latency
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditForm
from org.ict_ok.components.browser.component import AddComponentForm

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------

class MSubAddLatency(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add latency check')
    viewURL = 'add_latency.html'
    weight = 50

class MSubDisplayLatency(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Display latency check')
    viewURL = 'display.html'
    weight = 9

# --------------- object details ---------------------------


class LatencyDetails(ComponentDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []


class LatencyDisplay(LatencyDetails):
    """
    """
    pass

# --------------- forms ------------------------------------


class DetailsLatencyForm(DisplayForm):
    """ Display form for the object """
    label = _(u'Details of Snmp value')
    factory = Latency
    omitFields = LatencyDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)
    
    def update(self):
        DisplayForm.update(self)


class AddLatencyForm(AddComponentForm):
    """Add form."""
    label = _(u'Add Latency')
    factory = Latency
    attrInterface = ILatency
    addInterface = IAddLatency
    omitFields = LatencyDetails.omit_addfields
    allFields = fieldsForFactory(factory, omitFields)
    addFields = fieldsForInterface(addInterface, [])
    _session_key = 'org.ict_ok.components.muninvalue'


class EditLatencyForm(EditForm):
    """ Edit for for net """
    label = _(u'Latency Edit Form')
    factory = Latency
    omitFields = LatencyDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)


class DeleteLatencyForm(DeleteForm):
    """ Delete the net """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this net: '%s'?") % \
               IBrwsOverview(self.context).getTitle()
