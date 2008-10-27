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
"""implementation of browser class of Script object
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field

# ict_ok.org imports
from org.ict_ok.components.script.interfaces import IScript
from org.ict_ok.components.script.script import Script
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditForm

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddScript(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Script')
    viewURL = 'add_script.html'
    weight = 50


# --------------- object details ---------------------------


class ScriptDetails(ComponentDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + ['printHistory']
    omit_addfields = ComponentDetails.omit_addfields + ['printHistory']
    omit_editfields = ComponentDetails.omit_editfields + ['printHistory']

# --------------- forms ------------------------------------


#class DetailsScriptForm(DisplayForm):
    #""" Display form for the object """
    #label = _(u'settings of script')
    #fields = field.Fields(IScript).omit(*ScriptDetails.omit_viewfields)


class AddScriptForm(AddForm):
    """Add form."""
    label = _(u'Add Script')
    fields = field.Fields(IScript).omit(*ScriptDetails.omit_addfields)
    factory = Script


class EditScriptForm(EditForm):
    """ Edit for for net """
    label = _(u'Script Edit Form')
    fields = field.Fields(IScript).omit(*ScriptDetails.omit_editfields)


class DeleteScriptForm(DeleteForm):
    """ Delete the net """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this script: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


