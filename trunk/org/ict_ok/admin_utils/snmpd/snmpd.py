# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
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

# phython imports
import logging
import threading
import atexit
import time

# zope imports
from zope.interface import implements
from zope.component import getUtility, queryUtility
import transaction
from transaction.interfaces import IDataManager
from zope.app.component.hooks import getSite, setSite
from zope.app.intid.interfaces import IIntIds
from zope.security.simplepolicies import ParanoidSecurityPolicy
from zope.security.interfaces import IParticipation

# pysnmp imports
from pysnmp.v4.carrier.asynsock.dispatch import AsynsockDispatcher
from pysnmp.v4.carrier.asynsock.dgram import udp
from pyasn1.codec.ber import decoder
from pysnmp.v4.proto import api

# ict_ok.org imports
from org.ict_ok.admin_utils.supervisor.interfaces import \
     IAdmUtilSupervisor
from org.ict_ok.admin_utils.snmpd.interfaces import IAdmUtilSnmpd, ISnmpd
from org.ict_ok.components.supernode.supernode import Supernode


class AdmUtilSnmpd(Supernode):
    """Implementation of local Snmpd-Utility"""

    implements(IAdmUtilSnmpd)

    def __init__(self):
        Supernode.__init__(self)
        self.ikRevision = __version__



class SystemSnmpdPrincipal(object):
    implements(IParticipation)
    id = "idSystemSnmpdPrincipal"
    title = "Snmpd User"
    description = ""
 
systemSnmpdPrincipal = SystemSnmpdPrincipal()
    
    
class SystemSnmpdParticipation(object):
    implements(IParticipation)
    principal = systemSnmpdPrincipal
    interaction = None


class SnmpdThread(threading.Thread):
    """This thread is started at configuration time from the
    `mail:queuedDelivery` directive handler.
    """
    implements(IDataManager)

    database = None
    log = logging.getLogger("SnmpdThread")
    __stopped = False

    def __init__(self):
        self.log.info("started (org)")
        # Use the default thread transaction manager.
        self.transaction_manager = transaction.manager
        self.interaction = ParanoidSecurityPolicy(SystemSnmpdParticipation())
        self.transportDispatcher = AsynsockDispatcher()
        self.transportDispatcher.registerTransport(
            #    udp.domainName, udp.UdpSocketTransport().openServerMode(('localhost', 162))
            udp.domainName, udp.UdpSocketTransport().openServerMode(('', 1620))
        )
        self.transportDispatcher.registerRecvCbFun(self.cbFun)
        self.transportDispatcher.jobStarted(1) # this job would never finish
        threading.Thread.__init__(self)

    def run(self, forever=True):
        atexit.register(self.stop)
        while not self.__stopped:
            print "+++++++++++++++++++++++++++++++++++++9a"
            self.transportDispatcher.runDispatcher()
            print "+++++++++++++++++++++++++++++++++++++9b"
            if forever:
                time.sleep(1)
            else:
                break

    def stop(self):
        self.log.info("stopped (org)")
        self.__stopped = True

    def cbFun(self, transportDispatcher, transportDomain, transportAddress, wholeMsg):
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
                if msgVer == api.protoVersion1:
                    print 'Enterprise: %s' % (
                        pMod.apiTrapPDU.getEnterprise(reqPDU).prettyPrint()
                        )
                    print 'Agent Address: %s' % (
                        pMod.apiTrapPDU.getAgentAddr(reqPDU).prettyPrint()
                        )
                    print 'Generic Trap: %s' % (
                        pMod.apiTrapPDU.getGenericTrap(reqPDU).prettyPrint()
                        )
                    print 'Specific Trap: %s' % (
                        pMod.apiTrapPDU.getSpecificTrap(reqPDU).prettyPrint()
                        )
                    print 'Uptime: %s' % (
                        pMod.apiTrapPDU.getTimeStamp(reqPDU).prettyPrint()
                        )
                    varBinds = pMod.apiTrapPDU.getVarBindList(reqPDU)
                else:
                    varBinds = pMod.apiPDU.getVarBindList(reqPDU)
                print 'Var-binds:'
                for oid, val in varBinds:
                    print '%s = %s' % (oid.prettyPrint(), val.prettyPrint())
                # ---------------------------------------------------
                if SnmpdThread.database:
                    conn = SnmpdThread.database.open()
                    root = conn.root()
                    root_folder = root['Application']
                    old_site = getSite()
                    setSite(root_folder)
                    tmp_util = queryUtility(IAdmUtilSupervisor)
                    print "IAdmUtilSupervisor: ", tmp_util
                    uidutil = getUtility(IIntIds)
                    for (myid, myobj) in uidutil.items():
                        print "ddd:", myobj
                        try:
                            tickerAdapter = ISnmpd(myobj)
                            if tickerAdapter:
                                tickerAdapter.triggered(reqPDU)
                        except TypeError, err:
                            print "Error xxx: ", err
                    tmp_util = queryUtility(IAdmUtilSnmpd)
                    if tmp_util:
                        print "1:", tmp_util
                    setSite(old_site)
                    transaction.commit()
                    conn.close()
                # ---------------------------------------------------

        return wholeMsg
