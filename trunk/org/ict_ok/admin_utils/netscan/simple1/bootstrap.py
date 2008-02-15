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
from org.ict_ok.admin_utils.netscan.simple1.interfaces import \
     IAdmUtilSimple1
from org.ict_ok.admin_utils.netscan.simple1.simple1 import \
     AdmUtilSimple1

logger = logging.getLogger("AdmUtilSimple1")

def bootStrapSubscriberDatabase(event):
    """initialisation of simple1-generator utility on first database startup
    """
    if appsetup.getConfigContext().hasFeature('devmode'):
        logger.info(u"starting bootStrapSubscriberDatabase (org.ict_ok...)")
    dummy_db, connection, dummy_root, root_folder = \
            getInformationFromEvent(event)

    madeSimple = ensureUtility(root_folder, 
                               IAdmUtilSimple1,
                               'AdmUtilSimple1', 
                               AdmUtilSimple1,
                               name='NetScanner:Simple1',
                               copy_to_zlog=False, 
                               asObject=True)

    if isinstance(madeSimple, AdmUtilSimple1):
        logger.info(u"bootstrap: Ensure named AdmUtilSimple1")
        dcore = IWriteZopeDublinCore(madeSimple)
        dcore.title = u"Net Scanner (Simple1)"
        dcore.created = datetime.utcnow()
        madeSimple.ikName = dcore.title
        madeSimple.__post_init__()
        sitem = root_folder.getSiteManager()
        utils = [ util for util in sitem.registeredUtilities()
                    if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: made IAdmUtilSimple1-Utility")

    transaction.get().commit()
    connection.close()
