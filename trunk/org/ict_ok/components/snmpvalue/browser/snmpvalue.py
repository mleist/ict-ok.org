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

# python imports
import time
import rrdtool
import copy

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
    viewURL = 'add_snmpvalue.html'
    weight = 50

class MSubAddSnmpValueByVendor(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add SNMP Value (by template)')
    viewURL = 'add_snmps_by_vendor.html'
    weight = 51
    
class MSubDisplaySnmpValue(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Display SNMP Value')
    viewURL = 'display.html'
    weight = 9

class MSubTrendSnmpValue(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Trend of SNMP Value')
    viewURL = 'trend.html'
    weight = 21

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
            #rrdFile = "/home/markus/tmp/%s.rrd" % str(obj.objectID)
            rrdFile = "/opt/ict_ok.org/var/mrtg_data/127.0.0.1_2.rrd"
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
        
        #rrdFile = "/home/markus/tmp/%s.rrd" % (fname)
        rrdFile = "/opt/ict_ok.org/var/mrtg_data/127.0.0.1_2.rrd"
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
        obj = self.context # removeAllProxies(self.context)
        return zapi.getPath(obj)

    def getValue(self):
        from pysnmp.entity.rfc3413.oneliner import cmdgen
        oidStringList = self.context.oid1.strip(".").split(".")
        try:
            interfaceObj = self.context.getParent()
            interfaceIp = interfaceObj.ipv4List
            hostObj = interfaceObj.getParent()
            hostSnmpVers = hostObj.snmpVersion
            hostSnmpPort = hostObj.snmpPort
            hostSnmpReadCommunity = hostObj.snmpReadCommunity
            hostSnmpWriteCommunity = hostObj.snmpWriteCommunity
            oidIntList = [ int(i) for i in oidStringList]
            #errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(
                #cmdgen.CommunityData('my-agent', 'public01', 0),
                #cmdgen.UdpTransportTarget(('localhost', 161)),
                #tuple(oidIntList)
            #)
            #print "zuzu: ", hostSnmpVers
            errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(
                cmdgen.CommunityData('my-agent', hostSnmpReadCommunity, 0),
                cmdgen.UdpTransportTarget((interfaceIp, hostSnmpPort)),
                tuple(oidIntList)
            )
            print "1", errorIndication
            print "2", errorStatus
            print "3", varBinds
            #import pdb
            #pdb.set_trace()
            #aaa1 = self.context.convertQuantity(self.context.inpQuantity)
            #aaa2 = self.context.convertUnit(self.context.displUnitAbs)
            #aaa3 = self.context.convertUnit(self.context.displUnitVelocity)
            #aaa4 = self.context.convertUnit(self.context.displUnitAcceleration)
            #aaa5 = self.context.convertQuantity(self.context.maxQuantityAbs)
            #aaa6 = self.context.convertQuantity(self.context.maxQuantityVelocity)
            #aaa7 = self.context.convertQuantity(self.context.maxQuantityAcceleration)
            print "1111: ", self.context.getPQinpQuantity()
            print "1112: ", self.context.getPUdisplUnitAbs()
            print "1113: ", self.context.getPUdisplUnitVelocity()
            print "1114: ", self.context.getPUdisplUnitAcceleration()
            print "1115: ", self.context.getPQmaxQuantityAbs()
            print "1116: ", self.context.getPQmaxQuantityVelocity()
            print "1117: ", self.context.getPQmaxQuantityAcceleration()

            #print "--" * 30
            #print "getInputPhysical: ", self.context.getInputPhysical()
            #print "--" * 30
            #print "getMyFactor: ", self.context.getMyFactor()
            print "--" * 30
            print "tt2: ", self.context.getParent().ipv4List
            print "--" * 30
            print "tt3: ", self.context.getParent().getParent()
            print "tt3a: ", self.context.getParent().getParent().snmpVersion
            print "tt3b: ", self.context.getParent().getParent().snmpPort
            print "tt3c: ", self.context.getParent().getParent().snmpReadCommunity
            print "tt3d: ", self.context.getParent().getParent().snmpWriteCommunity

            print "--" * 30
            print varBinds[0]
            try:
                realValue = self.context.getPQinpQuantity() * \
                          float(varBinds[0][1])
                realValue.ounit(self.context.displUnitAbs)
                return realValue
                #return self.context.inpMultiplier * \
                       #self.context.getMyFactor() * \
                       #self.context.getDisplayPhysical() * \
                       #float(varBinds[0][1])
            except Exception, errText:
                return errText
        except ValueError:
            return None
        except TypeError:
            return None
        
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

class SnmpValueTrend(SnmpValueDetails):
    pass

class SnmpValueTestData(SnmpValueDetails):
    def getTestData2(self):
        return """&title=+,{font-size: 15px}&
&x_axis_steps=1&
&y_ticks=5,10,5&
&line=3,#008263&
&values=8,9,0,7,0,1,4,18,8,9,0,7,0,1,4,18,8,9,0,7,0,1,4,18,8,9,0,7,0,1,4,18,8&
&x_labels=8,9,0,7,0,1,4,18,8,9,0,7,0,1,4,18,8,9,0,7,0,1,4,18,8,9,0,7,0,1,4,18,8&
&y_min=0&
&y_max=20&
"""
    def getTestData(self):
        print "getTestData()"
        return """&title=Pie+Chart,{font-size:18px; color: #d01f3c}&
&x_axis_steps=1&
&y_ticks=5,10,5&
&line=3,#87421F&
&y_min=0&
&y_max=20&
&pie=60,#505050,{font-size: 12px; color: #404040;&
&values=13,12,6,15,8&
&pie_labels=IE,Firefox,Opera,Wii,Other&
&colours=#d01f3c,#356aa0,#C79810&
&links=&
&tool_tip=%23val%23%25&
"""
class AddSnmpByVendorClass(BrowserPagelet):
    columns = (
        GetterColumn(title=_('Title'),
                     getter=getTitel,
                     cell_formatter=raw_cell_formatter),
        )
    def update(self):
        if self.request.has_key('ictvendor'):
            if self.request.has_key('ictproduct'):
                self.label = _(u"Please select template for")
            else:
                self.label = _(u"Please select product for")
        else:
            self.label = _(u"Please select vendor")
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
    label = _(u'Details of Snmp value')
    fields = field.Fields(ISnmpValue).omit(*SnmpValueDetails.omit_viewfields)
    
    def update(self):
        print "--" * 30
        print self.context.oid1
        from pysnmp.entity.rfc3413.oneliner import cmdgen
        oidStringList = self.context.oid1.strip(".").split(".")
        try:
            oidIntList = [ int(i) for i in oidStringList]
            errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(
                cmdgen.CommunityData('my-agent', 'public01', 0),
                cmdgen.UdpTransportTarget(('localhost', 161)),
                tuple(oidIntList)
            )
            print "1", errorIndication
            if errorIndication != None:
                self.status = u"Error: SNMP connect error: '%s'" % \
                    (errorIndication)
            #import pdb
            #pdb.set_trace()
            if errorStatus != 0:
                self.status = u"Error: '%s'" % (errorStatus.prettyPrint())
            print "2", errorStatus
            #if errorStatus == 2:
                #self.status = u"Error: ddd"
            print "3", varBinds
            print "--" * 30
        except ValueError:
            self.status = u"Error: Value of OID1"
        DisplayForm.update(self)
        #import pdb
        #pdb.set_trace()


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
                        # must do a copy otherwise all future defaults will change
                        self.fields = copy.deepcopy(self.fields)
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

