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
"""implementation of browser class of Latency object
"""

__version__ = "$Id$"

# python imports
from tempfile import _RandomNameSequence as RandomNameSequence
from math import sqrt
import os
import time
import rrdtool

# zope imports
from zope.app import zapi
from zope.i18nmessageid import MessageFactory

# zc imports

# z3c imports
from z3c.form import field

# ict_ok.org imports
from org.ict_ok.components.latency.interfaces import ILatency
from org.ict_ok.components.latency.latency import Latency
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditForm

_ = MessageFactory('org.ict_ok')

# --------------- helper functions -------------------------

def rrd_get_stddev(rrdFile, ds, cf, start_time, end_time):
    """ from RRDhelper.pm
    """
    (realvals, names, array) = rrdtool.fetch(\
        str(rrdFile),
        str(cf),
        "--start=%d" % start_time,
        "--end=%d" % end_time)
    idx = list(names).index(ds)
    mysum = 0
    mysqsum = 0
    mycnt = 0
    for line in array:
        val = line[idx]
        if val is not None:
            mycnt += 1
            mysum += val
            mysqsum += val**2
    if mycnt > 0:
        mysqdev =  1.0 / mycnt * ( mysqsum - mysum**2 / mycnt )
        if mysqdev < 0.0:
            return 0.0
        else:
            return sqrt(mysqdev)
    else:
        return None

def rrd_get_mymax(rrdFile, start_time, end_time):
    argList = []
    argList.append("dummy")
    argList.append("--start=%d" % start_time)
    argList.append("--end=%d" % end_time)
    argList.append("DEF:maxping=%s:median:AVERAGE" % str(rrdFile))
    argList.append("PRINT:maxping:MAX:%le")
    (graphret,xs,ys) = rrdtool.graph(*argList)
    my_max = float(ys[0]) * 1.5
    return my_max

# --------------- menu entries -----------------------------

class MSubAddLatency(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add latency check')
    viewURL = 'add_latency.html'
    weight = 50

class MSubDisplayLatency(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Display latency check')
    viewURL = 'display.html'
    weight = 9

# --------------- object details ---------------------------


class LatencyDetails(ComponentDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []

    def getValuePngHref(self):
        """Url to picture"""
        obj = self.context
        return zapi.getPath(obj)

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
        if width is None:
            params['width'] = 540
        else:
            params['width'] = width
        if height is None:
            params['height'] = 120
        else:
            params['height'] = height
        return self.getValuePng(params)

    def getValuePng(self, params=None):
        """get Picture"""
        fileExt = RandomNameSequence().next()
        rrdFile = self.context.getRrdFilename()
        if not os.path.exists(rrdFile):
            return None
        targetPic = str("/tmp/%s%s_%s.png" % \
                        (str(self.context.objectID),
                         params['nameext'],
                         fileExt))
        self.request.response.setHeader('Content-Type', 'image/png')
        my_max = rrd_get_mymax(rrdFile,
                               int(params['starttime']),
                               int(params['endtime']))
        my_stddev = rrd_get_stddev(rrdFile,
                                   'median',
                                   'AVERAGE',
                                   int(params['starttime']),
                                   int(params['endtime']))
        swidth = my_max / params['height']
        argList = []
        argList.append(targetPic)
        argList.append("--start=%d" % int(params['starttime']))
        argList.append("--end=%d" % int(params['endtime']))
        argList.append("--height=%d" % params['height'])
        argList.append("--width=%d" % params['width'])
        argList.append("--rigid")
        argList.append("--upper-limit=%f" % my_max)
        argList.append("--lower-limit=0")
        argList.append("--vertical-label=Seconds")
        argList.append("--imgformat=PNG")
        argList.append("--color=SHADEA#E5FFF9")
        argList.append("--color=SHADEB#E5FFF9")
        argList.append("--color=BACK#E5FFF9")
        argList.append("--color=CANVAS#ffffff")
        argList.append("--watermark=ict-ok.org")
        for i in range(1, 21):
            argList.append("DEF:ping%d=%s:ping%d:AVERAGE" % (i, str(rrdFile), i))
        for i in range(1, 21):
            argList.append("CDEF:cp%d=ping%d,%f,LT,ping%d,INF,IF" % (i, i, my_max, i))
        argList.append("DEF:loss=%s:loss:AVERAGE" % str(rrdFile))
        argList.append("CDEF:smoke1=cp1,UN,UNKN,cp20,cp1,-,IF")
        argList.append("AREA:cp1")
        argList.append("STACK:smoke1#dddddd")
        argList.append("CDEF:smoke2=cp2,UN,UNKN,cp19,cp2,-,IF")
        argList.append("AREA:cp2")
        argList.append("STACK:smoke2#cacaca")
        argList.append("CDEF:smoke3=cp3,UN,UNKN,cp18,cp3,-,IF")
        argList.append("AREA:cp3")
        argList.append("STACK:smoke3#b7b7b7")
        argList.append("CDEF:smoke4=cp4,UN,UNKN,cp17,cp4,-,IF")
        argList.append("AREA:cp4")
        argList.append("STACK:smoke4#a4a4a4")
        argList.append("CDEF:smoke5=cp5,UN,UNKN,cp16,cp5,-,IF")
        argList.append("AREA:cp5")
        argList.append("STACK:smoke5#919191")
        argList.append("CDEF:smoke6=cp6,UN,UNKN,cp15,cp6,-,IF")
        argList.append("AREA:cp6")
        argList.append("STACK:smoke6#7e7e7e")
        argList.append("CDEF:smoke7=cp7,UN,UNKN,cp14,cp7,-,IF")
        argList.append("AREA:cp7")
        argList.append("STACK:smoke7#6b6b6b")
        argList.append("CDEF:smoke8=cp8,UN,UNKN,cp13,cp8,-,IF")
        argList.append("AREA:cp8")
        argList.append("STACK:smoke8#585858")
        argList.append("CDEF:smoke9=cp9,UN,UNKN,cp12,cp9,-,IF")
        argList.append("AREA:cp9")
        argList.append("STACK:smoke9#454545")
        argList.append("CDEF:smoke10=cp10,UN,UNKN,cp11,cp10,-,IF")
        argList.append("AREA:cp10")
        argList.append("STACK:smoke10#323232")
        argList.append("DEF:median=%s:median:AVERAGE" % str(rrdFile))
        argList.append("CDEF:ploss=loss,20,/,100,*")
        argList.append("VDEF:avmed=median,AVERAGE")
        if my_stddev is not None:
            argList.append("CDEF:mesd=median,POP,avmed,%f,/" % (my_stddev))
        argList.append("GPRINT:avmed:median rtt\:  %.1lf %ss avg")
        argList.append("GPRINT:median:MAX:%.1lf %ss max")
        argList.append("GPRINT:median:MIN:%.1lf %ss min")
        argList.append("GPRINT:median:LAST:%.1lf %ss now")
        if my_stddev is not None:
            argList.append("COMMENT:%.1f ms sd" % (1000.0 * my_stddev))
            argList.append("GPRINT:mesd:AVERAGE:%.1lf %s am/s\l")
        argList.append("LINE1:median#202020")
        argList.append("GPRINT:ploss:AVERAGE:packet loss\: %.2lf %% avg")
        argList.append("GPRINT:ploss:MAX:%.2lf %% max")
        argList.append("GPRINT:ploss:MIN:%.2lf %% min")
        argList.append("GPRINT:ploss:LAST:%.2lf %% now\l")
        argList.append("COMMENT:loss color\:")
        argList.append("CDEF:me0=loss,-1,GT,loss,0,LE,*,1,UNKN,IF,median,*")
        argList.append("CDEF:meL0=me0,%f,-" % (swidth))
        argList.append("CDEF:meH0=me0,0,*,%f,2,*,+" % (swidth))
        argList.append("AREA:meL0")
        argList.append("STACK:meH0#26ff00:0")
        argList.append("CDEF:me1=loss,0,GT,loss,1,LE,*,1,UNKN,IF,median,*")
        argList.append("CDEF:meL1=me1,%f,-" % (swidth))
        argList.append("CDEF:meH1=me1,0,*,%f,2,*,+" % (swidth))
        argList.append("AREA:meL1")
        argList.append("STACK:meH1#00b8ff:1/20")
        argList.append("CDEF:me2=loss,1,GT,loss,2,LE,*,1,UNKN,IF,median,*")
        argList.append("CDEF:meL2=me2,%f,-" % (swidth))
        argList.append("CDEF:meH2=me2,0,*,%f,2,*,+" % (swidth))
        argList.append("AREA:meL2")
        argList.append("STACK:meH2#0059ff:2/20")
        argList.append("CDEF:me3=loss,2,GT,loss,3,LE,*,1,UNKN,IF,median,*")
        argList.append("CDEF:meL3=me3,%f,-" % (swidth))
        argList.append("CDEF:meH3=me3,0,*,%f,2,*,+" % (swidth))
        argList.append("AREA:meL3")
        argList.append("STACK:meH3#5e00ff:3/20")
        argList.append("CDEF:me4=loss,3,GT,loss,4,LE,*,1,UNKN,IF,median,*")
        argList.append("CDEF:meL4=me4,%f,-" % (swidth))
        argList.append("CDEF:meH4=me4,0,*,%f,2,*,+" % (swidth))
        argList.append("AREA:meL4")
        argList.append("STACK:meH4#7e00ff:4/20")
        argList.append("CDEF:me10=loss,4,GT,loss,10,LE,*,1,UNKN,IF,median,*")
        argList.append("CDEF:meL10=me10,%f,-" % (swidth))
        argList.append("CDEF:meH10=me10,0,*,%f,2,*,+" % (swidth))
        argList.append("AREA:meL10")
        argList.append("STACK:meH10#dd00ff:10/20")
        argList.append("CDEF:me19=loss,10,GT,loss,19,LE,*,1,UNKN,IF,median,*")
        argList.append("CDEF:meL19=me19,%f,-" % (swidth))
        argList.append("CDEF:meH19=me19,0,*,%f,2,*,+" % (swidth))
        argList.append("AREA:meL19")
        argList.append("STACK:meH19#ff0000:19/20")
        argList.append("COMMENT: \l")
        argList.append("HRULE:0#000000")
        #pprint.pprint(argList)
        rrdtool.graph(*argList)
        pic = open(targetPic, "r")
        picMem = pic.read()
        pic.close()
        os.remove(targetPic)
        return picMem

class LatencyDisplay(LatencyDetails):
    """
    """
    pass

# --------------- forms ------------------------------------


class DetailsLatencyForm(DisplayForm):
    """ Display form for the object """
    label = _(u'Details of Snmp value')
    fields = field.Fields(ILatency).omit(*LatencyDetails.omit_viewfields)
    
    def update(self):
        DisplayForm.update(self)


class AddLatencyForm(AddForm):
    """Add form."""
    label = _(u'Add Latency')
    fields = field.Fields(ILatency).omit(*LatencyDetails.omit_addfields)
    factory = Latency


class EditLatencyForm(EditForm):
    """ Edit for for net """
    label = _(u'Latency Edit Form')
    fields = field.Fields(ILatency).omit(*LatencyDetails.omit_editfields)


class DeleteLatencyForm(DeleteForm):
    """ Delete the net """
    
    def getTitel(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this latency: '%s'?") % \
               IBrwsOverview(self.context).getTitle()

