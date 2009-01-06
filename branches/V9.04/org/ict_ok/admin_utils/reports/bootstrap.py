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
from org.ict_ok.admin_utils.supervisor.interfaces import \
     IAdmUtilSupervisor
from org.ict_ok.admin_utils.reports.interfaces import IAdmUtilReports
from org.ict_ok.admin_utils.reports.reports import AdmUtilReports

logger = logging.getLogger("AdmUtilReports")

def bootStrapSubscriberDatabase(event):
    """initialisation of ict_ok supervisor on first database startup
    """
    if appsetup.getConfigContext().hasFeature('devmode'):
        logger.info(u"starting bootStrapSubscriberDatabase (org.ict_ok...)")
    dummy_db, connection, dummy_root, root_folder = \
            getInformationFromEvent(event)
    madeAdmUtilReports = ensureUtility(root_folder, IAdmUtilReports,
                                       'AdmUtilReports',
                                       AdmUtilReports, '',
                                       copy_to_zlog=False, asObject=True)
    if isinstance(madeAdmUtilReports, AdmUtilReports):
        logger.info(u"bootstrap: Ensure named AdmUtilReports")
        dcore = IWriteZopeDublinCore(madeAdmUtilReports)
        dcore.title = u"Reports Utility"
        dcore.created = datetime.utcnow()
        madeAdmUtilReports.ikName = dcore.title
        madeAdmUtilReports.__post_init__()
        sitem = root_folder.getSiteManager()
        utils = [ util for util in sitem.registeredUtilities()
                    if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: made IAdmUtilReports-Utility")
    transaction.get().commit()
    connection.close()
