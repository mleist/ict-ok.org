# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=F0401,E1101,E0611,W0612,W0232,W0201,W0142
#
"""implementation of browser class of SnmpValue object
"""

__version__ = "$Id$"

# python imports
import os
import time
from tempfile import _RandomNameSequence as RandomNameSequence
import copy
from datetime import datetime

# zope imports
from zope.app import zapi
from zope.interface import directlyProvides
from zope.component import getUtility
from zope.i18nmessageid import MessageFactory
from zope.app.pagetemplate.urlquote import URLQuote

# zc imports
from zc.table.column import GetterColumn
from zc.table.table import StandaloneFullFormatter
from zc.table.interfaces import ISortableColumn

# z3c imports
from z3c.form import field
from z3c.form.browser import checkbox
from z3c.pagelet.browser import BrowserPagelet

# ict_ok.org imports
from org.ict_ok.admin_utils.snmpd.interfaces import IAdmUtilSnmpd
from org.ict_ok.components.snmpvalue.interfaces import \
    ISnmpValue, IAddSnmpValue
from org.ict_ok.components.snmpvalue.snmpvalue import SnmpValue
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditForm, raw_cell_formatter
from org.ict_ok.components.browser.component import AddComponentForm
from org.ict_ok.components.browser.component import ImportCsvDataComponentForm
from org.ict_ok.components.browser.component import ImportXlsDataComponentForm

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
        try:
            width = int(self.request.get('width', default=None))
        except ValueError:
            width = None
        except TypeError:
            width = None
        try:
            height = int(self.request.get('height', default=None))
        except ValueError:
            height = None
        except TypeError:
            height = None
        currtime = time.time()
        params = {}
        params['nameext'] = "_%dh" % hours
        params['starttime'] = currtime - 3600*hours
        params['endtime'] = currtime
        params['width'] = width
        params['height'] = height
        return self.getValuePng(params)

    def getValuePng(self, params=None):
        """get Picture"""
        if not os.path.exists(self.context.getRrdFilename()):
            return None
        fileExt = RandomNameSequence().next()
        #obj = removeAllProxies(self.context)
        params['targetname'] = str("/tmp/%s%s_%s.png" % \
                                   (str(self.context.objectID),
                                    params['nameext'],
                                    fileExt))
        self.context.generateValuePng(params)
        self.request.response.setHeader('Content-Type', 'image/png')
        pic = open(params['targetname'], "r")
        picMem = pic.read()
        pic.close()
        os.remove(params['targetname'])
        return picMem

    def getValuePngHref(self):
        """Url to picture"""
        obj = self.context
        return zapi.getPath(obj)

    def getValues(self):
        retList = []
        valueList = self.context.getSnmpValues()
        displayUnit = self.context.getPUdisplUnitAbs()
        if displayUnit is not None and \
           valueList is not None:
            for value in valueList:
                retList.append(str(\
                    value.ounit(displayUnit.out_unit)))
        return retList
    
    def nowTS(self):
        return datetime.now()
    

class SnmpValueFolderDetails(ComponentDetails):
    """ Class for MobilePhone details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + ['requirement']
    omit_addfields = ComponentDetails.omit_addfields + ['requirement']
    omit_editfields = ComponentDetails.omit_editfields + ['requirement']
    fields = field.Fields(ISnmpValue).omit(*SnmpValueDetails.omit_viewfields)
    attrInterface = ISnmpValue


class SnmpValueDisplay(SnmpValueDetails):
    """
    """

def getTitle(item, formatter):
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
    def getTestData1(self):
        return """&title=+,{font-size: 15px}&
&x_axis_steps=1&
&y_ticks=5,10,5&
&line=3,#008263&
&values=8,9,0,7,0,1,4,18,8,9,0,7,0,1,4,18,8,9,0,7,0,1,4,18,8,9,0,7,0,1,4,18,8&
&x_labels=8,9,0,7,0,1,4,18,8,9,0,7,0,1,4,18,8,9,0,7,0,1,4,18,8,9,0,7,0,1,4,18,8&
&y_min=0&
&y_max=20&
"""
    def getTestData2(self):
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
    def getTestData3(self):
        return """&title=Sketch,{font-size:20px; color: #ffffff; margin:10px; background-color: #d070ac; padding: 5px 15px 5px 15px;}&
&x_label_style=11,#303030,2&
&x_ticks=9&
&x_axis_steps=1&
&y_label_style=11,#303030&
&y_ticks=5,10,5&
&x_labels=January,February,March,April,May,June,July,August,September,October&
&y_min=0&
&y_max=10&
&bg_colour=#FDFDFD&
&x_axis_colour=#e0e0e0&
&x_grid_colour=#e0e0e0&
&y_axis_colour=#e0e0e0&
&y_grid_colour=#e0e0e0&
&bar_sketch=55,6,#d070ac,#000000,2006,10&
&values=4,3,8,8,4,2,4,3,4,6&
"""
    def getTestData4(self):
        return """&title=Pie+Chart,{font-size:18px; color: #d01f3c}&
&x_axis_steps=1&
&y_ticks=5,10,5&
&line=3,#87421F&
&y_min=0&
&y_max=20&
&pie=60,#E4F0DB,{display:none;},1,,1&
&values=7,7,5,6,10&
&pie_labels=IE,Firefox,Opera,Wii,Other,Slashdot&
&colours=#d01f3c,#356aa0,#C79810&
&links=javascript:alert('7'),javascript:alert('7'),javascript:alert('5'),javascript:alert('6'),javascript:alert('10')&
&tool_tip=Label%3A+%23x_label%23%3Cbr%3EValue%3A+%23val%23%25%26&
"""
    
class AddSnmpByVendorClass(BrowserPagelet):
    columns = (
        GetterColumn(title=_('Title'),
                     getter=getTitle,
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


#class AddSnmpValueForm(AddForm):
#    """Add form."""
#    label = _(u'Add SnmpValue')
#    fields = field.Fields(ISnmpValue).omit(*SnmpValueDetails.omit_addfields)
#    factory = SnmpValue
#
#    def update(self):
#        snmpd_utility = getUtility(IAdmUtilSnmpd)
#        if self.request.has_key('ictvendor'):
#            if self.request.has_key('ictproduct'):
#                if self.request.has_key('icttemplate'):
#                    templateData = snmpd_utility.mrtg_data[self.request['ictvendor']]\
#                                                          [self.request['ictproduct']]\
#                                                          [self.request['icttemplate']]
#                    if templateData.has_key('oid1') and \
#                       templateData.has_key('oid2'):
#                        # must do a copy otherwise all future defaults will change
#                        self.fields = copy.deepcopy(self.fields)
#                        self.fields['inp_addrs'].field.default = \
#                            [u"%s" % templateData['oid1'],
#                             u"%s" % templateData['oid2']]
#        AddForm.update(self)
        
        
class AddSnmpValueForm(AddComponentForm):
    label = _(u'Add SnmpValue')
    addFields = field.Fields(IAddSnmpValue)
    allFields = field.Fields(ISnmpValue).omit(*SnmpValueDetails.omit_addfields)
    allFields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget
    factory = SnmpValue
    attrInterface = ISnmpValue
    _session_key = 'org.ict_ok.components.snmpvalue'


class EditSnmpValueForm(EditForm):
    """ Edit for for net """
    label = _(u'SnmpValue Edit Form')
    fields = field.Fields(ISnmpValue).omit(*SnmpValueDetails.omit_editfields)
    fields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget


class DeleteSnmpValueForm(DeleteForm):
    """ Delete the net """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this snmp value: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportCsvDataForm(ImportCsvDataComponentForm):
    pass


class ImportXlsDataForm(ImportXlsDataComponentForm):
    allFields = field.Fields(ISnmpValue)
    attrInterface = ISnmpValue
    factoryId = u'org.ict_ok.components.snmpvalue.snmpvalue.SnmpValue'
