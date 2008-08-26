# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0612
#
"""implementation of "physical unit" valid schema
"""

__version__ = "$Id$"

# python imports
from magnitude import mg, MagnitudeError

# zope imports
from zope.schema import TextLine

# ict_ok.org imports
from org.ict_ok.schema.interfaces import PhysicalQuantityValidError, \
     PhysicalUnitValidError


class PhysicalQuantity(TextLine):
    """ physical quantity valid schema
    content TextLine should be: '1.0 m/s'
    """
    def _validate(self, value):
        """ validation method for forms """
        ## call parent validations
        TextLine._validate(self, value)
        valList = value.split(' ', 1)
        try:
            numerical_value = float(valList[0])
            physical_unit = mg(numerical_value, valList[1])
        except ValueError:
            raise PhysicalQuantityValidError(value, 1)
        except MagnitudeError:
            raise PhysicalQuantityValidError(value, 1)

class PhysicalUnit(TextLine):
    """ physical unit valid schema """
    def _validate(self, value):
        """ validation method for forms """
        ## call parent validations
        TextLine._validate(self, value)
        try:
            physical_quantity = mg(1.0, value)
        except MagnitudeError:
            raise PhysicalUnitValidError(value, 1)
