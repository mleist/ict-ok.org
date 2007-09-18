# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
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

__version__ = "$Id$"

# phython imports
from logging import INFO, log, NOTSET

# zope imports
from persistent import Persistent
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.security.management import queryInteraction
from zope.dublincore.interfaces import IWriteZopeDublinCore
from zope.app.keyreference.interfaces import IKeyReference
from zope.component import queryUtility

# zc imports
from zc.queue.interfaces import IQueue
from zc.queue import Queue

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import IMsgEvent, ISuperclass
from org.ict_ok.libs.lib import generateOid
from org.ict_ok.libs.history.entry import Entry
from org.ict_ok.admin_utils.eventcrossbar.interfaces import \
     IAdmUtilEventCrossbar


class Superclass(Persistent):
    """
    the superclass
    """

#    implements(IKeyReference, ISuperclass)
    implements(ISuperclass)
    key_type_id = 'org.ict_ok.components.superclass.keyreference'
    
    objectID = FieldProperty(ISuperclass['objectID'])
    ikName = FieldProperty(ISuperclass['ikName'])
    ikComment = FieldProperty(ISuperclass['ikComment'])
    ikNotes = FieldProperty(ISuperclass['ikNotes'])
    ikAuthor = FieldProperty(ISuperclass['ikAuthor'])
    ikEventTarget = FieldProperty(ISuperclass['ikEventTarget'])
    ref = FieldProperty(ISuperclass['ref'])

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
        self.history = []
        self.inpEQueue = Queue()
        self.outEQueue = Queue()
        self.outEReceiver = None
        interaction = queryInteraction()
        if interaction is not None:
            for participation in interaction.participations:
                #principalid = participation.principal.id
                principal_title = participation.principal.title
                self.ikAuthor += unicode(principal_title)
        self.ikRevision = __version__

    def __post_init__(self, **data):
        """
        triggerd after constructor has been finished
        """
        #myName = str(self.__class__).replace('<','').replace('>','')
        #newEntry = Entry(u"created object: %s [%s]" % \
                         #(myName, self.ikRevision),\
                         #self, level=u"info")
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

    def processEvents(self):
        print "processEvents(%s)" % (self.getDcTitle())
        while len(self.inpEQueue) > 0:
            # temp. direct connect
            self.outEQueue.put(self.inpEQueue.pull())

    def processOutEQueue(self):
        print "processOutEQueue(%s)" % (self.getDcTitle())
        if self.outEReceiver is not None and \
           len(self.outEQueue) > 0:
            utilXbar = queryUtility(IAdmUtilEventCrossbar)
            event = iter(self.outEQueue).next() # don't delete
            if utilXbar.injectEventFromObj(self, event):
                self.outEQueue.pull() # now delete

    def processInpEQueue(self):
        print "processInpEQueue(%s)" % (self.getDcTitle())
        

    def injectInpEQueue(self, event):
        print "injectInpEQueue(%s, %s)" % (self.getDcTitle(), event)
        self.inpEQueue.put(event)

    def tickerEvent(self):
        """
        got ticker event from ticker thread
        """
        if len(self.inpEQueue) + len(self.outEQueue) > 0:
            log(INFO, "tickerEvent (n:%s, n(i):%s, n(o):%s)" % \
                (self.getDcTitle(), len(self.inpEQueue), len(self.outEQueue)))
        self.processOutEQueue()
        self.processEvents()
        self.processInpEQueue()
        import time
        if time.gmtime()[5] == 10:
            self.injectInpEQueue(u'event0815')

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


class MsgEvent:
    """ Interface of an async event event
    """
    implements(IMsgEvent)

    def __init__(self, senderObj = None):
        self.transmissionHistory = []
        if senderObj is not None:
            self.transmissionHistory.append(senderObj.getObjectId())

    def hasSeen(self, obj):
        if obj.getObjectId() in self.transmissionHistory:
            return True
        else:
            self.transmissionHistory.append(obj.getObjectId())
            return False
