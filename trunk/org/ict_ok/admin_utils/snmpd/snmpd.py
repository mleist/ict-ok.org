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

# ict_ok.org imports
from org.ict_ok.admin_utils.supervisor.interfaces import \
     IAdmUtilSupervisor
from org.ict_ok.components.superclass.interfaces import ISnmpd
from org.ict_ok.admin_utils.snmpd.interfaces import IAdmUtilSnmpd
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
        threading.Thread.__init__(self)

    #def setMaildir(self, maildir):
        #"""Set the maildir.

        #This method is used just to provide a `maildir` stubs ."""
        #self.maildir = maildir

    #def setQueuePath(self, path):
        #self.maildir = Maildir(path, True)

    #def setMailer(self, mailer):
        #self.mailer = mailer

    #def _parseMessage(self, message):
        #"""Extract fromaddr and toaddrs from the first two lines of
        #the `message`.

        #Returns a fromaddr string, a toaddrs tuple and the message
        #string.
        #"""

        #fromaddr = ""
        #toaddrs = ()
        #rest = ""

        #try:
            #first, second, rest = message.split('\n', 2)
        #except ValueError:
            #return fromaddr, toaddrs, message

        #if first.startswith("X-Zope-From: "):
            #i = len("X-Zope-From: ")
            #fromaddr = first[i:]

        #if second.startswith("X-Zope-To: "):
            #i = len("X-Zope-To: ")
            #toaddrs = tuple(second[i:].split(", "))

        #return fromaddr, toaddrs, rest

    def run(self, forever=True):
        atexit.register(self.stop)
        while not self.__stopped:
            if SnmpdThread.database:
                try:
                    conn = SnmpdThread.database.open()
                    root = conn.root()
                    root_folder = root['Application']
                    #self.interaction = ParanoidSecurityPolicy(SystemConfigurationParticipation())
                    #self.log.info("dddd: %s" % root_folder)
                    #my_obj = root_folder['0bbe5e583af8492266f91c90e87ce5690']
                    #self.log.info("ddd2: %s" % my_obj)
                    #my_obj.snmpdEvent()
                    #site = root_folder
                    old_site = getSite()
                    setSite(root_folder)
                    tmp_util = queryUtility(IAdmUtilSupervisor)
                    #print "IAdmUtilSupervisor: ", tmp_util
                    uidutil = getUtility(IIntIds)
                    #import pdb; pdb.set_trace()
                    for (myid, myobj) in uidutil.items():
                        try:
                            snmpdAdapter = ISnmpd(myobj.object)
                            if snmpdAdapter:
                                snmpdAdapter.triggered()
                        except TypeError, err:
                            print "Error xxx: ", err
                    tmp_util = queryUtility(IAdmUtilSnmpd)
                    if tmp_util:
                        print "1:", tmp_util
                        try:
                            snmpdAdapter = ISnmpd(tmp_util)
                            if snmpdAdapter:
                                snmpdAdapter.triggered()
                        except TypeError, err:
                            print "Error xxx: ", err
                        
                    #setSite(old_site)
                    self.transaction_manager.commit()
                    conn.close()
                    # Blanket except because we don't want
                    # this thread to ever die
                except:
                    self.log.error("Error in Snmpd", exc_info=True)
                    self.transaction_manager.abort()
                    conn.close()
            if forever:
                time.sleep(1)
            else:
                break

    def stop(self):
        self.log.info("stopped (org)")
        self.__stopped = True
