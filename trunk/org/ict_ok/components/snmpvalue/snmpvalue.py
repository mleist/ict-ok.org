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
from time import time

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

# ict_ok.org imports
from org.ict_ok.components.component import Component
from org.ict_ok.components.snmpvalue.interfaces import ISnmpValue
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

class SnmpValue(Component):
    """
    the template instance
    """

    implements(ISnmpValue)
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
        for (name, value) in data.items():
            if name in ISnmpValue.names():
                setattr(self, name, value)
        self.ikRevision = __version__
        
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
        
    def getOidList(self):
        retList = []
        for addr in self.inp_addrs:
            if self.snmpIndexType == u"oid":
                retList.append(addr)
            elif self.snmpIndexType == u"index":
                raise Exception,\
                      "index type '%s' non implemented yet for %s" % \
                      (self.snmpIndexType, self.ikName)
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
        from pysnmp.entity.rfc3413.oneliner import cmdgen
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
        convMaxPQ.ounit("1/s")
        convMax = float(convMaxPQ)
        currtime = time()
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
        currtime = time()
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
            arg_string = "%f" % time()
            for snmpVal in self.getRawSnmpValues():
                arg_string += ":%d" % int(snmpVal)
            update_args.append(arg_string)
        else:
            snmpValList = self.getRawSnmpValues()
            arg_string = "%f" % time()
            for snmpVal in self.getRawSnmpValues():
                arg_string += ":%f" % snmpVal
            update_args.append(arg_string)
        return rrdtool.updatev(*update_args)
