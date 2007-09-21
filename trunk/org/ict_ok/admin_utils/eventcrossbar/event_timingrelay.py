# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611
#
"""implementation of a "eventcrossbar daemon" 
"""

__version__ = "$Id$"

# phython imports
import datetime

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

# zc imports

# ict_ok.org imports
from org.ict_ok.admin_utils.eventcrossbar.interfaces import \
     IEventTimingRelay, IEventIfEventTimingRelay
from org.ict_ok.admin_utils.eventcrossbar.event_logic import \
     EventLogic


class EventTimingRelay(EventLogic):
    """
    timing relay with trigger- and reset-input and
    one delayed output
    """

    implements(IEventTimingRelay, IEventIfEventTimingRelay)

    timeStart = FieldProperty(IEventTimingRelay['timeStart'])
    timeDelta = FieldProperty(IEventTimingRelay['timeDelta'])
    isRunning = FieldProperty(IEventTimingRelay['isRunning'])
    eventInpObjs_trigger = FieldProperty(\
        IEventIfEventTimingRelay['eventInpObjs_trigger'])
    eventInpObjs_reset = FieldProperty(\
        IEventIfEventTimingRelay['eventInpObjs_reset'])
    eventOutObjs_delayed = FieldProperty(\
        IEventIfEventTimingRelay['eventOutObjs_delayed'])

    def __init__(self, **data):
        """
        constructor of the object
        """
        EventLogic.__init__(self, **data)
        for (name, value) in data.items():
            if name in IEventTimingRelay.names():
                setattr(self, name, value)

        self.ikRevision = __version__

    def tickerEvent(self):
        """ got ticker event from ticker thread """
        utcNow = datetime.datetime.utcnow()
        if self.isRunning:
            print "EventTimingRelay.tickerEvent (%s) running" % (self.getDcTitle())
            if self.timeStart + self.timeDelta <= utcNow:
                self.eventOut_delayed()
                self.isRunning = False
        else:
            pass
            print "EventTimingRelay.tickerEvent (%s)" % (self.getDcTitle())
        EventLogic.tickerEvent(self)

    def eventInp_trigger(self):
        """ sends delayed event """
        print "EventTimingRelay.eventInp_trigger"
        pass

    def eventInp_reset(self):
        """ sends delayed event """
        print "EventTimingRelay.eventInp_reset"
        pass

    def eventOut_delayed(self):
        """ sends delayed event """
        print "EventTimingRelay.eventOut_delayed"
        pass
        #for my_event in self.eventOutObjs_1sec:
            #inst_event = MsgEvent(self, my_event)
            #self.injectOutEQueue(inst_event)
