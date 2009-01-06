# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232
#
"""startup of subsystem"""

__version__ = "$Id$"


# python imports
import logging
import transaction
from datetime import datetime

# zope imports
from zope.app.appsetup import appsetup
from zope.app.appsetup.bootstrap import getInformationFromEvent
from zope.app.appsetup.bootstrap import ensureUtility
from zope.dublincore.interfaces import IWriteZopeDublinCore

# ict_ok.org imports
from org.ict_ok.admin_utils.ticker.ticker import TickerThread
from org.ict_ok.admin_utils.supervisor.interfaces import \
     IAdmUtilSupervisor
from org.ict_ok.admin_utils.ticker.interfaces import IAdmUtilTicker
from org.ict_ok.admin_utils.ticker.ticker import AdmUtilTicker
from org.ict_ok.admin_utils.eventcrossbar.interfaces import \
     IAdmUtilEventCrossbar

logger = logging.getLogger("AdmUtilTicker")

def bootStrapSubscriberDatabase(event):
    """initialisation of ict_ok supervisor on first database startup
    """
    if appsetup.getConfigContext().hasFeature('devmode'):
        logger.info(u"starting bootStrapSubscriberDatabase (org.ict_ok...)")
    TickerThread.database = event.database
    dummy_db, connection, dummy_root, root_folder = \
            getInformationFromEvent(event)

    madeAdmUtilTicker = ensureUtility(root_folder, IAdmUtilTicker,
                                       'AdmUtilTicker', AdmUtilTicker, '',
                                       copy_to_zlog=False, asObject=True)

    if isinstance(madeAdmUtilTicker, AdmUtilTicker):
        logger.info(u"bootstrap: Ensure named AdmUtilTicker")
        dcore = IWriteZopeDublinCore(madeAdmUtilTicker)
        dcore.title = u"Ticker Utility"
        dcore.created = datetime.utcnow()
        madeAdmUtilTicker.ikName = dcore.title
        madeAdmUtilTicker.__post_init__()
        sitem = root_folder.getSiteManager()
        utils = [ util for util in sitem.registeredUtilities()
                    if util.provided.isOrExtends(IAdmUtilEventCrossbar)]
        utilEventXbar = utils[0].component
        if utilEventXbar.makeNewObjQueue(madeAdmUtilTicker):
            madeAdmUtilTicker.outEReceiver = utilEventXbar.getObjectId()
        utils = [ util for util in sitem.registeredUtilities()
                    if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: made IAdmUtilTicker-Utility")

    transaction.get().commit()
    connection.close()
