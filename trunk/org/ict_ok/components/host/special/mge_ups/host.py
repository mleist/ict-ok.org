# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0612,W0142
#
"""implementation of host object

host object represents a MGE UPS
tested with MGE Galaxy 3000
"""

__version__ = "$Id$"

# phython imports

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

# ict_ok.org imports
from org.ict_ok.components.host.special.mge_ups.interfaces import \
     IHostMgeUps, IEventIfHostMgeUps
from org.ict_ok.components.host.host import Host as HostBase
from org.ict_ok.components.superclass.superclass import MsgEvent


class Host(HostBase):
    """A MGE UPS object."""

    implements(IHostMgeUps, IEventIfHostMgeUps)

    eventOutObjs_onBattery = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_onBattery'])
    eventOutObjs_powerReturned = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_powerReturned'])

    #def eventOut_onBattery(self):
        #""" sends 'on battery' event """
        #print "Host.eventOut_onBattery   (MGE)"
        #for my_event in self.eventOutObjs_onBattery:
            #inst_event = MsgEvent(self, my_event)
            #self.injectOutEQueue(inst_event)

    #def eventOut_powerReturned(self):
        #""" sends 'power returned' event """
        #print "Host.eventOut_powerReturned   (MGE)"
        #for my_event in self.eventOutObjs_powerReturned:
            #inst_event = MsgEvent(self, my_event)
            #self.injectOutEQueue(inst_event)

    def eventOut_upsBatteryFault(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsBatteryFault:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsBatteryOK(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsBatteryOK:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsBatteryReplacementIndicated(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsBatteryReplacementIndicated:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsBatteryReplacementNotIndicated(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsBatteryReplacementNotIndicated:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsAtLowBattery(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsAtLowBattery:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsFromLowBattery(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsFromLowBattery:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsChargerFault(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsChargerFault:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsChargerOK(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsChargerOK:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsAtLowCondition(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsAtLowCondition:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsFromLowCondition(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsFromLowCondition:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsOnBattery(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsOnBattery:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsReturnFromBattery(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsReturnFromBattery:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsOnByPass(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsOnByPass:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsReturnFromByPass(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsReturnFromByPass:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsByPassUnavailable(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsByPassUnavailable:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsByPassAvailable(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsByPassAvailable:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsUtilityFailure(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsUtilityFailure:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsUtilityRestored(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsUtilityRestored:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsOnBoost(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsOnBoost:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsReturnFromBoost(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsReturnFromBoost:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsOverLoad(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsOverLoad:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsLoadOK(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsLoadOK:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsOverTemperature(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsOverTemperature:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsTemperatureOK(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsTemperatureOK:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsCommunicationFailure(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsCommunicationFailure:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsCommunicationRestored(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsCommunicationRestored:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsInputBad(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsInputBad:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsInputOK(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsInputOK:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsBatteryUnavailable(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsBatteryUnavailable:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsBatteryAvailable(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsBatteryAvailable:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsAtLowRecharge(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsAtLowRecharge:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsFromLowRecharge(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsFromLowRecharge:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsDiagnosticTestFail(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsDiagnosticTestFail:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsDiagnosticTestOK(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsDiagnosticTestOK:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsBatteryTestOK(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsBatteryTestOK:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsBatteryTestFail(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsBatteryTestFail:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsExternalAlarmActive(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsExternalAlarmActive:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsExternalAlarmInactive(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsExternalAlarmInactive:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsOnBuck(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsOnBuck:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsReturnFromBuck(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsReturnFromBuck:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsmgEnvironmentComFailure(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsmgEnvironmentComFailure:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsmgEnvironmentComOK(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsmgEnvironmentComOK:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsmgEnvironmentTemperatureLow(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsmgEnvironmentTemperatureLow:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsmgEnvironmentTemperatureHigh(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsmgEnvironmentTemperatureHigh:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsmgEnvironmentTemperatureOK(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsmgEnvironmentTemperatureOK:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsmgEnvironmentHumidityLow(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsmgEnvironmentHumidityLow:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsmgEnvironmentHumidityHigh(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsmgEnvironmentHumidityHigh:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsmgEnvironmentHumidityOK(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsmgEnvironmentHumidityOK:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsmgEnvironmentInput1Closed(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsmgEnvironmentInput1Closed:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsmgEnvironmentInput1Open(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsmgEnvironmentInput1Open:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsmgEnvironmentInput2Closed(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsmgEnvironmentInput2Closed:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsmgEnvironmentInput2Open(self):
        """ sends event (source is snmp """
        for my_event in self.eventOutObjs_upsmgEnvironmentInput2Open:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)


upsBatteryFault
upsBatteryOK
upsBatteryReplacementIndicated
upsBatteryReplacementNotIndicated
upsAtLowBattery
upsFromLowBattery
upsChargerFault
upsChargerOK
upsAtLowCondition
upsFromLowCondition
upsOnBattery
upsReturnFromBattery
upsOnByPass
upsReturnFromByPass
upsByPassUnavailable
upsByPassAvailable
upsUtilityFailure
upsUtilityRestored
upsOnBoost
upsReturnFromBoost
upsOverLoad
upsLoadOK
upsOverTemperature
upsTemperatureOK
upsCommunicationFailure
upsCommunicationRestored
upsInputBad
upsInputOK
upsBatteryUnavailable
upsBatteryAvailable
upsAtLowRecharge
upsFromLowRecharge
upsDiagnosticTestFail
upsDiagnosticTestOK
upsBatteryTestOK
upsBatteryTestFail
upsExternalAlarmActive
upsExternalAlarmInactive
upsOnBuck
upsReturnFromBuck
upsmgEnvironmentComFailure
upsmgEnvironmentComOK
upsmgEnvironmentTemperatureLow
upsmgEnvironmentTemperatureHigh
upsmgEnvironmentTemperatureOK
upsmgEnvironmentHumidityLow
upsmgEnvironmentHumidityHigh
upsmgEnvironmentHumidityOK
upsmgEnvironmentInput1Closed
upsmgEnvironmentInput1Open
upsmgEnvironmentInput2Closed
upsmgEnvironmentInput2Open

    def tickerEvent(self):
        """
        got ticker event from ticker thread
        """
        #print "Host.tickerEvent   (MGE)"
        HostBase.tickerEvent(self)
