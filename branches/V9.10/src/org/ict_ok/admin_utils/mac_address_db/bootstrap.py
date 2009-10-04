# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
#               Sebastian Napiorkowski <s.napiorkowski@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101
#
"""mac address db util

the mac address db util will display some information from ict-ok in form of a mac address db
"""

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
from org.ict_ok.admin_utils.mac_address_db.interfaces import \
     IAdmUtilMacAddressDb
from org.ict_ok.admin_utils.mac_address_db.mac_address_db import \
     AdmUtilMacAddressDb

logger = logging.getLogger("AdmUtilMacAddressDb")

def createUtils(root_folder, connection=None, dummy_db=None):
    madeAdmUtilMacAddressDb = ensureUtility(root_folder, IAdmUtilMacAddressDb,
                                       'AdmUtilMacAddressDb',
                                       AdmUtilMacAddressDb,
                                       name='AdmUtilMacAddressDb',
                                       copy_to_zlog=False, asObject=True)

    if isinstance(madeAdmUtilMacAddressDb, AdmUtilMacAddressDb):
        logger.info(u"bootstrap: Ensure named AdmUtilMacAddressDb")
        dcore = IWriteZopeDublinCore(madeAdmUtilMacAddressDb)
        dcore.title = u"MacAddressDb Utiltiy"
        dcore.created = datetime.utcnow()
        madeAdmUtilMacAddressDb.ikName = dcore.title
        madeAdmUtilMacAddressDb.__post_init__()
        sitem = root_folder.getSiteManager()
        utils = [util for util in sitem.registeredUtilities()
                 if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: made MacAddressDb Utiltiy")
    transaction.get().commit()
    if connection is not None:
        connection.close()

def bootStrapSubscriberDatabase(event):
    """initialisation of eventcrossbar utility on first database startup
    """
    if appsetup.getConfigContext().hasFeature('devmode'):
        logger.info(u"starting bootStrapSubscriberDatabase (org.ict_ok...)")
    dummy_db, connection, dummy_root, root_folder = \
            getInformationFromEvent(event)
    createUtils(root_folder, connection, dummy_db)

