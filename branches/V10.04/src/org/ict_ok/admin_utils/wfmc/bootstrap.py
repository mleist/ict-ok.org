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
from org.ict_ok.admin_utils.wfmc.interfaces import \
     IAdmUtilWFMC
from org.ict_ok.admin_utils.wfmc.wfmc import \
     AdmUtilWFMC

logger = logging.getLogger("AdmUtilWFMC")

def createUtils(root_folder, connection=None, dummy_db=None):
    madeAdmUtilWFMC = ensureUtility(root_folder, 
                                    IAdmUtilWFMC,
                                    'AdmUtilWFMC', 
                                    AdmUtilWFMC,
                                    name='AdmUtilWFMC',
                                    copy_to_zlog=False)
    
    if isinstance(madeAdmUtilWFMC, AdmUtilWFMC):
        logger.info(u"bootstrap: Ensure named AdmUtilWFMC")
        dcore = IWriteZopeDublinCore(madeAdmUtilWFMC)
        dcore.title = u"Workflow Manager"
        dcore.created = datetime.utcnow()
        madeAdmUtilWFMC.ikName = dcore.title
        madeAdmUtilWFMC.__post_init__()
        sitem = root_folder.getSiteManager()
        utils = [ util for util in sitem.registeredUtilities()
                  if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: made IAdmUtilWFMC-Utility")
    transaction.get().commit()
    if connection is not None:
        connection.close()

def bootStrapSubscriberDatabase(event):
    """initialisation of wfmc utility on first database startup
    """
    if appsetup.getConfigContext().hasFeature('devmode'):
        logger.info(u"starting bootStrapSubscriberDatabase (org.ict_ok...)")
    dummy_db, connection, dummy_root, root_folder = \
            getInformationFromEvent(event)
    createUtils(root_folder, connection, dummy_db)

