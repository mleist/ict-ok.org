# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0232
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
from zope.app.component.interfaces import ISite
from zope.app.container.interfaces import IContainer

# ict_ok.org imports
from org.ict_ok.admin_utils.supervisor.interfaces import \
     IAdmUtilSupervisor
from org.ict_ok.admin_utils.cron.interfaces import IAdmUtilCron
from org.ict_ok.admin_utils.cron.cron import AdmUtilCron
from org.ict_ok.admin_utils.cron.cron import globalCronUtility

logger = logging.getLogger("AdmUtilCron")

def recursiveCronSubscriber(obj):
    """distibution of cron event
    """

    if ISite.providedBy(obj):
        sitem = obj.getSiteManager()
        smList = list(sitem.getAllUtilitiesRegisteredFor(IAdmUtilCron))
        for utilObj in smList:
            if IAdmUtilCron.providedBy(utilObj) :
                globalCronUtility.subscribeToCron(utilObj)
    if IContainer.providedBy(obj):
        for (dummy_name, subObject) in obj.items():
            recursiveCronSubscriber(subObject)

def bootStrapSubscriberDatabase(event):
    """initialisation of cron utility on first database startup
    """
    if appsetup.getConfigContext().hasFeature('devmode'):
        logger.info(u"starting bootStrapSubscriberDatabase (org.ict_ok...)")
    dummy_db, connection, dummy_root, root_folder = \
            getInformationFromEvent(event)

    madeAdmUtilCron = ensureUtility(root_folder, IAdmUtilCron,
                                    'AdmUtilCron', AdmUtilCron, '',
                                    copy_to_zlog=False, asObject=True)

    if isinstance(madeAdmUtilCron, AdmUtilCron):
        logger.info(u"bootstrap: Ensure named AdmUtilCron")
        dcore = IWriteZopeDublinCore(madeAdmUtilCron)
        dcore.title = u"Timer"
        dcore.created = datetime.utcnow()
        madeAdmUtilCron.ikName = dcore.title
        madeAdmUtilCron.__post_init__()
        sitem = root_folder.getSiteManager()
        utils = [ util for util in sitem.registeredUtilities()
                    if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: made IAdmUtilCron-Utility")

    recursiveCronSubscriber(root_folder)
    
    transaction.get().commit()
    connection.close()
