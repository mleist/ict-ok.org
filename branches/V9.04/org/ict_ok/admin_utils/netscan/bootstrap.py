# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
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
from org.ict_ok.admin_utils.supervisor.interfaces import \
     IAdmUtilSupervisor
from org.ict_ok.admin_utils.netscan.interfaces import INetScan
from org.ict_ok.admin_utils.netscan.netscan import NetScan

logger = logging.getLogger("NetScan")

def bootStrapSubscriberDatabase(event):
    """initialisation of Message-Queue-Utility on first database startup
    """
    if appsetup.getConfigContext().hasFeature('devmode'):
        logger.info(u"starting bootStrapSubscriberDatabase (org.ict_ok...)")
    dummy_db, connection, dummy_root, root_folder = \
            getInformationFromEvent(event)

    madeNetScan = ensureUtility(root_folder, INetScan,
                                 'NetScan', NetScan, '',
                                 copy_to_zlog=False, asObject=True)

    if isinstance(madeNetScan, NetScan):
        logger.info(u"bootstrap: Ensure named NetScan")
        dcore = IWriteZopeDublinCore(madeNetScan)
        dcore.title = u"Net Scanner"
        dcore.created = datetime.utcnow()
        madeNetScan.ikName = dcore.title
        madeNetScan.__post_init__()
        sitem = root_folder.getSiteManager()
        utils = [ util for util in sitem.registeredUtilities()
                    if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: made INetScan-Utility")

    transaction.get().commit()
    connection.close()
