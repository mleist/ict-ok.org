# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=F0401,E1101,E0611,W0703,W0612,W0142
#
"""implementation of SnmpValue

SnmpValue does ....

"""

__version__ = "$Id$"

# python imports
import os
import rrdtool
import time
from pysnmp.entity.rfc3413.oneliner import cmdgen

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds
from zope.app.folder import Folder

# ict_ok.org imports
from org.ict_ok.libs.lib import getRefAttributeNames
from org.ict_ok.components.component import Component
from org.ict_ok.components.superclass.superclass import Superclass
from org.ict_ok.components.snmpvalue.interfaces import \
    ISnmpValue, IAddSnmpValue, ISnmpValueFolder
from org.ict_ok.components.interfaces import \
    IImportCsvData, IImportXlsData
from org.ict_ok.libs.physicalquantity import convertQuantity, \
     convertUnit

def SnmpVersions(dummy_context):
    terms = []
    for (gkey, gname) in {
        u"0": u"V1",
        u"1": u"V2c",
        }.items():
        terms.append(SimpleTerm(gkey, str(gkey), gname))
    return SimpleVocabulary(terms)

def SnmpCheckTypes(dummy_context):
    """In which production state a host may be
    """
    terms = []
    for (gkey, gname) in {
        u'address': u'SNMP address',
        u'cmd': u'Command',
        }.items():
        terms.append(SimpleTerm(gkey, str(gkey), gname))
    return SimpleVocabulary(terms)

def SnmpCheckCmds(dummy_context):
    terms = []
    for (gkey, gname) in {
        u"none": u"None",
        }.items():
        terms.append(SimpleTerm(gkey, str(gkey), gname))
    return SimpleVocabulary(terms)

def SnmpInpTypes(dummy_context):
    terms = []
    for (gkey, gname) in {
        u"cnt": u"Counter",
        u"gauge": u"Gauge",
        #u"rel": u"Relative",
        #u"relperc": u"Percent",
        }.items():
        terms.append(SimpleTerm(gkey, str(gkey), gname))
    return SimpleVocabulary(terms)

def SnmpIndexTypes(dummy_context):
    """what is used to retrieve same ports after rebooting the device
    """
    terms = []
    for (gkey, gname) in {
        u"oid": u"SNMP OID",
        u"index": u"Interface index",
        #u"ip": u"IP address",
        u"mac": u"Ethernet address",
        u"desc": u"Description",
        u"name": u"Name",
        }.items():
        terms.append(SimpleTerm(gkey, str(gkey), gname))
    return SimpleVocabulary(terms)

def AllSnmpValueTemplates(dummy_context):
    """Which SnmpValue templates exists
    """
    terms = []
    uidutil = getUtility(IIntIds)
    for (oid, oobj) in uidutil.items():
        if ISnmpValue.providedBy(oobj.object) and \
        oobj.object.isTemplate:
            myString = u"%s [T]" % (oobj.object.getDcTitle())
            terms.append(SimpleTerm(oobj.object,
                                    token=oid,
                                    title=myString))
    return SimpleVocabulary(terms)


class SnmpValue(Component):
    """
    the template instance
    """

    implements(ISnmpValue)
    shortName = "value"
    # for ..Contained we have to:
    __name__ = __parent__ = None
    checktype = FieldProperty(ISnmpValue['checktype'])
    snmpIndexType = FieldProperty(ISnmpValue['snmpIndexType'])
    inp_addrs = FieldProperty(ISnmpValue['inp_addrs'])
    cmd = FieldProperty(ISnmpValue['cmd'])
    inptype = FieldProperty(ISnmpValue['inptype'])
    displayMinMax = FieldProperty(ISnmpValue['displayMinMax'])
    checkMax = FieldProperty(ISnmpValue['checkMax'])
    inpQuantity = FieldProperty(ISnmpValue['inpQuantity'])
    displUnitAbs = FieldProperty(\
        ISnmpValue['displUnitAbs'])
    displUnitVelocity = FieldProperty(\
        ISnmpValue['displUnitVelocity'])
    displUnitAcceleration = FieldProperty(\
        ISnmpValue['displUnitAcceleration'])
    minQuantityAbs = FieldProperty(\
        ISnmpValue['minQuantityAbs'])
    minQuantityVelocity = FieldProperty(\
        ISnmpValue['minQuantityVelocity'])
    minQuantityAcceleration = FieldProperty(\
        ISnmpValue['minQuantityAcceleration'])
    maxQuantityAbs = FieldProperty(\
        ISnmpValue['maxQuantityAbs'])
    maxQuantityVelocity = FieldProperty(\
        ISnmpValue['maxQuantityVelocity'])
    maxQuantityAcceleration = FieldProperty(\
        ISnmpValue['maxQuantityAcceleration'])

    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(SnmpValue)
        for (name, value) in data.items():
            if name in ISnmpValue.names():
                if name not in refAttributeNames:
                    setattr(self, name, value)
        self.ikRevision = __version__
        self.snmpIndexDict = None
        self.snmpIndexDictTimeStamp = 0.0

    def getRefAttributeNames(self):
        return getRefAttributeNames(SnmpValue)

    def store_refs(self, **data):
        Component.store_refs(self, **data)
        refAttributeNames = self.getRefAttributeNames()
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)
        
    def get_health(self):
        overQuota =  self.overMaxQuota()
        underQuota = self.underMinQuota()
        if overQuota is not None and \
           overQuota > 0.05: # 5 %
            if underQuota is not None and \
               underQuota > 0.1: # 10 %
                return 1.0 - (overQuota * 6 + underQuota * 3) / 9
            else:
                return 1.0 - overQuota
        else:
            if underQuota is not None and \
               underQuota > 0.1: # 10 %
                return 1.0 - underQuota
            else:
                return None
        return None

    def getOidFromIndexType(self):
        if self.snmpIndexType == u"":
            pass
        elif self.snmpIndexType == u"":
            pass
        else:
            pass
        
    def getIndexDict(self):
        """ get the interface table index in form of:
        { integer index: internal snmp index position, ... }
        """
        if not self.snmpIndexType == u"index":
            return None
        nowTS = time.mktime(time.gmtime())
        if nowTS > self.snmpIndexDictTimeStamp + 1800.0: # Cache update
            self.snmpIndexDictTimeStamp = nowTS
            if self.snmpIndexDict is None:
                self.snmpIndexDict = {}
            else:
                self.snmpIndexDict.clear()
            interfaceObj = self.getParent()
            if len(interfaceObj.ipv4List) > 0:
                interfaceIp = interfaceObj.ipv4List[0]
            else:
                return None
            hostObj = interfaceObj.getParent()
            hostSnmpVers = hostObj.snmpVersion
            hostSnmpPort = hostObj.snmpPort
            hostSnmpReadCommunity = hostObj.snmpReadCommunity
            hostSnmpWriteCommunity = hostObj.snmpWriteCommunity
            oidIntList = [1,3,6,1,2,1,2,2,1,1] # IfIndex Table
            errorIndication, errorStatus, errorIndex, varBinds = \
                           cmdgen.CommandGenerator().nextCmd(
                               cmdgen.CommunityData('my-agent', 
                                                    hostSnmpReadCommunity,
                                                    int(hostSnmpVers)),
                               cmdgen.UdpTransportTarget((interfaceIp, 
                                                          hostSnmpPort)),
                               tuple(oidIntList)
                           )
            if len(varBinds) > 0:
                for pos in varBinds:
                    (snmpOid, snmpVal) = pos[0]
                    # get last number of SNMP oid
                    self.snmpIndexDict[int(snmpVal)] = \
                        int(snmpOid.prettyPrint().split(".")[-1])
        return self.snmpIndexDict
    
    def getOidList(self):
        """ return a converted snmp oid list
        e.g. interface index is translated into snmp oid
        """
        retList = []
        for addr in self.inp_addrs:
            if self.snmpIndexType == u"oid":
                retList.append(addr)
            elif self.snmpIndexType == u"index":
                indexDict = self.getIndexDict()
                retList.append(u"1.3.6.1.2.1.2.2.1.10.%d" % indexDict[int(addr)])
                retList.append(u"1.3.6.1.2.1.2.2.1.16.%d" % indexDict[int(addr)])
            elif self.snmpIndexType == u"mac":
                raise Exception,\
                      "index type '%s' non implemented yet for %s" % \
                      (self.snmpIndexType, self.ikName)
            elif self.snmpIndexType == u"desc":
                raise Exception,\
                      "index type '%s' non implemented yet for %s" % \
                      (self.snmpIndexType, self.ikName)
            elif self.snmpIndexType == u"name":
                raise Exception,\
                      "index type '%s' non implemented yet for %s" % \
                      (self.snmpIndexType, self.ikName)
            else:
                retList.append(addr)
        return retList

    def getDisplayUnit(self):
        """get unit tuple (displUnit, displayString)
        """
        displUnit = None
        displayString = None
        if self.inptype == u"cnt":
            if self.displUnitVelocity is not None:
                displUnit = convertUnit(self.displUnitVelocity)
                displayString = str(self.displUnitVelocity)
        elif self.inptype == u"gauge":
            if self.displUnitAbs is not None:
                displUnit = convertUnit(self.displUnitAbs)
                displayString = str(self.displUnitAbs)
        else:
            if self.displUnitVelocity is not None:
                displUnit = convertUnit(self.displUnitVelocity)
                displayString = str(self.displUnitVelocity)
        return (displUnit, displayString)

    def getMinQuantity(self):
        """get unit tuple (minQuantity, minString)
        """
        minQuantity = None
        minString = None
        if self.inptype == u"cnt":
            if self.minQuantityVelocity is not None:
                minQuantity = convertQuantity(self.minQuantityVelocity)
                minString = str(self.minQuantityVelocity)
        elif self.inptype == u"gauge":
            if self.minQuantityAbs is not None:
                minQuantity = convertQuantity(self.minQuantityAbs)
                minString = str(self.minQuantityAbs)
        else:
            if self.minQuantityVelocity is not None:
                minQuantity = convertQuantity(self.minQuantityVelocity)
                minString = str(self.minQuantityVelocity)
        return (minQuantity, minString)

    def getMaxQuantity(self):
        """get unit tuple (maxQuantity, maxString)
        """
        maxQuantity = None
        maxString = None
        if self.inptype == u"cnt":
            if self.maxQuantityVelocity is not None:
                maxQuantity = convertQuantity(self.maxQuantityVelocity)
                maxString = str(self.maxQuantityVelocity)
        elif self.inptype == u"gauge":
            if self.maxQuantityAbs is not None:
                maxQuantity = convertQuantity(self.maxQuantityAbs)
                maxString = str(self.maxQuantityAbs)
        else:
            if self.maxQuantityVelocity is not None:
                maxQuantity = convertQuantity(self.maxQuantityVelocity)
                maxString = str(self.maxQuantityVelocity)
        return (maxQuantity, maxString)

    def getRawSnmpValues(self):
        """ get raw snmp-Value without multiplier
        """
        retList = []
        for oid in self.getOidList():
            oidStringList = oid.strip(".").split(".")
            try:
                interfaceObj = self.getParent()
                if len(interfaceObj.ipv4List) > 0:
                    interfaceIp = interfaceObj.ipv4List[0]
                else:
                    return None
                hostObj = interfaceObj.getParent()
                hostSnmpVers = hostObj.snmpVersion
                hostSnmpPort = hostObj.snmpPort
                hostSnmpReadCommunity = hostObj.snmpReadCommunity
                hostSnmpWriteCommunity = hostObj.snmpWriteCommunity
                oidIntList = [ int(i) for i in oidStringList]
                errorIndication, errorStatus, errorIndex, varBinds = \
                               cmdgen.CommandGenerator().getCmd(
                                   cmdgen.CommunityData('my-agent', 
                                                        hostSnmpReadCommunity,
                                                        int(hostSnmpVers)),
                                   cmdgen.UdpTransportTarget((interfaceIp, 
                                                              hostSnmpPort)),
                                   tuple(oidIntList)
                               )
                if len(varBinds) > 0:
                    retList.append(float(varBinds[0][1]))
                else:
                    return None
            except Exception, errText:
                print "getRawSnmpValues-Error: ", errText
                return None
        return retList

    def getSnmpValues(self):
        """ get SnmpValue as physical value
        """
        retList = []
        try:
            for rawVal in self.getRawSnmpValues():
                retVal = self.getPQinpQuantity() * rawVal
                inpUnit = self.getPQinpQuantity().out_unit
                retVal.ounit(inpUnit)
                retList.append(retVal)
        except Exception, errText:
            print "getSnmpValues-Error: ", errText
            return None
        return retList

    def overMaxQuota(self, diffString="24h"):
        """ physical values over max in float 0..1
        """
        if not os.path.exists(self.getRrdFilename()):
            self.rrd_create()
            return None
        retFloat = 0.0
        # >>> tt1 = (convertQuantity("325 W") / convertQuantity("3600 s")) *\
        #           (convertQuantity("3600 s") / convertQuantity("0.5 W h"))
        # >>> print tt1
        # 0.1806 1 / s 
        inpPQ = self.getPQinpQuantity()
        (maxQuantity, maxString) = self.getMaxQuantity()
        if maxQuantity is None:
            return None
        convMaxPQ = maxQuantity / inpPQ
        # TODO error on abs. Counter
        convMaxPQ.ounit("1/s")
        convMax = float(convMaxPQ)
        currtime = time.time()
        rrdRet = rrdtool.fetch(\
            self.getRrdFilename(),
            "MAX",
            "--start=%d-%s" % (currtime, diffString),
            "--end=%d" % currtime
        )
        rrdTimeTup, rrdVarTup, rrdValList = rrdRet
        nbrPoints = 0
        nbrOverMax = 0
        for vals in rrdValList:
            for dim in range(len(vals)):
                if vals[dim] is not None:
                    nbrPoints += 1
                    if vals[dim] > convMax:
                        nbrOverMax += 1
        if nbrPoints > 0:
            retFloat = float(nbrOverMax) / float(nbrPoints)
        return retFloat

    def underMinQuota(self, diffString="24h"):
        """ physical values over max in float 0..1
        """
        if not os.path.exists(self.getRrdFilename()):
            self.rrd_create()
            return None
        retFloat = 0.0
        inpPQ = self.getPQinpQuantity()
        (minQuantity, minString) = self.getMinQuantity()
        if minQuantity is None:
            return None
        convMinPQ = minQuantity / inpPQ
        convMinPQ.ounit("1/s")
        convMin = float(convMinPQ)
        currtime = time.time()
        rrdRet = rrdtool.fetch(\
            self.getRrdFilename(),
            "MIN",
            "--start=%d-%s" % (currtime, diffString),
            "--end=%d" % currtime
        )
        rrdTimeTup, rrdVarTup, rrdValList = rrdRet
        nbrPoints = 0
        nbrUnderMin = 0
        for vals in rrdValList:
            for dim in range(len(vals)):
                if vals[dim] is not None:
                    nbrPoints += 1
                    if vals[dim] < convMin:
                        nbrUnderMin += 1
        if nbrPoints > 0:
            retFloat = float(nbrUnderMin) / float(nbrPoints)
        return retFloat
    
    def tickerEvent(self):
        """ trigger from ticker
        """
        pass
        
    def triggerMin(self):
        """ got ticker event from ticker thread every minute
        """
        try:
            self.rrd_update()
        except:
            pass

    def getPQinpQuantity(self):
        return convertQuantity(self.inpQuantity)

    def getPUdisplUnitAbs(self):
        return convertUnit(self.displUnitAbs)

    def getPUdisplUnitVelocity(self):
        return convertUnit(self.displUnitVelocity)

    def getPUdisplUnitAcceleration(self):
        return convertUnit(self.displUnitAcceleration)

    def getPQmaxQuantityAbs(self):
        return convertQuantity(self.maxQuantityAbs)

    def getPQmaxQuantityVelocity(self):
        return convertQuantity(self.maxQuantityVelocity)

    def getPQmaxQuantityAcceleration(self):
        return convertQuantity(self.maxQuantityAcceleration)

    def getRrdFilename(self):
        """ rrd filename incl. path
        """
        return "/opt/ict_ok.org/var/mrtg_data/%s.rrd" % \
               str(self.getObjectId())

    def rrd_create(self, interval=1):
        if not os.path.exists(self.getRrdFilename()):
            try:
                converted_addrs = self.getOidList()
                print "converted_addrs: ", converted_addrs
                rows = int(4000 / interval)
                minhb = interval * 60 * 2
                if minhb <600:
                    minhb = 600
                if True: #absi == 0:
                    absi = 'U'
                if True: #abso == 0:
                    abso = 'U'
                dstype = {
                    'u': 'COUNTER',
                    'a': 'ABSOLUTE',
                    'g': 'GAUGE',
                    'h': 'COUNTER',
                    'm': 'COUNTER',
                    'd': 'DERIVE',
                    "cnt": 'COUNTER',
                    "gauge": 'GAUGE',
                }
                try:
                    up_abs = dstype[self.inptype]
                except KeyError:
                    up_abs = 'COUNTER'
                
                # config values
                rrd_conf = {
                    'up_abs': up_abs,
                    'minhb': minhb,
                    'absi': absi,
                    'abso': abso,
                    'rows': rows,
                    'interval': interval,
                    'interval30': 30 / interval,
                    'interval120': 120 / interval,
                    'interval1440': 1440 / interval,
                    'interval7200': 7200 / interval,
                    }
                
                #create the list of create arguments
                create_args = []
                
                #the rrd target file
                create_args.append(self.getRrdFilename())
                
                create_args.append('-s %d' % (interval * 60))
                
                # datasources
                for (ds_nr, ds_oid) in enumerate(converted_addrs):
                    create_args.append(\
                        "DS:ds%02d" % ds_nr + \
                        ":%(up_abs)s:%(minhb)s:0:%(absi)s" % rrd_conf)
                #create_args.append(\
                    #"DS:ds1:GAUGE:%(minhb)s:0:U" % rrd_conf)
                #create_args.append(\
                    #"DS:ds1:%(up_abs)s:%(minhb)s:0:%(abso)s" % rrd_conf)
                
                # round robin archives
                create_args.append(\
                    "RRA:AVERAGE:0.5:1:%(rows)s" % rrd_conf)
                if interval < 30:
                    create_args.append(\
                        "RRA:AVERAGE:0.5:%(interval30)d:800" % rrd_conf)
                create_args.append(\
                    "RRA:AVERAGE:0.5:%(interval120)d:800" % rrd_conf)
                create_args.append(\
                    "RRA:AVERAGE:0.5:%(interval1440)d:800" % rrd_conf)
                create_args.append(\
                    "RRA:AVERAGE:0.5:%(interval7200)d:800" % rrd_conf)
                
                create_args.append("RRA:MIN:0.5:1:%(rows)d" % rrd_conf)
                if interval < 30:
                    create_args.append(\
                        "RRA:MIN:0.5:%(interval30)d:800" % rrd_conf)
                create_args.append(\
                    "RRA:MIN:0.5:%(interval120)d:800" % rrd_conf)
                create_args.append(\
                    "RRA:MIN:0.5:%(interval1440)d:800" % rrd_conf)
                create_args.append(\
                    "RRA:MIN:0.5:%(interval7200)d:800" % rrd_conf)
                
                create_args.append(\
                    "RRA:MAX:0.5:1:%(rows)d" % rrd_conf)
                if interval < 30:
                    create_args.append(\
                        "RRA:MAX:0.5:%(interval30)d:800" % rrd_conf)
                create_args.append(\
                    "RRA:MAX:0.5:%(interval120)d:800" % rrd_conf)
                create_args.append(\
                    "RRA:MAX:0.5:%(interval1440)d:800" % rrd_conf)
                create_args.append(\
                    "RRA:MAX:0.5:%(interval7200)d:800" % rrd_conf)
                rrdtool.create(*create_args)
            except Exception, errText:
                print "Exception: %s" % errText


    def rrd_update(self):
        if not os.path.exists(self.getRrdFilename()):
            self.rrd_create()
        #create the list of update arguments
        update_args = []
        
        #the rrd target file
        update_args.append(self.getRrdFilename())
        # magnitude quantities with "%f"-formatstring will only
        # result in the value
        if self.inptype == "cnt":
            snmpValList = self.getRawSnmpValues()
            arg_string = "%f" % time.time()
            for snmpVal in self.getRawSnmpValues():
                arg_string += ":%d" % int(snmpVal)
            update_args.append(arg_string)
        else:
            snmpValList = self.getRawSnmpValues()
            arg_string = "%f" % time.time()
            for snmpVal in self.getRawSnmpValues():
                arg_string += ":%f" % snmpVal
            update_args.append(arg_string)
        return rrdtool.updatev(*update_args)

    def rrdConfigureDefs(self, argList, rrdFile):
        converted_addrs = self.getOidList()
        for (ds_nr, ds_oid) in enumerate(converted_addrs):
            argList.append("DEF:f_avg%02d=%s:ds%02d:AVERAGE" % \
                           (ds_nr, rrdFile, ds_nr))
            if self.displayMinMax:
                argList.append("DEF:f_max%02d=%s:ds%02d:MAX" % \
                               (ds_nr, rrdFile, ds_nr))
                argList.append("DEF:f_min%02d=%s:ds%02d:MIN" % \
                               (ds_nr, rrdFile, ds_nr))

    def rrdConfigureCDefs(self, argList, arg_multiplier):
        converted_addrs = self.getOidList()
        for (ds_nr, ds_oid) in enumerate(converted_addrs):
            multiplier = arg_multiplier
            argList.append("CDEF:avg%02d=f_avg%02d,%f,*" % \
                           (ds_nr, ds_nr, multiplier))
            if self.displayMinMax:
                argList.append("CDEF:max%02d=f_max%02d,%f,*" % \
                               (ds_nr, ds_nr, multiplier))
                argList.append("CDEF:min%02d=f_min%02d,%f,*" % \
                               (ds_nr, ds_nr, multiplier))

    def rrdConfigureCDefsIndex(self, argList, arg_multiplier):
        converted_addrs = self.getOidList()
        for (ds_nr, ds_oid) in enumerate(converted_addrs):
            if ds_nr % 2 == 0: # odd / even
                multiplier = arg_multiplier
            else:
                multiplier = -1.0 * arg_multiplier
            argList.append("CDEF:avg%02d=f_avg%02d,%f,*" % \
                           (ds_nr, ds_nr, multiplier))
            if self.displayMinMax:
                argList.append("CDEF:max%02d=f_max%02d,%f,*" % \
                               (ds_nr, ds_nr, multiplier))
                argList.append("CDEF:min%02d=f_min%02d,%f,*" % \
                               (ds_nr, ds_nr, multiplier))

    def rrdConfigureMinimum(self, argList):
        (displUnit, displayString) = self.getDisplayUnit()
        (minQuantity, minString) = self.getMinQuantity()
        if minQuantity is not None:
            converted_addrs = self.getOidList()
            myMinValue = float(minQuantity / displUnit)
            for (ds_nr, ds_oid) in enumerate(converted_addrs):
                argList.append("CDEF:ulimitmin%02d=avg%02d,%f,LT,avg%02d,0,IF" % \
                               (ds_nr, ds_nr, myMinValue, ds_nr))
            argList.append("HRULE:%f#FFFF0080" % (myMinValue))

    def rrdConfigureMinimumIndex(self, argList):
        (displUnit, displayString) = self.getDisplayUnit()
        (minQuantity, minString) = self.getMinQuantity()
        if minQuantity is not None:
            converted_addrs = self.getOidList()
            for (ds_nr, ds_oid) in enumerate(converted_addrs):
                if ds_nr % 2 == 0: # odd / even
                    myMinValue = float(minQuantity / displUnit)
                    argList.append("CDEF:ulimitmin%02d=avg%02d,%f,LT,avg%02d,0,IF" % \
                                   (ds_nr, ds_nr, myMinValue, ds_nr))
                else:
                    myMinValue = -1.0 * float(minQuantity / displUnit)
                    argList.append("CDEF:ulimitmin%02d=avg%02d,%f,GT,avg%02d,0,IF" % \
                                   (ds_nr, ds_nr, myMinValue, ds_nr))
                argList.append("HRULE:%f#FFFF0080" % (myMinValue))

    def rrdConfigureMaximum(self, argList):
        (displUnit, displayString) = self.getDisplayUnit()
        (maxQuantity, maxString) = self.getMaxQuantity()
        if maxQuantity is not None:
            myMaxValue = float(maxQuantity / displUnit)
            converted_addrs = self.getOidList()
            for (ds_nr, ds_oid) in enumerate(converted_addrs):
                argList.append("CDEF:limitmax%02d=avg%02d,%f,GT,%f,0,IF" % \
                               (ds_nr, ds_nr, myMaxValue, myMaxValue))
                argList.append("CDEF:olimitmax%02d=avg%02d,%f,GT,avg%02d,%f,-,0,IF" % \
                               (ds_nr, ds_nr, myMaxValue, ds_nr, myMaxValue))
                argList.append("CDEF:ulimitmax%02d=avg%02d,%f,GT,0,avg%02d,IF" % \
                               (ds_nr, ds_nr, myMaxValue, ds_nr))
            argList.append("HRULE:%f#FF000080" % (myMaxValue))

    def rrdConfigureMaximumIndex(self, argList):
        (displUnit, displayString) = self.getDisplayUnit()
        (maxQuantity, maxString) = self.getMaxQuantity()
        if maxQuantity is not None:
            converted_addrs = self.getOidList()
            for (ds_nr, ds_oid) in enumerate(converted_addrs):
                if ds_nr % 2 == 0: # odd / even
                    myMaxValue = float(maxQuantity / displUnit)
                    argList.append("CDEF:limitmax%02d=avg%02d,%f,GT,%f,0,IF" % \
                                   (ds_nr, ds_nr, myMaxValue, myMaxValue))
                    argList.append("CDEF:olimitmax%02d=avg%02d,%f,GT,avg%02d,%f,-,0,IF" % \
                                   (ds_nr, ds_nr, myMaxValue, ds_nr, myMaxValue))
                    argList.append("CDEF:ulimitmax%02d=avg%02d,%f,GT,0,avg%02d,IF" % \
                                   (ds_nr, ds_nr, myMaxValue, ds_nr))
                else:
                    myMaxValue = -1.0 * float(maxQuantity / displUnit)
                    argList.append("CDEF:limitmax%02d=avg%02d,%f,LT,%f,0,IF" % \
                                   (ds_nr, ds_nr, myMaxValue, myMaxValue))
                    argList.append("CDEF:olimitmax%02d=avg%02d,%f,LT,avg%02d,%f,-,0,IF" % \
                                   (ds_nr, ds_nr, myMaxValue, ds_nr, myMaxValue))
                    argList.append("CDEF:ulimitmax%02d=avg%02d,%f,LT,0,avg%02d,IF" % \
                                   (ds_nr, ds_nr, myMaxValue, ds_nr))
                argList.append("HRULE:%f#FF000080" % (myMaxValue))

    def rrdConfigureLegend(self, argList):
        (displUnit, displayString) = self.getDisplayUnit()
        converted_addrs = self.getOidList()
        for (ds_nr, ds_oid) in enumerate(converted_addrs):
            argList.append(\
                'GPRINT:avg%02d:AVERAGE:avg%02d\: %%6.2lf %s' % \
                (ds_nr, ds_nr, displayString))
        if self.displayMinMax:
            argList.append(\
                'GPRINT:max00:MAX:max00\: %%6.2lf %s' % displayString)
            argList.append(\
                'GPRINT:min00:MIN:min00\: %%6.2lf %s' % displayString)

    def rrdConfigureGraphs(self, argList):
        (minQuantity, minString) = self.getMinQuantity()
        (maxQuantity, maxString) = self.getMaxQuantity()
        if minQuantity is not None:
            if maxQuantity is not None: # min and max are valid
                argList.append("AREA:ulimitmax00#008263")
                argList.append("AREA:limitmax00#E07771")
                argList.append("STACK:olimitmax00#FF0000")
                argList.append("AREA:ulimitmin00#CFD138")
            else: # only min is valid
                argList.append("AREA:avg00#7DD0BC:\"average 00\"")
                argList.append("AREA:ulimitmin00#CFD138")
        else:
            if maxQuantity is not None: # only max are valid
                argList.append("AREA:ulimitmax00#008263")
                argList.append("AREA:limitmax00#E07771")
                argList.append("STACK:olimitmax00#FF0000")
            else: # neither min nor max are valid
                argList.append("AREA:avg00#7DD0BC:\"average 00\"")
                #argList.append("STACK:avg01#008263:\"average 01\"")
        if self.displayMinMax:
            argList.append("LINE1:max00#008263:\"max00\"")

    def rrdConfigureGraphsIndex(self, argList):
        (minQuantity, minString) = self.getMinQuantity()
        (maxQuantity, maxString) = self.getMaxQuantity()
        if minQuantity is not None:
            if maxQuantity is not None: # min and max are valid
                argList.append("AREA:ulimitmax00#008263")
                argList.append("AREA:limitmax00#E07771")
                argList.append("STACK:olimitmax00#FF0000")
                argList.append("AREA:ulimitmin00#CFD138")
                argList.append("AREA:ulimitmax01#008263")
                argList.append("AREA:limitmax01#E07771")
                argList.append("STACK:olimitmax01#FF0000")
                argList.append("AREA:ulimitmin01#CFD138")
            else: # only min is valid
                argList.append("AREA:avg00#7DD0BC:\"average 00\"")
                argList.append("AREA:ulimitmin00#CFD138")
                argList.append("AREA:avg01#7DD0BC:\"average 01\"")
                argList.append("AREA:ulimitmin01#CFD138")
        else:
            if maxQuantity is not None: # only max are valid
                argList.append("AREA:ulimitmax00#008263")
                argList.append("AREA:limitmax00#E07771")
                argList.append("STACK:olimitmax00#FF0000")
                argList.append("AREA:ulimitmax01#008263")
                argList.append("AREA:limitmax01#E07771")
                argList.append("STACK:olimitmax01#FF0000")
            else: # neither min nor max are valid
                argList.append("LINE1:avg00#7DD0BC:\"average 00\"")
                argList.append("LINE1:avg01#008263:\"average 01\"")
        argList.append("HRULE:0.0#00000080")
        if self.displayMinMax:
            argList.append("LINE1:max00#008263:\"max00\"")

    def generateValuePng(self, params=None):
        """generate Picture
        """
        rrdFile = self.getRrdFilename()
        if not os.path.exists(self.getRrdFilename()):
            return None
        unitInRrd = convertQuantity(self.inpQuantity) \
                  / convertQuantity("1.0 s")
        (displUnit, displayString) = self.getDisplayUnit()
        (minQuantity, minString) = self.getMinQuantity()
        (maxQuantity, maxString) = self.getMaxQuantity()
        if unitInRrd is not None and \
           displUnit is not None:
            multiplier = float(unitInRrd / displUnit)
        else:
            multiplier = 1.0
        if 1: ##fileage > 60:
            rrdFile = self.getRrdFilename()
            argList = []
            argList.append(params['targetname'])
            # Defs
            self.rrdConfigureDefs(argList, rrdFile)
            # CDefs
            if self.snmpIndexType == u"index":
                self.rrdConfigureCDefsIndex(argList, multiplier)
            else:
                self.rrdConfigureCDefs(argList, multiplier)
            # Minimum settings
            if self.snmpIndexType == u"index":
                self.rrdConfigureMinimumIndex(argList)
            else:
                self.rrdConfigureMinimum(argList)
            # Maximum settings
            if self.snmpIndexType == u"index":
                self.rrdConfigureMaximumIndex(argList)
            else:
                self.rrdConfigureMaximum(argList)
            argList.append("--start=%d" % params['starttime'])
            argList.append("--end=%d" % params['endtime'])
            try:
                if params['width'] is not None:
                    argList.append("--width=%d" % int(params['width']))
                else:
                    argList.append("--width=540")
            except ValueError:
                argList.append("--width=540")
            try:
                if params['height'] is not None:
                    argList.append("--height=%d" % int(params['height']))
                else:
                    argList.append("--height=120")
            except ValueError:
                argList.append("--height=120")
            argList.append("--color=SHADEA#E5FFF9")
            argList.append("--color=SHADEB#E5FFF9")
            argList.append("--color=BACK#E5FFF9")
            argList.append("--color=CANVAS#ffffff")
            argList.append("--watermark=ICT-OK.ORG")
            argList.append("--vertical-label=%s" % displayString)
            # Legend
            self.rrdConfigureLegend(argList)
            # Graph
            if self.snmpIndexType == u"index":
                self.rrdConfigureGraphsIndex(argList)
            else:
                self.rrdConfigureGraphs(argList)
            argList.append("--imgformat=PNG")
            argList.append("--imginfo=<IMG SRC=\"/img/%s\" WIDTH=\"%lu\" " \
                           "HEIGHT=\"%lu\" ALT=\"Demo\">")
            #print "argList: ", argList
            rrdtool.graph(*argList)


class SnmpValueFolder(Superclass, Folder):
    implements(ISnmpValueFolder, 
               IImportCsvData,
               IImportXlsData,
               IAddSnmpValue)
    def __init__(self, **data):
        """
        constructor of the object
        """
        Superclass.__init__(self, **data)
        Folder.__init__(self)
