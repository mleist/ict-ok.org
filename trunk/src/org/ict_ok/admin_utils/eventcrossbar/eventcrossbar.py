# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0613,W0612
#
"""implementation of a "eventcrossbar daemon" 
"""

__version__ = "$Id$"

# python imports
import logging
import os
from datetime import datetime
from pytz import timezone
from persistent.dict import PersistentDict

# zope imports
from zope.app import zapi
from zope.interface import implements
from zope.component.interfaces import ComponentLookupError
from zope.app.publisher.xmlrpc import MethodPublisher
from zope.dublincore.interfaces import IWriteZopeDublinCore
from zope.app.catalog.interfaces import ICatalog
from zope.app.intid.interfaces import IIntIds
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.component import queryUtility

# zc imports
from zc.queue import Queue

# ict_ok.org imports
from org.ict_ok.libs.history.entry import Entry
from org.ict_ok.components.site.interfaces import ISite
from org.ict_ok.components.ipnet.interfaces import IIpNet
from org.ict_ok.components.host.interfaces import IHost
from org.ict_ok.components.interface.interfaces import IInterface
from org.ict_ok.components.service.interfaces import IService
from org.ict_ok.components.snmpvalue.interfaces import ISnmpValue
from org.ict_ok.components.supernode.supernode import Supernode
from org.ict_ok.admin_utils.eventcrossbar.interfaces import \
     IAdmUtilEvent, IAdmUtilEventCrossbar, IEventLogic
from org.ict_ok.admin_utils.eventcrossbar.interfaces import \
     IGlobalEventCrossbarUtility
from org.ict_ok.admin_utils.graphviz.interfaces import \
     IGenGraphvizDot
from org.ict_ok.components.interfaces import IComponent
from org.ict_ok.admin_utils.notifier.imail.interfaces import INotifierEmail

logger = logging.getLogger("AdmUtilEventCrossbar")
berlinTZ = timezone('Europe/Berlin')


def AllObjectInstances(dummy_context):
    """Which objects are there
    """
    print "here cleanup 3ffvd"
    iid = zapi.getUtility(IIntIds, '')
    terms = []
    for (oid, oobj) in iid.items():
        if ISite.providedBy(oobj.object) or \
           IIpNet.providedBy(oobj.object) or \
           IHost.providedBy(oobj.object) or \
           IInterface.providedBy(oobj.object) or \
           IService.providedBy(oobj.object) or \
           ISnmpValue.providedBy(oobj.object) or \
           IEventLogic.providedBy(oobj.object):
            terms.append(\
                SimpleTerm(oobj.object.objectID,
                           str(oobj.object.objectID),
                           oobj.object.getDcTitle()))
    for iface in [INotifierEmail]:
        my_util = queryUtility(iface)
        if my_util is not None:
            terms.append(\
                SimpleTerm(my_util.objectID,
                           str(my_util.objectID),
                           my_util.getDcTitle()))
    return SimpleVocabulary(terms)

def AllObjectInstancesWithEventInputs(dummy_context):
    """Which objects are there
    """
    print "here cleanup jfd98"
    iid = zapi.getUtility(IIntIds, '')
    terms = []
    for (oid, oobj) in iid.items():
        if ISite.providedBy(oobj.object) or \
           IIpNet.providedBy(oobj.object) or \
           IHost.providedBy(oobj.object) or \
           IInterface.providedBy(oobj.object) or \
           IService.providedBy(oobj.object) or \
           ISnmpValue.providedBy(oobj.object) or \
           IEventLogic.providedBy(oobj.object):
            inpEventNames = oobj.object.getAllInpEventNames().keys()
            if len(inpEventNames) > 0:
                for inpEventName in inpEventNames:
                    myId = oobj.object.objectID + u'.' + inpEventName
                    terms.append(\
                        SimpleTerm(myId,
                                   str(myId),
                                   oobj.object.getDcTitle() + \
                                   u'->' + inpEventName))
    for iface in [INotifierEmail]:
        my_util = queryUtility(iface)
        if my_util is not None:
            inpEventNames = my_util.getAllInpEventNames().keys()
            if len(inpEventNames) > 0:
                for inpEventName in inpEventNames:
                    myId = my_util.objectID + u'.' + inpEventName
                    terms.append(\
                        SimpleTerm(myId,
                                   str(myId),
                                   my_util.getDcTitle()+ u'->' + inpEventName))
    return SimpleVocabulary(terms)

def AllEventInstances(dummy_context):
    """Which events are there
    """
    print "here cleanup 7dhd6"
    try:
        eventXbar = zapi.getUtility(IAdmUtilEventCrossbar, '')
    except ComponentLookupError:
        return SimpleVocabulary([])
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

    def fillDotFile(self, dotFile, mode=None):
        """generate the dot file
        """
        my_catalog = zapi.getUtility(ICatalog)
        objIdSet = set()
        objSet = set()
        eventSet = set()
        for (oid, oobj) in self.items():
            objIdSet.add(oid)
        for objId in self.inpEQueues:
            objIdSet.add(objId)
        for objId in self.outEQueues:
            objIdSet.add(objId)
        for objId in objIdSet:
            for result in my_catalog.searchResults(oid_index=objId):
                if IAdmUtilEvent.providedBy(result):
                    eventSet.add(result)
                elif IEventLogic.providedBy(result):
                    objSet.add(result)
                elif IEventLogic.providedBy(result):
                    objSet.add(result)
                elif IComponent.providedBy(result):
                    if result.isConnectedToEvent():
                        objSet.add(result)
                else:
                    pass
        print >> dotFile, '// GraphViz DOT-File'
        print >> dotFile, 'digraph "%s" {' % (zapi.getRoot(self).__name__)
        if mode and mode.lower() == "fview":
            print >> dotFile, '\tgraph [bgcolor="#E5FFF9", dpi="100.0"];'
        else:
            print >> dotFile, '\tgraph [bgcolor="#E5FFF9", size="6.2,5.2",' +\
            ' splines="true", ratio = "auto", dpi="100.0"];'
        print >> dotFile, '\tnode [fontname = "Helvetica",fontsize = 10];'
        print >> dotFile, '\tedge [style = "setlinewidth(2)", color = black];'
        print >> dotFile, '\trankdir = LR;'
        print >> dotFile, '\t// objects ----------------------------------'
        for obj in objSet:
            objGraphvizDot = IGenGraphvizDot(obj)
            objGraphvizDot.traverse4DotGenerator(dotFile, level=1,
                                                 comments=True,
                                                 signalsOutput=True,
                                                 recursive=False)
        #print "-" * 80
        #uidutil = zapi.getUtility(IIntIds)
        #print >> dotFile, '\t// locations ----------------------------------'
        #for (oid, oobj) in uidutil.items():
            #if ILocation.providedBy(oobj.object):
                #print "Location: ", oobj.object.ikName
                #print >> dotFile, \
                      #'\tsubgraph "cluster_location" '\
                      #'{ color=blue; label="location"};'
            ##elif IRoom.providedBy(oobj.object):
                ##print "Room: ", oobj.object.ikName
            ##elif ILocation.providedBy(oobj.object):
                ##print "Location: ", oobj.object.ikName
        #print "-" * 80

        print >> dotFile, '\t// events ----------------------------------'
        for event in eventSet:
            eventGraphvizDot = IGenGraphvizDot(event)
            eventGraphvizDot.traverse4DotGenerator(dotFile,
                                                   level=1,
                                                   comments=True)
        for obj in objSet:
            allInpNamesDict = obj.getAllInpEventNames()
            allOutNamesDict = obj.getAllOutEventNames()
            for inpName in allInpNamesDict.keys():
                for iObj in allInpNamesDict[inpName]:
                    print >> dotFile, '\t "%s"-> "%s":"%s"' % (iObj,
                                                               obj.objectID,
                                                               inpName)
            for outName in allOutNamesDict.keys():
                for iObj in allOutNamesDict[outName]:
                    print >> dotFile, '\t "%s":"%s"-> "%s"' % (obj.objectID,
                                                               outName,
                                                               iObj)
        print >> dotFile, '}'
        dotFile.flush()

        
    def getIMGFile(self, imgtype, mode=None):
        """get dot file and convert to png
        """
        dotFileName = '/tmp/dotFile_%s.dot' % os.getpid()
        outFileName = '/tmp/dotFile_%s.out' % os.getpid()
        dotFile = open(dotFileName, 'w')
        self.fillDotFile(dotFile, mode)
        dotFile.close()
        os.system("dot -T%s -o %s %s" % (imgtype,
                                         outFileName, 
                                         dotFileName))
        pic = open(outFileName, "r")
        picMem = pic.read()
        pic.close()
        return picMem

    def getCmapxText(self, root_obj):
        """get dot file and convert to client side image map
        """
        its = root_obj.items()
        dotFileName = '/tmp/dotFile_%s.dot' % os.getpid()
        outFileName = '/tmp/dotFile_%s.out' % os.getpid()
        dotFile = open(dotFileName, 'w')
        self.fillDotFile(its, dotFile)
        dotFile.close()
        os.system("%s -Tcmapx -o %s %s" % (self.graphviz_type, 
                                           outFileName, 
                                           dotFileName))
        mymap = open(outFileName, "r")
        mapMem = mymap.read()
        mymap.close()
        return mapMem


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
                foundObj = False
                for result in my_catalog.searchResults(oid_index=objId):
                    event = iter(outQueue).next() # don't delete
                    if result.injectInpEQueue(event):
                        foundObj = True
                        outQueue.pull() # now delete
                #if not foundObj:
                    #print "delete trash"
                    #outQueue.pull() # delete trash
    
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
                    for oid in self.outEQueues:
                        for receiverObj in my_catalog.searchResults(\
                            oid_index=oid):
                            if (inpEvent.oidEventObject in \
                                receiverObj.getAllInpEventObjs()):
                                processed = True
                                receiverObj.injectInpEQueue(inpEvent)
                if not processed:
                    inpEvent.stopit(self)

    def tickerEvent(self):
        ## debug if queue not empty
        #for qid in self.inpEQueues:
            #if len(self.inpEQueues[qid]) > 0:
                #logger.info("tickerEvent (n:%s, n(i):%s, n(o):%s)" % \
                            #(qid,
                             #len(self.inpEQueues[qid]),
                             #len(self.outEQueues[qid])
                             #))
        self.processOutEQueues()
        self.processEvents()
        self.processInpEQueues()
        
    def logIntoEvent(self, oidEventObject, logEntry):
        if self.has_key(oidEventObject):
            eventObject = self[oidEventObject]
            if eventObject.logAllEvents:
                newEntry = Entry(logEntry, eventObject, level=u"info")
                eventObject.history.append(newEntry)
                eventObject._p_changed = True

    def getEvent(self, oidEventObject):
        if self.has_key(oidEventObject):
            return self[oidEventObject]
        else:
            return None

    def debugEventHistory(self, eventObject=None):
        if eventObject is not None:
            my_catalog = zapi.getUtility(ICatalog)
            print "debugEventHistory:"
            print "-" * 40
            for entry in eventObject.transmissionHistory:
                for obj in my_catalog.searchResults(oid_index=entry):
                    print " -> ", obj.getDcTitle()
            print "-" * 40


class GlobalEventCrossbarUtility(object):

    implements(IGlobalEventCrossbarUtility)

    lastEventCrossbar = "no signal since start"

    def __init__(self):
        self.subscriber_list = []
        super(GlobalEventCrossbarUtility, self).__init__()

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
    