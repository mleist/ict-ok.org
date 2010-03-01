# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0613,W0232,W0142,R0901
#
from twisted.web.sux import ParseError
"""implementation of browser class of supervisor
"""

__version__ = "$Id$"

# python imports
from datetime import timedelta
import os
from datetime import datetime
import tempfile

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
from zope.app.catalog.interfaces import ICatalog
from zope.traversing.browser import absoluteURL
from zope.app.rotterdam.xmlobject import setNoCacheHeaders

# z3c imports
from z3c.form import button, field, form, interfaces
from z3c.formui import layout
from z3c.pagelet.browser import BrowserPagelet

# zc imports
from zc.table.column import GetterColumn
from zc.table.table import StandaloneFullFormatter
from zc.table.interfaces import ISortableColumn
from zc.i18n.duration import format as i18nformat

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory
from org.ict_ok.components.supernode.interfaces import IState
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     DisplayForm, EditForm, Overview
from org.ict_ok.admin_utils.supervisor.supervisor import \
     AdmUtilSupervisor
from org.ict_ok.components.superclass.browser import \
     superclass
from org.ict_ok.admin_utils.usermanagement.usermanagement import \
     getUserTimezone
from org.ict_ok.admin_utils.objmq.interfaces import IAdmUtilObjMQ
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.version import getIkVersion
from org.ict_ok.admin_utils.supervisor.interfaces import \
    IAdmUtilSupervisor, IImportAllData
from org.ict_ok.components.interfaces import IImportXlsData

_ = MessageFactory('org.ict_ok')

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

class MSubIndices(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Indices')
    viewURL = 'indices.html'
    weight = 51

class MSubImportAllData(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Import All Data')
    viewURL = 'importalldata.html'
    weight = 290

class MSubExportAllData(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Export All Data')
    viewURL = 'exportalldata.html'
    weight = 291



# --------------- object details ---------------------------


class AdmUtilSupervisorDetails(SupernodeDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = SupernodeDetails.omit_viewfields + ['ikName', 'fsearchText']
    omit_editfields = SupernodeDetails.omit_editfields + ['ikName', 'fsearchText']

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
                   (zapi.absoluteURL(self.context, self.request),
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
                   (zapi.absoluteURL(self.context, self.request),
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
        return i18nformat(self.request,
                          timedelta(seconds=self.context.getSystemUptime()))
    

    def cmd(self):
        """
        commnds for objmq
        """
        obj = self.context
        print "cmd/objmq"
        print "path: %s" % (zapi.absoluteURL(obj, self.request))
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
                         #(obj.objectID, obj.ipv4My, zapi.absoluteURL(obj, self.request))
                #to_adr = u"http://%s@%s:8080/++etc++site/default/AdmUtilSupervisor" % \
                         #(str(obj.oidMaster), str(obj.ipv4Master))
                #mq_utility.send(from_adr, [to_adr], "msg_start")
                
            elif action == 'stop':
                print "stop"
                mq_utility = zapi.getUtility(IMailDelivery,
                                              'ikObjTransportQueue')
                from_adr = u"http://%s@%s:8080%s" % \
                         (obj.objectID, obj.ipv4My, zapi.absoluteURL(obj, self.request))
                to_adr = u"http://%s@%s:8080/++etc++site/"+\
                       "default/AdmUtilSupervisor" % \
                         (str(obj.oidMaster), str(obj.ipv4Master))
                mq_utility.send(from_adr, [to_adr], "msg_stop")
            elif action == 'ping':
                obj.sendPing()
            else:
                pass
        return self.request.response.redirect('./@@objmq')

    def exportAllData(self):
        """get data file for all objects"""
        self.request.response.setHeader('Content-Type', 'application/x-ict-ok-data')
        self.request.response.setHeader(\
            'Content-Disposition',
            'attachment; filename=\"%s.xml\"' % self.context.objectID)
        setNoCacheHeaders(self.request.response)
        return self.context.exportAllData()        #self.context is AdmUtilSupervisor

class AdmUtilSupervisorVersion(SupernodeDetails):
    """ for version display
    """

    def getSystemUptime(self):
        """
        get the uptime of the running system
        no args, returns string
        """
        return i18nformat(self.request,
                          timedelta(seconds=self.context.getSystemUptime()))

    def getVersion(self):
        """
        special format list of the history for web-view
        """
        return getIkVersion()

    def getDbSize(self):
        """
        return the size of Database
        """
        size = self.request.publication.db.getSize()
        return size / 1000


def formatEntryDate(entry, formatter):
    """Entry Date for history in Web-Browser"""
    try:
        userTZ = getUserTimezone()
        my_formatter = formatter.request.locale.dates.getFormatter(
            'dateTime', 'short')
        timeString = my_formatter.format(userTZ.fromutc(entry['date']))
        timeStringHTML = timeString.replace(" ", "&nbsp;")
        my_formatter = formatter.request.locale.dates.getFormatter(
            'dateTime', 'long')
        longTimeString = my_formatter.format(userTZ.fromutc(entry['date']))
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

def formatIndicesName(index, formatter):
    return index.__name__

def formatIndicesDocuments(index, formatter):
    return index.documentCount()

def formatIndicesWords(index, formatter):
    return index.wordCount()

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
        formatter.batch_size = 150
        formatter.cssClasses['table'] = 'listing'
        return formatter()


class ViewAdmUtilSupervisorIndicesForm(BrowserPagelet):
    """Generation Pagelet"""
    label = _(u'Indices')
    columns = (
        GetterColumn(title=_('Name'),
                     getter=formatIndicesName),
        GetterColumn(title=_('Documents'),
                     getter=formatIndicesDocuments),
        GetterColumn(title=_('Words'),
                     getter=formatIndicesWords),
    )
    
    def objs(self):
        """list of generation manager objects"""
        retList =[]
        utilCatalog = getUtility(ICatalog)
        for idx_name, idx_obj in utilCatalog.items():
            retList.append(idx_obj)
        return retList

    def table(self):
        """ Properties of table are defined here"""
        directlyProvides(self.columns[0], ISortableColumn)
        directlyProvides(self.columns[1], ISortableColumn)
        directlyProvides(self.columns[2], ISortableColumn)
        formatter = StandaloneFullFormatter(
            self.context, self.request, self.objs(),
            columns=self.columns, sort_on=((_('Name'), False),))
        formatter.batch_size = 150
        formatter.cssClasses['table'] = 'listing'
        return formatter()


# --------------- forms ------------------------------------


class ViewAdmUtilSupervisorForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of supervisor')
    factory = AdmUtilSupervisor
    omitFields = AdmUtilSupervisorDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class EditAdmUtilSupervisorForm(EditForm):
    """ Edit for for net """
    label = _(u'edit supervisor')
    factory = AdmUtilSupervisor
    omitFields = AdmUtilSupervisorDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)


class FSearchForm(Overview):
    """ Search Form """
#    form.extends(form.Form)
    label = _(u"Search for what?")
    fsearchText = None
    
    def objs(self):
        """List of Content objects"""
        retList = []
        if self.fsearchText is not None:
            my_catalog = zapi.getUtility(ICatalog)
            try:
                res = my_catalog.searchResults(all_fulltext_index=self.fsearchText)
                for obj in res:
                    retList.append(obj)
            except ParseError, errText:
                self.status = u"Error: '%s'" % errText
        return retList
    
    def update(self):
        if self.request.has_key('key'):
            self.fsearchText = self.request['key']
        else:
            myForm = self.request.form
            if myForm.has_key('form.widgets.fsearchText'):
                self.fsearchText = myForm['form.widgets.fsearchText']


class TypeSearchForm(Overview):
    """ Search Form """
#    form.extends(form.Form)
    fsearchText = None
    
    def objs(self):
        """List of Content objects"""
        retList = []
        uidutil = getUtility(IIntIds)
        for (oid, oobj) in uidutil.items():
            retList.append(oobj.object)
#            import pprint
#            pprint.pprint(retList)
        return retList
    
#    def update(self):
#        if self.request.has_key('key'):
#            self.fsearchText = self.request['key']
#        else:
#            myForm = self.request.form
#            if myForm.has_key('form.widgets.fsearchText'):
#                self.fsearchText = myForm['form.widgets.fsearchText']

class ImportAllDataForm(layout.FormLayoutSupport, form.Form):
    """ Delete the net """
    
    form.extends(form.Form)
    label = _(u"Import an 'all-data file' data")
    fields = field.Fields(IImportAllData)
    
    @button.buttonAndHandler(u'Submit')
    def handleSubmit(self, action):
        """submit was pressed"""
        if 'alldata' in self.widgets:
            fileWidget=self.widgets['alldata']
            fileUpload = fileWidget.extract()
            xml_string = ''.join(fileUpload.readlines())
            if self.context.importAllData(xml_string):
                # ERROR behandlung
                pass
        url = absoluteURL(self.context, self.request)
        self.request.response.redirect(url)

    @button.buttonAndHandler(u'Cancel')
    def handleCancel(self, action):
        """cancel was pressed"""
        url = absoluteURL(self.context, self.request)
        self.request.response.redirect(url)

    def update(self):
        """update all widgets"""
        #if ISuperclass.providedBy(self.context):
            #self.label = self.getTitle()
        form.Form.update(self)


class ImportAllXlsDataForm(layout.FormLayoutSupport, form.Form):
    """ Import all objects """
    
    form.extends(form.Form)
    label = _(u"Import all XLS data")
    fields = field.Fields(IImportXlsData)
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return u"aaa"

    @button.buttonAndHandler(u'Submit')
    def handleSubmit(self, action):
        """submit was pressed"""
        #import pdb
        #pdb.set_trace()
        supervisor = getUtility(IAdmUtilSupervisor,
                                name='AdmUtilSupervisor')
        if 'xlsdata' in self.widgets:
            codepage=self.widgets['codepage'].value[0]
            fileWidget=self.widgets['xlsdata']
            fileUpload = fileWidget.extract()
            filename = datetime.now().strftime('in_%Y%m%d%H%M%S.xls')
            f_handle, f_name = tempfile.mkstemp(filename)
            outf = open(f_name, 'wb')
            outf.write(fileUpload.read())
            outf.close()
            try:
                supervisor.importAllXlsData(self.request, f_name, codepage)
            finally:
                os.remove(f_name)
        url = absoluteURL(self.context, self.request)
        self.request.response.redirect(url)

    @button.buttonAndHandler(u'Cancel')
    def handleCancel(self, action):
        """cancel was pressed"""
        url = absoluteURL(self.context, self.request)
        self.request.response.redirect(url)
    def update(self):
        """update all widgets"""
        #if ISuperclass.providedBy(self.context):
            #self.label = self.getTitle()
        form.Form.update(self)

class RootFolderDetails:
    def exportAllXlsData(self):
        """get XLS file for all folder objects"""
        supervisor = getUtility(IAdmUtilSupervisor,
                                name='AdmUtilSupervisor')
        (filename, dataMem) = supervisor.exportAllXlsData(self.request)
        self.request.response.setHeader('Content-Type', 'application/vnd.ms-excel')
        self.request.response.setHeader(\
            'Content-Disposition',
            'attachment; filename=\"%s\"' % filename)
        setNoCacheHeaders(self.request.response)
        return dataMem
