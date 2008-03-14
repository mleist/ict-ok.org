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

# ict_ok imports
from org.ict_ok.admin_utils.supervisor.interfaces import \
     IAdmUtilSupervisor
from org.ict_ok.admin_utils.netscan.demo1.interfaces import \
     IAdmUtilDemo1
from org.ict_ok.admin_utils.netscan.demo1.demo1 import AdmUtilDemo1

logger = logging.getLogger("AdmUtilDemo1")

def bootStrapSubscriberDatabase(event):
    """initialisation of demo1-generator utility on first database startup
    """
    if appsetup.getConfigContext().hasFeature('devmode'):
        logger.info(u"starting bootStrapSubscriberDatabase (org.ict_ok...)")
    dummy_db, connection, dummy_root, root_folder = \
            getInformationFromEvent(event)

    madeNmap = ensureUtility(root_folder, 
                             IAdmUtilDemo1,
                             'AdmUtilDemo1', 
                             AdmUtilDemo1,
                             name='NetScanner:Demo1',
                             copy_to_zlog=False, 
                             asObject=True)

    if isinstance(madeNmap, AdmUtilDemo1):
        logger.info(u"bootstrap: Ensure named AdmUtilDemo1")
        dcore = IWriteZopeDublinCore(madeNmap)
        dcore.title = u"Net Scanner (Demo1)"
        dcore.created = datetime.utcnow()
        madeNmap.ikName = dcore.title
        madeNmap.__post_init__()
        sitem = root_folder.getSiteManager()
        utils = [ util for util in sitem.registeredUtilities()
                    if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instIkAdmUtilSupervisor = utils[0].component
        instIkAdmUtilSupervisor.appendEventHistory( \
            u" bootstrap: made IAdmUtilDemo1-Utility")

    transaction.get().commit()
    connection.close()
