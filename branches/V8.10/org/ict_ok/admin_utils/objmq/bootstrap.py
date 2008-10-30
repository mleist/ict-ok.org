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
from org.ict_ok.admin_utils.objmq.interfaces import IAdmUtilObjMQ
from org.ict_ok.admin_utils.objmq.objmq import AdmUtilObjMQ

logger = logging.getLogger("AdmUtilObjMQ")

def bootStrapSubscriberDatabase(event):
    """initialisation of Message-Queue-Utility on first database startup
    """
    if appsetup.getConfigContext().hasFeature('devmode'):
        logger.info(u"starting bootStrapSubscriberDatabase (org.ict_ok...)")
    dummy_db, connection, dummy_root, root_folder = \
            getInformationFromEvent(event)

    madeAdmUtilObjMQ = ensureUtility(root_folder, IAdmUtilObjMQ,
                                        'AdmUtilObjMQ', AdmUtilObjMQ, '',
                                        copy_to_zlog=False, asObject=True)

    if isinstance(madeAdmUtilObjMQ, AdmUtilObjMQ):
        logger.info(u"bootstrap: Ensure named AdmUtilObjMQ")
        dcore = IWriteZopeDublinCore(madeAdmUtilObjMQ)
        dcore.title = u"Object Message Queue"
        dcore.created = datetime.utcnow()
        madeAdmUtilObjMQ.ikName = dcore.title
        madeAdmUtilObjMQ.__post_init__()
        sitem = root_folder.getSiteManager()
        utils = [ util for util in sitem.registeredUtilities()
                    if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: made IAdmUtilObjMQ-Utility")

    transaction.get().commit()
    connection.close()