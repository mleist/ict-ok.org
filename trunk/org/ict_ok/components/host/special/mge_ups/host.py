# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0612,W0142,C0103,R0904
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


    eventOutObjs_upsBatteryFault = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsBatteryFault'])
    eventOutObjs_upsBatteryOK = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsBatteryOK'])
    eventOutObjs_upsBatteryReplacementIndicated = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsBatteryReplacementIndicated'])
    eventOutObjs_upsBatteryReplacementNotIndicated = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsBatteryReplacementNotIndicated'])
    eventOutObjs_upsAtLowBattery = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsAtLowBattery'])
    eventOutObjs_upsFromLowBattery = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsFromLowBattery'])
    eventOutObjs_upsChargerFault = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsChargerFault'])
    eventOutObjs_upsChargerOK = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsChargerOK'])
    eventOutObjs_upsAtLowCondition = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsAtLowCondition'])
    eventOutObjs_upsFromLowCondition = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsFromLowCondition'])
    eventOutObjs_upsOnBattery = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsOnBattery'])
    eventOutObjs_upsReturnFromBattery = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsReturnFromBattery'])
    eventOutObjs_upsOnByPass = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsOnByPass'])
    eventOutObjs_upsReturnFromByPass = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsReturnFromByPass'])
    eventOutObjs_upsByPassUnavailable = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsByPassUnavailable'])
    eventOutObjs_upsByPassAvailable = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsByPassAvailable'])
    eventOutObjs_upsUtilityFailure = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsUtilityFailure'])
    eventOutObjs_upsUtilityRestored = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsUtilityRestored'])
    eventOutObjs_upsOnBoost = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsOnBoost'])
    eventOutObjs_upsReturnFromBoost = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsReturnFromBoost'])
    eventOutObjs_upsOverLoad = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsOverLoad'])
    eventOutObjs_upsLoadOK = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsLoadOK'])
    eventOutObjs_upsOverTemperature = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsOverTemperature'])
    eventOutObjs_upsTemperatureOK = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsTemperatureOK'])
    eventOutObjs_upsCommunicationFailure = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsCommunicationFailure'])
    eventOutObjs_upsCommunicationRestored = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsCommunicationRestored'])
    eventOutObjs_upsInputBad = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsInputBad'])
    eventOutObjs_upsInputOK = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsInputOK'])
    eventOutObjs_upsBatteryUnavailable = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsBatteryUnavailable'])
    eventOutObjs_upsBatteryAvailable = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsBatteryAvailable'])
    eventOutObjs_upsAtLowRecharge = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsAtLowRecharge'])
    eventOutObjs_upsFromLowRecharge = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsFromLowRecharge'])
    eventOutObjs_upsDiagnosticTestFail = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsDiagnosticTestFail'])
    eventOutObjs_upsDiagnosticTestOK = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsDiagnosticTestOK'])
    eventOutObjs_upsBatteryTestOK = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsBatteryTestOK'])
    eventOutObjs_upsBatteryTestFail = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsBatteryTestFail'])
    eventOutObjs_upsExternalAlarmActive = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsExternalAlarmActive'])
    eventOutObjs_upsExternalAlarmInactive = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsExternalAlarmInactive'])
    eventOutObjs_upsOnBuck = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsOnBuck'])
    eventOutObjs_upsReturnFromBuck = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsReturnFromBuck'])
    eventOutObjs_upsmgEnvironmentComFailure = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsmgEnvironmentComFailure'])
    eventOutObjs_upsmgEnvironmentComOK = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsmgEnvironmentComOK'])
    eventOutObjs_upsmgEnvironmentTemperatureLow = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsmgEnvironmentTemperatureLow'])
    eventOutObjs_upsmgEnvironmentTemperatureHigh = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsmgEnvironmentTemperatureHigh'])
    eventOutObjs_upsmgEnvironmentTemperatureOK = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsmgEnvironmentTemperatureOK'])
    eventOutObjs_upsmgEnvironmentHumidityLow = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsmgEnvironmentHumidityLow'])
    eventOutObjs_upsmgEnvironmentHumidityHigh = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsmgEnvironmentHumidityHigh'])
    eventOutObjs_upsmgEnvironmentHumidityOK = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsmgEnvironmentHumidityOK'])
    eventOutObjs_upsmgEnvironmentInput1Closed = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsmgEnvironmentInput1Closed'])
    eventOutObjs_upsmgEnvironmentInput1Open = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsmgEnvironmentInput1Open'])
    eventOutObjs_upsmgEnvironmentInput2Closed = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsmgEnvironmentInput2Closed'])
    eventOutObjs_upsmgEnvironmentInput2Open = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_upsmgEnvironmentInput2Open'])



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
        self.appendHistoryEntry(u"upsBatteryFault")
        for my_event in self.eventOutObjs_upsBatteryFault:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsBatteryOK(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsBatteryOK")
        for my_event in self.eventOutObjs_upsBatteryOK:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsBatteryReplacementIndicated(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsBatteryReplacementIndicated")
        for my_event in self.eventOutObjs_upsBatteryReplacementIndicated:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsBatteryReplacementNotIndicated(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsBatteryReplacementNotIndicated")
        for my_event in self.eventOutObjs_upsBatteryReplacementNotIndicated:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsAtLowBattery(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsAtLowBattery")
        for my_event in self.eventOutObjs_upsAtLowBattery:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsFromLowBattery(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsFromLowBattery")
        for my_event in self.eventOutObjs_upsFromLowBattery:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsChargerFault(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsChargerFault")
        for my_event in self.eventOutObjs_upsChargerFault:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsChargerOK(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsChargerOK")
        for my_event in self.eventOutObjs_upsChargerOK:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsAtLowCondition(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsAtLowCondition")
        for my_event in self.eventOutObjs_upsAtLowCondition:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsFromLowCondition(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsFromLowCondition")
        for my_event in self.eventOutObjs_upsFromLowCondition:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsOnBattery(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsOnBattery")
        for my_event in self.eventOutObjs_upsOnBattery:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsReturnFromBattery(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsReturnFromBattery")
        for my_event in self.eventOutObjs_upsReturnFromBattery:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsOnByPass(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsOnByPass")
        for my_event in self.eventOutObjs_upsOnByPass:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsReturnFromByPass(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsReturnFromByPass")
        for my_event in self.eventOutObjs_upsReturnFromByPass:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsByPassUnavailable(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsByPassUnavailable")
        for my_event in self.eventOutObjs_upsByPassUnavailable:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsByPassAvailable(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsByPassAvailable")
        for my_event in self.eventOutObjs_upsByPassAvailable:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsUtilityFailure(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsUtilityFailure")
        for my_event in self.eventOutObjs_upsUtilityFailure:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsUtilityRestored(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsUtilityRestored")
        for my_event in self.eventOutObjs_upsUtilityRestored:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsOnBoost(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsOnBoost")
        for my_event in self.eventOutObjs_upsOnBoost:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsReturnFromBoost(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsReturnFromBoost")
        for my_event in self.eventOutObjs_upsReturnFromBoost:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsOverLoad(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsOverLoad")
        for my_event in self.eventOutObjs_upsOverLoad:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsLoadOK(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsLoadOK")
        for my_event in self.eventOutObjs_upsLoadOK:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsOverTemperature(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsOverTemperature")
        for my_event in self.eventOutObjs_upsOverTemperature:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsTemperatureOK(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsTemperatureOK")
        for my_event in self.eventOutObjs_upsTemperatureOK:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsCommunicationFailure(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsCommunicationFailure")
        for my_event in self.eventOutObjs_upsCommunicationFailure:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsCommunicationRestored(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsCommunicationRestored")
        for my_event in self.eventOutObjs_upsCommunicationRestored:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsInputBad(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsInputBad")
        for my_event in self.eventOutObjs_upsInputBad:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsInputOK(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsInputOK")
        for my_event in self.eventOutObjs_upsInputOK:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsBatteryUnavailable(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsBatteryUnavailable")
        for my_event in self.eventOutObjs_upsBatteryUnavailable:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsBatteryAvailable(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsBatteryAvailable")
        for my_event in self.eventOutObjs_upsBatteryAvailable:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsAtLowRecharge(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsAtLowRecharge")
        for my_event in self.eventOutObjs_upsAtLowRecharge:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsFromLowRecharge(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsFromLowRecharge")
        for my_event in self.eventOutObjs_upsFromLowRecharge:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsDiagnosticTestFail(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsDiagnosticTestFail")
        for my_event in self.eventOutObjs_upsDiagnosticTestFail:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsDiagnosticTestOK(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsDiagnosticTestOK")
        for my_event in self.eventOutObjs_upsDiagnosticTestOK:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsBatteryTestOK(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsBatteryTestOK")
        for my_event in self.eventOutObjs_upsBatteryTestOK:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsBatteryTestFail(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsBatteryTestFail")
        for my_event in self.eventOutObjs_upsBatteryTestFail:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsExternalAlarmActive(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsExternalAlarmActive")
        for my_event in self.eventOutObjs_upsExternalAlarmActive:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsExternalAlarmInactive(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsExternalAlarmInactive")
        for my_event in self.eventOutObjs_upsExternalAlarmInactive:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsOnBuck(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsOnBuck")
        for my_event in self.eventOutObjs_upsOnBuck:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsReturnFromBuck(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsReturnFromBuck")
        for my_event in self.eventOutObjs_upsReturnFromBuck:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsmgEnvironmentComFailure(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsmgEnvironmentComFailure")
        for my_event in self.eventOutObjs_upsmgEnvironmentComFailure:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsmgEnvironmentComOK(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsmgEnvironmentComOK")
        for my_event in self.eventOutObjs_upsmgEnvironmentComOK:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsmgEnvironmentTemperatureLow(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsmgEnvironmentTemperatureLow")
        for my_event in self.eventOutObjs_upsmgEnvironmentTemperatureLow:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsmgEnvironmentTemperatureHigh(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsmgEnvironmentTemperatureHigh")
        for my_event in self.eventOutObjs_upsmgEnvironmentTemperatureHigh:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsmgEnvironmentTemperatureOK(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsmgEnvironmentTemperatureOK")
        for my_event in self.eventOutObjs_upsmgEnvironmentTemperatureOK:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsmgEnvironmentHumidityLow(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsmgEnvironmentHumidityLow")
        for my_event in self.eventOutObjs_upsmgEnvironmentHumidityLow:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsmgEnvironmentHumidityHigh(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsmgEnvironmentHumidityHigh")
        for my_event in self.eventOutObjs_upsmgEnvironmentHumidityHigh:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsmgEnvironmentHumidityOK(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsmgEnvironmentHumidityOK")
        for my_event in self.eventOutObjs_upsmgEnvironmentHumidityOK:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsmgEnvironmentInput1Closed(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsmgEnvironmentInput1Closed")
        for my_event in self.eventOutObjs_upsmgEnvironmentInput1Closed:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsmgEnvironmentInput1Open(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsmgEnvironmentInput1Open")
        for my_event in self.eventOutObjs_upsmgEnvironmentInput1Open:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsmgEnvironmentInput2Closed(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsmgEnvironmentInput2Closed")
        for my_event in self.eventOutObjs_upsmgEnvironmentInput2Closed:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_upsmgEnvironmentInput2Open(self):
        """ sends event (source is snmp """
        self.appendHistoryEntry(u"upsmgEnvironmentInput2Open")
        for my_event in self.eventOutObjs_upsmgEnvironmentInput2Open:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def tickerEvent(self):
        """
        got ticker event from ticker thread
        """
        #print "Host.tickerEvent   (MGE)"
        HostBase.tickerEvent(self)
