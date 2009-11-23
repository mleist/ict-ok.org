# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
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

# python imports

# zope imports
from zope.interface import implements
from zope.component import adapts

# ict_ok.org imports
from org.ict_ok.libs.history.entry import Entry
from org.ict_ok.admin_utils.snmpd.interfaces import ISnmptrapd
from org.ict_ok.components.host.adapter.snmp import Snmptrapd as BaseSnmptrapd
from org.ict_ok.components.host.special.mge_ups.interfaces import IHostMgeUps

# pysnmp imports
from pysnmp.proto import api


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
        print "Snmptrapd %s triggered (reqPDU:%s)!!" % (self.context, reqPDU)
        print '-' * 80
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
                   u'1.3.6.1.4.1.705.1.11':
                    #print "MGE UPS <----"
                    #self.context.trigger_offline()
                    specificTrap = pMod.apiTrapPDU.getSpecificTrap(reqPDU)
                    if specificTrap == 1:
                        self.context.eventOut_upsBatteryFault()
                    elif specificTrap == 2:
                        self.context.eventOut_upsBatteryOK()
                    elif specificTrap == 3:
                        self.context.eventOut_upsBatteryReplacementIndicated()
                    elif specificTrap == 4:
                        self.context.eventOut_upsBatteryReplacementNotIndicated()
                    elif specificTrap == 5:
                        self.context.eventOut_upsAtLowBattery()
                    elif specificTrap == 6:
                        self.context.eventOut_upsFromLowBattery()
                    elif specificTrap == 7:
                        self.context.eventOut_upsChargerFault()
                    elif specificTrap == 8:
                        self.context.eventOut_upsChargerOK()
                    elif specificTrap == 9:
                        self.context.eventOut_upsAtLowCondition()
                    elif specificTrap == 10:
                        self.context.eventOut_upsFromLowCondition()
                    elif specificTrap == 11:
                        self.context.eventOut_upsOnBattery()
                    elif specificTrap == 12:
                        self.context.eventOut_upsReturnFromBattery()
                    elif specificTrap == 13:
                        self.context.eventOut_upsOnByPass()
                    elif specificTrap == 14:
                        self.context.eventOut_upsReturnFromByPass()
                    elif specificTrap == 15:
                        self.context.eventOut_upsByPassUnavailable()
                    elif specificTrap == 16:
                        self.context.eventOut_upsByPassAvailable()
                    elif specificTrap == 17:
                        self.context.eventOut_upsUtilityFailure()
                    elif specificTrap == 18:
                        self.context.eventOut_upsUtilityRestored()
                    elif specificTrap == 19:
                        self.context.eventOut_upsOnBoost()
                    elif specificTrap == 20:
                        self.context.eventOut_upsReturnFromBoost()
                    elif specificTrap == 21:
                        self.context.eventOut_upsOverLoad()
                    elif specificTrap == 22:
                        self.context.eventOut_upsLoadOK()
                    elif specificTrap == 23:
                        self.context.eventOut_upsOverTemperature()
                    elif specificTrap == 24:
                        self.context.eventOut_upsTemperatureOK()
                    elif specificTrap == 37:
                        self.context.eventOut_upsCommunicationFailure()
                    elif specificTrap == 38:
                        self.context.eventOut_upsCommunicationRestored()
                    elif specificTrap == 39:
                        self.context.eventOut_upsInputBad()
                    elif specificTrap == 40:
                        self.context.eventOut_upsInputOK()
                    elif specificTrap == 41:
                        self.context.eventOut_upsBatteryUnavailable()
                    elif specificTrap == 42:
                        self.context.eventOut_upsBatteryAvailable()
                    elif specificTrap == 43:
                        self.context.eventOut_upsAtLowRecharge()
                    elif specificTrap == 44:
                        self.context.eventOut_upsFromLowRecharge()
                    elif specificTrap == 45:
                        self.context.eventOut_upsDiagnosticTestFail()
                    elif specificTrap == 46:
                        self.context.eventOut_upsDiagnosticTestOK()
                    elif specificTrap == 47:
                        self.context.eventOut_upsBatteryTestOK()
                    elif specificTrap == 48:
                        self.context.eventOut_upsBatteryTestFail()
                    elif specificTrap == 49:
                        self.context.eventOut_upsExternalAlarmActive()
                    elif specificTrap == 50:
                        self.context.eventOut_upsExternalAlarmInactive()
                    elif specificTrap == 51:
                        self.context.eventOut_upsOnBuck()
                    elif specificTrap == 52:
                        self.context.eventOut_upsReturnFromBuck()
                    elif specificTrap == 53:
                        self.context.eventOut_upsmgEnvironmentComFailure()
                    elif specificTrap == 54:
                        self.context.eventOut_upsmgEnvironmentComOK()
                    elif specificTrap == 55:
                        self.context.eventOut_upsmgEnvironmentTemperatureLow()
                    elif specificTrap == 56:
                        self.context.eventOut_upsmgEnvironmentTemperatureHigh()
                    elif specificTrap == 57:
                        self.context.eventOut_upsmgEnvironmentTemperatureOK()
                    elif specificTrap == 58:
                        self.context.eventOut_upsmgEnvironmentHumidityLow()
                    elif specificTrap == 59:
                        self.context.eventOut_upsmgEnvironmentHumidityHigh()
                    elif specificTrap == 60:
                        self.context.eventOut_upsmgEnvironmentHumidityOK()
                    elif specificTrap == 61:
                        self.context.eventOut_upsmgEnvironmentInput1Closed()
                    elif specificTrap == 62:
                        self.context.eventOut_upsmgEnvironmentInput1Open()
                    elif specificTrap == 63:
                        self.context.eventOut_upsmgEnvironmentInput2Closed()
                    elif specificTrap == 64:
                        self.context.eventOut_upsmgEnvironmentInput2Open()
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
        
#15:05:32.418926 IP (tos 0x0, ttl 199, id 28318, offset 0, flags [none], proto UDP (17), length 74) 
#192.168.154.50.161 > 192.168.157.98.162: [udp sum ok]  
#{ SNMPv1 { Trap(31)  .1.3.6.1.4.1.705.1.11 192.168.154.50 enterpriseSpecific s=56 1046121494 } }

#15:06:59.688919 IP (tos 0x0, ttl 199, id 29021, offset 0, flags [none], proto UDP (17), length 74) 
#192.168.154.50.161 > 192.168.157.98.162: [udp sum ok]  
#{ SNMPv1 { Trap(31)  .1.3.6.1.4.1.705.1.11 192.168.154.50 enterpriseSpecific s=57 1046130226 } }
        
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
#53:upsmgEnvironmentComFailure (level 2) Environment Probe communication failure.
#54:upsmgEnvironmentComOK Environment Probe communication restored.
#55:upsmgEnvironmentTemperatureLow (level 2) Temperature is below low threshold.
#56:upsmgEnvironmentTemperatureHigh (level 2) Temperature is above high threshold.
#57:upsmgEnvironmentTemperatureOK Temperature is in normal range.
#58:upsmgEnvironmentHumidityLow (level 2) Humidity is below low threshold.
#59:upsmgEnvironmentHumidityHigh (level 2) Humidity is above high threshold.
#60:upsmgEnvironmentHumidityOK Humidity is in normal range.
#61:upsmgEnvironmentInput1Closed (level 2) Input #1 is Closed.
#62:upsmgEnvironmentInput1Open (level 2) Input #1 is Open.
#63:upsmgEnvironmentInput2Closed (level 2) Input #2 is Closed.
#64:upsmgEnvironmentInput2Open (level 2) Input #2 is Open.
