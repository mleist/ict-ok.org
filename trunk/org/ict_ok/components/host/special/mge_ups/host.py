# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0612,W0142
#
"""implementation of host object

host object represents a MGE UPS
tested with MGE Galaxy 3000
"""

__version__ = "$Id$"

# phython imports

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

# ict_ok.org imports
from org.ict_ok.components.host.special.mge_ups.interfaces import \
     IHostMgeUps, IEventIfHostMgeUps
from org.ict_ok.components.host.host import Host as HostBase
from org.ict_ok.components.superclass.superclass import MsgEvent


class Host(HostBase):
    """A MGE UPS object."""

    implements(IHostMgeUps, IEventIfHostMgeUps)

    eventOutObjs_onBattery = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_onBattery'])
    eventOutObjs_powerReturned = FieldProperty(\
        IEventIfHostMgeUps['eventOutObjs_powerReturned'])

    def eventOut_onBattery(self):
        """ sends 'on battery' event """
        print "Host.eventOut_onBattery   (MGE)"
        for my_event in self.eventOutObjs_onBattery:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def eventOut_powerReturned(self):
        """ sends 'power returned' event """
        print "Host.eventOut_powerReturned   (MGE)"
        for my_event in self.eventOutObjs_powerReturned:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)

    def tickerEvent(self):
        """
        got ticker event from ticker thread
        """
        #print "Host.tickerEvent   (MGE)"
        HostBase.tickerEvent(self)
