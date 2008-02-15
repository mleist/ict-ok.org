# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0232,W0613,W0142,R0901
#
"""implementation of browser class of Site object
"""

__version__ = "$Id$"

# phython imports

# zope imports
from pytz import timezone
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field

# zc imports

# ict_ok imports
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditContent, EditForm
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.components.site.interfaces import ISite
from org.ict_ok.components.site.site import Site
from org.ict_ok.skin.menu import GlobalMenuSubItem

_ = MessageFactory('org.ict_ok')
berlinTZ = timezone('Europe/Berlin')


# --------------- menu entries -----------------------------


class MSubAddSite(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Site')
    viewURL = 'add_site.html'
    weight = 50


# --------------- object details ---------------------------


class SiteDetails(ComponentDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []


# --------------- forms ------------------------------------


class DetailsSiteForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of site')
    fields = field.Fields(ISite).omit(*SiteDetails.omit_viewfields)

class AddSiteForm(AddForm):
    """Add form."""
    label = _(u'add site')
    fields = field.Fields(ISite).omit(*SiteDetails.omit_addfields)
    factory = Site

class EditSiteForm(EditForm):
    """ Edit for for site """
    label = _(u'edit site settings')
    fields = field.Fields(ISite).omit(*SiteDetails.omit_editfields)


class DeleteSiteForm(DeleteForm):
    """ Delete the net """
    
    def getTitel(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this site: '%s'?") % \
               IBrwsOverview(self.context).getTitle()
