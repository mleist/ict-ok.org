# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,C0111
#
"""
python package
"""
__version__ = "$Id$"

# python imports

# zope imports
from org.ict_ok.skin.interfaces import IMasterMenu
from zope.i18nmessageid import MessageFactory
from zope.viewlet import manager
from zope.app.component import hooks
from zope.component import getUtility
from zope.traversing.browser import absoluteURL
from zope.app.pagetemplate import viewpagetemplatefile
from zope.i18n import translate

# z3c imports
from z3c.menu.simple.menu import TabMenu
from z3c.menu.simple import menu
from z3c.menu.simple import ITab
from z3c.menu.simple.menu import Tab

# ict_ok.org imports
from org.ict_ok.components.superclass.superclass import objectsWithInterface
from org.ict_ok.admin_utils.util_manager.interfaces import IUtilManager

_ = MessageFactory('org.ict_ok')

def getSortableTitel((name, viewlet)):
    try:
        return translate(viewlet.title, domain='org.ict_ok', context=viewlet.request).upper()
    except AttributeError:
        return 0


class GlobalMenuItem(menu.TabItem):
    """Menu item viewlet generating global/site related links."""

    selectedView = None
    viewURL = u''

    @property
    def selected(self):
        if (self.selectedView is not None and
            self.selectedView.providedBy(self.__parent__)):
            return True
        return False

    @property
    def url(self):
        siteURL = absoluteURL(hooks.getSite(), self.request)
        return siteURL + '/' + self.viewURL

    @property
    def posInManager(self):
        return self.manager.viewlets.index(self)

class ContextMenuItem(menu.TabItem):
    """Menu item viewlet generating global/site related links."""

    selectedView = None
    viewURL = u''

    @property
    def selected(self):
        if (self.selectedView is not None and
            self.selectedView.providedBy(self.__parent__)):
            return True
        return False

    @property
    def url(self):
        contextURL = absoluteURL(self.context, self.request)
        return contextURL + '/' + self.viewURL
    
    @property
    def posInManager(self):
        return self.manager.viewlets.index(self)

class GlobalMenuMainItem(GlobalMenuItem):
    """Menu item viewlet generating global/site related links."""
    template = viewpagetemplatefile.ViewPageTemplateFile('menu_main_item.pt')
    @property
    def menu_class(self):
        if self.posInManager > 0:
            if self.selected:
                return u"navmainother selected"
            else:
                return u"navmainother"
        else:
            if self.selected:
                return u"navmainstart selected"
            else:
                return u"navmainstart"

class GlobalMenuSubItem(ContextMenuItem):
    """Menu item viewlet generating global/site related links."""
    template = viewpagetemplatefile.ViewPageTemplateFile('menu_sub_item.pt')
    @property
    def menu_class(self):
        if self.posInManager > 0:
            if self.selected:
                return u"navsub selected"
            else:
                return u"navsub"
        else:
            if self.selected:
                return u"navsub first selected"
            else:
                return u"navsub"

    
class GlobalMenuAddItem(GlobalMenuSubItem):
    def __init__(self, context, request, view, manager):
        GlobalMenuSubItem.__init__(self, context, request, view, manager)
        self.firstFolder = iter(objectsWithInterface(self.folderInterface)).next()
    @property
    def url(self):
        if self.firstFolder is not None:
            try:
                contextURL = absoluteURL(self.firstFolder, self.request)
            except TypeError:
                contextURL = u''
        else:
            contextURL = absoluteURL(self.context, self.request)
        return contextURL + '/' + self.viewURL
    def render(self):
        """Return the template with the option 'menus'"""
        if self.firstFolder is not None:
            return self.template()
        else:
            return ""


    
class GlobalMenuSubSubItem(ContextMenuItem):
    """Menu item viewlet generating global/site related links."""
    template = viewpagetemplatefile.ViewPageTemplateFile('menu_sub_item.pt')
    @property
    def menu_class(self):
        if self.posInManager > 0:
            if self.selected:
                return u"navsub selected"
            else:
                return u"navsub"
        else:
            if self.selected:
                return u"navsub first selected"
            else:
                return u"navsub"

    
class DashboardItem(GlobalMenuMainItem):
    title = _(u'Dashboard')
    viewURL = 'view_dashboard.html'
    weight = 5

class NotificationsItem(GlobalMenuMainItem):
    title = _(u'Notifications')
    viewURL = 'view_notifications.html'
    weight = 105

class SearchItem(GlobalMenuMainItem):
    title = _(u'Search')
    viewURL = 'search.html'
    weight = 8500

class HelpItem(GlobalMenuMainItem):
    title = _(u'Help')
    viewURL = 'help.html'
    weight = 9999

class NetworksItem(GlobalMenuMainItem):
    title = _(u'Networks')
    viewURL = 'all_networks.html'
    weight = 1000

class HostsItem(GlobalMenuMainItem):
    title = _(u'Hosts')
    viewURL = 'all_hosts.html'
    weight = 2000

class ServicesItem(GlobalMenuMainItem):
    title = _(u'Services')
    viewURL = 'all_services.html'
    weight = 2000

class AdmUtilManagerItem(GlobalMenuMainItem):
    title = _(u'Utilities')
    weight = 8000
    
    @property
    def url(self):
        utilManager = getUtility(IUtilManager)
        if utilManager is not None:
            return absoluteURL(utilManager, self.request) + \
                   u'/@@overview.html'
        else:
            return absoluteURL(hooks.getSite(), self.request) + \
                   '/NoUtilManager'


class MenuMainTab(Tab):
    template = viewpagetemplatefile.ViewPageTemplateFile('menu_main_tab.pt')

class MenuContextTab(Tab):
    template = viewpagetemplatefile.ViewPageTemplateFile('menu_context_tab.pt')

class MenuSubTab(Tab):
    template = viewpagetemplatefile.ViewPageTemplateFile('menu_sub_tab.pt')


#class MenuSubTemplateTab(Tab):
    #def render(self):
        #if len(self.viewlets) > 0:
            #return Tab.render(self)
        #else:
            #return u''

class MenuSubGeneralTab(Tab):
    template = viewpagetemplatefile.ViewPageTemplateFile('menu_sub_general_tab.pt')


class MenuSubGeneralAddsTab(Tab):
    template = viewpagetemplatefile.ViewPageTemplateFile('menu_sub_general_adds_tab.pt')

    def sort(self, viewlets):
        print ">" * 80
        #import pdb
        #pdb.set_trace()
        print viewlets
        print "<" * 80
        return sorted(viewlets, key=getSortableTitel)

class MenuSubInventoryTab(Tab):
    template = viewpagetemplatefile.ViewPageTemplateFile('menu_sub_inventory_tab.pt')

class MenuSubInventoryByTypeTab(Tab):
    template = viewpagetemplatefile.ViewPageTemplateFile('menu_sub_inventory_by_type_tab.pt')
    def sort(self, viewlets):
        return sorted(viewlets, key=getSortableTitel)

class MenuSubInventoryWarningsTab(Tab):
    template = viewpagetemplatefile.ViewPageTemplateFile('menu_sub_inventory_warnings_tab.pt')

class MenuSubReportsTab(Tab):
    template = viewpagetemplatefile.ViewPageTemplateFile('menu_sub_reports_tab.pt')

class MenuSubReportsOvervPdfTab(Tab):
    template = viewpagetemplatefile.ViewPageTemplateFile('menu_sub_reports_overv_pdf_tab.pt')

class MenuSubEventTab(Tab):
    template = viewpagetemplatefile.ViewPageTemplateFile('menu_sub_event_tab.pt')

class MenuSubScriptTab(Tab):
    template = viewpagetemplatefile.ViewPageTemplateFile('menu_sub_script_tab.pt')

class MenuSubAdminTab(Tab):
    template = viewpagetemplatefile.ViewPageTemplateFile('menu_sub_admin_tab.pt')
