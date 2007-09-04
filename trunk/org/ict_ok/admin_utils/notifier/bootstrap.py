# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101
#
"""startup of subsystem"""

__version__ = "$Id$"

# phython imports
import logging
import transaction
from datetime import datetime

# zope imports
from zope.app.appsetup import appsetup
from zope.app.appsetup.bootstrap import getInformationFromEvent
from zope.app.appsetup.bootstrap import ensureUtility
from zope.dublincore.interfaces import IWriteZopeDublinCore

# ict_ok.org imports
from org.ict_ok.admin_utils.supervisor.interfaces import \
     IAdmUtilSupervisor
from org.ict_ok.admin_utils.notifier.interfaces import INotifierUtil
from org.ict_ok.admin_utils.notifier.notifier import NotifierUtil

logger = logging.getLogger("Notifier")

def bootStrapSubscriberDatabase(event):
    """initialisation of Message-Queue-Utility on first database startup
    """
    if appsetup.getConfigContext().hasFeature('devmode'):
        logger.info(u"starting bootStrapSubscriberDatabase (org.ict_ok...)")
    dummy_db, connection, dummy_root, root_folder = \
            getInformationFromEvent(event)

    madeNotifier = ensureUtility(root_folder, INotifierUtil,
                                  'Notifier', NotifierUtil, '',
                                  copy_to_zlog=False, asObject=True)

    if isinstance(madeNotifier, NotifierUtil):
        logger.info(u"bootstrap: Ensure named Notifier")
        dcore = IWriteZopeDublinCore(madeNotifier)
        dcore.title = u"Notifier"
        dcore.created = datetime.utcnow()
        madeNotifier.__post_init__()
        sitem = root_folder.getSiteManager()
        utils = [ util for util in sitem.registeredUtilities()
                    if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: made INotifier-Utility")

    transaction.get().commit()
    connection.close()
