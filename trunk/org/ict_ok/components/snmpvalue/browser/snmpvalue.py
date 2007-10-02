# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0232,W0142
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
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field

# ict_ok.org imports
from org.ict_ok.components.snmpvalue.interfaces import ISnmpValue
from org.ict_ok.components.snmpvalue.snmpvalue import SnmpValue
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditForm

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddSnmpValue(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add SNMP Value')
    viewURL = 'add_snmpvalue.html'
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

# --------------- forms ------------------------------------


class DetailsSnmpValueForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of net')
    fields = field.Fields(ISnmpValue).omit(*SnmpValueDetails.omit_viewfields)


class AddSnmpValueForm(AddForm):
    """Add form."""
    label = _(u'Add SnmpValue')
    fields = field.Fields(ISnmpValue).omit(*SnmpValueDetails.omit_addfields)
    factory = SnmpValue


class EditSnmpValueForm(EditForm):
    """ Edit for for net """
    label = _(u'Hello SnmpValue Edit Form')
    fields = field.Fields(ISnmpValue).omit(*SnmpValueDetails.omit_editfields)


class DeleteSnmpValueForm(DeleteForm):
    """ Delete the net """
    
    def getTitel(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this net: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


