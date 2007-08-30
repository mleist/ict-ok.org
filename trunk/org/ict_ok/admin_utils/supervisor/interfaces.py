# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0213,W0232,W0622
#
"""Interface of supervisor"""

__version__ = "$Id$"

# zope imports
from zope.schema import Choice, Datetime, Int
from zope.i18nmessageid import MessageFactory

# ict_ok.org imports
from org.ict_ok.components.supernode.interfaces import ISupernode
from org.ict_ok.schema.ipvalid import IpValid
from org.ict_ok.schema.objectidvalid import ObjectIdValid

_ = MessageFactory('org.ict_ok')


class IAdmUtilSupervisor(ISupernode):
    """
    major component for registration and event distribution 
    """

    nbrStarts = Int(
        min = 0,
        title = _("Starts"),
        description = _("Number of Starts"),
        default = 0,
        readonly = True,
        required = True)

    ipv4My = IpValid(
        min_length = 1,
        max_length = 30,
        title = _("My active IP"),
        description = _("Active IP address of this host."),
        default = u"0.0.0.0",
        readonly = True,
        required = True)
    
    objectID = ObjectIdValid(
        title = _("My object id"),
        description = _("object id of this supervisor"),
        readonly = True,
        required = True)
    
    ipv4Master = IpValid(
        min_length = 1,
        max_length = 30,
        title = _("Master IP"),
        description = _("IP address of master."),
        default = u"0.0.0.0",
        readonly = False,
        required = False)
    
    oidMaster = ObjectIdValid(
        title = _("Master object id"),
        description = _("object id of our master supervisor"),
        readonly = False,
        required = False)

    lastSeenMaster = Datetime(
        title=_("last seen Master"),
        description=_("Time since last contact with the Master"),
        required=False)
    
    status2Master = Choice(
        title = _("status2Master"),
        description = _("Status of connection to master."),
        values = [ u"no master", u"connecting", u"permission denied", \
                   u"unknown system", u"connected", u"interrupted", \
                   u"will be a slave"],
        readonly = False,
        required = False )

    ipv4Slave = IpValid(
        min_length = 1,
        max_length = 30,
        title = _("Slave IP"),
        description = _("IP address of slave."),
        default = u"0.0.0.0",
        readonly = False,
        required = False)
    
    oidSlave = ObjectIdValid(
        title = _("Slave object id"),
        description = _("object id of our slave supervisor"),
        readonly = False,
        required = False)
    
    lastSeenSlave = Datetime(
        title=_("last seen Slave"),
        description=_("Time since last contact with the slave"),
        required=False)

    def getlastEvents(self):
        """getter for event list
        """

    def getStartCnt(self):
        """getter for start counter of all starts
        """

    def generateOid(*args ):
        """
          Generates a universally unique ID.
          Any arguments only create more randomness.
        """

    def getSystemVersion(self):
        """
        Version string of System
        no args, returns string
        """
        
    def getNetworkDevList(self):
        """
        get a list of network device names
        no args, returns list of strings
        """
    
    def getLocalMacAddress(self, dev="eth0"):
        """
        get the mac address of the running system device
        argument is device name, default is 'eth0'
        returns string
        """
    
    def getLocalIpV4AddressList(self, dev="eth0"):
        """
        get the IpV4 addresses of the running system device
        argument is device name, default is 'eth0'
        returns list of strings
        """
        
    def getNetworkInfoDict(slef):
        """
        returns an informational dictonary with network device settings
        """
        
    def getCpuVendorId(self):
        """
        get the cpu vendor of the running system
        no args, returns string
        """
    
    def getCpuModelName(self):
        """
        get the cpu model of the running system
        no args, returns string
        """
    
    def getKernelVersion(self):
        """
        get the kernel version of the running system
        no args, returns string
        """
        
    def getNodeName(self):
        """
        get the name of the running system
        no args, returns string
        """
    
    def getSystemUptime(self):
        """
        get the uptime of the running system
        no args, returns string
        """
    
    def getSystemLoad(self):
        """
        get the cpu load of the running system
        no args, returns string
        """
        
    def appendSlave(self, msgHeader):
        """
        append oid to slave list
        """
        
    def isMaster(self):
        """
        this supervisor is a master?
        """

    def isSlave(self):
        """
        this supervisor is a slave?
        """

    def sendPing(self):
        """
        send ping request
        """
            
    def sendPong(self, msgHeader, nodename=None):
        """
        revert message header and sends a pong as response to the ping
        """
        
    def receivedPing(self, msgHeader):
        """
        we have received a ping request
        """

    def receivedPong(self, msgHeader):
        """
        we have received a pong response
        """

    def addObject(self, msgHeader, msgOldparent, msgNewparent, msgObj):
        """
        a new object should be created
        """

    def removeObject(self, msgHeader, msgOldparent, msgNewparent, msgObjectOid):
        """
        an object should be removed
        """
        
    def modifyObject(self, msgHeader, msgObj):
        """
        an object should be modified
        """

    def moveObject(self, msgHeader, msgOldparent,
                   msgNewparent, msgObjectOid):
        """
        an object should be moved
        """
        
    #def setStatus2Master(self, statustext):
        #"""
        #setter for status2master
        #"""
