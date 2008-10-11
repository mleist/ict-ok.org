# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=F0401,E1101,E1102,E0611,W0703,W0612,W0142
#
"""implementation of Latency

Latency does ....

"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.app import zapi

# ict_ok.org imports
from org.ict_ok.components.component import Component
from org.ict_ok.components.latency.interfaces import ILatency


class Latency(Component):
    """
    the template instance
    """

    implements(ILatency)
    # for ..Contained we have to:
    __name__ = __parent__ = None
    checkcount = FieldProperty(ILatency['checkcount'])

    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        for (name, value) in data.items():
            if name in ILatency.names():
                setattr(self, name, value)
        self.ikRevision = __version__
        
    def get_health(self):
        """
        output of health, 0-1 (float)
        """
        return None

    def tickerEvent(self):
        """ trigger from ticker
        """
        pass
        
    def triggerMin(self):
        """ got ticker event from ticker thread every minute
        """
        pass

    def getRrdFilename(self):
        """ rrd filename incl. path
        """
        data_path = zapi.getPath(self)
        return "/opt/smokeping/data/%s.rrd" % data_path
