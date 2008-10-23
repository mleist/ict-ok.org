# -*- coding: utf-8 -*-
#
# Copyright (c) 2007, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0232,W0142
"""Interface of compliance utility

the compliance utility should store the compliance/requirement-templates
for the host- or service-instances
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
from org.ict_ok.admin_utils.compliance.interfaces import IRequirement
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DisplayForm, EditForm
from org.ict_ok.skin.menu import GlobalMenuSubItem

_ = MessageFactory('org.ict_ok')

# --------------- menu entries -----------------------------

class MSubDisplayRequirements(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Requirements')
    viewURL = 'display_reqs.html'
    weight = 80

class MSubAllRequirements(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'All Requirements')
    viewURL = 'allreqs.html'
    weight = 80

# --------------- details -----------------------------

class AdmUtilRequirementDetails(SupernodeDetails):
    """Requirement Utiltiy
    """
    
    omit_viewfields = SupernodeDetails.omit_viewfields + ['ikName']
    omit_editfields = SupernodeDetails.omit_editfields + ['ikName']


# --------------- forms ------------------------------------


class DetailsAdmUtilRequirementForm(DisplayForm):
    """ Display form for the object """
    
    label = _(u'settings of Requirement')
    fields = field.Fields(IRequirement).omit(
       *AdmUtilRequirementDetails.omit_viewfields)
    
    def update(self):
        DisplayForm.update(self)
    
class AdmUtilRequirementDisplayAll(DisplayForm):
    """for all Requirements
    """
    label = _(u'display all requirements')



class EditAdmUtilRequirementForm(EditForm):
    """ Display form for the object """
    
    label = _(u'edit Requirement properties')
    fields = field.Fields(IRequirement).omit(
       *AdmUtilRequirementDetails.omit_editfields)
