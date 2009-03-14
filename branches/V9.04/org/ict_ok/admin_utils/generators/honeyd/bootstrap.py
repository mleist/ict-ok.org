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
from org.ict_ok.admin_utils.generators.honeyd.interfaces import \
     IAdmUtilGeneratorHoneyd
from org.ict_ok.admin_utils.generators.honeyd.honeyd import \
     AdmUtilGeneratorHoneyd

logger = logging.getLogger("AdmUtilGeneratorHoneyd")

def createUtils(root_folder, connection=None, dummy_db=None):
    madeAdmUtilGeneratorHoneyd = ensureUtility(root_folder, 
                                                 IAdmUtilGeneratorHoneyd,
                                                 'AdmUtilGeneratorHoneyd', 
                                                 AdmUtilGeneratorHoneyd, '',
                                                 copy_to_zlog=False, 
                                                 asObject=True)

    if isinstance(madeAdmUtilGeneratorHoneyd, AdmUtilGeneratorHoneyd):
        logger.info(u"bootstrap: Ensure named AdmUtilGeneratorHoneyd")
        dcore = IWriteZopeDublinCore(madeAdmUtilGeneratorHoneyd)
        dcore.title = u"Honeyd"
        dcore.created = datetime.utcnow()
        madeAdmUtilGeneratorHoneyd.ikName = dcore.title
        madeAdmUtilGeneratorHoneyd.__post_init__()
        sitem = root_folder.getSiteManager()
        utils = [ util for util in sitem.registeredUtilities()
                    if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: made IAdmUtilGeneratorHoneyd-Utility")

    transaction.get().commit()
    if connection is not None:
        connection.close()

def bootStrapSubscriberDatabase(event):
    """initialisation of honeyd-generator utility on first database startup
    """
    if appsetup.getConfigContext().hasFeature('devmode'):
        logger.info(u"starting bootStrapSubscriberDatabase (org.ict_ok...)")
    dummy_db, connection, dummy_root, root_folder = \
            getInformationFromEvent(event)
    createUtils(root_folder, connection, dummy_db)

