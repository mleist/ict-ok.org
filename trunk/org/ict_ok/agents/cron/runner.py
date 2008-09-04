# -*- coding: utf-8 -*-
#
# Copyright (c) 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0621,W0212
#
"""Cron runner based on gocept.runner
"""

__version__ = "$Id$"

# python imports
import time
import logging
import transaction
import gocept.runner


# zope imports
from zope.app.appsetup.bootstrap import getInformationFromEvent

# ict_ok.org imports
from org.ict_ok.version import getIkVersion
from org.ict_ok.admin_utils.supervisor.interfaces import IAdmUtilSupervisor


class TimeCheckSpace:
    """ global memory class for cron purpose
    """
    def __init__(self):
        self.timestamp = time.gmtime()
        self.timestamp_min = self.timestamp[:-4]
        self.timestamp_hour = self.timestamp[:-5]
        self.timestamp_day = self.timestamp[:-6]
        self.timestamp_month = self.timestamp[:-7]
        self.timestamp_year = self.timestamp[:-8]

# and the real memory for cron purpose
timeSpace = TimeCheckSpace()

def bootStrapSubscriber(event):
    """ log the startup to our supervisor
    """
    dummy_db, connection, dummy_root, root_folder = \
            getInformationFromEvent(event)
    sitem = root_folder.getSiteManager()
    utils = [ util for util in sitem.registeredUtilities()
              if util.provided.isOrExtends(IAdmUtilSupervisor)]
    instAdmUtilSupervisor = utils[0].component
    instAdmUtilSupervisor.appendEventHistory(\
        u"'cron runner' started (Vers. %s) (%d bytes) (%d objects)" \
        % (getIkVersion(), dummy_db.getSize(), dummy_db.objectCount()))
    transaction.get().commit()
    connection.close()

def getTimeChangeSignals():
    """return a
    (signal_min, signal_hour, signal_day, signal_month, signal_year)
    tuple
    """
    global timeSpace
    signal_min = False
    signal_hour = False
    signal_day = False
    signal_month = False
    signal_year = False
    now_ts = time.gmtime()
    if now_ts[:-4] != timeSpace.timestamp_min:
        signal_min = True
        timeSpace.timestamp_min = now_ts[:-4]
    if now_ts[:-5] != timeSpace.timestamp_hour:
        signal_hour = True
        timeSpace.timestamp_hour = now_ts[:-5]
    if now_ts[:-6] != timeSpace.timestamp_day:
        signal_day = True
        timeSpace.timestamp_day = now_ts[:-6]
    if now_ts[:-7] != timeSpace.timestamp_month:
        signal_month = True
        timeSpace.timestamp_month = now_ts[:-7]
    if now_ts[:-8] != timeSpace.timestamp_year:
        signal_year = True
        timeSpace.timestamp_year = now_ts[:-8]
    return (signal_min, signal_hour,
            signal_day, signal_month,
            signal_year)


@gocept.runner.appmain(ticks=1.0, principal='zope.mgr')
def runner():
    """ this function will run every second
    """
    # import in this context
    from zope.app.intid.interfaces import IIntIds
    import time
    import zope.app.component.hooks
    import zope.security.management
    import zope.app.appsetup.product
    from org.ict_ok.components.superclass.interfaces import ITicker
    from org.ict_ok.admin_utils.supervisor.interfaces import IAdmUtilSupervisor
    (signal_min, signal_hour,
     signal_day, signal_month,
     signal_year) = getTimeChangeSignals()
    interaction = zope.security.management.getInteraction()
    principal = interaction.participations[0].principal
    site = zope.app.component.hooks.getSite()
    db = site._p_jar.db()
    sm = site.getSiteManager()
    admSupervisor = sm.getUtility(IAdmUtilSupervisor)
    uidutil = sm.getUtility(IIntIds)
    for (myid, myobj) in uidutil.items():
        try:
            tickerAdapter = ITicker(myobj.object)
            if tickerAdapter:
                tickerAdapter.db = db
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
            pass
