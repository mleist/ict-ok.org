# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232
#
"""Interface of SnmpValue"""

__version__ = "$Id$"

# zope imports
from zope.i18nmessageid import MessageFactory
from zope.schema import Bool, Choice, Int, TextLine, Float

# ict_ok.org imports
from org.ict_ok.components.interfaces import IComponent
from org.ict_ok.schema.snmpoidvalid import SnmpOidValid
from org.ict_ok.schema.physicalvalid import PhysicalQuantity, \
     PhysicalUnit

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

    #inpMultiplier = Float(
        #title=_(u"input multiplier"),
        #default=1.0,
        #required = True)

    inptype = Choice(
        title=_(u"Input Type"),
        description=_(u"Input Type"),
        default=u"cnt",
        required = True,
        vocabulary = "SnmpInpTypes")

    #inpUnit = Choice(
        #title=_(u"input dimension"),
        #description=_(u"input dimension"),
        #default=u"Mbit",
        #required = True,
        #vocabulary = "SnmpDimensionUnits")

    #displayUnitNumerator = Choice(
        #title=_(u"display dimension numerator"),
        #description=_(u"input dimension numerator"),
        #default=u"Mbit",
        #required = True,
        #vocabulary = "SnmpDimensionUnits")
    
    #displayUnitDenominator = Choice(
        #title=_(u"display dimension denominator"),
        #description=_(u"display dimension denominator"),
        #default=u"1",
        #required = True,
        #vocabulary = "SnmpTimeDimensionUnits")

    checkMax = Bool(
        title=_("max-checks"),
        description=_("enable check 'max' for this entry"),
        default=False,
        required=True)

    #checkMaxLevel = Int(
        #min=0,
        #max=100000000,
        #title=_("max level"),
        #description=_("'max'-level for this entry (bit/s)"),
        #default=100000,
        #required=False)

    #checkMaxLevelUnitNumerator = Choice(
        #title=_(u"max level dimension numerator"),
        #description=_(u"max level dimension numerator"),
        #default=u"bit",
        #required = False,
        #vocabulary = "SnmpDimensionUnits")

    #checkMaxLevelUnitDenominator = Choice(
        #title=_(u"max level dimension denominator"),
        #description=_(u"max level dimension denominator"),
        #default=u"1",
        #required = False,
        #vocabulary = "SnmpTimeDimensionUnits")

    snmpIndexType = Choice(
        title = _("SNMP index type"),
        vocabulary="SnmpIndexTypes",
        default = u"mac",
        required = True)

    #pq = PhysicalQuantity(
        #max_length=400,
        #title=_("Physical quantity"),
        #default=u"1.0 m/s",
        #required=False)

    #pu = PhysicalUnit(
        #max_length=400,
        #title=_("Physical unit"),
        #default=u"m/s",
        #required=False)

    #pu = PhysicalUnit(
        #max_length=400,
        #title=_("Physical unit"),
        #default=u"m/s",
        #required=False)

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
        default=u"b/s",
        required=False)

    displUnitAcceleration = PhysicalUnit(
        max_length=400,
        title=_("Display unit (acceleration)"),
        default=u"b/s2",
        required=False)

    maxQuantityAbs = PhysicalQuantity(
        max_length=400,
        title=_("Max. quantity"),
        default=u"1.0 b",
        required=False)

    maxQuantityVelocity = PhysicalQuantity(
        max_length=400,
        title=_("Max. quantity (velocity)"),
        default=u"1.0 b/s",
        required=False)

    maxQuantityAcceleration = PhysicalQuantity(
        max_length=400,
        title=_("Max. quantity (acceleration)"),
        default=u"1.0 b/s2",
        required=False)


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
