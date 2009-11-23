# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
#               Sebastian Napiorkowski <s.napiorkowski@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0232,W0142
"""Interface of mac address db util

the mac address db util will display some information from ict-ok in form of a mac address db
"""
"""implementation of browser class of eventCrossbar handler
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory
from zope.dublincore.interfaces import IZopeDublinCore

# zc imports
from zc.table.column import GetterColumn
from zc.table.table import StandaloneFullFormatter

# z3c imports
from z3c.form import field
from z3c.pagelet.browser import BrowserPagelet

# ict_ok.org imports
from org.ict_ok.admin_utils.mac_address_db.interfaces import \
     IAdmUtilMacAddressDb
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DisplayForm, EditForm
from org.ict_ok.skin.menu import GlobalMenuSubItem

_ = MessageFactory('org.ict_ok')

# --------------- menu entries -----------------------------


class AdmUtilMacAddressDbDetails(SupernodeDetails):
    """MacAddressDb Utiltiy
    """
    
    omit_viewfields = SupernodeDetails.omit_viewfields + ['ikName']
    omit_editfields = SupernodeDetails.omit_editfields + ['ikName']



# --------------- forms ------------------------------------


class DetailsAdmUtilMacAddressDbForm(DisplayForm):
    """ Display form for the object """
    
    label = _(u'settings of MacAddressDb')
    fields = field.Fields(IAdmUtilMacAddressDb).omit(
       *AdmUtilMacAddressDbDetails.omit_viewfields)


class EditAdmUtilMacAddressDbForm(EditForm):
    """ Display form for the object """
    
    label = _(u'edit MacAddressDb properties')
    fields = field.Fields(IAdmUtilMacAddressDb).omit(
       *AdmUtilMacAddressDbDetails.omit_editfields)
