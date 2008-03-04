# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0612,W0142
#
"""implementation of site """

__version__ = "$Id$"

# phython imports

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

# ict-ok.org imports
from org.ict_ok.components.superclass.superclass import MsgEvent
from org.ict_ok.components.component import Component
from org.ict_ok.components.site.interfaces import ISite, IEventIfEventSite
from org.ict_ok.components.net.interfaces import INet


class Site(Component):
    """ ICT_Ok site object """
    implements(ISite, IEventIfEventSite)
    sitename = FieldProperty(ISite['sitename'])
    eventInpObjs_inward_relaying_shutdown = FieldProperty(\
        IEventIfEventSite['eventInpObjs_inward_relaying_shutdown'])

    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        for (name, value) in data.items():
            if name in ISite.names():
                setattr(self, name, value)
        self.eventInpObjs_inward_relaying_shutdown = set([])
        self.ikRevision = __version__

    def eventInp_inward_relaying_shutdown(self, eventMsg=None):
        """
        forward the event to all objects in this container through the signal filter
        """
        print "Site.eventInp_inward_relaying_shutdown()"
        for name, obj in self.items():
            if ISite.providedBy(obj):
                targetFunctionName = "inward_relaying_shutdown"
            elif INet.providedBy(obj):
                targetFunctionName = "inward_relaying_shutdown"
            else:
                targetFunctionName = None
            if eventMsg is not None:
                inst_event = MsgEvent(senderObj = self,
                                      oidEventObject = eventMsg.oidEventObject,
                                      logText = u"inward relaying by site '%s'"\
                                      % self.ikName,
                                      targetFunctionName = targetFunctionName)
                eventMsg.stopit(self,
                                u"relaying by site '%s'" % self.ikName)
            else:
                inst_event = MsgEvent(senderObj = self,
                                      logText = u"inward relaying by site '%s'"\
                                      % self.ikName,
                                      targetFunctionName = targetFunctionName)
            obj.injectInpEQueue(inst_event)
