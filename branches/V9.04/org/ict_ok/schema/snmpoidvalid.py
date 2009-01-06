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
"""implementation of IP valid schema
"""

__version__ = "$Id$"

# python imports
from re import match

# zope imports
from zope.schema import TextLine

# ict_ok.org imports
from org.ict_ok.schema.interfaces import SnmpOidValidError


class SnmpOidValid(TextLine):
    """ snmp oid address valid schema """
    def _validate(self, value):
        """ validation method for forms """
        ## call parent validations
        TextLine._validate(self, value)
        regStrg = r"^([\.0-9a-zA-Z\$]*)$"
        if not match(regStrg, value.upper()):
            raise SnmpOidValidError(value, 1)
