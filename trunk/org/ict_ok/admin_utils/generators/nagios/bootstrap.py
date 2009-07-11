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
from org.ict_ok.admin_utils.generators.nagios.interfaces import \
     IAdmUtilGeneratorNagios
from org.ict_ok.admin_utils.generators.nagios.nagios import \
     AdmUtilGeneratorNagios

logger = logging.getLogger("AdmUtilGeneratorNagios")

def createUtils(root_folder, connection=None, dummy_db=None):
    madeAdmUtilGeneratorNagios = ensureUtility(root_folder, 
                                               IAdmUtilGeneratorNagios,
                                               'AdmUtilGeneratorNagios', 
                                               AdmUtilGeneratorNagios,
                                               name='AdmUtilGeneratorNagios',
                                               copy_to_zlog=False, 
                                               asObject=True)

    if isinstance(madeAdmUtilGeneratorNagios, AdmUtilGeneratorNagios):
        logger.info(u"bootstrap: Ensure named AdmUtilGeneratorNagios")
        dcore = IWriteZopeDublinCore(madeAdmUtilGeneratorNagios)
        dcore.title = u"Nagios Scanner"
        dcore.created = datetime.utcnow()
        madeAdmUtilGeneratorNagios.ikName = dcore.title
        madeAdmUtilGeneratorNagios.__post_init__()
        sitem = root_folder.getSiteManager()
        utils = [ util for util in sitem.registeredUtilities()
                    if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: made IAdmUtilGeneratorNagios-Utility")

    transaction.get().commit()
    if connection is not None:
        connection.close()

def bootStrapSubscriberDatabase(event):
    """initialisation of nagios-generator utility on first database startup
    """
    if appsetup.getConfigContext().hasFeature('devmode'):
        logger.info(u"starting bootStrapSubscriberDatabase (org.ict_ok...)")
    dummy_db, connection, dummy_root, root_folder = \
            getInformationFromEvent(event)
    createUtils(root_folder, connection, dummy_db)

