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
"""implementation of browser class of eventCrossbar handler
"""

__version__ = "$Id$"

# phython imports

# zope imports
from zope.i18nmessageid import MessageFactory

# zc imports

# z3c imports
from z3c.form import field

# ict_ok.org imports
from org.ict_ok.admin_utils.eventcrossbar.interfaces import \
     IEventTimingRelay, IEventIfEventTimingRelay
from org.ict_ok.admin_utils.eventcrossbar.event_timingrelay import \
     EventTimingRelay
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DisplayForm, EditForm
from org.ict_ok.skin.menu import GlobalMenuSubItem

_ = MessageFactory('org.ict_ok')

# --------------- menu entries -----------------------------

class MSubAddEventTimingRelay(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Timing Relay')
    viewURL = 'add_event_timingrelay.html'
    weight = 50


class EventTimingRelayDetails(SupernodeDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = SupernodeDetails.omit_viewfields + []
    omit_addfields = SupernodeDetails.omit_addfields + []
    omit_editfields = SupernodeDetails.omit_editfields + []

# --------------- forms ------------------------------------


class DetailsEventTimingRelayForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Event')
    fields = field.Fields(IEventTimingRelay).omit(\
        *EventTimingRelayDetails.omit_viewfields) #+ \
           #field.Fields(IZopeDublinCore).select('modified')
    #def update(self):
        #self.context.removeInvalidOidFromInpOutObjects()
        #DisplayForm.update(self)


class AddEventTimingRelayForm(AddForm):
    """Add form."""
    label = _(u'add timing relay')
    fields = field.Fields(IEventTimingRelay,
                          omitReadOnly = True).omit(\
        *EventTimingRelayDetails.omit_addfields)
    factory = EventTimingRelay


class EditEventTimingRelayForm(EditForm):
    """ Edit form for the object """
    label = _(u'edit timing relay properties')
    fields = field.Fields(IEventTimingRelay,
                          omitReadOnly = True).omit(\
        *EventTimingRelayDetails.omit_editfields)
    #def update(self):
        #self.context.removeInvalidOidFromInpOutObjects()
        #EditForm.update(self)
        
class EditEventTimingRelayEventIfForm(EditForm):
    """ Edit Event Interface of object """
    label = _(u'timing relay event interfaces form')
    fields = field.Fields(IEventIfEventTimingRelay)
