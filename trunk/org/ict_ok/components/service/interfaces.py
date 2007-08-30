# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0213,W0232
#
"""Interface of Service"""

__version__ = "$Id$"

# zope imports
from zope.i18nmessageid import MessageFactory

# ict_ok.org imports
from org.ict_ok.components.supernode.interfaces import ISupernode

_ = MessageFactory('org.ict_ok')


class IService(ISupernode):
    """A service object."""

