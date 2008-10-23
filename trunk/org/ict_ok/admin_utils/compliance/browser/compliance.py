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
from org.ict_ok.admin_utils.compliance.interfaces import \
     IAdmUtilCompliance
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DisplayForm, EditForm
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.admin_utils.compliance.interfaces import IRequirement

_ = MessageFactory('org.ict_ok')

# --------------- menu entries -----------------------------


# --------------- details -----------------------------

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

    def update(self):
        DisplayForm.update(self)

def getTitel(item, formatter):
    """
    Titel for Overview
    """
    try:
        return item.ikName
    except TypeError:
        return str(item.__class__.__name__)

from org.ict_ok.components.superclass.browser.superclass import \
     Overview, getModifiedDate, raw_cell_formatter, \
     link, getActionBottons, getSize
class AdmUtilRequirementDisplayAll(Overview):
    """for all Requirements
    """
    label = _(u'display all requirements')
    columns = (
        GetterColumn(title=_('Title'),
                     getter=getTitel,
                     cell_formatter=link('overview.html')),
        GetterColumn(title=_('Modified On'),
                     getter=getModifiedDate,
                     subsort=True,
                     cell_formatter=raw_cell_formatter),
        GetterColumn(title=_('Size'),
                     getter=getSize,
                     cell_formatter=raw_cell_formatter),
        GetterColumn(title=_('Actions'),
                     getter=getActionBottons,
                     cell_formatter=raw_cell_formatter),
        )
    sort_columns = [1]
    status = None
    
    def objs(self):
        """List of Content objects"""
        #import pdb
        #pdb.set_trace()
        return [obj
                for obj in self.context.values()
                if IRequirement.providedBy(obj)]
        #retList = []
        #for myObj in self.context:
            
        #return retList


class EditAdmUtilComplianceForm(EditForm):
    """ Display form for the object """
    
    label = _(u'edit Compliance properties')
    fields = field.Fields(IAdmUtilCompliance).omit(
       *AdmUtilComplianceDetails.omit_editfields)
