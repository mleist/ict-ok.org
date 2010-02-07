# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0702,W0613,W0612,W0212,W0102,R0201
#
"""supervisor object

the supervisor object will manage all starts of and
will notice special events in an event-history

"""

__version__ = "$Id$"

# python imports
from os import access, getloadavg, popen, uname, R_OK
from datetime import datetime
from pytz import timezone
from types import UnicodeType
import pickle

# zope imports
from ZODB.interfaces import IConnection
from zope.app import zapi
from zope.app.zapi import getPath
from zope.component import adapts, createObject
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.size.interfaces import ISized
from zope.i18nmessageid import MessageFactory
from zope.lifecycleevent import ObjectCreatedEvent
from zope.event import notify
from zope.app.catalog.interfaces import ICatalog
from zope.copypastemove.interfaces import IObjectMover
from zope.security.proxy import removeSecurityProxy
from zope.app.intid.interfaces import IIntIds
from zope.xmlpickle import toxml, fromxml, loads

# ict_ok.org imports
from org.ict_ok.components.supernode.supernode import Supernode
from org.ict_ok.admin_utils.supervisor.interfaces import \
    IAdmUtilSupervisor, IFSearchText, IImportAllData
from org.ict_ok.version import getIkVersion
from org.ict_ok.admin_utils.objmq.interfaces import IAdmUtilObjMQ
from org.ict_ok.components.slave.interfaces import ISlave
from org.ict_ok.components.superclass.interfaces import ISuperclass

_ = MessageFactory('org.ict_ok')
utcTZ = timezone('UTC')
berlinTZ = timezone('Europe/Berlin')


class AdmUtilSupervisor(Supernode):
    """Supervisor instance
    """

    implements(IAdmUtilSupervisor,
               IFSearchText,
               IImportAllData)

    nbrStarts = FieldProperty(IAdmUtilSupervisor['nbrStarts'])
    ipv4My = FieldProperty(IAdmUtilSupervisor['ipv4My'])
#    objectID = FieldProperty(IAdmUtilSupervisor['objectID'])
    ipv4Master = FieldProperty(IAdmUtilSupervisor['ipv4Master'])
    oidMaster = FieldProperty(IAdmUtilSupervisor['oidMaster'])
    lastSeenMaster = FieldProperty(IAdmUtilSupervisor['lastSeenMaster'])
    status2Master = FieldProperty(IAdmUtilSupervisor['status2Master'])
    ipv4Slave = FieldProperty(IAdmUtilSupervisor['ipv4Slave'])
    oidSlave = FieldProperty(IAdmUtilSupervisor['oidSlave'])
    lastSeenSlave = FieldProperty(IAdmUtilSupervisor['lastSeenSlave'])


    def __init__(self):
        Supernode.__init__(self)
        try:
            IAdmUtilSupervisor['ipv4My'].readonly = False
            myFirstNetDev = self.getNetworkDevList()[0]
            # getLocalIpV4AddressList(9 return like '172.16.64.35/24'
            self.ipv4My = unicode(\
                self.getLocalIpV4AddressList(myFirstNetDev)[0]).split('/')[0]
        except:
            self.ipv4My = u"192.168.3.1"
        IAdmUtilSupervisor['ipv4My'].readonly = True
        #self.objectID = generateOid(self)
        self.ipv4Master = None
        self.oidMaster = None
        self.lastSeenMaster = None
        #IAdmUtilSupervisor['status2Master'].readonly = False
        self.status2Master = u"no master"
        #IAdmUtilSupervisor['status2Master'].readonly = True
        self.ipv4Slave = None
        self.oidSlave = None
        self.lastSeenSlave = None
        self.lastService = u"no service done"
        self.lastEvents = []
        self.instanceCounter = {}
        self.appendEventHistory(u"Database was initialized")
        self._p_changed = True
        #super(AdmUtilSupervisor, self).__init__(self)
        self.ikRevision = __version__

    def appendEventHistory(self, msg):
        """
        This method will append a text on the application history
        """
        if isinstance(msg, UnicodeType):
            dateNow = datetime.utcnow()
            if len(self.lastEvents) < 1000:
                self.lastEvents.append({'nbr': self.nbrStarts, \
                                        'date': dateNow, \
                                        'msg': msg})
            else:
                del self.lastEvents[0]
                self.lastEvents.append({'nbr': self.nbrStarts, \
                                        'date': dateNow, \
                                        'msg': msg})
            self._p_changed = True

    def getlastEvents(self):
        """getter for event list
        """
        return self.lastEvents

    def getStartCnt(self):
        """getter for start counter of all starts
        """
        return self.nbrStarts
    
    def getSystemVersion(self):
        """
        Version string of System
        no args, returns string
        """
        return getIkVersion()
    
    def getNetworkDevList(self, dev_types=['eth']):
        """
        get a list of network device names
        arg dev_types: list of device types stings (default: ['eth'])
        returns list of strings
        """
        searchString = "".join([" " + dtype.strip() + '\n' \
                                for dtype in dev_types])
        tmpFile = popen("/sbin/ip link | grep -F '%s'" % searchString)
        stringLines = tmpFile.readlines()
        tmpFile.close()
        ethDevs = []
        for line in stringLines:
            ethDevs.append(line.strip().split(':')[1].strip())
        return ethDevs
    
    def getLocalMacAddress(self, dev="eth0"):
        """
        get the mac address of the running system device
        argument is device name, default is 'eth0'
        returns string
        """
        tmpFile = popen("/sbin/ip link show %s| grep 'link/ether'" % dev)
        tmpString = tmpFile.readline().strip()
        tmpFile.close()
        try:
            outString = tmpString.split(' ')[1]
        except:
            outString = _("unknown")
        return outString
    
    def getLocalIpV4AddressList(self, dev="eth0"):
        """
        get the IpV4 addresses of the running system device
        argument is device name, default is 'eth0'
        returns list of strings
        """
        tmpFile = popen("/sbin/ip addr show %s | grep ' inet '" % dev)
        stringLines = tmpFile.readlines()
        tmpFile.close()
        ipV4s = []
        for line in stringLines:
            ipV4s.append(line.strip().split(' ')[1].strip())
        return ipV4s
    
    def getNetworkInfoDict(self):
        """
        returns an informational dictonary with network device settings
        """
        ret_dict = {}
        for net_dev in self.getNetworkDevList(dev_types=['eth']):
            net_info = {}
            net_info['mac'] = self.getLocalMacAddress(net_dev)
            net_info['ipv4s'] = self.getLocalIpV4AddressList(net_dev)
            if len(net_info['ipv4s']) > 0:
                ret_dict[net_dev] = net_info
        return ret_dict
    
    def getCpuVendorId(self):
        """
        get the cpu vendor of the running system
        no args, returns string
        """
        tmpFile = popen("cat /proc/cpuinfo | grep '^vendor_id'")
        tmpString = tmpFile.readline().strip()
        tmpFile.close()
        try:
            outString = tmpString.split(':')[1].strip()
        except:
            outString = _("unknown")
        return outString
    
    def getCpuModelName(self):
        """
        get the cpu model of the running system
        no args, returns string
        """
        tmpFile = popen("cat /proc/cpuinfo | grep '^model\ name'")
        tmpString = tmpFile.readline().strip()
        tmpFile.close()
        try:
            outString = tmpString.split(':')[1].strip()
        except:
            outString = _("unknown")
        return outString
    
    def getKernelVersion(self):
        """
        get the kernel version of the running system
        no args, returns string
        """
        #tmpFile = popen("cat /proc/version")
        #tmpString = tmpFile.readline().strip()
        #tmpFile.close()
        #return tmpString
        return uname()[2]
    
    def getNodeName(self):
        """
        get the name of the running system
        no args, returns string
        """
        return uname()[1]
    
    def getSystemUptime(self):
        """
        get the uptime of the running system
        no args, returns float
        """
        if access("/proc/uptime", R_OK):
            f_uptime = open('/proc/uptime', 'r')
            data = f_uptime.read()
            data = data[:-1]          # Remove the newline
            f_uptime.close()
            (uptime, idletime) = data.split(" ")
            return float(uptime)
        else:
            return -1.0
    
    def getSystemLoad(self):
        """
        get the cpu load of the running system
        no args, returns string
        """
        #f = open('/proc/loadavg', 'r')
        #data = f.read()
        #data = data[:-1]          # Remove the newline
        #f.close()
        #(load1min, load5min, load15min, nr_runningNr_tasks, last_pid) = \
         #data.split(" ")
        #return [float(load1min), float(load5min), float(load15min)]
        return getloadavg()
    
    def appendSlave(self, msgHeader, nodename=None):
        """
        append oid to slave list
        """
        if nodename:
            if nodename in zapi.getRoot(self):
                newSlaveNode = zapi.getRoot(self)[nodename]
            else:
                #self.oidSlave = msgHeader['from_oid']
                newSlaveNode = createObject(\
                    u"org.ict_ok.slave.slave.Slave")
                ISlave['objectID'].readonly = False
                newSlaveNode.objectID = msgHeader['from_oid']
                ISlave['objectID'].readonly = True
                newSlaveNode.ikName = unicode(nodename)
                notify(ObjectCreatedEvent(newSlaveNode))
                zapi.getRoot(self)[nodename] = newSlaveNode
        slaveSupervisor = zapi.queryUtility(IAdmUtilSupervisor,
                                            context=newSlaveNode)
        if slaveSupervisor:
            #slaveSupervisor.ipv4Master = msgHeader['to_ip']
            #slaveSupervisor.oidMaster = msgHeader['to_oid']
            slaveSupervisor.status2Master = u"connected"
            slaveSupervisor.ipv4Slave = msgHeader['from_ip']
            slaveSupervisor.oidSlave = msgHeader['from_oid']
            slaveSupervisor.lastSeenSlave = datetime.now(berlinTZ)
        self._p_changed = True
        mq_utility = zapi.queryUtility(IAdmUtilObjMQ)
        if mq_utility:
            my_data = {'cmd': 'connected'}
            my_data['header'] = mq_utility.switchFromTo(msgHeader)
            mq_utility.sendPerMq(my_data)

    def sendPing(self):
        """
        send ping request
        """
        mq_utility = zapi.getUtility(IAdmUtilObjMQ)
        my_data = {'cmd': 'ping',
                   'nodename': unicode(self.getNodeName())}
        if self.isMaster() and not self.isSlave():
            my_data['header'] = {'from_oid': self.objectID,
                                 'from_ip': self.ipv4My,
                                 'from_path': getPath(self),
                                 'to_oid': self.oidSlave,
                                 'to_ip': self.ipv4Slave,
                                 'to_path': u"/++etc++site/default"+\
                                 "/AdmUtilSupervisor"
                             }
            print "sendPing: %s" % my_data
            mq_utility.sendPerMq(my_data)
        if self.isSlave() and not self.isMaster():
            my_data['header'] = {'from_oid': self.objectID,
                                 'from_ip': self.ipv4My,
                                 'from_path': getPath(self),
                                 'to_oid': self.oidMaster,
                                 'to_ip': self.ipv4Master,
                                 'to_path': u"/++etc++site/default"+\
                                 "/AdmUtilSupervisor"
                             }
            print "sendPing: %s" % my_data
            mq_utility.sendPerMq(my_data)
        
            
    def sendPong(self, msgHeader, nodename=None):
        """
        revert message header and sends a pong as response to the ping
        """
        if nodename:
            if nodename in zapi.getRoot(self):
                newSlaveNode = zapi.getRoot(self)[nodename]
                slaveSupervisor = zapi.queryUtility(IAdmUtilSupervisor,
                                                    context=newSlaveNode)
                if slaveSupervisor:
                    slaveSupervisor.lastSeenMaster = datetime.now(berlinTZ)
        mq_utility = zapi.queryUtility(IAdmUtilObjMQ)
        if mq_utility:
            my_data = {'cmd': 'pong'}
            my_data['header'] = mq_utility.switchFromTo(msgHeader)
            mq_utility.sendPerMq(my_data)
            
    def sendObjectModified(self, event):
        """
        an Object was modified
        """
        print "AdmUtilSupervisor: an Object was modified"
        print "SV OID: %s" % self.objectID
        print "event: %s" % event

    def packDbByTicker(self, db=None):
        """
        will pack the database
        """
        #pass
        #print "ddd: <%s>" % dir(db)
        if not db:
            size_pre = db.getSize()
            db.pack(days=0)
            size_post = db.getSize()
            ratio = float(size_post)/size_pre*100
            self.appendEventHistory(\
                u"zodb packed on ticker; %d bytes -> %d bytes (%.1f%%)" % \
                (size_pre, size_post, ratio))
        #nextURL = self.request.get('nextURL', default=None)
        #if nextURL:
            #return self.request.response.redirect(nextURL)
        #else:
            #return self.request.response.redirect('./@@details.html')

    def receivedPing(self, msgHeader):
        """
        we have received a ping request
        """
        #print "receivedPing: !!!!!!!!!!!!!!!!!!!!!!!!! Ping"
        if self.isMaster() and not self.isSlave():
            self.lastSeenSlave = datetime.now(berlinTZ)
        if self.isSlave() and not self.isMaster():
            self.lastSeenMaster = datetime.now(berlinTZ)
        self.sendPong(msgHeader)

    def receivedPong(self, msgHeader):
        """
        we have received a pong response
        """
        #print "receivedPong: !!!!!!!!!!!!!!!!!!!!!!!!! Pong"
        if self.isMaster() and not self.isSlave():
            self.lastSeenSlave = datetime.now(berlinTZ)
        if self.isSlave() and not self.isMaster():
            self.lastSeenMaster = datetime.now(berlinTZ)

    def addObject(self, msgHeader, msgOldparent, msgNewparent, msgObj):
        """
        a new object should be created
        """
        print "addObject"
        print "msgHeader: %s" % msgHeader
        print "msgOldparent: %s" % msgOldparent
        print "msgNewparent: %s" % msgNewparent
        print "msgObj: %s" % msgObj
        if msgObj.has_key('myFactory'):
            newObj = zapi.createObject(msgObj['myFactory'])
            print "newObj: %s" % newObj
            print "msgObj['listAttr']: %s" % msgObj['listAttr']

            try:
                ISlave['objectID'].readonly = False
                for i in msgObj['listAttr']:
                    print "atr:  %s = %s" % (i, msgObj['listAttr'][i])
                    newObj.__setattr__(i, msgObj['listAttr'][i])
            finally:
                ISlave['objectID'].readonly = True
            newOid = msgObj['listAttr']['objectID']
            notify(ObjectCreatedEvent(newObj))
            #if (not msgOldparent) and (not msgNewparent):
                ##search from_oid -> ikslave
                #my_catalog = zapi.getUtility(ICatalog)
                #for result in my_catalog.searchResults(
                    #oid_index=msgHeader['from_oid']):
                    #print "result: %s = %s" % (result.ikName, result)
                    #if result.has_key(newOid):
                        #result.__delitem__(newOid)
                    #result[newOid] = newObj
            my_catalog = zapi.getUtility(ICatalog)
            newParentObj = None
            if not msgNewparent: # in root-folder of slave
                res = my_catalog.searchResults(oid_index=msgHeader['from_oid'])
                if len(res) > 0:
                    newParentObj = iter(res).next()
            else:
                res = my_catalog.searchResults(oid_index=msgNewparent)
                if len(res) > 0:
                    newParentObj = iter(res).next()
            if newParentObj and newParentObj.has_key(newOid):
                newParentObj.__delitem__(newOid)
            newParentObj[newOid] = newObj

    def reindex_db(self):
        """
        will reindex the catalogs of all tables in database
        """
        iid = zapi.getUtility(IIntIds, '')
        my_catalog = zapi.getUtility(ICatalog)
        my_catalog.updateIndexes()
        self.appendEventHistory(\
            u"reindex the catalogs of all tables in database")
#        connection = IConnection(self)
#        oc = connection.root()['_oq_collection']
#        for (oid, oobj) in iid.items():
#            if ISuperclass.providedBy(oobj.object):
#                try:
#                    oc.index(oobj.object)
#                except AttributeError:
#                    pass
#                except TypeError:
#                    pass
#        self.appendEventHistory(\
#            u"reindex the object query catalogs in database")

    def removeObject(self, msgHeader, msgOldparent,
                     msgNewparent, msgObjectOid):
        """
        an object should be removed
        """
        print "removeObject"
        print "msgHeader: %s" % msgHeader
        print "msgOldparent: %s" % msgOldparent
        print "msgNewparent: %s" % msgNewparent
        print "msgObjectOid: %s" % msgObjectOid
        my_catalog = zapi.getUtility(ICatalog)
        for result in my_catalog.searchResults(oid_index=msgObjectOid):
            print "result: %s = %s" % (result.ikName, result)
            #del result
            objParent = zapi.getParent(result)
            print "objParent: %s" % objParent
            if objParent.has_key(msgObjectOid):
                objParent.__delitem__(msgObjectOid)
                
    def modifyObject(self, msgHeader, msgObj):
        """
        an object should be modified
        """
        objectID = msgObj['listAttr']['objectID']
        my_catalog = zapi.getUtility(ICatalog)
        for result in my_catalog.searchResults(oid_index=objectID):
            for i in msgObj['listAttr']:
                old_attr = getattr(result, i)
                new_attr = msgObj['listAttr'][i]
                if not old_attr == new_attr:
                    setattr(result, i, new_attr)

    def moveObject(self, msgHeader, msgOldparent,
                   msgNewparent, msgObjectOid):
        """
        an object should be moved
        """
        print "moveObject"
        print "msgHeader: %s" % msgHeader
        print "msgOldparent: %s" % msgOldparent
        print "msgNewparent: %s" % msgNewparent
        print "msgObjectOid: %s" % msgObjectOid
        my_catalog = zapi.getUtility(ICatalog)
        newParentObj = None
        if not msgNewparent: # in root-folder of slave
            res = my_catalog.searchResults(oid_index=msgHeader['from_oid'])
            if len(res) > 0:
                newParentObj = iter(res).next()
        else:
            res = my_catalog.searchResults(oid_index=msgNewparent)
            if len(res) > 0:
                newParentObj = iter(res).next()
        objToMove = None
        res = my_catalog.searchResults(oid_index=msgObjectOid)
        if len(res) > 0:
            objToMove = iter(res).next()
        if objToMove and newParentObj:
            mover = IObjectMover(objToMove)
            if mover.moveableTo(newParentObj):
                mover.moveTo(newParentObj)
            else:
                raise Exception, "object not movable to new parent"
        #raise Exception, "moveObject not ready"

    def isMaster(self):
        """
        this supervisor is a master?
        """
        return bool(self.oidSlave)

    def isSlave(self):
        """
        this supervisor is a slave?
        """
        ifConnected = self.status2Master == u"connected"
        return bool(self.oidMaster) and ifConnected
        
    #def setStatus2Master(self, statustext):
        #"""
        #setter for status2master
        #"""
        #self.status2Master = statustext


    def exportAllData(self):
        """get data file for all objects"""
        #dataStructure = {
            #'objects': ['a', 'b', 'c'],
            #'conns': [1, 2, 3],
            #}
        dataStructure = {
            'objects': [],
            'conns': [],
            }
        sitemanger = zapi.getParent(self)
        locSitemanager = zapi.getParent(sitemanger)
        root_folder = zapi.getParent(locSitemanager)
        for folder in root_folder.values():
            for obj in folder.values():
                obj.getAllExportData(dataStructure)
        print "*" * 80
        from pprint import pprint
        pprint(dataStructure)
        print "*" * 80
        python_pickle = pickle.dumps(dataStructure)
        return toxml(python_pickle)

    def importAllData(self, xml_str):
        """get data file for all objects"""
        from pprint import pprint
        print "#" * 80
        data_structure = loads(xml_str)
        print 'objects'
        pprint(data_structure['objects'])
        print 'conns'
        pprint(data_structure['conns'])
        print "#" * 80
        for obj in data_structure['objects']:
            #import pdb
            #pdb.set_trace()
            print "Obj: ", obj['ikName']
            print "myFactory: ", obj['meta']['myFactory']
            o2=zapi.createObject(obj['meta']['myFactory'])
            print o2
        #print data_structure
        return True


class AdmUtilSupervisorSized(object):
    """ISized adapter for WorkflowProcessRepository."""

    adapts(IAdmUtilSupervisor)

    implements(ISized)

    def __init__(self, context):
        self.context = context

    def sizeForSorting(self):
        """See `ISized`"""
        return ('item', self.context.nbrStarts)

    def sizeForDisplay(self):
        """See `ISized`"""
        size = _('%d starts' % self.context.nbrStarts)
        #size.mapping = {'items': str(4)}
        return size
