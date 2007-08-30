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
"""implementation of browser class of eventCrossbar handler
"""

__version__ = "$Id$"

# phython imports

# zope imports
from zope.i18nmessageid import MessageFactory
from zope.dublincore.interfaces import IZopeDublinCore

# z3c imports
from z3c.form import field

# ict_ok.org imports
from org.ict_ok.admin_utils.eventcrossbar.interfaces import \
     IAdmUtilEvent, IAdmUtilEventCrossbar
from org.ict_ok.admin_utils.eventcrossbar.event import \
     AdmUtilEvent
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DisplayForm, EditForm
from org.ict_ok.skin.menu import GlobalMenuSubItem

_ = MessageFactory('org.ict_ok')

# --------------- menu entries -----------------------------

class MSubAddEvent(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Event')
    viewURL = 'add_event.html'
    weight = 50


class AdmUtilEventDetails(SupernodeDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = SupernodeDetails.omit_viewfields + []
    omit_editfields = SupernodeDetails.omit_editfields + []


class AdmUtilEventCrossbarDetails(SupernodeDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = SupernodeDetails.omit_viewfields + ['ikName']
    omit_editfields = SupernodeDetails.omit_editfields + ['ikName']

    def getInstanceCounter(self):
        """convert instance counter for display
        """
        return self.context.getInstanceCounter()

    def getEventCrossbarTime(self):
        """convert eventcrossbar timestamp for display
        """
        from zope.proxy import removeAllProxies
        from zope.traversing.browser import absoluteurl
        obj = removeAllProxies(self.context)
        print "#########->", absoluteurl.absoluteURL(obj, self.request)
        return self.context.getEventCrossbarTime()


# --------------- forms ------------------------------------


class DetailsAdmUtilEventCrossbarForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Event')
    fields = field.Fields(IAdmUtilEventCrossbar).omit(\
        *AdmUtilEventCrossbarDetails.omit_viewfields) + \
           field.Fields(IZopeDublinCore).select('modified')


class EditAdmUtilEventCrossbarForm(EditForm):
    """ Edit form for the object """
    label = _(u'edit crossbar properties')
    fields = field.Fields(IAdmUtilEventCrossbar).omit(\
        *AdmUtilEventCrossbarDetails.omit_editfields)


class DetailsAdmUtilEventForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Event')
    fields = field.Fields(IAdmUtilEvent).omit(\
        *AdmUtilEventDetails.omit_viewfields) + \
           field.Fields(IZopeDublinCore).select('modified')


class AddAdmUtilEventForm(AddForm):
    """Add form."""
    label = _(u'add event')
    fields = field.Fields(IAdmUtilEvent).omit(*AdmUtilEventDetails.omit_addfields)
    factory = AdmUtilEvent


class EditAdmUtilEventForm(EditForm):
    """ Edit form for the object """
    label = _(u'edit event properties')
    fields = field.Fields(IAdmUtilEvent).omit(\
        *AdmUtilEventDetails.omit_editfields)
