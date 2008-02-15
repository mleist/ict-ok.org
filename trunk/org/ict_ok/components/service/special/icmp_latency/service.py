# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: service.py 73 2007-10-02 09:37:48Z markusleist $
#
# pylint: disable-msg=E1101,W0142
#
"""implementation of Service

Service does ....

"""

__version__ = "$Id: service.py 73 2007-10-02 09:37:48Z markusleist $"

# phython imports

# zope imports
from zope.interface import implements

# ict_ok.org imports
from org.ict_ok.components.service.special.icmp_latency.interfaces import \
     IServiceIcmpLatency
from org.ict_ok.components.service.service import Service as ServiceBase


class Service(ServiceBase):
    """
    the template instance
    """

    implements(IServiceIcmpLatency)
    
    def tickerEvent(self):
        """
        got ticker event from ticker thread
        """
        #print "ServiceIcmpLatency.tickerEvent   "
        ServiceBase.tickerEvent(self)
