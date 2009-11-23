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
from zope.schema import Datetime
from zope.interface import implements

# ict_ok.org imports
from org.ict_ok.schema.interfaces import IIctDatetime

class IctDatetime(Datetime):
    """ special ict-ok purpose """
    implements(IIctDatetime)
