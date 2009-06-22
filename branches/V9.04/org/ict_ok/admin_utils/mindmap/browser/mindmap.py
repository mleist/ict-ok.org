# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
#               Sebastian Napiorkowski <s.napiorkowski@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: cog_template.py_cog 273 2008-08-26 13:23:57Z markusleist $
#
# pylint: disable-msg=E1101,E0611,W0232,W0142
"""Interface of mind map util

the mind map util will display some information from ict-ok in form of a mind map
"""
"""implementation of browser class of eventCrossbar handler
"""

__version__ = "$Id: cog_template.py_cog 273 2008-08-26 13:23:57Z markusleist $"

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
from org.ict_ok.admin_utils.mindmap.interfaces import \
     IAdmUtilMindMap
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DisplayForm, EditForm
from org.ict_ok.skin.menu import GlobalMenuSubItem

_ = MessageFactory('org.ict_ok')

# --------------- menu entries -----------------------------


class AdmUtilMindMapDetails(SupernodeDetails):
    """MindMap Utiltiy
    """
    
    omit_viewfields = SupernodeDetails.omit_viewfields + ['ikName']
    omit_editfields = SupernodeDetails.omit_editfields + ['ikName']



# --------------- forms ------------------------------------


class DetailsAdmUtilMindMapForm(DisplayForm):
    """ Display form for the object """
    
    label = _(u'settings of MindMap')
    fields = field.Fields(IAdmUtilMindMap).omit(
       *AdmUtilMindMapDetails.omit_viewfields)


class EditAdmUtilMindMapForm(EditForm):
    """ Display form for the object """
    
    label = _(u'edit MindMap properties')
    fields = field.Fields(IAdmUtilMindMap).omit(
       *AdmUtilMindMapDetails.omit_editfields)
