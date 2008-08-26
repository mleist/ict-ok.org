# -*- coding: utf-8 -*-
#
# Copyright (c) 2007,
#               Thomas Richter <thomas.richter at xwml.de>,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0611
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
from org.ict_ok.admin_utils.public_viewing.interfaces import \
     IAdmUtilPublicViewing
from org.ict_ok.admin_utils.supervisor.interfaces import \
     IAdmUtilSupervisor
from org.ict_ok.admin_utils.public_viewing.public_viewing import \
     AdmUtilPublicViewing

logger = logging.getLogger("AdmUtilPublicViewing")

def bootStrapSubscriberDatabase(event):
    """initialisation of usermanagement utility on first database startup
    """
    if appsetup.getConfigContext().hasFeature('devmode'):
        logger.info(u"starting bootStrapSubscriberDatabase (org.ict_ok...)")
    dummy_db, connection, dummy_root, root_folder = \
            getInformationFromEvent(event)

    madePublicViewing = ensureUtility(\
        root_folder,
        IAdmUtilPublicViewing,
        'AdmUtilPublicViewing',
        AdmUtilPublicViewing,
        copy_to_zlog=False,
        asObject=True)

    if isinstance(madePublicViewing, AdmUtilPublicViewing):
        logger.info(u"bootstrap: Ensure named AdmUtilPublicViewing")
        dcore = IWriteZopeDublinCore(madePublicViewing)
        dcore.title = u"Public Viewing"
        dcore.created = datetime.utcnow()
        madePublicViewing.ikName = dcore.title
        madePublicViewing.__post_init__()
        sitem = root_folder.getSiteManager()
        utils = [ util for util in sitem.registeredUtilities()
                    if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: made AdmUtilPublicViewing-Utility")
    transaction.get().commit()
    connection.close()
