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

# python imports
import os
from datetime import datetime
import pytz
from logging import INFO, log, NOTSET
import xml.dom.minidom
#import xml.dom.ext

# zope imports
from zope.app import zapi
from persistent import Persistent
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.security.management import queryInteraction
from zope.dublincore.interfaces import IWriteZopeDublinCore, IDCTimes, IZopeDublinCore
from zope.app.keyreference.interfaces import IKeyReference
from zope.component import adapter, queryUtility
from zope.app.catalog.interfaces import ICatalog
from zope.app.security.interfaces import IAuthentication
from zope.app.container.interfaces import \
     IObjectAddedEvent, \
     IObjectMovedEvent, \
     IObjectRemovedEvent
from zope.lifecycleevent.interfaces import \
     IObjectModifiedEvent


# zc imports
from zc.queue.interfaces import IQueue
from zc.queue import Queue

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory, oidIsValid
from org.ict_ok.components.superclass.interfaces import \
     IEventIfSuperclass, IMsgEvent, ISuperclass
from org.ict_ok.libs.lib import generateOid, oidIsValid, RingBuffer
from org.ict_ok.libs.history.entry import Entry
from org.ict_ok.admin_utils.eventcrossbar.interfaces import \
     IAdmUtilEventCrossbar
from org.ict_ok.admin_utils.generators.nagios.interfaces import \
     IAdmUtilGeneratorNagios, IGenNagios
from org.ict_ok.admin_utils.reports.interfaces import IRptPdf, IRptXML
from org.ict_ok.admin_utils.reports.rpt_document import RptDocument

import transaction
from gocept.objectquery import indexsupport
index_synch = indexsupport.IndexSynchronizer()
transaction.manager.registerSynch(index_synch)


class Superclass(Persistent):
    """
    the superclass
    """

#    implements(IKeyReference, ISuperclass)
#    implements(ISuperclass, IEventIfSuperclass)
    implements(ISuperclass)
    shortName = "generic"
    key_type_id = 'org.ict_ok.components.superclass.keyreference'

    objectID = FieldProperty(ISuperclass['objectID'])
    ikName = FieldProperty(ISuperclass['ikName'])
    ikComment = FieldProperty(ISuperclass['ikComment'])
    ikNotes = FieldProperty(ISuperclass['ikNotes'])
    ikAuthor = FieldProperty(ISuperclass['ikAuthor'])
    ikEventTarget = FieldProperty(ISuperclass['ikEventTarget'])
    #ref = FieldProperty(ISuperclass['ref'])
    
    fullTextSearchFields = ['objectID', 'ikName',
                            'ikComment', 'ikAuthor']
    
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
        self.ikName = self.objectID
        for (name, value) in data.items():
            if name in ISuperclass.names():
                setattr(self, name, value)
        ISuperclass['objectID'].readonly = True
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
        dc = IZopeDublinCore(self, None)
        if dc is not None:
            now = datetime.now(pytz.utc)
            dc.created = now
            dc.modified = now

    def canBeDeleted(self):
        """
        a object can be deleted with normal delete permission
        special objects can overload this for special delete rules
        (e.g. IAdmUtilCatHostGroup)
        return True or False
        """
        return True
    
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
        return str(self.objectID)

    def setObjectId(self, arg_oid):
        """
        set 'Universe ID' of object
        only for backup/restore functions
        """
        if oidIsValid(arg_oid):
            ISuperclass['objectID'].readonly = False
            self.objectID = arg_oid
            ISuperclass['objectID'].readonly = True

    def getShortname(self):
        """
        get a short class name of object
        returns str
        """
        return self.shortName
    
    def getParent(self):
        """
        returns parent object
        """
        return zapi.getParent(self)

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
        try:
            dcore = IWriteZopeDublinCore(self)
            if len(dcore.title) > 0:
                return dcore.title
            else:
                return self.ikName
        except TypeError:
            return self.ikName

    def setDcTitle(self, title):
        """
        set the Title to Dublin Core
        """
        dcore = IWriteZopeDublinCore(self)
        dcore.title = unicode(title)
        
    def getDisplayTitle(self):
        """ display text for some views
        """
        return self.getDcTitle()

    def getLongTitle(self):
        """ display text for some views
        """
        return self.getDcTitle()

    def getModifiedTime(self):
        """
        get the modified time from Dublin Core
        """
        return IDCTimes(self).modified

    def appendHistoryEntry(self, entryText, level=u"info",
                           request=None, withAuthor=False,
                           dontCount=False):
        """
        append an text entry to the history
        """
        if withAuthor and request is not None:
            principalId = request.principal.id.split('.')[1]
            pau_utility = queryUtility(IAuthentication)
            if pau_utility.has_key('principals'):
                internalPrincipal = pau_utility['principals'][principalId]
            if pau_utility.has_key('LDAPAuthentication'):
                ldapAuth = pau_utility[u'LDAPAuthentication']
                internalPrincipal = ldapAuth.principalInfo(\
                                           ldapAuth.prefix+principalId)
            entryText = u'%s (%s)' % (entryText, internalPrincipal.title)
        lastEntry = self.history.get()[-1]
        if not dontCount and entryText == lastEntry.getText():
            lastEntry.appendRepeatCounter()
            lastEntry._p_changed = 1
        else:
            newEntry = Entry(entryText, self, level)
            newEntry.setObjVersion(self.ikRevision)
            self.history.append(newEntry)
        self._p_changed = 1

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
                (self.ikName, len(self.inpEQueue), len(self.outEQueue)))
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
        print "getAllInpEventObjs:", retSet
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
        print "getAllInpEventNames:", retDict
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
        print "getAllInpEventNames:", retDict
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

    def generatePdf(self, absFilename, authorStr, versionStr, request=None):
        """
        will generate a object pdf report
        steps to do:
        - toReportSet = set([])
        - 1. select of objects (e.g. locations), append  toReportSet
        - 2. select of objects (e.g. buildings), append  toReportSet
        - 3. select of objects (e.g. rooms), append  toReportSet
        - generate Report (1st run, content)
        - generate Report (2nd run, references)
        """
        ##
        ##
        ## TODO:
        ##
        ## evil, very alpha, evaluation code for some kind of "Query Language"
        ## ... to be removed ...
        ##
        ##
        
        #-> from ZODB.interfaces import IConnection
        #-> connection = IConnection(self)
        #(Pdb) 
        #> /Users/markus/Projekte/ict_ok.org/inst/lib/python/org/ict_ok/components/superclass/superclass.py(447)generatePdf()
        #-> from gocept.objectquery.collection import ObjectCollection
        #(Pdb) connection
        #<Connection at 01f19910>
        #(Pdb) dir(connection)
        #['_Connection__onCloseCallbacks', '__class__', '__delattr__', '__dict__', '__doc__', '__getattribute__', '__getitem__', '__hash__', '__implemented__', '__init__', '__module__', '__new__', '__providedBy__', '__provides__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__str__', '__weakref__', '_abort', '_abort_savepoint', '_added', '_added_during_commit', '_cache', '_cache_items', '_code_timestamp', '_commit', '_commit_savepoint', '_conflicts', '_creating', '_db', '_debug_info', '_flush_invalidations', '_handle_independent', '_handle_one_serial', '_handle_serial', '_implicitlyAdding', '_import', '_importDuringCommit', '_inv_lock', '_invalidate_creating', '_invalidated', '_invalidatedCache', '_load_before_or_conflict', '_load_count', '_log', '_modified', '_needs_to_join', '_normal_storage', '_opened', '_pre_cache', '_reader', '_register', '_registered_objects', '_resetCache', '_reset_counter', '_rollback', '_savepoint_storage', '_setstate', '_setstate_noncurrent', '_storage', '_storage_sync', '_store_count', '_store_objects', '_tpc_cleanup', '_txn_time', '_version', 'abort', 'add', 'afterCompletion', 'beforeCompletion', 'cacheGC', 'cacheMinimize', 'close', 'commit', 'connections', 'db', 'exchange', 'exportFile', 'get', 'getDebugInfo', 'getTransferCounts', 'getVersion', 'get_connection', 'importFile', 'invalidate', 'invalidateCache', 'isReadOnly', 'modifiedInVersion', 'newTransaction', 'new_oid', 'oldstate', 'onCloseCallback', 'open', 'register', 'root', 'savepoint', 'setDebugInfo', 'setstate', 'sortKey', 'sync', 'tpc_abort', 'tpc_begin', 'tpc_finish', 'tpc_vote', 'transaction_manager']
        #(Pdb) connection.transaction_manager
        #<transaction._manager.ThreadTransactionManager object at 0x1239bf0>
        #(Pdb) pp dir(connection.transaction_manager)
        #['__class__',
        # '__delattr__',
        # '__dict__',
        # '__doc__',
        # '__getattribute__',
        # '__hash__',
        # '__init__',
        # '__module__',
        # '__new__',
        # '__reduce__',
        # '__reduce_ex__',
        # '__repr__',
        # '__setattr__',
        # '__str__',
        # '__weakref__',
        # '_synchs',
        # '_txns',
        # 'abort',
        # 'begin',
        # 'commit',
        # 'doom',
        # 'free',
        # 'get',
        # 'isDoomed',
        # 'registerSynch',
        # 'savepoint',
        # 'unregisterSynch']
        #(Pdb) connection.transaction_manager.registerSynch(index_synch)
        #(Pdb) connection.root()['_oq_collection'] = oc
        #*** NameError: name 'oc' is not defined
        #(Pdb) l
        #442                  publ = request.publication
        #443                  import pdb
        #444                  pdb.set_trace()
        #445                  from ZODB.interfaces import IConnection
        #446                  connection = IConnection(self)
        #447  ->                from gocept.objectquery.collection import ObjectCollection
        #448                  from gocept.objectquery.pathexpressions import RPEQueryParser
        #449                  from gocept.objectquery.processor import QueryProcessor
        #450                  from zope.app import zapi
        #451                  parser = RPEQueryParser()
        #452                  oc = ObjectCollection(connection)
        #(Pdb) n
        #> /Users/markus/Projekte/ict_ok.org/inst/lib/python/org/ict_ok/components/superclass/superclass.py(448)generatePdf()
        #-> from gocept.objectquery.pathexpressions import RPEQueryParser
        #(Pdb) 
        #> /Users/markus/Projekte/ict_ok.org/inst/lib/python/org/ict_ok/components/superclass/superclass.py(449)generatePdf()
        #-> from gocept.objectquery.processor import QueryProcessor
        #(Pdb) 
        #> /Users/markus/Projekte/ict_ok.org/inst/lib/python/org/ict_ok/components/superclass/superclass.py(450)generatePdf()
        #-> from zope.app import zapi
        #(Pdb) 
        #> /Users/markus/Projekte/ict_ok.org/inst/lib/python/org/ict_ok/components/superclass/superclass.py(451)generatePdf()
        #-> parser = RPEQueryParser()
        #(Pdb) 
        #> /Users/markus/Projekte/ict_ok.org/inst/lib/python/org/ict_ok/components/superclass/superclass.py(452)generatePdf()
        #-> oc = ObjectCollection(connection)
        #(Pdb) 
        #> /Users/markus/Projekte/ict_ok.org/inst/lib/python/org/ict_ok/components/superclass/superclass.py(453)generatePdf()
        #-> d1 = zapi.getParent(self)
        #(Pdb) connection.root()['_oq_collection'] = oc
        #(Pdb) connection.transaction_manager.commit()
        #(Pdb) 
        
        
        from org.ict_ok.components.happliance.interfaces import IHardwareAppliance
        if IHardwareAppliance.providedBy(self):
            publ = request.publication
            from ZODB.interfaces import IConnection
            connection = IConnection(self)
            from gocept.objectquery.collection import ObjectCollection
            from gocept.objectquery.pathexpressions import RPEQueryParser
            from gocept.objectquery.processor import QueryProcessor
            from zope.app import zapi
            parser = RPEQueryParser()
            oc = ObjectCollection(connection)
            d1 = zapi.getParent(self)
            d2 = zapi.getParent(d1)
            d3 = zapi.getParent(d2)
            from pprint import pprint
            print "-" * 80
            print "class_index:"
            pprint(list(oc.class_index._index))
    #        print "attribute_index:"
    #        pprint(list(oc.attribute_index._index))
    #        print "structure_index:"
    #        pprint(list(oc.structure_index.paths))
            oc.index(connection.root())
            print "-" * 80
            print "class_index:"
            pprint(list(oc.class_index._index))
            print "attribute_index:"
            pprint(list(oc.attribute_index._index))
            print "structure_index:"
            pprint(list(oc.structure_index.paths))
            oc.index(d2)
            print "-" * 80
            print "class_index:"
            pprint(list(oc.class_index._index))
            print "attribute_index:"
            pprint(list(oc.attribute_index._index))
            print "structure_index:"
            pprint(list(oc.structure_index.paths))
            oc.index(d1)
            print "-" * 80
            print "class_index:"
            pprint(list(oc.class_index._index))
            print "attribute_index:"
            pprint(list(oc.attribute_index._index))
            print "structure_index:"
            pprint(list(oc.structure_index.paths))
            oc.index(self)
            print "-" * 80
            print "class_index:"
            pprint(list(oc.class_index._index))
            print "attribute_index:"
            pprint(list(oc.attribute_index._index))
            print "structure_index:"
            pprint(list(oc.structure_index.paths))
            print "-" * 80
            if0 = self.interfaces[0]
            oc.index(if0)
            oc3 = connection.root()['_oq_collection']
            query = QueryProcessor(parser, oc3)
            tt2 = oc3.is_child(self._p_oid,d1._p_oid)
            tt1 = oc3.is_child(d1._p_oid,d2._p_oid)
            tt3 = oc3.is_child(self._p_oid,if0._p_oid)
            tt4 = oc3.is_child(if0._p_oid,self._p_oid)
            ee=query('/Folder')
            ff=query('/Folder/HardwareApplianceFolder/HardwareAppliance')
            print "ff: ", ff
        files2delete = []
        document = RptDocument(absFilename)
        #document.setVolumeNo("1")
        document.setAuthorName(authorStr)
        document.setVersionStr(versionStr)
        adapterRptPdf = IRptPdf(self)
        if adapterRptPdf:
            adapterRptPdf.document = document
            adapterRptPdf.traverse4Rpt(1, True)
            files2delete.extend(adapterRptPdf.files2delete)
            del adapterRptPdf
        document.buildPdf()
        document.outConsoleTree(0)
        for i_filename in files2delete:
            try:
                os.remove(i_filename)
            except OSError:
                pass
            
    def generateXML(self, absFilename, authorStr, versionStr):
        """
        will generate a object pdf report
        """
        #files2delete = []
        document = xml.dom.minidom.Document()
        #document.setVolumeNo("1")
        #document.setAuthorName(authorStr)
        #document.setVersionStr(versionStr)
        adapterRptXML = IRptXML(self)
        if adapterRptXML:
            adapterRptXML.document = document
            adapterRptXML.traverse4Rpt(1, True)
            #files2delete.extend(adapterRptXML.files2delete)
            del adapterRptXML
        #document.buildPdf()
        file_object = open(absFilename, "w")
        # what here? xml.dom.ext.PrettyPrint(document, file_object)
        file_object.close()
        #for i_filename in files2delete:
            #try:
                #os.remove(i_filename)
            #except OSError:
                #pass

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

def objectsWithInterface(interface):
    """objects from catalog searhed by interface
    """
    my_catalog = zapi.getUtility(ICatalog)
    dottedInterfaceName = unicode(interface.__module__ + '.' + 
                                  interface.__name__)
#    for i in my_catalog.searchResults(all_interfaces_index=dottedInterfaceName):
#        yield i
    try:
        return my_catalog.searchResults(all_interfaces_index=dottedInterfaceName)
    except KeyError:
        return []

