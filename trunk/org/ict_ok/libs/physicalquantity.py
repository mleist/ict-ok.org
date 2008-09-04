# -*- coding: utf-8 -*-
#
# CopyrightPhysicalQuantityc) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232
#
"""Physical quantities for ict-ok.org
see http://juanreyero.com/magnitude/index.html
"""

__version__ = "$Id$"

# python imports
from magnitude import Magnitude, MagnitudeError


class PhysicalQuantity(Magnitude):
    """
    """

def physq(value, unit='', ounit=''):
    """Builds a Magnitude from a number and a units string"""
    pq = PhysicalQuantity(value)
    if unit:
        u = pq.sunit2mag(unit)
        pq.mult_by(u)
    if not ounit:
        ounit = unit
    pq.ounit(ounit)
    return pq

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
    except MagnitudeError:
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
    except MagnitudeError:
        return physq(-1.0)
    return physical_quantity

