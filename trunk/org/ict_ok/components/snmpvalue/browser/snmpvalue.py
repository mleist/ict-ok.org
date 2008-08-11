# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=F0401,E1101,E0611,W0232,W0142
#
"""implementation of browser class of SnmpValue object
"""

__version__ = "$Id$"

# phython imports
import time
import rrdtool

# zope imports
from zope.app import zapi
from zope.proxy import removeAllProxies
from zope.interface import directlyProvides
from zope.component import getUtility
from zope.i18nmessageid import MessageFactory
from zope.app.container.interfaces import IOrderedContainer
from zope.app.pagetemplate.urlquote import URLQuote

# zc imports
from zc.table.column import Column, GetterColumn
from zc.table.table import StandaloneFullFormatter
from zc.table.interfaces import ISortableColumn

# z3c imports
from z3c.form import field
from z3c.pagelet.browser import BrowserPagelet

# ict_ok.org imports
from org.ict_ok.admin_utils.snmpd.interfaces import IAdmUtilSnmpd
from org.ict_ok.components.snmpvalue.interfaces import ISnmpValue
from org.ict_ok.components.snmpvalue.snmpvalue import SnmpValue
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditForm, raw_cell_formatter

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddSnmpValue(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add SNMP Value')
    #viewURL = 'add_snmpvalue.html'
    viewURL = 'add_snmps_by_vendor.html'
    weight = 50


# --------------- object details ---------------------------


class SnmpValueDetails(ComponentDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []
    
    def getValuePngDeltaT(self):
        """get Picture for special time interval"""
        hours = float(self.request.get('hours', default="1"))
        currtime = time.time()
        params = {}
        params['nameext'] = "_%dh" % hours
        params['starttime'] = currtime - 3600*hours
        params['endtime'] = currtime
        return self.getValuePng(params)
        
    def getValuePng(self, params=None):
        """get Picture"""
        self.request.response.setHeader('Content-Type', 'image/png')
        obj = removeAllProxies(self.context)
        targetPic = str("/tmp/%s%s.png" % \
                        (str(obj.objectID), params['nameext']))
        if 1: ##fileage > 60:
            myDisplayString1 = "bit"
            myDisplayString2 = "bit"
            rrdFile = "/home/markus/tmp/%s.rrd" % str(obj.objectID)
            rrdtool.graph(
               targetPic,
               "DEF:avg0=%s:ds1:AVERAGE" % (rrdFile),
               "DEF:max0=%s:ds1:MAX" % (rrdFile),
               "CDEF:avg=avg0,%f,*" % (1.0),
               "CDEF:max=max0,%f,*" % (1.0),
               "--start=%d" % params['starttime'],
               "--end=%d" % params['endtime'],
               "--width=540",
               "--height=120",
               "--vertical-label=%s" %myDisplayString1,
               'GPRINT:avg:AVERAGE:avg\: %%lf %s' %myDisplayString2,
               'GPRINT:max:MAX:max\: %%lf %s' %myDisplayString2,
               "AREA:avg#7DD0BC:\"average\"",
               "LINE1:max#008263:\"max\"",
               "--imgformat=PNG",
               "--imginfo=<IMG SRC=\"/img/%s\" WIDTH=\"%lu\" " \
               "HEIGHT=\"%lu\" ALT=\"Demo\">")
        pic = open(targetPic, "r")
        picMem = pic.read()
        pic.close()
        return picMem
    
    def getValuePng3(self, params=None):
        """TODO: test purpose"""
        self.request.response.setHeader('Content-Type', 'image/png')
        
        fname = "c5d37d2528fc45d050c391826787b8813"
        fname2 = "%s" % self.context.objectID
        
        print "fname: %s" % fname
        print "fname2: %s" % fname2
        
        rrdFile = "/home/markus/tmp/%s.rrd" % (fname)
        targetPic = "/tmp/%s.png" % (fname)
        myDisplayString1 = "bit"
        myDisplayString2 = "bit"
        currtime = time.time()
        params = {}
        params['starttime'] = currtime - 3600*12
        params['endtime'] = currtime
        
        
        rrdtool.graph(
           targetPic,
           "DEF:avg0=%s:ds1:AVERAGE" % (rrdFile),
           "DEF:max0=%s:ds1:MAX" % (rrdFile),
           "CDEF:avg=avg0,%f,*" % (1.0),
           "CDEF:max=max0,%f,*" % (1.0),
           "--start=%d" % params['starttime'],
           "--end=%d" % params['endtime'],
           "--width=600",
           "--height=150",
           "--vertical-label=%s" %myDisplayString1,
           'GPRINT:avg:AVERAGE:avg\: %%lf %s' %myDisplayString2,
           'GPRINT:max:MAX:max\: %%lf %s' %myDisplayString2,
           "AREA:avg#009783:\"average\"",
           "LINE1:max#5020b0:\"max\"",
           "--imgformat=PNG",
           "--imginfo=<IMG SRC=\"/img/%s\" WIDTH=\"%lu\" " \
           "HEIGHT=\"%lu\" ALT=\"Demo\">")
        pic = open(targetPic, "r")
        picMem = pic.read()
        pic.close()
        return picMem

    def getValuePngHref(self):
        """Url to picture"""
        obj = removeAllProxies(self.context)
        return zapi.getPath(obj)

def getTitel(item, formatter):
    """
    Titel for Overview
    """
    if item.has_key('vendor'):
        retString = u"<a href='%s?ictvendor=%s" % \
                  (item['view'],
                   item['vendor'])
        if item.has_key('product'):
            retString += u"&ictproduct=%s" % item['product']
            if item.has_key('template'):
                retString += u"&icttemplate=%s" % item['template']
        retString += u"'>%s</a>" % item['title']
        return retString
    return u"--error--"


class AddSnmpByVendorClass(BrowserPagelet):
    columns = (
        GetterColumn(title=_('Title'),
                     getter=getTitel,
                     cell_formatter=raw_cell_formatter),
        )
    label = "aaa"
    ddd = None
    def update(self):
        self.label = "zzzz"
        if self.request.has_key('ictvendor'):
            self.ddd = self.request['ictvendor']
            #self.label = _(u"Dashboard of %s") % \
                #self.request.principal.title
        BrowserPagelet.update(self)

    def objs(self):
        """List of Content objects
        an object will be: {'title': u'title',
                            'vendor': u'quoted vendor title',
                            'product': u'quoted product title',
        """
        snmpd_utility = getUtility(IAdmUtilSnmpd)
        retList = []
        if self.request.has_key('ictvendor'):
            if self.request.has_key('ictproduct'):
                for name in snmpd_utility.mrtg_data[self.request['ictvendor']]\
                                                   [self.request['ictproduct']].keys():
                    retList.append({'title': unicode(name),
                                    'view': 'add_snmpvalue.html',
                                    'vendor': URLQuote(self.request['ictvendor']).quote(),
                                    'product': URLQuote(self.request['ictproduct']).quote(),
                                    'template': URLQuote(name).quote()})
            else:
                for name in snmpd_utility.mrtg_data[self.request['ictvendor']].keys():
                    retList.append({'title': unicode(name),
                                    'view': 'add_snmps_by_vendor.html',
                                    'vendor': URLQuote(self.request['ictvendor']).quote(),
                                    'product': URLQuote(name).quote()})
        else:
            for name in snmpd_utility.mrtg_data.keys():
                retList.append({'title': unicode(name),
                                'view': 'add_snmps_by_vendor.html',
                                'vendor': URLQuote(name).quote()})
        return retList

    def table(self):
        """ Properties of table are defined here"""
        columnList = list(self.columns)
        directlyProvides(columnList[0], ISortableColumn)
        formatter = StandaloneFullFormatter(
            self.context, self.request, self.objs(),
            columns=columnList, sort_on=((_('Title'), False),))
        formatter.cssClasses['table'] = 'listing'
        return formatter()

# --------------- forms ------------------------------------


class DetailsSnmpValueForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of net')
    fields = field.Fields(ISnmpValue).omit(*SnmpValueDetails.omit_viewfields)
    
    def update(self):
        print "--" * 30
        print self.context.oid1
        from pysnmp.entity.rfc3413.oneliner import cmdgen
        oidStringList = self.context.oid1.strip(".").split(".")
        oidIntList = [ int(i) for i in oidStringList]
        errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(
            cmdgen.CommunityData('my-agent', 'public01', 0),
            cmdgen.UdpTransportTarget(('localhost', 161)),
            tuple(oidIntList)
        )
        print "1", errorIndication
        print "2", errorStatus
        print "3", varBinds
        print "--" * 30
        DisplayForm.update(self)
        import pdb
        pdb.set_trace()


class AddSnmpValueForm(AddForm):
    """Add form."""
    label = _(u'Add SnmpValue')
    fields = field.Fields(ISnmpValue).omit(*SnmpValueDetails.omit_addfields)
    factory = SnmpValue

    def update(self):
        snmpd_utility = getUtility(IAdmUtilSnmpd)
        if self.request.has_key('ictvendor'):
            if self.request.has_key('ictproduct'):
                if self.request.has_key('icttemplate'):
                    templateData = snmpd_utility.mrtg_data[self.request['ictvendor']]\
                                                          [self.request['ictproduct']]\
                                                          [self.request['icttemplate']]
                    if templateData.has_key('oid1') and \
                       templateData.has_key('oid2'):
                        self.fields['oid1'].field.default = u"%s" % templateData['oid1']
                        self.fields['oid2'].field.default = u"%s" % templateData['oid2']
        AddForm.update(self)

class EditSnmpValueForm(EditForm):
    """ Edit for for net """
    label = _(u'SnmpValue Edit Form')
    fields = field.Fields(ISnmpValue).omit(*SnmpValueDetails.omit_editfields)


class DeleteSnmpValueForm(DeleteForm):
    """ Delete the net """
    
    def getTitel(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this net: '%s'?") % \
               IBrwsOverview(self.context).getTitle()

