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

# phython imports
import logging
import threading
import atexit
import time

# zope imports
from zope.interface import implements
from zope.component import getUtility, queryUtility
import transaction
from zope.schema.fieldproperty import FieldProperty
from transaction.interfaces import IDataManager
from zope.app.component.hooks import getSite, setSite
from zope.app.intid.interfaces import IIntIds
from zope.security.simplepolicies import ParanoidSecurityPolicy
from zope.security.interfaces import IParticipation

# ict_ok.org imports
from org.ict_ok.admin_utils.supervisor.interfaces import \
     IAdmUtilSupervisor
from org.ict_ok.components.superclass.interfaces import ITicker
from org.ict_ok.admin_utils.ticker.interfaces import \
     IAdmUtilTicker, IEventIfAdmUtilTicker
from org.ict_ok.admin_utils.eventcrossbar.interfaces import \
     IAdmUtilEventCrossbar
from org.ict_ok.admin_utils.generators.nagios.interfaces import \
     IAdmUtilGeneratorNagios
from org.ict_ok.components.supernode.supernode import Supernode
from org.ict_ok.components.superclass.superclass import MsgEvent


class AdmUtilTicker(Supernode):
    """Implementation of local Ticker-Utility"""

    implements(IAdmUtilTicker, IEventIfAdmUtilTicker)

    eventOutObjs_1sec = FieldProperty(IEventIfAdmUtilTicker['eventOutObjs_1sec'])

    def __init__(self):
        Supernode.__init__(self)
        self.ikRevision = __version__

    def eventOut_1sec(self):
        """ sends one-second event """
        for my_event in self.eventOutObjs_1sec:
            inst_event = MsgEvent(self, my_event)
            self.injectOutEQueue(inst_event)


class SystemTickerPrincipal(object):
    implements(IParticipation)
    id = "idSystemTickerPrincipal"
    title = "Ticker User"
    description = ""
 
systemTickerPrincipal = SystemTickerPrincipal()
    
    
class SystemTickerParticipation(object):
    implements(IParticipation)
    principal = systemTickerPrincipal
    interaction = None


class TickerThread(threading.Thread):
    """This thread is started at configuration time from the
    `mail:queuedDelivery` directive handler.
    """
    implements(IDataManager)

    database = None
    log = logging.getLogger("TickerThread")
    __stopped = False

    def __init__(self):
        self.log.info("started (org)")
        # Use the default thread transaction manager.
        self.transaction_manager = transaction.manager
        self.interaction = ParanoidSecurityPolicy(SystemTickerParticipation())
        self.timestamp = time.gmtime()
        self.timestamp_min = self.timestamp[:-4]
        self.timestamp_hour = self.timestamp[:-5]
        self.timestamp_day = self.timestamp[:-6]
        self.timestamp_month = self.timestamp[:-7]
        self.timestamp_year = self.timestamp[:-8]
        threading.Thread.__init__(self)
    
    def run(self, forever=True):
        atexit.register(self.stop)
        while not self.__stopped:
            if TickerThread.database:
                try:
                    signal_min = False
                    signal_hour = False
                    signal_day = False
                    signal_month = False
                    signal_year = False
                    now_ts = time.gmtime()
                    if now_ts[:-4] != self.timestamp_min:
                        signal_min = True
                        self.timestamp_min = now_ts[:-4]
                    if now_ts[:-5] != self.timestamp_hour:
                        signal_hour = True
                        self.timestamp_hour = now_ts[:-5]
                    if now_ts[:-6] != self.timestamp_day:
                        signal_day = True
                        self.timestamp_day = now_ts[:-6]
                    if now_ts[:-7] != self.timestamp_month:
                        signal_month = True
                        self.timestamp_month = now_ts[:-7]
                    if now_ts[:-8] != self.timestamp_year:
                        signal_year = True
                        self.timestamp_year = now_ts[:-8]
                    if signal_min:
                        size_pre = TickerThread.database.getSize()
                        TickerThread.database.pack(days=0)
                        size_post = TickerThread.database.getSize()
                        ratio = float(size_post)/size_pre*100
                        print u"zodb packed on ticker; %d bytes -> %d bytes (%.1f%%)" % \
                              (size_pre, size_post, ratio)
                    conn = TickerThread.database.open()
                    root = conn.root()
                    root_folder = root['Application']
                    old_site = getSite()
                    setSite(root_folder)
                    # Utility Ticker
                    tmp_util = queryUtility(IAdmUtilTicker)
                    if tmp_util is not None:
                        tmp_util.eventOut_1sec()
                    # Utility Supervisor
                    tmp_util = queryUtility(IAdmUtilSupervisor)
                    uidutil = getUtility(IIntIds)
                    for (myid, myobj) in uidutil.items():
                        try:
                            tickerAdapter = ITicker(myobj.object)
                            if tickerAdapter:
                                tickerAdapter.db = TickerThread.database
                                tickerAdapter.triggered()
                                if signal_min:
                                    tickerAdapter.triggerMin()
                                if signal_hour:
                                    tickerAdapter.triggerHour()
                                if signal_day:
                                    tickerAdapter.triggerDay()
                                if signal_month:
                                    tickerAdapter.triggerMonth()
                                if signal_year:
                                    tickerAdapter.triggerYear()
                        except TypeError, err:
                            print "Error xxx: ", err
                    for utilInterface in (IAdmUtilSupervisor,
                                          IAdmUtilEventCrossbar,
                                          IAdmUtilTicker,
                                          IAdmUtilGeneratorNagios,
                                          ):
                        tmp_util = queryUtility(utilInterface)
                        if tmp_util is not None:
                            try:
                                tickerAdapter = ITicker(tmp_util)
                                if tickerAdapter:
                                    tickerAdapter.db = TickerThread.database
                                    tickerAdapter.triggered()
                                    if signal_min:
                                        tickerAdapter.triggerMin()
                                    if signal_hour:
                                        tickerAdapter.triggerHour()
                                    if signal_day:
                                        tickerAdapter.triggerDay()
                                    if signal_month:
                                        tickerAdapter.triggerMonth()
                                    if signal_year:
                                        tickerAdapter.triggerYear()
                            except TypeError, err:
                                print "Error xxx: ", err
                    setSite(old_site)
                    self.transaction_manager.commit()
                    conn.close()
                    # Blanket except because we don't want
                    # this thread to ever die
                except:
                    self.log.error("Error in Ticker", exc_info=True)
                    self.transaction_manager.abort()
                    conn.close()
            if forever:
                time.sleep(1)
            else:
                break

    def stop(self):
        self.log.info("stopped (org)")
        self.__stopped = True
