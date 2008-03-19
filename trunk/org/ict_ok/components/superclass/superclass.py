# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0613,W0142
#
"""implementation of Superclass

Superclass for non containing objects 

"""

# TODO move MsgEvent to other file

__version__ = "$Id$"

# phython imports
from logging import INFO, log, NOTSET

# zope imports
from zope.app import zapi
from persistent import Persistent
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.security.management import queryInteraction
from zope.dublincore.interfaces import IWriteZopeDublinCore
from zope.app.keyreference.interfaces import IKeyReference
from zope.component import adapter, queryUtility
from zope.app.catalog.interfaces import ICatalog
from zope.app.container.interfaces import \
     IObjectAddedEvent, \
     IObjectModifiedEvent, \
     IObjectMovedEvent, \
     IObjectRemovedEvent

# zc imports
from zc.queue.interfaces import IQueue
from zc.queue import Queue

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import \
     IEventIfSuperclass, IMsgEvent, ISuperclass
from org.ict_ok.libs.lib import generateOid, oidIsValid, RingBuffer
from org.ict_ok.libs.history.entry import Entry
from org.ict_ok.admin_utils.eventcrossbar.interfaces import \
     IAdmUtilEventCrossbar
from org.ict_ok.admin_utils.generators.nagios.interfaces import \
     IGenNagios

class Superclass(Persistent):
    """
    the superclass
    """

#    implements(IKeyReference, ISuperclass)
    implements(ISuperclass, IEventIfSuperclass)
    key_type_id = 'org.ict_ok.components.superclass.keyreference'
    
    objectID = FieldProperty(ISuperclass['objectID'])
    ikName = FieldProperty(ISuperclass['ikName'])
    ikComment = FieldProperty(ISuperclass['ikComment'])
    ikNotes = FieldProperty(ISuperclass['ikNotes'])
    ikAuthor = FieldProperty(ISuperclass['ikAuthor'])
    ikEventTarget = FieldProperty(ISuperclass['ikEventTarget'])
    ref = FieldProperty(ISuperclass['ref'])
    
    # IEventIfSuperclass
    #eventInpObjs_Ping = FieldProperty(IEventIfSuperclass['eventInpObjs_Ping'])
    #eventOutObjs_Pong = FieldProperty(IEventIfSuperclass['eventOutObjs_Pong'])

    def __init__(self, **data):
        """
        constructor of Superclass
        """
        Persistent.__init__(self)
        ISuperclass['objectID'].readonly = False
        self.objectID = generateOid(self)
        ISuperclass['objectID'].readonly = True
        self.ikName = self.objectID
        for (name, value) in data.items():
            if name in ISuperclass.names():
                setattr(self, name, value)
        self.ikAuthor = u""
        self.dbgLevel = NOTSET
        self.history = RingBuffer(20)
        self.inpEQueue = Queue()
        self.outEQueue = Queue()
        self.outEReceiver = None
        self.workflows = {}
        self.wf_worklist = []
        interaction = queryInteraction()
        if interaction is not None:
            for participation in interaction.participations:
                #principalid = participation.principal.id
                principal_title = participation.principal.title
                self.ikAuthor += unicode(principal_title)
        self.myFactory = str(self.__class__).split("'")[1]
        self.ikRevision = __version__

    def __post_init__(self, **data):
        """
        triggerd after constructor has been finished
        """
        newEntry = Entry(u"Object created", self, level=u"info")
        newEntry.setObjVersion(self.ikRevision)
        self.history.append(newEntry)
        self.connectToEventXbar()
        newEntry = Entry(u"Object connected to event crossbar", self, level=u"info")
        newEntry.setObjVersion(self.ikRevision)
        self.history.append(newEntry)

    def enabledDebug(self):
        """
        is debug output enabled?
        return True or False
        """
        return self.dbgLevel > 0

    def getDebugLevel(self):
        """
        get debug level of object
        0: none
        1: normal
        2: all
        """
        return self.dbgLevel

    def getObjectId(self):
        """
        get 'Universe ID' of object
        returns str
        """
        return self.objectID

    def outputDebug(self):
        """
        normal debug output
        """
        if self.enabledDebug():
            log(self.getDebugLevel(), "I'm Superclass: %s" % self. __name__)

    def setDebugLevel(self, dbgLevel):
        """
        set debug level of object
        0: none
        1: normal
        2: all
        """
        self.__setattr__("dbgLevel", dbgLevel)
        
    def getDcTitle(self):
        """
        get the Title from Dublin Core
        """
        dcore = IWriteZopeDublinCore(self)
        return dcore.title

    def setDcTitle(self, title):
        """
        set the Title to Dublin Core
        """
        dcore = IWriteZopeDublinCore(self)
        dcore.title = unicode(title)

    def appendHistoryEntry(self, entryText):
        """
        append an text entry to the history
        """
        newEntry = Entry(entryText, self, level=u"info")
        newEntry.setObjVersion(self.ikRevision)
        self.history.append(newEntry)

    def isConnectedToEvent(self):
        for attrName in self.__dict__:
            attrObjsPrefix = "eventInpObjs_"
            if attrName.find(attrObjsPrefix) == 0: # attribute name starts with ...
                objs = getattr(self, attrName, None)
                if len(objs) > 0:
                    return True
            attrObjsPrefix = "eventOutObjs_"
            if attrName.find(attrObjsPrefix) == 0: # attribute name starts with ...
                objs = getattr(self, attrName, None)
                if len(objs) > 0:
                    return True
        return False
        
    def processEvents(self):
        while len(self.inpEQueue) > 0:
            # temp. direct connect
            eventMsg = self.inpEQueue.pull()
            if not eventMsg.hasSeen(self):
                #print ">>> %s / %s [fnctName:%s]" % \
                      #(self.getObjectId(),
                       #eventMsg.oidEventObject,
                       #eventMsg.targetFunctionName)
                # call possible event ipnut methods by name
                fnctList = []
                for attrName in self.__dict__:
                    attrObjsPrefix = "eventInpObjs_"
                    attrFnctPrefix = "eventInp_"
                    if attrName.find(attrObjsPrefix) == 0: # attribute name starts with ...
                        fnctName = attrFnctPrefix + attrName[len(attrObjsPrefix):]
                        objs = getattr(self, attrName, None)
                        fnct = getattr(self, fnctName, None)
                        if fnct is not None and \
                           objs is not None:
                            # find the RIGHT object list
                            if eventMsg.oidEventObject in objs: 
                                fnctList.append(fnct)
                            elif eventMsg.targetFunctionName == \
                                 attrName[len(attrObjsPrefix):]:
                                fnctList.append(fnct)
                for fnct in fnctList:
                    fnct(eventMsg)
                if len(fnctList) == 0:
                    # direct input to output
                    self.outEQueue.put(eventMsg)
            else:
                eventMsg.stopit(self, "cycle!")

    def processOutEQueue(self):
        if self.outEReceiver is not None:
            while len(self.outEQueue) > 0:
                utilXbar = queryUtility(IAdmUtilEventCrossbar)
                event = iter(self.outEQueue).next() # don't delete
                if utilXbar.injectEventFromObj(self, event):
                    self.outEQueue.pull() # now delete

    def processInpEQueue(self):
        pass
        

    def injectInpEQueue(self, event):
        self.inpEQueue.put(event)
        return True

    def injectOutEQueue(self, event):
        if self.outEReceiver is not None:
            self.outEQueue.put(event)
        return True
    
    def tickerEvent(self):
        """
        got ticker event from ticker thread
        """
        ## debug if queue not empty
        if len(self.inpEQueue) + len(self.outEQueue) > 0:
            log(INFO, "tickerEvent (n:%s, n(i):%s, n(o):%s)" % \
                (self.getDcTitle(), len(self.inpEQueue), len(self.outEQueue)))
        self.processOutEQueue()
        self.processEvents()
        self.processInpEQueue()
        ## TODO test pupose
        #import time
        #if time.gmtime()[5] == 10:
            #if self.getDcTitle()==u'Host1':
                #inst_event = MsgEvent(self)
                #self.injectOutEQueue(inst_event)

    def connectToEventXbar(self):
        if self.outEReceiver is None:
            utilXbar = queryUtility(IAdmUtilEventCrossbar)
            if utilXbar is None:
                return False
            if utilXbar.makeNewObjQueue(self):
                self.outEReceiver = utilXbar.getObjectId()
                return True
            else: # can't create
                raise Exception, "connection failed"
        else: # already connected
            self.disconnectFromEventXbar()
            return self.connectToEventXbar()
        return False
        
    def disconnectFromEventXbar(self):
        if self.outEReceiver is not None:
            utilXbar = queryUtility(IAdmUtilEventCrossbar)
            if utilXbar is None:
                return False
            if utilXbar.destroyObjQueue(self):
                self.outEReceiver = None
                return True
            else: # can't destroy
                raise Exception, "destruction failed"
        return False

    def getAllOutEventObjs(self):
        """ returns a list of all active referenced event object oids for update purpose
        attribute name must start with 'eventOutObjs_'
        """
        retSet = set([])
        for attrName in self.__dict__:
            if attrName.find("eventOutObjs_") == 0: # attribute name starts with ...
                for tmpOid in self.__dict__[attrName]:
                    retSet.add(tmpOid)
        return retSet

    def getAllInpEventObjs(self):
        """ returns a list of all active referenced event object oids for update purpose
        attribute name must start with 'eventInpObjs_'
        """
        retSet = set([])
        for attrName in self.__dict__:
            if attrName.find("eventInpObjs_") == 0: # attribute name starts with ...
                for tmpOid in self.__dict__[attrName]:
                    retSet.add(tmpOid)
        return retSet

    def getAllInpEventNames(self):
        """ returns a list of all input event methods
        attribute name must start with 'eventInpObjs_'
        """
        retDict = {}
        for attrName in self.__dict__:
            if attrName.find("eventInpObjs_") == 0: # attribute name starts with ...
                retDict[attrName[len('eventInpObjs_'):]] =  \
                       self.__dict__[attrName]
                #retList.append(attrName[len('eventInpObjs_'):])
        return retDict

    def getAllOutEventNames(self):
        """ returns a list of all output event methods
        attribute name must start with 'eventOutObjs_'
        """
        retDict = {}
        for attrName in self.__dict__:
            if attrName.find("eventOutObjs_") == 0: # attribute name starts with ...
                retDict[attrName[len('eventOutObjs_'):]] =  \
                       self.__dict__[attrName]
                #retList.append(attrName[len('eventOutObjs_'):])
        return retDict


    def addToEventInpObjs(self, inputName, eventObj):
        """ add the event to the list of inp event object oids
        """
        if "eventInpObjs_"+inputName in self.__dict__:
            myObjIdSet = self.__dict__["eventInpObjs_"+inputName]
            print "myObjIdSet 1 :", myObjIdSet
            newOid = eventObj.getObjectId()
            if newOid not in myObjIdSet:
                myObjIdSet.add(newOid)
                self._p_changed = True
            print "myObjIdSet 2 :", myObjIdSet

    def delFromEventInpObjs(self, inputName, eventObj):
        """ add the event to the list of inp event object oids
        """
        if "eventInpObjs_"+inputName in self.__dict__:
            myObjIdSet = self.__dict__["eventInpObjs_"+inputName]
            print "myObjIdSet 1 :", myObjIdSet
            oldOid = eventObj.getObjectId()
            if oldOid in myObjIdSet:
                myObjIdSet.remove(oldOid)
                self._p_changed = True
            print "myObjIdSet 2 :", myObjIdSet

class MsgEvent:
    """ Interface of an async event message
    """
    implements(IMsgEvent)

    def __init__(self, senderObj = None,
                 oidEventObject = None,
                 logText=u"new event",
                 targetFunctionName = None):
        self.transmissionHistory = []
        self.timeToLive = 10
        self.oidEventObject = oidEventObject
        self.targetFunctionName = targetFunctionName
        utilEventXbar = queryUtility(IAdmUtilEventCrossbar)
        if senderObj is not None:
            self.transmissionHistory.append(senderObj.getObjectId())
            logText = u"'%s' creates event" % (senderObj.getDcTitle())
        if self.oidEventObject is not None:
            utilEventXbar.logIntoEvent(self.oidEventObject, logText)

    def stopit(self, stopperObj, additionalText=u""):
        utilEventXbar = queryUtility(IAdmUtilEventCrossbar)
        if utilEventXbar is not None:
            logText = u"event destroyed by '%s' (Hops: %d) " % \
                    (stopperObj.getDcTitle(),
                     len(self.transmissionHistory))
            logText += additionalText
            if self.oidEventObject is not None:
                utilEventXbar.logIntoEvent(self.oidEventObject, logText)
            #utilEventXbar.debugEventHistory(self)

    def hasSeen(self, obj):
        if obj.getObjectId() in self.transmissionHistory:
            return True
        else:
            self.transmissionHistory.append(obj.getObjectId())
            return False

def isOidInCatalog(arg_oid):
    """can arg_oid be found in Catalog"""
    if oidIsValid(arg_oid):
        my_catalog = zapi.getUtility(ICatalog)
        if len(my_catalog.searchResults(oid_index=arg_oid)) > 0:
            return True
    return False

@adapter(ISuperclass, IObjectAddedEvent)
def notifyAddedEvent(instance, event):
    """
    Node was added
    """
    print "Superclass.notifyAddedEvent"
    #import pdb
    #pdb.set_trace()
    nagiosAdapter = IGenNagios(event.object)
    if nagiosAdapter is not None:
        nagiosAdapter.nagiosConfigFileOut()

@adapter(ISuperclass, IObjectModifiedEvent)
def notifyModifiedEvent(instance, event):
    """
    Node was modified
    """
    print "Superclass.notifyModifiedEvent"
    #import pdb
    #pdb.set_trace()
    allEventObjs = event.object.getAllOutEventObjs()
    utilXbar = queryUtility(IAdmUtilEventCrossbar)
    for eventObj in allEventObjs:
        try:
            utilXbar[eventObj].addOidToInpObjects(event.object.objectID)
        except KeyError:
            pass

@adapter(ISuperclass, IObjectMovedEvent)
def notifyMovedEvent(instance, event):
    """
    Node was moved
    """
    print "Superclass.notifyMovedEvent"
    #import pdb
    #pdb.set_trace()

@adapter(ISuperclass, IObjectRemovedEvent)
def notifyRemovedEvent(instance, event):
    """
    Node was removed
    """
    print "Superclass.notifyRemovedEvent"
    print "ikName:", event.object.ikName
    print "getObjectId():", event.object.getObjectId()
    nagiosAdapter = IGenNagios(event.object)
    if nagiosAdapter is not None:
        nagiosAdapter.nagiosConfigFileRemove()
    
    #import pdb
    #pdb.set_trace()

