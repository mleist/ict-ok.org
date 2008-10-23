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
"""Interface of schema
"""

__version__ = "$Id$"

# zope imports
from zope.schema.interfaces import ITextLine
from zope.schema.interfaces import IText, IDatetime
from zope.schema._bootstrapinterfaces import ValidationError
from zope.i18nmessageid import MessageFactory

# ict_ok.org imports

_ = MessageFactory('org.ict_ok')


class IpValidError(ValidationError):
    """Error notification for non valid IPv4-Address"""
    __doc__ = _("""IP-address not ok""")

class HostIpValidError(ValidationError):
    """Error notification for non valid IPv4-Address"""
    __doc__ = _("""Host IP-address not ok""")

class HostNetmaskValidError(ValidationError):
    """Error notification for non valid IPv4-Address"""
    __doc__ = _("""Host IP-address has wrong netmask""")

class NetIpValidError(ValidationError):
    """Error notification for non valid IPv4-Address"""
    __doc__ = _("""Network IP-address not ok""")

class MacValidError(ValidationError):
    """Error notification for non valid IPv4-Address"""
    __doc__ = _("""IP-address not ok""")

class ColorValidError(ValidationError):
    """Error notification for non valid Email-Address"""
    __doc__ = _("""Color not ok (#rrggbb)""")

class EmailValidError(ValidationError):
    """Error notification for non valid Email-Address"""
    __doc__ = _("""Email-address not ok""")

class SnmpOidValidError(ValidationError):
    """Error notification for non valid SNMP-OID-Address"""
    __doc__ = _("""SNMP oid not ok""")

class NetsValidError(ValidationError):
    """Error notification for non valid IPv4-Address-List"""
    __doc__ = _("""netaddress is not ok""")

class ObjectIdValidError(ValidationError):
    """Error notification for non valid Universe ID"""
    __doc__ = _("""Universe ID not ok""")

class PhysicalQuantityValidError(ValidationError):
    """Error notification for non valid physical value"""
    __doc__ = _("""Physical quantity not ok""")
class PhysicalUnitValidError(ValidationError):
    """Error notification for non valid physical value"""
    __doc__ = _("""Physical unit not ok""")

class IIpV4Valid(ITextLine):
    """A field containing an IPv4-Address
    """

class IMacValid(ITextLine):
    """A field containing an IPv4-Address
    """

class IPhysicalQuantityValid(ITextLine):
    """A field containing a physical quantity
    """

class IPhysicalUnitValid(ITextLine):
    """A field containing a physical unit
    """

class IV4NetsValid(IText):
    """A field containing a list of IPv4-Addresses
    """

class IObjectIdValid(ITextLine):
    """A field containing an Universe ID
    """

class IIctDatetime(IDatetime):
    """Interface for special ict-ok purpose
    """
