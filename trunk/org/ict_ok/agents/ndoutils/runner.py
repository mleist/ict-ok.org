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
import transaction
import gocept.runner


# zope imports
from zope.app.appsetup.bootstrap import getInformationFromEvent

# ict_ok.org imports
from org.ict_ok.version import getIkVersion
from org.ict_ok.admin_utils.supervisor.interfaces import IAdmUtilSupervisor


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


@gocept.runner.appmain(ticks=1.0, principal='zope.mgr')
def runner():
    """ this function will run every second
    """
    # import in this context
    import zope.app.component.hooks
    import zope.security.management
    import zope.app.appsetup.product
    from org.ict_ok.admin_utils.supervisor.interfaces import IAdmUtilSupervisor
    site = zope.app.component.hooks.getSite()
    sm = site.getSiteManager()
    admSupervisor = sm.getUtility(IAdmUtilSupervisor)
    print "admSupervisor: ", admSupervisor
    #uidutil = sm.getUtility(IIntIds)
    #for (myid, myobj) in uidutil.items():
        #try:
            #tickerAdapter = ITicker(myobj.object)
            #if tickerAdapter:
                #tickerAdapter.db = db
                #if signal_min:
                    #tickerAdapter.triggerMin()
                #if signal_hour:
                    #tickerAdapter.triggerHour()
                #if signal_day:
                    #tickerAdapter.triggerDay()
                #if signal_month:
                    #tickerAdapter.triggerMonth()
                #if signal_year:
                    #tickerAdapter.triggerYear()
        #except TypeError, err:
            #pass
