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
from org.ict_ok.schema.interfaces import ObjectIdValidError
# ict_ok.org imports
#from org.ict_ok.schema.interfaces import ObjectIdValidError


class ObjectIdValid(TextLine):
    """A field containing an Universe ID
    """
    def _validate(self, arg_value):
        """ validation method for forms """
        ## call parent validations
        TextLine._validate(self, arg_value)
        try:
            value = str(arg_value)
            uid = value[:-1]
            crc = value[-1]
            icrc_cmp = 0
            int_list = [int(i,16) for i in uid]
            for i in int_list:
                icrc_cmp ^= i
            crc_cmp = u"%x" % icrc_cmp
            if crc != crc_cmp:
                raise ObjectIdValidError(value, 1)
        except:
            raise ObjectIdValidError(value, 1)
