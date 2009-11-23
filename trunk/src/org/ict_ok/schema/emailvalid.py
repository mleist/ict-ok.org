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
"""implementation of e-mail address valid schema
"""

__version__ = "$Id$"

# python imports
from re import match

# zope imports
from zope.schema import TextLine

# ict_ok.org imports
from org.ict_ok.schema.interfaces import EmailValidError


class EmailValid(TextLine):
    """ Email address valid schema """
    def _validate(self, value):
        """ validation method for forms """
        ## call parent validations
        TextLine._validate(self, value)
        # from http://www.regular-expressions.info/email.html
        regStrg = r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+" +\
                "(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@" +\
                "(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+" +\
                "[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
        if not match(regStrg, value.lower()):
            raise EmailValidError(value, 1)
