# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
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
from org.ict_ok.components.superclass.superclass import isOidInCatalog
from org.ict_ok.admin_utils.eventcrossbar.interfaces import \
     IEventTimer, IEventIfEventTimer
from org.ict_ok.admin_utils.eventcrossbar.event_logic import \
     EventLogic
from org.ict_ok.components.superclass.superclass import MsgEvent


class EventTimer(EventLogic):
    """
    timer with start- and stop-input and
    one pulse output
    """

    implements(IEventTimer, IEventIfEventTimer)

    timeNext = FieldProperty(IEventTimer['timeNext'])
    timePulse = FieldProperty(IEventTimer['timePulse'])
    isRunning = FieldProperty(IEventTimer['isRunning'])
    eventInpObjs_start = FieldProperty(\
        IEventIfEventTimer['eventInpObjs_start'])
    eventInpObjs_stop = FieldProperty(\
        IEventIfEventTimer['eventInpObjs_stop'])
    eventOutObjs_pulse = FieldProperty(\
        IEventIfEventTimer['eventOutObjs_pulse'])

    def __init__(self, **data):
        """
        constructor of the object
        """
        EventLogic.__init__(self, **data)
        self.eventInpObjs_start = set([])
        self.eventInpObjs_stop = set([])
        self.eventOutObjs_pulse = set([])
        for (name, value) in data.items():
            if name in IEventTimer.names() or \
               name in IEventIfEventTimer.names():
                setattr(self, name, value)
        self.ikRevision = __version__
        
    def removeInvalidOidFromInpOutObjects(self):
        """ delete all invalid oids 
        oids not in catalog will be deleted (exclude ticker)
        """
        removeIDs = []
        for oid in self.eventInpObjs_start:
            if not isOidInCatalog(oid):
                removeIDs.append(oid)
        for oid in removeIDs:
            self.eventInpObjs_start.remove(oid)
        removeIDs = []
        for oid in self.eventInpObjs_stop:
            if not isOidInCatalog(oid):
                removeIDs.append(oid)
        for oid in removeIDs:
            self.eventInpObjs_stop.remove(oid)
        removeIDs = []
        for oid in self.eventOutObjs_pulse:
            if not isOidInCatalog(oid):
                removeIDs.append(oid)
        for oid in removeIDs:
            self.eventOutObjs_pulse.remove(oid)

    def tickerEvent(self):
        """ got ticker event from ticker thread """
        #print "EventTimer.tickerEvent"
        utcNow = datetime.datetime.utcnow()
        if self.isRunning:
            if utcNow >= self.timeNext:
                IEventTimer['timeNext'].readonly = False
                self.timeNext = utcNow + self.timePulse
                IEventTimer['timeNext'].readonly = True
                self.eventOut_pulse()
        else:
            pass
        # and up to superclass
        EventLogic.tickerEvent(self)

    def eventInp_start(self, eventMsg=None):
        """ start the timer """
        #print "EventTimer.eventInp_start"
        if not self.isRunning:
            self.isRunning = True
            IEventTimer['timeNext'].readonly = False
            self.timeNext = datetime.datetime.utcnow() + self.timePulse
            IEventTimer['timeNext'].readonly = True

    def eventInp_stop(self, eventMsg=None):
        """ stop the timer """
        #print "EventTimer.eventInp_stop"
        if self.isRunning:
            self.isRunning = False
            IEventTimer['timeNext'].readonly = False
            self.timeNext = datetime.datetime(1901, 1, 1, 0, 0)
            IEventTimer['timeNext'].readonly = True

    def eventOut_pulse(self):
        """ sends pulse event """
        for my_event in self.eventOutObjs_pulse:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)
