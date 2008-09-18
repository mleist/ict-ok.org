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
"""implementation of browser class of Host object
"""

__version__ = "$Id$"

# python imports

# zope imports
import zope.event
from zope.app import zapi
from zope.component import getUtility
from zope.size.interfaces import ISized
from zope.proxy import removeAllProxies
from zope.i18nmessageid import MessageFactory
from zope.security import checkPermission
from zope.lifecycleevent import Attributes, ObjectModifiedEvent
from zope.app.intid.interfaces import IIntIds
from zope.app.pagetemplate.urlquote import URLQuote
from zope.app.appsetup import appsetup
from zope.app.catalog.interfaces import ICatalog

# z3c imports
from z3c.form import form, field
from z3c.pagelet.browser import BrowserPagelet
from zc.table.column import GetterColumn

# ict_ok.org imports
from org.ict_ok.components.supernode.interfaces import IState
from org.ict_ok.components.host.interfaces import IHost, IEventIfEventHost
from org.ict_ok.components.host.host import getAllHosts, Host
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.components.superclass.browser.superclass import applyChanges
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditContent, EditForm
from org.ict_ok.admin_utils.eventcrossbar.interfaces import \
     IAdmUtilEvent
from org.ict_ok.components.superclass.interfaces import \
     IEventIfSuperclass
from org.ict_ok.components.superclass.browser.superclass import \
     Overview, \
     getStateIcon, getTitel, getModifiedDate, getActionBottons, getHealth, \
     raw_cell_formatter, IPsGetterColumn, TitleGetterColumn

_ = MessageFactory('org.ict_ok')

# --------------- menu entries -----------------------------


class MSubAddHost(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Host')
    viewURL = 'add_hosts.html'
    weight = 50

# --------------- helper funktions -----------------------------

def getHostIp(item, formatter):
    """
    Ip for Overview
    """
    return ", ".join(item.getIpList())

# --------------- object details ---------------------------


class HostDetails(ComponentDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + ['osList']
    omit_addfields = ComponentDetails.omit_addfields + ['osList']
    omit_editfields = ComponentDetails.omit_editfields + ['osList']
    #omit_viewfields = ComponentDetails.omit_viewfields + []
    #omit_addfields = ComponentDetails.omit_addfields + []
    #omit_editfields = ComponentDetails.omit_editfields + []
    
    def actions(self):
        """
        gives us the action dict of the object
        """
        try:
            objId = getUtility(IIntIds).getId(self.context)
        except:
            objId = 1000
        retList = []
        if appsetup.getConfigContext().hasFeature('devmode') and \
           checkPermission('org.ict_ok.components.host.Edit', self.context):
            quoter = URLQuote(self.request.getURL())
            tmpDict = {}
            tmpDict['oid'] = u"c%strigger_online" % objId
            tmpDict['title'] = _(u"Trigger online")
            tmpDict['href'] = u"%s/@@trigger_online?nextURL=%s" % \
                   (zapi.getPath( self.context),
                    quoter.quote())
            retList.append(tmpDict)
            tmpDict = {}
            tmpDict['oid'] = u"c%strigger_offline" % objId
            tmpDict['title'] = _(u"Trigger offline")
            tmpDict['href'] = u"%s/@@trigger_offline?nextURL=%s" % \
                   (zapi.getPath( self.context),
                    quoter.quote())
            retList.append(tmpDict)
            tmpDict = {}
            tmpDict['oid'] = u"c%strigger_not1" % objId
            tmpDict['title'] = _(u"Trigger notification1")
            tmpDict['href'] = u"%s/@@trigger_not1?nextURL=%s" % \
                   (zapi.getPath( self.context),
                    quoter.quote())
            retList.append(tmpDict)
        adapSize = ISized(self.context)
        if checkPermission('org.ict_ok.components.interface.Add', self.context) and \
           (adapSize.sizeForSorting()[1] < 1):
            tmpDict = {}
            tmpDict['oid'] = u"c%sstart_snmp_if_scanner" % objId
            tmpDict['title'] = _(u"start snmp interface scanner")
            tmpDict['href'] = u"%s/@@start_snmp_if_scanner.html" % \
                   zapi.getPath(self.context)
            tmpDict['tooltip'] = _(u"starts the interface scanner with snmp scan (as user:%s)"\
                                   % self.request.principal.title)
            retList.append(tmpDict)
        return retList

    def state(self):
        """
        gives us the state dict of the object
        """
        return IState(self.context).getStateDict()

    def trigger_online(self):
        """
        trigger workflow
        """
        print "trigger_online@browser"
        self.context.trigger_online()
        nextURL = self.request.get('nextURL', default=None)
        if nextURL:
            return self.request.response.redirect(nextURL)
        else:
            return self.request.response.redirect('./@@details.html')

    def trigger_offline(self):
        """
        trigger workflow
        """
        print "trigger_offline@browser"
        self.context.trigger_offline()
        nextURL = self.request.get('nextURL', default=None)
        if nextURL:
            return self.request.response.redirect(nextURL)
        else:
            return self.request.response.redirect('./@@details.html')

    def trigger_not1(self):
        """
        trigger workflow
        """
        print "trigger_not1@browser"
        self.context.trigger_not1()
        nextURL = self.request.get('nextURL', default=None)
        if nextURL:
            return self.request.response.redirect(nextURL)
        else:
            return self.request.response.redirect('./@@details.html')
        
    def getHistory(self):
        """
        return List of history entries for the browser
        """
        retList = []
        obj = removeAllProxies(self.context)
        historyList = obj.history
        for entry in historyList:
            tmpList = entry.getList(['date', 'text', 'level', \
                                     'version', 'bgcolor'])
            retList.append(tmpList )
        retList.sort(lambda a, b: cmp(b[0], a[0]))
        return retList
    
    def getWFMC(self):
        """
        return list of Workflows of this object
        """
        from zope.component import queryUtility
        from org.ict_ok.admin_utils.wfmc.interfaces import \
             IAdmUtilWFMC
        
        utilWFMC = queryUtility(IAdmUtilWFMC)
        #print "utilWFMC: %s" % utilWFMC
        
        from org.ict_ok.components.host.wf import pd
        return pd.activities
        #return utilWFMC
        
    def getWFMCs(self):
        """
        return list of Workflows of this object
        """
        obj = removeAllProxies(self.context)
        owfs = obj.workflows
        return owfs


class AddHostClass(BrowserPagelet):
    def update(self):
        pass


# --------------- forms ------------------------------------


class DetailsHostForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of host')
    fields = field.Fields(IHost).omit(*HostDetails.omit_viewfields)


class AddHostForm(AddForm):
    """Add form."""
    label = _(u'Add Host')
    fields = field.Fields(IHost).omit(*HostDetails.omit_addfields)
    factory = Host


class EditHostForm(EditForm):
    """ Edit form for host """
    form.extends(form.EditForm)
    label = _(u'Host Edit Form')
    fields = field.Fields(IHost).omit(*HostDetails.omit_editfields)


class DeleteHostForm(DeleteForm):
    """ Delete the net """
    
    def getTitel(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this host: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class EditEventHostEventIfForm(EditForm):
    """ Edit Event Interface of object """
    label = _(u'host event interfaces form')
    fields = field.Fields(IEventIfEventHost)
    
    def applyChanges(self, data):
        content = self.getContent()
        changes = applyChanges(self, content, data)
        # ``changes`` is a dictionary; if empty, there were no changes
        if changes:
            #import pdb;pdb.set_trace()
            # Construct change-descriptions for the object-modified event
            descriptions = []
            for interface, attrs in changes.items():
                if interface == IAdmUtilEvent:
                    print "##### Event 2 #######"
                elif IEventIfSuperclass.isEqualOrExtendedBy(interface):
                    print "##### Superclass 2 #######"
                names = attrs.keys()
                for attr in attrs: 
                    if attr.find("eventInpObjs_") == 0: # attribute name starts with ...
                        functionName = attr[len('eventInpObjs_'):]
                        print "attr: %s (I:%s)" % (attr, interface)
                        print "   old: ", attrs[attr]['oldval']
                        print "   new: ", attrs[attr]['newval']
                        newSet = attrs[attr]['newval']
                        oldSet = attrs[attr]['oldval']
                        if type(newSet) == type(set()) and \
                           type(oldSet) == type(set()):
                            newEntries = newSet.difference(oldSet)
                            oldEntries = oldSet.difference(newSet)
                            for oldOid in oldEntries:
                                my_catalog = zapi.getUtility(ICatalog)
                                for resObj in my_catalog.searchResults(oid_index=oldOid):
                                    if IAdmUtilEvent.providedBy(resObj):
                                        resObj.removeOidFromOutObjects(
                                            content.objectID + "." + functionName)
                                        resObj.removeInvalidOidFromInpOutObjects()
                                        resObj._p_changed = True
                            for newOid in newEntries:
                                my_catalog = zapi.getUtility(ICatalog)
                                for resObj in my_catalog.searchResults(oid_index=newOid):
                                    if IAdmUtilEvent.providedBy(resObj):
                                        resObj.addOidToOutObjects(
                                            content.objectID + "." + functionName)
                                        resObj.removeInvalidOidFromInpOutObjects()
                                        resObj._p_changed = True
                descriptions.append(Attributes(interface, *names))
            # Send out a detailed object-modified event
            zope.event.notify(ObjectModifiedEvent(content, *descriptions))
        return changes


class AllHosts(Overview):
    """Overview Pagelet"""
    columns = (
        GetterColumn(title="",
                     getter=getStateIcon,
                     cell_formatter=raw_cell_formatter),
        GetterColumn(title=_('Health'),
                     getter=getHealth),
        TitleGetterColumn(title=_('Title'),
                          getter=getTitel),
        IPsGetterColumn(title=_('IP'),
                     getter=getHostIp),
        GetterColumn(title=_('Modified On'),
                     getter=getModifiedDate,
                     cell_formatter=raw_cell_formatter),
        GetterColumn(title=_('Actions'),
                     getter=getActionBottons,
                     cell_formatter=raw_cell_formatter),
        )
    sort_columns = [1, 2, 3, 4]
    def objs(self):
        """List of Content objects"""
        return getAllHosts()

