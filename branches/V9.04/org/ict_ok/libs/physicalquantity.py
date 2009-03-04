# -*- coding: utf-8 -*-
#
# CopyrightPhysicalQuantityc) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232,W0212
#
"""Physical quantities for ict-ok.org
see http://juanreyero.com/magnitude/index.html
"""

__version__ = "$Id$"

# python imports
import magnitude
#from magnitude import Magnitude, MagnitudeError

# zope imports
from zope.security.checker import BasicTypes, NoProxy

if not magnitude._mags.has_key('Euro'):
    magnitude.new_mag('Euro', magnitude.Magnitude(1.0, dollar=1))
if not magnitude._mags.has_key('Unit'):
    magnitude.new_mag('Unit', magnitude.Magnitude(1.0, bit=1))


class PhysicalQuantity(magnitude.Magnitude):
    """
    our own wrapper class
    """
    def isLength(self):
        # ['m', 's', 'K', 'kg', 'A', 'mol', 'cd', '$', 'bit']
        return self.unit == [1,0,0,0,0,0,0,0,0]

def physq(value, unit='', ounit=''):
    """Builds a Magnitude from a number and a units string"""
    phq = PhysicalQuantity(value)
    if unit:
        tmp_u = phq.sunit2mag(unit)
        phq.mult_by(tmp_u)
    if not ounit:
        ounit = unit
    phq.ounit(ounit)
    return phq

def convertQuantity(inpString):
    """converts an input string to the physical quantity
    """
    if not inpString:
        return None
    try:
        valList = inpString.split(' ', 1)
        numerical_value = float(valList[0])
        if len(valList) > 1:
            physical_quantity = physq(numerical_value, valList[1])
        else:
            physical_quantity = physq(numerical_value, "")
    except ValueError:
        return physq(-1.0)
    except magnitude.MagnitudeError:
        return physq(-1.0)
    return physical_quantity

def convertUnit(inpString):
    """converts an input string to the physical unit of
    the quantity 1.0
    """
    if not inpString:
        return None
    try:
        physical_quantity = physq(1.0, inpString)
    except ValueError:
        return physq(-1.0)
    except magnitude.MagnitudeError:
        return physq(-1.0)
    return physical_quantity

# PhysicalQuantity and magnitude.Magnitude shouldn't use security proxy
BasicTypes.update({PhysicalQuantity: NoProxy,
                   magnitude.Magnitude: NoProxy,
                   })
