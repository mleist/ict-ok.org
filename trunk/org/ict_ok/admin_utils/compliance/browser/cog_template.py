# -*- coding: utf-8 -*-
#
# Copyright (c) 2007, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: cog_template.py_cog 88 2007-10-16 13:36:24Z markusleist $
#
# pylint: disable-msg=E1101,E0611,W0232,W0142
"""Interface of compliance utility

the compliance utility should store the compliance/requirement-templates
for the host- or service-instances
"""
"""implementation of browser class of eventCrossbar handler
"""

__version__ = "$Id: cog_template.py_cog 88 2007-10-16 13:36:24Z markusleist $"

# phython imports

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
from org.ict_ok.admin_utils.compliance.interfaces import \
     IAdmUtilCompliance
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DisplayForm, EditForm
from org.ict_ok.skin.menu import GlobalMenuSubItem

_ = MessageFactory('org.ict_ok')

# --------------- menu entries -----------------------------


class AdmUtilComplianceDetails(SupernodeDetails):
    """Compliance Utiltiy
    """
    
    omit_viewfields = SupernodeDetails.omit_viewfields + ['ikName']
    omit_editfields = SupernodeDetails.omit_editfields + ['ikName']



# --------------- forms ------------------------------------


class DetailsAdmUtilComplianceForm(DisplayForm):
    """ Display form for the object """
    
    label = _(u'settings of Compliance')
    fields = field.Fields(IAdmUtilCompliance).omit(
       *AdmUtilComplianceDetails.omit_viewfields)


class EditAdmUtilComplianceForm(EditForm):
    """ Display form for the object """
    
    label = _(u'edit Compliance properties')
    fields = field.Fields(IAdmUtilCompliance).omit(
       *AdmUtilComplianceDetails.omit_editfields)
