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
from zope.interface import implements
from zope.app.publisher.xmlrpc import MethodPublisher
from zope.dublincore.interfaces import IWriteZopeDublinCore
from zope.app.catalog.interfaces import ICatalog

# zc imports
from zc.queue.interfaces import IQueue
from zc.queue import Queue

# ict_ok.org imports
from org.ict_ok.components.supernode.supernode import Supernode
from org.ict_ok.admin_utils.eventcrossbar.interfaces import \
     IAdmUtilEventCrossbar
from org.ict_ok.admin_utils.eventcrossbar.interfaces import \
     IGlobalEventCrossbarUtility
from org.ict_ok.admin_utils.eventcrossbar.interfaces import \
     IContentDDD

logger = logging.getLogger("AdmUtilEventCrossbar")
berlinTZ = timezone('Europe/Berlin')






class AdmUtilEventCrossbar(Supernode):
    """Implementation of local EventCrossbar Utility"""

    implements(IAdmUtilEventCrossbar)

    lastEventCrossbar = "no signal since start"

    def __init__(self):
        #super(AdmUtilEventCrossbar, self).__init__(self)
        #IAdmUtilEventCrossbar.__init__(self)
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
        """ will inject an event from the sender object into the accordant queue """
        objId = senderObj.getObjectId()
        #print "injectEventFromObj / %s" % (objId)
        for i in self.inpEQueues:
            print "i: ", i
        if self.inpEQueues.has_key(objId):
            self.inpEQueues[objId].put(event)
            return True
        return False

    def processOutEQueues(self):
        #print "processOutEQueues(%s)" % (self.getDcTitle())
        for objId in self.outEQueues:
            outQueue = self.outEQueues[objId]
            if len(outQueue) > 0:
                my_catalog = zapi.getUtility(ICatalog)
                for result in my_catalog.searchResults(oid_index=objId):
                    event = iter(outQueue).next() # don't delete
                    if result.injectFromEventXbar(self, event):
                        outQueue.pull() # now delete
    
    def processEvents(self):
        #print "processEvents(%s)" % (self.getDcTitle())
        pass
        
    def processInpEQueues(self):
        pass

    def tickerEvent(self):
        #print "AdmUtilEventCrossbar.tickerEvent: (%s, %s)" % \
              #(self.inpEQueues, self.outEQueues)
        #for i in self.inpEQueues:
            #print "i:", i
        for qid in self.inpEQueues:
            if len(self.inpEQueues[qid]) > 0:
                logger.info("tickerEvent (n:%s, n(i):%s, n(o):%s)" % \
                            (qid,
                             len(self.inpEQueues[qid]),
                             len(self.outEQueues[qid])
                             ))
            #else:
                #logger.info("tickerEvent (n:%s, n(i):%s)" % \
                            #(qid, len(self.inpEQueues[qid])))
        self.processOutEQueues()
        self.processEvents()
        self.processInpEQueues()

class GlobalEventCrossbarUtility(object):

    implements(IGlobalEventCrossbarUtility)

    lastEventCrossbar = "no signal since start"

    def __init__(self):
        #logger.info(u"GlobalEventCrossbarUtility started")
        self.subscriber_list = []
        super(GlobalEventCrossbarUtility, self).__init__(self)

    def subscribeToEventCrossbar(self, obj):
        #logger.info(u"GlobalEventCrossbarUtility::"
                    #u"subscribe2eventcrossbar(%s)" % obj)
        if obj not in self.subscriber_list:
            self.subscriber_list.append(obj)

    def unsubscribeFromEventCrossbar(self, obj):
        #logger.info(u"GlobalEventCrossbarUtility::"
                    #u"unsubscribeFromEventCrossbar(%s)" % obj)
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
        #from pprint import pprint
        #pprint(self.subscriber_list)
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

class ContentDDD(object):
    implements(IContentDDD)
    var = True
    