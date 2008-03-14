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
"""implementation of browser class of Interface object
"""

__version__ = "$Id$"

# phython imports

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field

# ict_ok.org imports
from org.ict_ok.components.interface.interfaces import IInterface
from org.ict_ok.components.interface.interface import Interface
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditForm

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddInterface(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Interface')
    viewURL = 'add_interface.html'
    weight = 50


# --------------- object details ---------------------------


class InterfaceDetails(ComponentDetails):
    """ Class for Web-Browser-Details
    """
    #omit_viewfields = ComponentDetails.omit_viewfields + ['ipv4List']
    #omit_addfields = ComponentDetails.omit_addfields + ['ipv4List']
    #omit_editfields = ComponentDetails.omit_editfields + ['ipv4List']
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []

# --------------- forms ------------------------------------


class DetailsInterfaceForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of interface')
    fields = field.Fields(IInterface).omit(*InterfaceDetails.omit_viewfields)


class AddInterfaceForm(AddForm):
    """Add form."""
    label = _(u'Add Interface')
    fields = field.Fields(IInterface).omit(*InterfaceDetails.omit_addfields)
    factory = Interface


class EditInterfaceForm(EditForm):
    """ Edit for for net """
    label = _(u'Interface Edit Form')
    fields = field.Fields(IInterface).omit(*InterfaceDetails.omit_editfields)


class DeleteInterfaceForm(DeleteForm):
    """ Delete the net """
    
    def getTitel(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this net: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


