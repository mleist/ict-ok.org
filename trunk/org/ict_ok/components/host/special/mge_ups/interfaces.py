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

    def eventOut_upsBatteryFault():
        """ sends event (source is snmp """
    def eventOut_upsBatteryOK():
        """ sends event (source is snmp """
    def eventOut_upsBatteryReplacementIndicated():
        """ sends event (source is snmp """
    def eventOut_upsBatteryReplacementNotIndicated():
        """ sends event (source is snmp """
    def eventOut_upsAtLowBattery():
        """ sends event (source is snmp """
    def eventOut_upsFromLowBattery():
        """ sends event (source is snmp """
    def eventOut_upsChargerFault():
        """ sends event (source is snmp """
    def eventOut_upsChargerOK():
        """ sends event (source is snmp """
    def eventOut_upsAtLowCondition():
        """ sends event (source is snmp """
    def eventOut_upsFromLowCondition():
        """ sends event (source is snmp """
    def eventOut_upsOnBattery():
        """ sends event (source is snmp """
    def eventOut_upsReturnFromBattery():
        """ sends event (source is snmp """
    def eventOut_upsOnByPass():
        """ sends event (source is snmp """
    def eventOut_upsReturnFromByPass():
        """ sends event (source is snmp """
    def eventOut_upsByPassUnavailable():
        """ sends event (source is snmp """
    def eventOut_upsByPassAvailable():
        """ sends event (source is snmp """
    def eventOut_upsUtilityFailure():
        """ sends event (source is snmp """
    def eventOut_upsUtilityRestored():
        """ sends event (source is snmp """
    def eventOut_upsOnBoost():
        """ sends event (source is snmp """
    def eventOut_upsReturnFromBoost():
        """ sends event (source is snmp """
    def eventOut_upsOverLoad():
        """ sends event (source is snmp """
    def eventOut_upsLoadOK():
        """ sends event (source is snmp """
    def eventOut_upsOverTemperature():
        """ sends event (source is snmp """
    def eventOut_upsTemperatureOK():
        """ sends event (source is snmp """
    def eventOut_upsCommunicationFailure():
        """ sends event (source is snmp """
    def eventOut_upsCommunicationRestored():
        """ sends event (source is snmp """
    def eventOut_upsInputBad():
        """ sends event (source is snmp """
    def eventOut_upsInputOK():
        """ sends event (source is snmp """
    def eventOut_upsBatteryUnavailable():
        """ sends event (source is snmp """
    def eventOut_upsBatteryAvailable():
        """ sends event (source is snmp """
    def eventOut_upsAtLowRecharge():
        """ sends event (source is snmp """
    def eventOut_upsFromLowRecharge():
        """ sends event (source is snmp """
    def eventOut_upsDiagnosticTestFail():
        """ sends event (source is snmp """
    def eventOut_upsDiagnosticTestOK():
        """ sends event (source is snmp """
    def eventOut_upsBatteryTestOK():
        """ sends event (source is snmp """
    def eventOut_upsBatteryTestFail():
        """ sends event (source is snmp """
    def eventOut_upsExternalAlarmActive():
        """ sends event (source is snmp """
    def eventOut_upsExternalAlarmInactive():
        """ sends event (source is snmp """
    def eventOut_upsOnBuck():
        """ sends event (source is snmp """
    def eventOut_upsReturnFromBuck():
        """ sends event (source is snmp """
    def eventOut_upsmgEnvironmentComFailure():
        """ sends event (source is snmp """
    def eventOut_upsmgEnvironmentComOK():
        """ sends event (source is snmp """
    def eventOut_upsmgEnvironmentTemperatureLow():
        """ sends event (source is snmp """
    def eventOut_upsmgEnvironmentTemperatureHigh():
        """ sends event (source is snmp """
    def eventOut_upsmgEnvironmentTemperatureOK():
        """ sends event (source is snmp """
    def eventOut_upsmgEnvironmentHumidityLow():
        """ sends event (source is snmp """
    def eventOut_upsmgEnvironmentHumidityHigh():
        """ sends event (source is snmp """
    def eventOut_upsmgEnvironmentHumidityOK():
        """ sends event (source is snmp """
    def eventOut_upsmgEnvironmentInput1Closed():
        """ sends event (source is snmp """
    def eventOut_upsmgEnvironmentInput1Open():
        """ sends event (source is snmp """
    def eventOut_upsmgEnvironmentInput2Closed():
        """ sends event (source is snmp """
    def eventOut_upsmgEnvironmentInput2Open():
        """ sends event (source is snmp """
