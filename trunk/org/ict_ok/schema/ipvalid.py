# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
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

# phython imports

# zope imports
from zope.schema import TextLine

# ict_ok.org imports
from org.ict_ok.schema.IPy import IP
from org.ict_ok.schema.interfaces import IpValidError


class IpValid(TextLine):
    """ IP valid schema """
    def _validate(self, value):
        """ validation method for forms """
        ## call parent validations
        TextLine._validate(self, value)
        try:
            ## we only try to initialize an instance of IPy
            ip = IP(value)
        except:
            raise IpValidError(value, 1)
