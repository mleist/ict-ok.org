# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0142
#
"""implementation of Service

Service does ....

"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements

# ict_ok.org imports
from org.ict_ok.components.service.special.ssh.interfaces import \
     IServiceSsh
from org.ict_ok.components.service.service import Service as ServiceBase


class Service(ServiceBase):
    """
    the template instance
    """

    implements(IServiceSsh)
    
    def tickerEvent(self):
        """
        got ticker event from ticker thread
        """
        #print "ServiceSsh.tickerEvent   "
        ServiceBase.tickerEvent(self)
