# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0612,W0142
#
"""implementation of SnmpValue

SnmpValue does ....

"""

__version__ = "$Id$"

# phython imports

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

# ict_ok.org imports
from org.ict_ok.components.component import Component
from org.ict_ok.components.snmpvalue.interfaces import ISnmpValue
from org.ict_ok.libs.physicalquantity import PhysicalQuantity

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
        u'oid': u'OID',
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
        u"rel": u"Relative",
        u"relperc": u"Percent",
        }.items():
        terms.append(SimpleTerm(gkey, str(gkey), gname))
    return SimpleVocabulary(terms)

def SnmpDimensionUnits(dummy_context):
    terms = []
    for (gkey, gname) in {
        u"bit": u"bit",
        u"kbit": u"kbit",
        u"Mbit": u"Mbit",
        u"Kibit": u"Kibit",
        u"Mibit": u"Mibit",
        u"byte": u"byte",
        u"kbyte": u"kbyte",
        u"Mbyte": u"Mbyte",
        u"Kibyte": u"Kibyte",
        u"Mibyte": u"Mibyte",
        u"event": u"event",
        u"cnt": u"cnt",
        u"degC": u"degC",
        u"degF": u"degF",
        u"V": u"V",
        u"A": u"A",
        u"dA": u"dA",
        u"Hz": u"Hz",
        u"dHz": u"dHz",
        u"W": u"W",
        u"kW": u"kW",
        u"W*h": u"W*h",
        u"kW*h": u"kW*h",
        u"s": u"s",
        u"min": u"min",
        u"h": u"h",
        u"%": u"%",
        }.items():
        terms.append(SimpleTerm(gkey, str(gkey), gname))
    return SimpleVocabulary(terms)

def SnmpTimeDimensionUnits(dummy_context):
    terms = []
    for (gkey, gname) in {
        u"1": u"1",
        u"s": u"s",
        u"min": u"min",
        u"h": u"h",
        u"d": u"d",
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
    oid1 = FieldProperty(ISnmpValue['oid1'])
    oid2 = FieldProperty(ISnmpValue['oid2'])
    cmd = FieldProperty(ISnmpValue['cmd'])
    inptype = FieldProperty(ISnmpValue['inptype'])
    inpUnit = FieldProperty(ISnmpValue['inpUnit'])
    inpMultiplier = FieldProperty(ISnmpValue['inpMultiplier'])
    #displayUnitNumerator = FieldProperty(ISnmpValue['displayUnitNumerator'])
    #displayUnitDenominator = FieldProperty(ISnmpValue['displayUnitDenominator'])
    #checkMax = FieldProperty(ISnmpValue['checkMax'])
    #checkMaxLevel = FieldProperty(ISnmpValue['checkMaxLevel'])
    #checkMaxLevelUnitNumerator = FieldProperty(ISnmpValue['checkMaxLevelUnitNumerator'])
    #checkMaxLevelUnitDenominator = FieldProperty(ISnmpValue['checkMaxLevelUnitDenominator'])

    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        for (name, value) in data.items():
            if name in ISnmpValue.names():
                setattr(self, name, value)
        self.ikRevision = __version__

    def getInputPhysical(self):
        """ return inpunt physical as PhysicalQuantity
        """
        if self.inptype == "cnt":
            tmpDenominator = "s"
            inpPhys = PhysicalQuantity("1.0 %s/%s" % (str(self.inpUnit),
                                                      str(tmpDenominator)))
        elif self.inptype == "relperc":
            inpPhys = PhysicalQuantity("1.0 cnt/cnt")
        elif self.inptype == "gauge":
            if self.inpUnit == "%":
                inpPhys = PhysicalQuantity("1.0 cnt/cnt")
            else:
                inpPhys = PhysicalQuantity("1.0 %s" % (str(self.inpUnit) ))
        else:
            tmpDenominator = "1"
            inpPhys = PhysicalQuantity("1.0 %s/%s" % (str(self.inpUnit),
                                                      str(tmpDenominator)))
        return inpPhys
    
    def getDisplayPhysical(self):
        """ return display physical as PhysicalQuantity
        """
        if self.displayUnitNumerator == "%":
            displayPhys = PhysicalQuantity("1 cnt/cnt")
        else:
            if self.displayUnitDenominator == "1":
                displayPhys = PhysicalQuantity("1 %s" %
                    (str(self.displayUnitNumerator)))
            else:
                displayPhys = PhysicalQuantity("1 %s/%s" %
                    (str(self.displayUnitNumerator),
                     str(self.displayUnitDenominator)))
        return displayPhys
        
    def getMyFactor(self):
        """ factor for adaption from inpType to displayType
        """
        inpPhys = self.getInputPhysical()
        displayPhys = self.getDisplayPhysical()
        try:
            myFactor = inpPhys / displayPhys
        except:
            myFactor = inpPhys.inBaseUnits() / \
                     displayPhys.inBaseUnits()
        return myFactor

    def getSnmpValue(self):
        from pysnmp.entity.rfc3413.oneliner import cmdgen
        oidStringList = self.oid1.strip(".").split(".")
        try:
            interfaceObj = self.getParent()
            interfaceIp = interfaceObj.ipv4List
            hostObj = interfaceObj.getParent()
            hostSnmpVers = hostObj.snmpVersion
            hostSnmpPort = hostObj.snmpPort
            hostSnmpReadCommunity = hostObj.snmpReadCommunity
            hostSnmpWriteCommunity = hostObj.snmpWriteCommunity
            oidIntList = [ int(i) for i in oidStringList]
            errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(
                cmdgen.CommunityData('my-agent', hostSnmpReadCommunity, int(hostSnmpVers)),
                cmdgen.UdpTransportTarget((interfaceIp, hostSnmpPort)),
                tuple(oidIntList)
            )
            return self.inpMultiplier * \
                   self.getMyFactor() * \
                   self.getDisplayPhysical() * \
                   float(varBinds[0][1])
        except:
            return None

    def tickerEvent(self):
        pass
        #print "iiiiiiiiiiiiiiiiiiiiiiiii: ", self.getSnmpValue()