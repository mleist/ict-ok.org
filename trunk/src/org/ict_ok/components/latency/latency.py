# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=F0401,E1101,E1102,E0611,W0703,W0612,W0142
#
"""implementation of Latency

Latency does ....

"""

__version__ = "$Id$"

# python imports
from math import sqrt
import os
import rrdtool
import time
import tempfile
from datetime import datetime

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.app import zapi
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds
from zope.app.folder import Folder

# ict_ok.org imports
from org.ict_ok.components.component import getRefAttributeNames
from org.ict_ok.version import getIkVersion
from org.ict_ok.components.superclass.superclass import Superclass
from org.ict_ok.components.component import Component, ComponentFolder
from org.ict_ok.components.interfaces import \
    IImportCsvData, IImportXlsData
from org.ict_ok.components.latency.interfaces import \
    ILatency, IAddLatency, ILatencyFolder
from org.ict_ok.admin_utils.usermanagement.usermanagement import \
     getUserTimezone

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
    (graphret, xs, ys) = rrdtool.graph(*argList)
    my_max = float(ys[0]) * 1.5
    return my_max


def AllLatencyTemplates(dummy_context):
    """Which MobilePhone templates exists
    """
    terms = []
    uidutil = getUtility(IIntIds)
    for (oid, oobj) in uidutil.items():
        if ILatency.providedBy(oobj.object) and \
        oobj.object.isTemplate:
            myString = u"%s [T]" % (oobj.object.getDcTitle())
            terms.append(SimpleTerm(oobj.object,
                                    token=getattr(oobj.object, 'objectID', oid),
                                    title=myString))
    return SimpleVocabulary(terms)



# --------------- object details ---------------------------

class Latency(Component):
    """
    the template instance
    """

    implements(ILatency)
    shortName = "value"
    # for ..Contained we have to:
    __name__ = __parent__ = None
    checkcount = FieldProperty(ILatency['checkcount'])

    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(Latency)
        for (name, value) in data.items():
            if name in ILatency.names():
                if name not in refAttributeNames:
                    setattr(self, name, value)
        self.ikRevision = __version__

    def getRefAttributeNames(self):
        return getRefAttributeNames(Latency)

    def store_refs(self, **data):
        Component.store_refs(self, **data)
        refAttributeNames = self.getRefAttributeNames()
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)
        
    def get_health(self):
        """
        output of health, 0-1 (float)
        """
        return None

    def tickerEvent(self):
        """ trigger from ticker
        """
        pass
        
    def triggerMin(self, context):
        """ got ticker event from ticker thread every minute
        """
        pass
        #filename = datetime.now().strftime('ictrpt_%Y%m%d%H%M%S.pdf')
        #f_handle, f_name = tempfile.mkstemp("iop"+filename)
        #versionStr = "[%s]" % (getIkVersion())
        #authorStr = context.principal.title
        #self.generatePdf(f_name, authorStr, versionStr)

    def getRrdFilename(self):
        """ rrd filename incl. path
        """
        data_path = zapi.getPath(self)
        return "/opt/smokeping/data/%s.rrd" % data_path

    def generateValuePng(self, params=None):
        """generate Picture
        """
        rrdFile = self.getRrdFilename()
        if not os.path.exists(rrdFile):
            return None
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
        argList.append(str(params['targetname']))
        argList.append("--start=%d" % int(params['starttime']))
        argList.append("--end=%d" % int(params['endtime']))
        argList.append("--height=%d" % params['height'])
        argList.append("--width=%d" % params['width'])
        argList.append("--rigid")
        argList.append("--upper-limit=%f" % my_max)
        argList.append("--lower-limit=0")
        argList.append("--vertical-label=Seconds")
        argList.append("--imgformat=%s" % str(params['imgtype']))
        argList.append("--color=SHADEA#E5FFF9")
        argList.append("--color=SHADEB#E5FFF9")
        argList.append("--color=BACK#E5FFF9")
        argList.append("--color=CANVAS#ffffff")
        argList.append("--watermark=ICT-OK.ORG")
        for i in range(1, 21):
            argList.append("DEF:ping%d=%s:ping%d:AVERAGE" % \
                           (i, str(rrdFile), i))
        for i in range(1, 21):
            argList.append("CDEF:cp%d=ping%d,%f,LT,ping%d,INF,IF" % \
                           (i, i, my_max, i))
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


class LatencyFolder(ComponentFolder):
    implements(ILatencyFolder, 
               IAddLatency)
    contentFactory = Latency

    def __init__(self, **data):
        """
        constructor of the object
        """
        ComponentFolder.__init__(self, **data)
