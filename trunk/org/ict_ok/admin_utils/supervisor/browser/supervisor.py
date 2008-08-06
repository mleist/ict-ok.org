# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0232,W0142,R0901
#
"""implementation of browser class of supervisor
"""

__version__ = "$Id$"

# phython imports
from pytz import timezone

# zope imports
from zope.interface import implements
from zope.app import zapi
from zope.component import getUtility
from zope.size.interfaces import ISized
from zope.app.intid.interfaces import IIntIds
from zope.i18nmessageid import MessageFactory
from zope.security import checkPermission
from zope.sendmail.interfaces import IMailDelivery
from zope.app.zapi import getPath
from zope.interface import directlyProvides
from zope.app.pagetemplate.urlquote import URLQuote
from zope.app.generations.generations import findManagers

# z3c imports
from z3c.form import field
from z3c.pagelet.browser import BrowserPagelet

# zc imports
from zc.table.column import GetterColumn
from zc.table.table import StandaloneFullFormatter
from zc.table.interfaces import ISortableColumn

# ict_ok.org imports
from org.ict_ok.components.supernode.interfaces import IState
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     DisplayForm, EditForm
from org.ict_ok.admin_utils.supervisor.interfaces import \
     IAdmUtilSupervisor
from org.ict_ok.components.superclass.browser import \
     superclass
from org.ict_ok.libs.lib import convertSystemUptime2String
from org.ict_ok.admin_utils.objmq.interfaces import IAdmUtilObjMQ
from org.ict_ok.skin.menu import GlobalMenuSubItem

_ = MessageFactory('org.ict_ok')
berlinTZ = timezone('Europe/Berlin')

# --------------- menu entries -----------------------------


class MSubEvents(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Events')
    viewURL = 'events.html'
    weight = 90

class MSubGenerations(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Generations')
    viewURL = 'generations.html'
    weight = 50


# --------------- object details ---------------------------


class AdmUtilSupervisorDetails(SupernodeDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = SupernodeDetails.omit_viewfields + ['ikName']
    omit_editfields = SupernodeDetails.omit_editfields + ['ikName']

    def actions(self):
        """
        gives us the action dict of the object
        """
        try:
            objId = getUtility(IIntIds).getId(self.context)
        except KeyError:
            objId = 1000
        retList = []
        adapSize = ISized(self.context)
        if checkPermission('org.ict_ok.admin_utils.supervisor.ReindexDB',
                           self.context):
            quoter = URLQuote(self.request.getURL())
            tmpDict = {}
            tmpDict['oid'] = u"c%sreindex_db" % objId
            tmpDict['title'] = _(u"reindex database")
            tmpDict['href'] = u"%s/@@reindex_db?nextURL=%s" % \
                   (zapi.getPath( self.context),
                    quoter.quote())
            tmpDict['tooltip'] = _(u"will reindex the catalogs of all "\
                                   u"tables in database")
            retList.append(tmpDict)
        if checkPermission('org.ict_ok.admin_utils.supervisor.PackDB',
                           self.context):
            quoter = URLQuote(self.request.getURL())
            tmpDict = {}
            tmpDict['oid'] = u"c%spack_db" % objId
            tmpDict['title'] = _(u"pack database")
            tmpDict['href'] = u"%s/@@pack_db?nextURL=%s" % \
                   (zapi.getPath( self.context),
                    quoter.quote())
            tmpDict['tooltip'] = _(u"will pack the database and delete "\
                                   u"all backups")
            retList.append(tmpDict)
        return retList
    
    def state(self):
        """
        gives us the state dict of the object
        """
        return IState(self.context).getStateDict()

    def reindex_db(self):
        """
        will reindex the catalogs of all tables in database
        """
        self.context.reindex_db()
        nextURL = self.request.get('nextURL', default=None)
        if nextURL:
            return self.request.response.redirect(nextURL)
        else:
            return self.request.response.redirect('./@@details.html')

    def pack_db(self):
        """
        will pack the database
        """
        size_pre = self.request.publication.db.getSize()
        self.request.publication.db.pack(days=0)
        size_post = self.request.publication.db.getSize()
        ratio = float(size_post)/size_pre*100
        self.context.appendEventHistory(\
            u"zodb packed by '%s'; %d bytes -> %d bytes (%.1f%%)" % \
            (self.request.principal.title, size_pre, size_post, ratio))
        nextURL = self.request.get('nextURL', default=None)
        if nextURL:
            return self.request.response.redirect(nextURL)
        else:
            return self.request.response.redirect('./@@details.html')
        
        
    def getlastEvents(self):
        """convert event history for display
        """
        eventList = self.context.getlastEvents()
        return eventList[:1000]

    def getStartCnt(self):
        """convert start counter for display
        """
        return self.context.getStartCnt()
    
    def getSystemUptime(self):
        """
        get the uptime of the running system
        no args, returns string
        """
        return convertSystemUptime2String(self.context.getSystemUptime())

    def cmd(self):
        """
        commnds for objmq
        """
        #obj = removeAllProxies(self.context)
        obj = self.context
        print "cmd/objmq"
        print "path: %s" % (zapi.getPath(obj))
        action = self.request.get('cmd', default=None)
        if action:
            if action == 'start':
                obj.status2Master = u"connecting"
                #print "start"
                #print "obj.oidSlave: %s" % (obj.oidSlave)
                #obj.appendSlaveUid(u"bc6ae87821e43509dc3a5152a030951b0")
                #print "dir(obj.oidSlave): %s" % dir(obj.oidSlave)
                #print "obj.oidSlave: %s" % (obj.oidSlave)
                mq_utility = zapi.getUtility(IAdmUtilObjMQ)
                my_data = {'cmd': 'connect',
                           'nodename': unicode(obj.getNodeName())}
                my_data['header'] = {'from_oid': obj.objectID,
                                     'from_ip': obj.ipv4My,
                                     'from_path': getPath(obj),
                                     'to_oid': obj.oidMaster,
                                     'to_ip': obj.ipv4Master,
                                     'to_path': u"/++etc++site/default"+\
                                     "/AdmUtilSupervisor"
                                 }
                mq_utility.sendPerMq(my_data)

                #python_pickle = pickle.dumps(my_data)
                ##print "toxml: %s" % toxml(python_pickle)
                #mq_utility.sendPerMq(toxml(python_pickle))
                #mq_utility = zapi.getUtility(IMailDelivery, 'ikObjTransportQueue')
                #from_adr = u"http://%s@%s:8080%s" % \
                         #(obj.objectID, obj.ipv4My, zapi.getPath(obj))
                #to_adr = u"http://%s@%s:8080/++etc++site/default/AdmUtilSupervisor" % \
                         #(str(obj.oidMaster), str(obj.ipv4Master))
                #mq_utility.send(from_adr, [to_adr], "msg_start")
                
            elif action == 'stop':
                print "stop"
                mq_utility = zapi.getUtility(IMailDelivery,
                                              'ikObjTransportQueue')
                from_adr = u"http://%s@%s:8080%s" % \
                         (obj.objectID, obj.ipv4My, zapi.getPath(obj))
                to_adr = u"http://%s@%s:8080/++etc++site/"+\
                       "default/AdmUtilSupervisor" % \
                         (str(obj.oidMaster), str(obj.ipv4Master))
                mq_utility.send(from_adr, [to_adr], "msg_stop")
            elif action == 'ping':
                obj.sendPing()
            else:
                pass
        return self.request.response.redirect('./@@objmq')

def formatEntryDate(entry, formatter):
    """Entry Date for history in Web-Browser"""
    try:
        my_formatter = formatter.request.locale.dates.getFormatter(
            'dateTime', 'short')
        timeString = my_formatter.format(berlinTZ.fromutc(entry['date']))
        timeStringHTML = timeString.replace(" ", "&nbsp;")
        my_formatter = formatter.request.locale.dates.getFormatter(
            'dateTime', 'long')
        longTimeString = my_formatter.format(berlinTZ.fromutc(entry['date']))
        ttid = u"id" + str(abs(hash(timeString)))
        tooltip = u"<script type=\"text/javascript\">tt_%s = new YAHOO." \
                u"widget.Tooltip('tt_%s', { autodismissdelay:'15000', " \
                u"context:'%s', text:'%s' });</script>" \
                % (ttid, ttid, ttid, longTimeString)
        resString = u'<span id="%s">%s</span>' % (ttid, timeStringHTML)
    except AttributeError:
        resString = u"---"
        tooltip = u""
    return resString + tooltip

def formatEntryNbr(entry, formatter):
    return entry['nbr']

def formatEntryMessage(entry, formatter):
    return entry['msg']

def formatGenerationNbr(genManager, formatter):
    return genManager.generation

def formatGenerationMinimum(genManager, formatter):
    return genManager.minimum_generation

def formatGenerationName(genManager, formatter):
    return genManager.package_name

class DateGetterColumn(GetterColumn):
    """Getter columnt that has locale aware sorting."""
    implements(ISortableColumn)
    def getSortKey(self, item, formatter):
        return item['date']

    
#class Events(BrowserPagelet):
class ViewAdmUtilSupervisorEventsForm(BrowserPagelet):
    """History Pagelet"""
    label = _(u'Supervisor events')
    columns = (
        GetterColumn(title=_('Start number'),
                     getter=formatEntryNbr),
        DateGetterColumn(title=_('Date'),
                     getter=formatEntryDate,
                     cell_formatter=superclass.raw_cell_formatter),
        GetterColumn(title=_('Message'),
                     getter=formatEntryMessage),
    )
    def objs(self):
        """List of Content objects"""
        eventList = self.context.getlastEvents()
        return eventList[:1000]

    def table(self):
        """ Properties of table are defined here"""
        directlyProvides(self.columns[0], ISortableColumn)
        directlyProvides(self.columns[1], ISortableColumn)
        directlyProvides(self.columns[2], ISortableColumn)
        formatter = StandaloneFullFormatter(
            self.context, self.request, self.objs(),
            columns=self.columns, sort_on=((_('Date'), True),))
        formatter.batch_size = 30
        formatter.cssClasses['table'] = 'listing'
        return formatter()


class ViewAdmUtilSupervisorGenerationsForm(BrowserPagelet):
    """Generation Pagelet"""
    label = _(u'Generations')
    columns = (
        GetterColumn(title=_('Name'),
                     getter=formatGenerationName),
        GetterColumn(title=_('Generation'),
                     getter=formatGenerationNbr),
        GetterColumn(title=_('Minimum Generation'),
                     getter=formatGenerationMinimum),
    )
    def objs(self):
        """list of generation manager objects"""
        retList =[]
        for (genManagerName, genManagerObj) in findManagers():
            retList.append(genManagerObj)
        return retList

    def table(self):
        """ Properties of table are defined here"""
        directlyProvides(self.columns[0], ISortableColumn)
        directlyProvides(self.columns[1], ISortableColumn)
        directlyProvides(self.columns[2], ISortableColumn)
        formatter = StandaloneFullFormatter(
            self.context, self.request, self.objs(),
            columns=self.columns, sort_on=((_('Name'), False),))
        formatter.batch_size = 30
        formatter.cssClasses['table'] = 'listing'
        return formatter()


# --------------- forms ------------------------------------


class ViewAdmUtilSupervisorForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of supervisor')
    fields = field.Fields(IAdmUtilSupervisor).omit(\
        *AdmUtilSupervisorDetails.omit_viewfields)


class EditAdmUtilSupervisorForm(EditForm):
    """ Edit for for net """
    label = _(u'edit supervisor')
    fields = field.Fields(IAdmUtilSupervisor).omit(\
        *AdmUtilSupervisorDetails.omit_editfields)
