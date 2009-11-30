# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0702,W0221
#
"""implementation of a "Object-Message-Queue-Utility" 
"""

__version__ = "$Id$"

# python imports
import logging
import threading
import atexit
import time
from datetime import datetime

# zope imports
from zope.app import zapi
from zope.interface import implements
from zope.component import getUtility, queryUtility
import transaction
from transaction.interfaces import IDataManager
from zope.app.component.hooks import getSite, setSite
from zope.app.intid.interfaces import IIntIds
from zope.security.simplepolicies import ParanoidSecurityPolicy
from zope.security.interfaces import IParticipation
from zope.app.catalog.interfaces import ICatalog
from zope.configuration.config import ConfigurationExecutionError

# pysnmp imports
from pysnmp.carrier.asynsock.dispatch import AsynsockDispatcher
from pysnmp.carrier.asynsock.dgram import udp
from pyasn1.codec.ber import decoder
from pysnmp.proto import api

# ict_ok.org imports
from org.ict_ok.admin_utils.supervisor.interfaces import \
     IAdmUtilSupervisor
from org.ict_ok.admin_utils.snmpd.interfaces import IAdmUtilSnmpd, ISnmptrapd
from org.ict_ok.components.supernode.supernode import Supernode
from org.ict_ok.components.interface.adapter.search import convertIpV4


class AdmUtilSnmpd(Supernode):
    """Implementation of local Snmpd-Utility"""

    implements(IAdmUtilSnmpd)

    def __init__(self):
        Supernode.__init__(self)
        self.ikRevision = __version__
        self.mrtg_data = None
        self.mrtg_data_timestamp = 0.0

    def getMrtgDataUpdateDatetime(self):
        """ update time of mrtg data as datetime object
        """
        return(datetime.fromtimestamp(self.mrtg_data_timestamp))


class SystemSnmpdPrincipal(object):
    """ this principal is used for internal security system """
    implements(IParticipation)
    id = "idSystemSnmpdPrincipal"
    title = "Snmpd User"
    description = ""
 
systemSnmpdPrincipal = SystemSnmpdPrincipal()
    
    
class SystemSnmpdParticipation(object):
    """ this participation is used for internal security system """
    implements(IParticipation)
    principal = systemSnmpdPrincipal
    interaction = None

class SnmpdThread(threading.Thread):
    """This thread is started at configuration time from the
    `mail:queuedDelivery` directive handler.
    this thread will handle all the incomming snmptraps
    """
    implements(IDataManager)

    database = None
    log = logging.getLogger("SnmpdThread")
    __stopped = False

    def __init__(self):
        self.log.info("started (org)")
        # Use the default thread transaction manager.
        try:
            self.transaction_manager = transaction.manager
            self.interaction = ParanoidSecurityPolicy(SystemSnmpdParticipation())
            self.transportDispatcher = AsynsockDispatcher()
            self.transportDispatcher.registerTransport(
                #    udp.domainName, udp.UdpSocketTransport().openServerMode(('localhost', 162))
                udp.domainName, udp.UdpSocketTransport().openServerMode(('', 11162))
            )
            self.transportDispatcher.registerRecvCbFun(self.cbFun)
            self.transportDispatcher.jobStarted(1) # this job would never finish
        except:
            # TODO: don't do this
            pass
        threading.Thread.__init__(self)

    def run(self, forever=True):
        """ forever loop which will run the snmptrapd dispatcher """
        atexit.register(self.stop)
        while not self.__stopped:
            if self.transportDispatcher is not None:
                self.transportDispatcher.runDispatcher()
            if forever:
                time.sleep(1)
            else:
                break

    def stop(self):
        """ stop the displatcher """
        self.log.info("stopped (org)")
        self.__stopped = True

    def cbFun(self, transportDispatcher, transportDomain, transportAddress, wholeMsg):
        """ this callback function which will handle the snmptrap message from pysnmp stack """
        while wholeMsg:
            msgVer = int(api.decodeMessageVersion(wholeMsg))
            if api.protoModules.has_key(msgVer):
                pMod = api.protoModules[msgVer]
            else:
                print 'Unsupported SNMP version %s' % msgVer
                return
            reqMsg, wholeMsg = decoder.decode(
                wholeMsg, asn1Spec=pMod.Message(),
                )
            print 'Notification message from %s:%s: ' % (
                transportDomain, transportAddress
                )
            reqPDU = pMod.apiMessage.getPDU(reqMsg)
            if reqPDU.isSameTypeWith(pMod.TrapPDU()):
                if SnmpdThread.database:
                    conn = SnmpdThread.database.open()
                    root = conn.root()
                    root_folder = root['Application']
                    old_site = getSite()
                    setSite(root_folder)
                    my_catalog = zapi.getUtility(ICatalog)
                    search_ip = pMod.apiTrapPDU.getAgentAddr(reqPDU).prettyPrint()
                    search_ip_conv = convertIpV4(search_ip)
                    for result in my_catalog.searchResults(\
                        interface_ip_index=search_ip_conv):
                        parentObj = result.__parent__
                        snmpAdapter = ISnmptrapd(parentObj)
                        snmpAdapter.triggered(reqPDU, msgVer, pMod)
                    setSite(old_site)
                    transaction.commit()
                    conn.close()
        return wholeMsg
