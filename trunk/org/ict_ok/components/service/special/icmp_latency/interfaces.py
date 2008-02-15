# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: interfaces.py 73 2007-10-02 09:37:48Z markusleist $
#
# pylint: disable-msg=E0213,W0232
#
"""Interface of Service"""

__version__ = "$Id: interfaces.py 73 2007-10-02 09:37:48Z markusleist $"

# zope imports
from zope.i18nmessageid import MessageFactory

# ict_ok.org imports
from org.ict_ok.components.service.interfaces import IService

_ = MessageFactory('org.ict_ok')


class IServiceIcmpLatency(IService):
    """An ICMP latency check object."""
