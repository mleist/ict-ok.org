# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Thomas Richter <thomas.richter at xwml.de>,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0232,W0142
#
"""implementation of browser class of usermanagement handler
"""

__version__ = "$Id$"

# phython imports

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field

# ict_ok.org imports
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditContent, EditForm
from org.ict_ok.admin_utils.public_viewing.interfaces import \
     IAdmUtilPublicViewing

_ = MessageFactory('org.ict_ok')

# --------------- menu entries -----------------------------

# --------------- object details ---------------------------


class AdmUtilPublicViewingDetails(SupernodeDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = SupernodeDetails.omit_viewfields + []
    omit_editfields = SupernodeDetails.omit_editfields + []

# --------------- forms ------------------------------------


class ViewAdmUtilPublicViewingForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of public viewing')
    fields = field.Fields(IAdmUtilPublicViewing).omit(\
        *AdmUtilPublicViewingDetails.omit_viewfields)


class EditAdmUtilPublicViewingForm(EditForm):
    """ Edit for for net """
    label = _(u'edit public viewing')
    fields = field.Fields(IAdmUtilPublicViewing).omit(\
        *AdmUtilPublicViewingDetails.omit_editfields)
