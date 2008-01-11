# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232
#
"""Interface of a mge ups
this device may sends:
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
"""

__version__ = "$Id$"

# zope imports
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, Set

# ict_ok.org imports
from org.ict_ok.components.supernode.interfaces import \
     IEventIfSupernode
from org.ict_ok.components.host.interfaces import IHost

_ = MessageFactory('org.ict_ok')


class IHostMgeUps(IHost):
    """A MGE UPS object."""

class IEventIfHostMgeUps(IEventIfSupernode):
    """ event interface of object """
    #eventOutObjs_onBattery = Set(
        #title = _("on battery ->"),
        #value_type = Choice(
            #title = _("objects"),
            #vocabulary="AllEventInstances"),
        #default = set([]),
        #readonly = False,
        #required = False)
    #eventOutObjs_powerReturned = Set(
        #title = _("power returned ->"),
        #value_type = Choice(
            #title = _("objects"),
            #vocabulary="AllEventInstances"),
        #default = set([]),
        #readonly = False,
        #required = False)
    #def eventOut_onBattery(self):
        #""" sends 'on battery' event """
    #def eventOut_powerReturned(self):
        #""" sends 'power returned' event """

    eventOutObjs_upsBatteryFault = Set(
        title = _("upsBatteryFault ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsBatteryOK = Set(
        title = _("upsBatteryOK ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsBatteryReplacementIndicated = Set(
        title = _("upsBatteryReplacementIndicated ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsBatteryReplacementNotIndicated = Set(
        title = _("upsBatteryReplacementNotIndicated ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsAtLowBattery = Set(
        title = _("upsAtLowBattery ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsFromLowBattery = Set(
        title = _("upsFromLowBattery ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsChargerFault = Set(
        title = _("upsChargerFault ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsChargerOK = Set(
        title = _("upsChargerOK ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsAtLowCondition = Set(
        title = _("upsAtLowCondition ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsFromLowCondition = Set(
        title = _("upsFromLowCondition ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsOnBattery = Set(
        title = _("upsOnBattery ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsReturnFromBattery = Set(
        title = _("upsReturnFromBattery ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsOnByPass = Set(
        title = _("upsOnByPass ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsReturnFromByPass = Set(
        title = _("upsReturnFromByPass ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsByPassUnavailable = Set(
        title = _("upsByPassUnavailable ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsByPassAvailable = Set(
        title = _("upsByPassAvailable ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsUtilityFailure = Set(
        title = _("upsUtilityFailure ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsUtilityRestored = Set(
        title = _("upsUtilityRestored ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsOnBoost = Set(
        title = _("upsOnBoost ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsReturnFromBoost = Set(
        title = _("upsReturnFromBoost ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsOverLoad = Set(
        title = _("upsOverLoad ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsLoadOK = Set(
        title = _("upsLoadOK ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsOverTemperature = Set(
        title = _("upsOverTemperature ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsTemperatureOK = Set(
        title = _("upsTemperatureOK ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsCommunicationFailure = Set(
        title = _("upsCommunicationFailure ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsCommunicationRestored = Set(
        title = _("upsCommunicationRestored ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsInputBad = Set(
        title = _("upsInputBad ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsInputOK = Set(
        title = _("upsInputOK ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsBatteryUnavailable = Set(
        title = _("upsBatteryUnavailable ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsBatteryAvailable = Set(
        title = _("upsBatteryAvailable ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsAtLowRecharge = Set(
        title = _("upsAtLowRecharge ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsFromLowRecharge = Set(
        title = _("upsFromLowRecharge ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsDiagnosticTestFail = Set(
        title = _("upsDiagnosticTestFail ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsDiagnosticTestOK = Set(
        title = _("upsDiagnosticTestOK ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsBatteryTestOK = Set(
        title = _("upsBatteryTestOK ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsBatteryTestFail = Set(
        title = _("upsBatteryTestFail ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsExternalAlarmActive = Set(
        title = _("upsExternalAlarmActive ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsExternalAlarmInactive = Set(
        title = _("upsExternalAlarmInactive ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsOnBuck = Set(
        title = _("upsOnBuck ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsReturnFromBuck = Set(
        title = _("upsReturnFromBuck ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsmgEnvironmentComFailure = Set(
        title = _("upsmgEnvironmentComFailure ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsmgEnvironmentComOK = Set(
        title = _("upsmgEnvironmentComOK ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsmgEnvironmentTemperatureLow = Set(
        title = _("upsmgEnvironmentTemperatureLow ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsmgEnvironmentTemperatureHigh = Set(
        title = _("upsmgEnvironmentTemperatureHigh ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsmgEnvironmentTemperatureOK = Set(
        title = _("upsmgEnvironmentTemperatureOK ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsmgEnvironmentHumidityLow = Set(
        title = _("upsmgEnvironmentHumidityLow ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsmgEnvironmentHumidityHigh = Set(
        title = _("upsmgEnvironmentHumidityHigh ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsmgEnvironmentHumidityOK = Set(
        title = _("upsmgEnvironmentHumidityOK ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsmgEnvironmentInput1Closed = Set(
        title = _("upsmgEnvironmentInput1Closed ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsmgEnvironmentInput1Open = Set(
        title = _("upsmgEnvironmentInput1Open ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsmgEnvironmentInput2Closed = Set(
        title = _("upsmgEnvironmentInput2Closed ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_upsmgEnvironmentInput2Open = Set(
        title = _("upsmgEnvironmentInput2Open ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)

    def eventOut_upsBatteryFault(self):
        """ sends event (source is snmp """
    def eventOut_upsBatteryOK(self):
        """ sends event (source is snmp """
    def eventOut_upsBatteryReplacementIndicated(self):
        """ sends event (source is snmp """
    def eventOut_upsBatteryReplacementNotIndicated(self):
        """ sends event (source is snmp """
    def eventOut_upsAtLowBattery(self):
        """ sends event (source is snmp """
    def eventOut_upsFromLowBattery(self):
        """ sends event (source is snmp """
    def eventOut_upsChargerFault(self):
        """ sends event (source is snmp """
    def eventOut_upsChargerOK(self):
        """ sends event (source is snmp """
    def eventOut_upsAtLowCondition(self):
        """ sends event (source is snmp """
    def eventOut_upsFromLowCondition(self):
        """ sends event (source is snmp """
    def eventOut_upsOnBattery(self):
        """ sends event (source is snmp """
    def eventOut_upsReturnFromBattery(self):
        """ sends event (source is snmp """
    def eventOut_upsOnByPass(self):
        """ sends event (source is snmp """
    def eventOut_upsReturnFromByPass(self):
        """ sends event (source is snmp """
    def eventOut_upsByPassUnavailable(self):
        """ sends event (source is snmp """
    def eventOut_upsByPassAvailable(self):
        """ sends event (source is snmp """
    def eventOut_upsUtilityFailure(self):
        """ sends event (source is snmp """
    def eventOut_upsUtilityRestored(self):
        """ sends event (source is snmp """
    def eventOut_upsOnBoost(self):
        """ sends event (source is snmp """
    def eventOut_upsReturnFromBoost(self):
        """ sends event (source is snmp """
    def eventOut_upsOverLoad(self):
        """ sends event (source is snmp """
    def eventOut_upsLoadOK(self):
        """ sends event (source is snmp """
    def eventOut_upsOverTemperature(self):
        """ sends event (source is snmp """
    def eventOut_upsTemperatureOK(self):
        """ sends event (source is snmp """
    def eventOut_upsCommunicationFailure(self):
        """ sends event (source is snmp """
    def eventOut_upsCommunicationRestored(self):
        """ sends event (source is snmp """
    def eventOut_upsInputBad(self):
        """ sends event (source is snmp """
    def eventOut_upsInputOK(self):
        """ sends event (source is snmp """
    def eventOut_upsBatteryUnavailable(self):
        """ sends event (source is snmp """
    def eventOut_upsBatteryAvailable(self):
        """ sends event (source is snmp """
    def eventOut_upsAtLowRecharge(self):
        """ sends event (source is snmp """
    def eventOut_upsFromLowRecharge(self):
        """ sends event (source is snmp """
    def eventOut_upsDiagnosticTestFail(self):
        """ sends event (source is snmp """
    def eventOut_upsDiagnosticTestOK(self):
        """ sends event (source is snmp """
    def eventOut_upsBatteryTestOK(self):
        """ sends event (source is snmp """
    def eventOut_upsBatteryTestFail(self):
        """ sends event (source is snmp """
    def eventOut_upsExternalAlarmActive(self):
        """ sends event (source is snmp """
    def eventOut_upsExternalAlarmInactive(self):
        """ sends event (source is snmp """
    def eventOut_upsOnBuck(self):
        """ sends event (source is snmp """
    def eventOut_upsReturnFromBuck(self):
        """ sends event (source is snmp """
    def eventOut_upsmgEnvironmentComFailure(self):
        """ sends event (source is snmp """
    def eventOut_upsmgEnvironmentComOK(self):
        """ sends event (source is snmp """
    def eventOut_upsmgEnvironmentTemperatureLow(self):
        """ sends event (source is snmp """
    def eventOut_upsmgEnvironmentTemperatureHigh(self):
        """ sends event (source is snmp """
    def eventOut_upsmgEnvironmentTemperatureOK(self):
        """ sends event (source is snmp """
    def eventOut_upsmgEnvironmentHumidityLow(self):
        """ sends event (source is snmp """
    def eventOut_upsmgEnvironmentHumidityHigh(self):
        """ sends event (source is snmp """
    def eventOut_upsmgEnvironmentHumidityOK(self):
        """ sends event (source is snmp """
    def eventOut_upsmgEnvironmentInput1Closed(self):
        """ sends event (source is snmp """
    def eventOut_upsmgEnvironmentInput1Open(self):
        """ sends event (source is snmp """
    def eventOut_upsmgEnvironmentInput2Closed(self):
        """ sends event (source is snmp """
    def eventOut_upsmgEnvironmentInput2Open(self):
        """ sends event (source is snmp """
