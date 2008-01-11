# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0611
#
"""Adapter implementation of snmp-methods
"""

__version__ = "$Id$"

# phython imports

# zope imports
from zope.interface import implements
from zope.component import adapts

# ict_ok.org imports
from org.ict_ok.admin_utils.snmpd.interfaces import ISnmptrapd
from org.ict_ok.components.host.adapter.snmp import Snmptrapd as BaseSnmptrapd
from org.ict_ok.components.host.special.mge_ups.interfaces import IHostMgeUps

# pysnmp imports
from pysnmp.v4.proto import api


class Snmptrapd(BaseSnmptrapd):
    """Ticker-Adapter."""

    implements(ISnmptrapd)
    adapts(IHostMgeUps)

    def __init__(self, context):
        print "Snmptrapd.__init__ mge_ups"
        self.context = context

    def triggered(self, reqPDU, msgVer, pMod):
        """
        got snmp event from snmp thread
        """
        #print "Snmptrapd %s triggered (reqPDU:%s)!!" % (self.context, reqPDU)
        #print '-' * 80
        if reqPDU.isSameTypeWith(pMod.TrapPDU()):
            if msgVer == api.protoVersion1:
                #print 'Enterprise: %s' % (
                    #pMod.apiTrapPDU.getEnterprise(reqPDU).prettyPrint()
                    #)
                #print 'Agent Address: %s' % (
                    #pMod.apiTrapPDU.getAgentAddr(reqPDU).prettyPrint()
                    #)
                #print 'Generic Trap: %s' % (
                    #pMod.apiTrapPDU.getGenericTrap(reqPDU).prettyPrint()
                    #)
                #print 'Specific Trap: %s' % (
                    #pMod.apiTrapPDU.getSpecificTrap(reqPDU).prettyPrint()
                    #)
                #print 'Uptime: %s' % (
                    #pMod.apiTrapPDU.getTimeStamp(reqPDU).prettyPrint()
                    #)
                varBinds = pMod.apiTrapPDU.getVarBindList(reqPDU)
                # AT
                #if pMod.apiTrapPDU.getEnterprise(reqPDU).prettyPrint() == \
                   #u'1.3.6.1.4.1.207.1.4.29':
                # TODO remove this big fake
                if pMod.apiTrapPDU.getEnterprise(reqPDU).prettyPrint() == \
                   u'1.3.6.1.4.1.9.1.516':
                    print "Cisco - Switch!!!"
                    if pMod.apiTrapPDU.getGenericTrap(reqPDU).prettyPrint() == 'linkUp(3)':
                        #print "UP"
                        self.context.eventOut_powerReturned()
                    if pMod.apiTrapPDU.getGenericTrap(reqPDU).prettyPrint() == 'linkDown(2)':
                        #print "DOWN"
                        self.context.eventOut_onBattery()
            else:
                varBinds = pMod.apiPDU.getVarBindList(reqPDU)
            #if len(varBinds) > 0:
                #print 'Var-binds:'
                #for oid, val in varBinds:
                    #print '-' * 40
                    #print '%s = %s' % (oid.prettyPrint(), val.prettyPrint())
                    #print '-' * 40
        #print '-' * 80

#1:upsBatteryFault (level 2) UPS battery fault status
#2:upsBatteryOK
#3:upsBatteryReplacementIndicated (level 3) UPS battery replacement indicator
#4:upsBatteryReplacementNotIndicated
#5:upsAtLowBattery (level 1) UPS low battery internal indicator
#6:upsFromLowBattery
#7:upsChargerFault (level 3) UPS battery charger fault status
#8:upsChargerOK
#9:upsAtLowCondition (level 1) UPS battery minimum condition status
#10:upsFromLowCondition
#11:upsOnBattery (level 1) UPS on battery backup status
#12:upsReturnFromBattery
#13:upsOnByPass (level 2) UPS on bypass status
#14:upsReturnFromByPass
#15:upsByPassUnavailable (level 3) UPS bypass unavailable/available
#16:upsByPassAvailable
#17:upsUtilityFailure (level 2) UPS mains input failure indicator
#18:upsUtilityRestored
#19:upsOnBoost (level 3) UPS booster feature enabled
#20:upsReturnFromBoost
#21:upsOverLoad (level 2) UPS load in excess of rated value
#22:upsLoadOK
#23:upsOverTemperature (level 2) Incorrect UPS internal temperature
#24:upsTemperatureOK
#37:upsCommunicationFailure (level 1) State of serial communication with UPS
#38:upsCommunicationRestored
#39:upsInputBad (level 3) Incorrect input voltage or frequency
#40:upsInputOK
#41:upsBatteryUnavailable (level 3) UPS battery unavailable
#42:upsBatteryAvailable
#43:upsAtLowRecharge (level 4) UPS awaiting restart condition
#44:upsFromLowRecharge
#45:upsDiagnosticTestFail (level 3) UPS internal self test state
#46:upsDiagnosticTestOK
#47:upsBatteryTestOK (level 3) UPS battery test state
#48:upsBatteryTestFail
#49:upsExternalAlarmActive (level 2) External alarm state
#50:upsExternalAlarmInactive
#51:upsOnBuck (level 3) Activation of UPS fader
#52:upsReturnFromBuck
#53: upsmgEnvironmentComFailure (level 2) Environment Probe communication failure.
#54: upsmgEnvironmentComOK Environment Probe communication restored.
#55: upsmgEnvironmentTemperatureLow (level 2) Temperature is below low threshold.
#56: upsmgEnvironmentTemperatureHigh (level 2) Temperature is above high threshold.
#57: upsmgEnvironmentTemperatureOK Temperature is in normal range.
#58: upsmgEnvironmentHumidityLow (level 2) Humidity is below low threshold.
#59: upsmgEnvironmentHumidityHigh (level 2) Humidity is above high threshold.
#60: upsmgEnvironmentHumidityOK Humidity is in normal range.
#61: upsmgEnvironmentInput1Closed (level 2) Input #1 is Closed.
#62: upsmgEnvironmentInput1Open (level 2) Input #1 is Open.
#63: upsmgEnvironmentInput2Closed (level 2) Input #2 is Closed.
#64: upsmgEnvironmentInput2Open (level 2) Input #2 is Open.
