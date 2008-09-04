# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0213,E0211,W0232
#
"""Interface of SnmpValue"""

__version__ = "$Id$"

# zope imports
from zope.i18nmessageid import MessageFactory
from zope.interface import Invalid, invariant
from zope.schema import Bool, Choice

# ict_ok.org imports
from org.ict_ok.components.interfaces import IComponent
from org.ict_ok.schema.snmpoidvalid import SnmpOidValid
from org.ict_ok.schema.physicalvalid import PhysicalQuantity, \
     PhysicalUnit
from org.ict_ok.libs.physicalquantity import physq, convertQuantity, \
     convertUnit

_ = MessageFactory('org.ict_ok')


class ISnmpValue(IComponent):
    """A service object."""

    checktype = Choice(
        title=_(u"Check Type"),
        default=u"oid",
        required = True,
        vocabulary = "SnmpCheckTypes")

    oid1 = SnmpOidValid(
        max_length=400,
        title=_("OID1"),
        description=_("OID1"),
        default=u"1.3.6.1.2.1.1.1.0",
        required=False)

    oid2 = SnmpOidValid(
        max_length=400,
        title=_("OID2"),
        description=_("OID2"),
        default=u"1.3.6.1.2.1.1.1.0",
        required=False)

    cmd = Choice(
        title=_(u"Check Command"),
        description=_(u"Check Command"),
        default=u"none",
        required = True,
        vocabulary = "SnmpCheckCmds")

    inptype = Choice(
        title=_(u"Input Type"),
        description=_(u"Input Type"),
        default=u"cnt",
        required = True,
        vocabulary = "SnmpInpTypes")

    displayMinMax = Bool(
        title=_("diplay min/max"),
        description=_("enable the display of min and max values"),
        default=False,
        required=True)
    
    checkMax = Bool(
        title=_("max-checks"),
        description=_("enable check 'max' for this entry"),
        default=False,
        required=True)

    snmpIndexType = Choice(
        title = _("SNMP index type"),
        vocabulary="SnmpIndexTypes",
        default = u"mac",
        required = True)

    inpQuantity = PhysicalQuantity(
        max_length=400,
        title=_("Input quantity"),
        default=u"8.0 bit",
        required=True)

    displUnitAbs = PhysicalUnit(
        max_length=400,
        title=_("Display unit"),
        default=u"b",
        required=True)

    displUnitVelocity = PhysicalUnit(
        max_length=400,
        title=_("Display unit (velocity)"),
        required=False)

    displUnitAcceleration = PhysicalUnit(
        max_length=400,
        title=_("Display unit (acceleration)"),
        required=False)

    maxQuantityAbs = PhysicalQuantity(
        max_length=400,
        title=_("Max. quantity"),
        required=False)

    maxQuantityVelocity = PhysicalQuantity(
        max_length=400,
        title=_("Max. quantity (velocity)"),
        required=False)

    maxQuantityAcceleration = PhysicalQuantity(
        max_length=400,
        title=_("Max. quantity (acceleration)"),
        required=False)
    
    @invariant
    def ensureC1(obj_snmp):
        """The input quantity must have a dimension
        """
        convPQinpQuantity = convertQuantity(obj_snmp.inpQuantity)
        if convPQinpQuantity.dimensionless():
            raise Invalid("The input quantity '%s' must have a dimension" \
                          % (convPQinpQuantity))

    @invariant
    def ensureC3(obj_snmp):
        """The input quantity and the display unit must
        have the same dimension
        """
        convPQinpQuantity = convertQuantity(obj_snmp.inpQuantity)
        convPUdisplUnitAbs = convertUnit(obj_snmp.displUnitAbs)
        physFactor = convPUdisplUnitAbs / convPQinpQuantity
        if not physFactor.dimensionless():
            raise Invalid("The input quantity '%s' and the "\
                          "display unit '%s'"\
                          " must have the same dimension" \
                          % (convPQinpQuantity, convPUdisplUnitAbs))

    @invariant
    def ensureC4(obj_snmp):
        """The input quantity and the display unit (velocity) * s
        must have the same dimension
        """
        if obj_snmp.displUnitVelocity:
            convPQinpQuantity = convertQuantity(obj_snmp.inpQuantity)
            convPUdisplUnitVelocity = convertUnit(obj_snmp.displUnitVelocity)
            physFactor = convPUdisplUnitVelocity \
                       / convPQinpQuantity \
                       * physq(1.0, "s")
            if not physFactor.dimensionless():
                raise Invalid("The input quantity '%s' and the "\
                              "display unit (velocity) '%s' * s"\
                              " must have the same dimension" \
                              % (convPQinpQuantity, convPUdisplUnitVelocity))

    @invariant
    def ensureC5(obj_snmp):
        """The input quantity and the display unit (acceleration) * s * s
        must have the same dimension
        """
        if obj_snmp.displUnitAcceleration:
            convPQinpQuantity = convertQuantity(obj_snmp.inpQuantity)
            convPUdisplUnitAcceleration = convertUnit(\
                obj_snmp.displUnitAcceleration)
            physFactor = convPUdisplUnitAcceleration \
                       / convPQinpQuantity \
                       * physq(1.0, "s2")
            if not physFactor.dimensionless():
                raise Invalid("The input quantity '%s' and the "\
                              "display unit (acceleration) '%s' * s * s"\
                              " must have the same dimension" \
                              % (convPQinpQuantity,
                                 convPUdisplUnitAcceleration))

    @invariant
    def ensureC6(obj_snmp):
        """The input quantity and the max unit must have the same dimension
        """
        if obj_snmp.maxQuantityAbs:
            convPQinpQuantity = convertQuantity(obj_snmp.inpQuantity)
            convPQmaxQuantityAbs = convertQuantity(obj_snmp.maxQuantityAbs)
            physFactor = convPQinpQuantity / convPQmaxQuantityAbs
            if not physFactor.dimensionless():
                raise Invalid("The input quantity '%s' and the "\
                              "max unit '%s'"\
                              " must have the same dimension" \
                              % (convPQinpQuantity, convPQmaxQuantityAbs))

    @invariant
    def ensureC7(obj_snmp):
        """The input quantity and the max unit (velocity) '%s' * s
        must have the same dimension
        """
        if obj_snmp.maxQuantityVelocity:
            convPQinpQuantity = convertQuantity(obj_snmp.inpQuantity)
            convPQmaxQuantityVelocity = convertQuantity(\
                obj_snmp.maxQuantityVelocity)
            physFactor = convPQmaxQuantityVelocity \
                       / convPQinpQuantity \
                       * physq(1.0, "s")
            if not physFactor.dimensionless():
                raise Invalid("The input quantity '%s' and the "\
                              "max unit (velocity) '%s' * s"\
                              " must have the same dimension" \
                              % (convPQinpQuantity,
                                 convPQmaxQuantityVelocity))

    @invariant
    def ensureC8(obj_snmp):
        """The input quantity and the max unit (acceleration) * s * s
        must have the same dimension
        """
        if obj_snmp.maxQuantityAcceleration:
            convPQinpQuantity = convertQuantity(obj_snmp.inpQuantity)
            convPQmaxQuantityAcceleration = convertQuantity(\
                obj_snmp.maxQuantityAcceleration)
            physFactor = convPQmaxQuantityAcceleration \
                       / convPQinpQuantity \
                       * physq(1.0, "s2")
            if not physFactor.dimensionless():
                raise Invalid("The input quantity '%s' and the "\
                              "max unit (acceleration) '%s' * s * s"\
                              " must have the same dimension" \
                              % (convPQinpQuantity,
                                 convPQmaxQuantityAcceleration))

    def getInputPhysical():
        """ return inpunt physical as PhysicalQuantity
        """
    def getDisplayPhysical():
        """ return display physical as PhysicalQuantity
        """
    def getMyFactor():
        """ factor for adaption from inpType to displayType
        """
    def convertQuantity(inpString):
        """converts an input string to the physical quantity
        """
    def convertUnit(inpString):
        """converts an input string to the physical unit of
        the quantity 1.0
        """
    def getPQinpQuantity(self):
        """convertQuantity(self.inpQuantity)
        """
    def getPUdisplUnitAbs(self):
        """convertUnit(self.displUnitAbs)
        """
    def getPUdisplUnitVelocity(self):
        """convertUnit(self.displUnitVelocity)
        """
    def getPUdisplUnitAcceleration(self):
        """convertUnit(self.displUnitAcceleration)
        """
    def getPQmaxQuantityAbs(self):
        """convertQuantity(self.maxQuantityAbs)
        """
    def getPQmaxQuantityVelocity(self):
        """convertQuantity(self.maxQuantityVelocity)
        """
    def getPQmaxQuantityAcceleration(self):
        """convertQuantity(self.maxQuantityAcceleration)
        """
    def getRrdFilename(self):
        """ rrd filename incl. path
        """
    def getRawSnmpValue(self):
        """ get raw snmp-Value without multiplier
        """
    def getSnmpValue(self):
        """ get SnmpValue as physical value
        """
