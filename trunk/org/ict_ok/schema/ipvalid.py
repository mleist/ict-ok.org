# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0612
#
"""implementation of IP valid schema
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.schema import TextLine

# ict_ok.org imports
from org.ict_ok.schema.IPy import IP
from org.ict_ok.schema.interfaces import NetIpValidError,\
     HostIpValidError, HostNetmaskValidError


class NetIpValid(TextLine):
    """ IP valid schema """
    def _validate(self, value):
        """ validation method for forms """
        ## call parent validations
        TextLine._validate(self, value)
        try:
            ## we only try to initialize an instance of IPy
            ip = IP(value)
        except:
            raise NetIpValidError(value, 1)


class HostIpValid(TextLine):
    """ IP valid schema """
    def _validate(self, value):
        """ validation method for forms """
        ## call parent validations
        TextLine._validate(self, value)
        try:
            ## we only try to initialize an instance of IPy
            ip = IP(value)
        except:
            raise HostIpValidError(value, 1)
        if ip.strNetmask() != '255.255.255.255':
            raise HostNetmaskValidError(value, 1)
