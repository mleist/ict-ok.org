# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: template.py_cog 396 2009-01-08 00:21:51Z markusleist $
#
# pylint: disable-msg=W0232,W0142
#
"""implementation of browser class of MobilePhone"""

__version__ = "$Id: template.py_cog 396 2009-01-08 00:21:51Z markusleist $"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field

# ict_ok.org imports
from org.ict_ok.components.mobilephone.interfaces import IMobilePhone
from org.ict_ok.components.mobilephone.mobilephone import MobilePhone
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditForm

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddMobilePhone(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Mobile phone')
    viewURL = 'add_mobilephone.html'

    weight = 50

# --------------- object details ---------------------------


class MobilePhoneDetails(ComponentDetails):
    """ Class for MobilePhone details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + ['requirement']
    omit_addfields = ComponentDetails.omit_addfields + ['requirement']
    omit_editfields = ComponentDetails.omit_editfields + ['requirement']

# --------------- forms ------------------------------------


class DetailsMobilePhoneForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Mobile phone')
    fields = field.Fields(IMobilePhone).omit(*MobilePhoneDetails.omit_viewfields)


class AddMobilePhoneForm(AddForm):
    """Add Mobile phone form"""
    label = _(u'Add Mobile phone')
    fields = field.Fields(IMobilePhone).omit(*MobilePhoneDetails.omit_addfields)
 
    factory = MobilePhone


class EditMobilePhoneForm(EditForm):
    """ Edit for Mobile phone """
    label = _(u'Mobile phone Edit Form')
    fields = field.Fields(IMobilePhone).omit(*MobilePhoneDetails.omit_editfields)


class DeleteMobilePhoneForm(DeleteForm):
    """ Delete the Mobile phone """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this MobilePhone: '%s'?") % \
               IBrwsOverview(self.context).getTitle()

