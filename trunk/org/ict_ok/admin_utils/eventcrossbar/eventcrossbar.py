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
import logging
from datetime import datetime
from pytz import timezone
from persistent.dict import PersistentDict

# zope imports
from zope.app import zapi
from zope.interface import implements
from zope.app.publisher.xmlrpc import MethodPublisher
from zope.dublincore.interfaces import IWriteZopeDublinCore
from zope.app.catalog.interfaces import ICatalog
from zope.app.intid.interfaces import IIntIds
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

# zc imports
from zc.queue import Queue

# ict_ok.org imports
from org.ict_ok.libs.history.entry import Entry
from org.ict_ok.components.superclass.interfaces import ISuperclass
from org.ict_ok.components.site.interfaces import ISite
from org.ict_ok.components.net.interfaces import INet
from org.ict_ok.components.host.interfaces import IHost
from org.ict_ok.components.interface.interfaces import IInterface
from org.ict_ok.components.service.interfaces import IService
from org.ict_ok.components.snmpvalue.interfaces import ISnmpValue
from org.ict_ok.admin_utils.ticker.interfaces import IAdmUtilTicker
from org.ict_ok.admin_utils.eventcrossbar.interfaces import IEventTimingRelay
from org.ict_ok.components.supernode.supernode import Supernode
from org.ict_ok.admin_utils.eventcrossbar.interfaces import \
     IAdmUtilEvent, IAdmUtilEventCrossbar, IEventTimingRelay
from org.ict_ok.admin_utils.eventcrossbar.interfaces import \
     IGlobalEventCrossbarUtility

logger = logging.getLogger("AdmUtilEventCrossbar")
berlinTZ = timezone('Europe/Berlin')


def AllObjectInstances(dummy_context):
    """Which objects are there
    """
    iid = zapi.getUtility(IIntIds, '')
    terms = []
    for (oid, oobj) in iid.items():
        if ISite.providedBy(oobj.object) or \
           INet.providedBy(oobj.object) or \
           IHost.providedBy(oobj.object) or \
           IInterface.providedBy(oobj.object) or \
           IService.providedBy(oobj.object) or \
           ISnmpValue.providedBy(oobj.object) or \
           IEventTimingRelay.providedBy(oobj.object):
            terms.append(\
                SimpleTerm(oobj.object.objectID,
                           str(oobj.object.objectID),
                           oobj.object.getDcTitle()))
    my_util = zapi.getUtility(IAdmUtilTicker)
    terms.append(\
        SimpleTerm(my_util.objectID,
                   str(my_util.objectID),
                   my_util.getDcTitle()))
    return SimpleVocabulary(terms)

def AllObjectInstancesWithEventInputs(dummy_context):
    """Which objects are there
    """
    iid = zapi.getUtility(IIntIds, '')
    terms = []
    for (oid, oobj) in iid.items():
        if ISite.providedBy(oobj.object) or \
           INet.providedBy(oobj.object) or \
           IHost.providedBy(oobj.object) or \
           IInterface.providedBy(oobj.object) or \
           IService.providedBy(oobj.object) or \
           ISnmpValue.providedBy(oobj.object) or \
           IEventTimingRelay.providedBy(oobj.object):
            inpEventNames = oobj.object.getAllInpEventNames()
            if len(inpEventNames) > 0:
                for inpEventName in inpEventNames:
                    myId = oobj.object.objectID + u'.' + inpEventName
                    terms.append(\
                        SimpleTerm(myId,
                                   str(myId),
                                   oobj.object.getDcTitle()+ u'->' + inpEventName))
    return SimpleVocabulary(terms)

def AllEventInstances(dummy_context):
    """Which events are there
    """
    eventXbar = zapi.getUtility(IAdmUtilEventCrossbar, '')
    terms = []
    for (oid, oobj) in eventXbar.items():
        if IAdmUtilEvent.providedBy(oobj):
            if oobj.ikComment is None:
                terms.append(\
                    SimpleTerm(oobj.objectID,
                               str(oobj.objectID),
                               oobj.getDcTitle()))
            else:
                terms.append(\
                    SimpleTerm(oobj.objectID,
                               str(oobj.objectID),
                               oobj.getDcTitle() + u' - ' + oobj.ikComment))
    return SimpleVocabulary(terms)

class AdmUtilEventCrossbar(Supernode):
    """Implementation of local EventCrossbar Utility"""

    implements(IAdmUtilEventCrossbar)

    lastEventCrossbar = "no signal since start"

    def __init__(self):
        Supernode.__init__(self)
        self.ikRevision = __version__
        self.inpEQueues = PersistentDict()
        self.outEQueues = PersistentDict()

    def receiveEventCrossbar(self, request, str_time, mode=None):
        """receive eventcrossbar signal
        """
        self.lastEventCrossbar = str_time
        dcore = IWriteZopeDublinCore(self)
        dcore.modified = datetime.now(berlinTZ)

    def getEventCrossbarTime(self):
        """get last eventcrossbar timestamp
        """
        try:
            retVal = self.lastEventCrossbar
        except NameError:
            self.__setattr__("lastEventCrossbar", "not set")
            retVal = self.lastEventCrossbar
        return retVal

    def makeNewObjQueue(self, senderObj):
        """ will create a new input and output queue for this sender object """
        objId = senderObj.getObjectId()
        if not self.inpEQueues.has_key(objId):
            self.inpEQueues[objId] = Queue()
        if not self.outEQueues.has_key(objId):
            self.outEQueues[objId] = Queue()
        return True

    def destroyObjQueue(self, senderObj):
        """ will destroy the input and output queue for this sender object """
        objId = senderObj.getObjectId()
        if self.inpEQueues.has_key(objId):
            del self.inpEQueues[objId]
        if self.outEQueues.has_key(objId):
            del self.outEQueues[objId]
        return True

    def injectEventFromObj(self, senderObj, event):
        """ will inject an event from the sender object
        into the accordant queue """
        objId = senderObj.getObjectId()
        if self.inpEQueues.has_key(objId):
            self.inpEQueues[objId].put(event)
            return True
        return False

    def processOutEQueues(self):
        for objId in self.outEQueues:
            outQueue = self.outEQueues[objId]
            while len(outQueue) > 0:
                my_catalog = zapi.getUtility(ICatalog)
                for result in my_catalog.searchResults(oid_index=objId):
                    event = iter(outQueue).next() # don't delete
                    if result.injectInpEQueue(event):
                        outQueue.pull() # now delete
    
    def processEvents(self):
        pass
        
    def processInpEQueues(self):
        my_catalog = zapi.getUtility(ICatalog)
        for senderOid in self.inpEQueues:
            inpQueue = self.inpEQueues[senderOid]
            while len(inpQueue) > 0:
                inpEvent = inpQueue.pull()
                processed = False
                for eventObj in self.values():
                    if IAdmUtilEvent.providedBy(eventObj):
                        if (senderOid in eventObj.inpObjects) and \
                           (eventObj.objectID == inpEvent.oidEventObject):
                            for receiverOid in eventObj.outObjects:
                                for receiverObj in my_catalog.searchResults(\
                                    oid_index=receiverOid):
                                    processed = True
                                    receiverObj.injectInpEQueue(inpEvent)
                if not processed:
                    inpEvent.stopit(self)

    def tickerEvent(self):
        for qid in self.inpEQueues:
            if len(self.inpEQueues[qid]) > 0:
                logger.info("tickerEvent (n:%s, n(i):%s, n(o):%s)" % \
                            (qid,
                             len(self.inpEQueues[qid]),
                             len(self.outEQueues[qid])
                             ))
        self.processOutEQueues()
        self.processEvents()
        self.processInpEQueues()
        #for eventObj in self.values():
            #if IEventTimingRelay.providedBy(eventObj):
                #eventObj.tickerEvent()
        
    def logIntoEvent(self, oidEventObject, logEntry):
        if self.has_key(oidEventObject):
            eventObject = self[oidEventObject]
            if eventObject.logAllEvents:
                newEntry = Entry(logEntry, eventObject, level=u"info")
                eventObject.history.append(newEntry)
                eventObject._p_changed = True


class GlobalEventCrossbarUtility(object):

    implements(IGlobalEventCrossbarUtility)

    lastEventCrossbar = "no signal since start"

    def __init__(self):
        self.subscriber_list = []
        super(GlobalEventCrossbarUtility, self).__init__(self)

    def subscribeToEventCrossbar(self, obj):
        if obj not in self.subscriber_list:
            self.subscriber_list.append(obj)

    def unsubscribeFromEventCrossbar(self, obj):
        if obj in self.subscriber_list:
            self.subscriber_list.remove(obj)

    def receiveEventCrossbar(self, request, str_time, str_mode=None):
        mode = None
        if str_mode.lower() in ['minute', 'hour', 'day',
                                'month', 'year', 'db_pack', 'db_pack_0']:
            mode = str_mode.lower()
        if mode == 'db_pack':
            size_pre = request.publication.db.getSize()
            request.publication.db.pack(days=5)
            size_post = request.publication.db.getSize()
            logger.info(u"GlobalEventCrossbarUtility / "
                        u"zodb packed %d -> %d" % \
                        (size_pre, size_post))
        if mode == 'db_pack_0':
            size_pre = request.publication.db.getSize()
            request.publication.db.pack(days=0)
            size_post = request.publication.db.getSize()
            logger.info(u"GlobalEventCrossbarUtility / "
                        u"zodb packed %d -> %d" % \
                        (size_pre, size_post))
        for obj in self.subscriber_list:
            obj.receiveEventCrossbar(request, str_time, mode)

    def getEventCrossbarTime(self):
        try:
            retVal = self.lastEventCrossbar
        except NameError:
            self.__setattr__("lastEventCrossbar", "not set")
            retVal = self.lastEventCrossbar
        return retVal


class AdmUtilEventCrossbarRpcMethods(MethodPublisher):
    def triggerEventCrossbarEvent(self, str_time, str_mode):
        from zope.proxy import removeAllProxies
        obj = removeAllProxies(self.context)
        obj.__setattr__("lastEventCrossbar", str_time)
        globalEventCrossbarUtility.receiveEventCrossbar(self.request,
                                                        str_time,
                                                        str_mode)
        
    def isUp(self):
        """reachable check on the XMLRPC-Interface"""
        logger.info(u"AdmUtilEventCrossbarRpcMethods::isUp (%s)" % \
                    self.__name__)
        return True

globalEventCrossbarUtility = GlobalEventCrossbarUtility()
    