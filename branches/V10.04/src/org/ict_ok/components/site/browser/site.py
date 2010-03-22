# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0232,W0613,W0611,W0142,R0901
#
"""implementation of browser class of Site object
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# ict_ok imports
from org.ict_ok.libs.lib import fieldsForFactory
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditContent, EditForm
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.components.site.site import Site
from org.ict_ok.skin.menu import GlobalMenuSubItem

_ = MessageFactory('org.ict_ok')


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
    omit_viewfields = ComponentDetails.omit_viewfields + ['xlsdata', 'codepage']
    omit_addfields = ComponentDetails.omit_addfields + ['xlsdata', 'codepage']
    omit_editfields = ComponentDetails.omit_editfields + ['xlsdata', 'codepage']

# --------------- forms ------------------------------------


class DetailsSiteForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of site')
    factory = Site
    omitFields = SiteDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class AddSiteForm(AddForm):
    """Add form."""
    label = _(u'add site')
    factory = Site
    omitFields = SiteDetails.omit_addfields
    _session_key = 'org.ict_ok.components.site'
    fields = fieldsForFactory(factory, omitFields)


class EditSiteForm(EditForm):
    """ Edit for for site """
    label = _(u'edit site settings')
    factory = Site
    omitFields = SiteDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)


class DeleteSiteForm(DeleteForm):
    """ Delete the net """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this site: '%s'?") % \
               IBrwsOverview(self.context).getTitle()

class EditSiteEventIfForm(EditForm):
    """ Event edit for site """
    label = _(u'Site Event Interfaces Form')
    #fields = field.Fields(IEventIfEventSite)
