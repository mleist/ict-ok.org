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

# phython imports

# zope imports
from org.ict_ok.skin.interfaces import IMasterMenu
from zope.i18nmessageid import MessageFactory
from zope.viewlet import manager
from zope.app.component import hooks
from zope.component import getUtility
from zope.traversing.browser import absoluteURL
from zope.app.pagetemplate import viewpagetemplatefile

# z3c imports
from z3c.menu.simple.menu import TabMenu
from z3c.menu.simple import menu
from z3c.menu.simple import ITab
from z3c.menu.simple.menu import Tab

# ict_ok.org imports
from org.ict_ok.admin_utils.util_manager.interfaces import IUtilManager

_ = MessageFactory('org.ict_ok')

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

    
class DashboardItem(GlobalMenuMainItem):
    title = _(u'Dashboard')
    viewURL = 'view_dashboard.html'
    weight = 5

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

class MenuSubTab(Tab):
    template = viewpagetemplatefile.ViewPageTemplateFile('menu_sub_tab.pt')
