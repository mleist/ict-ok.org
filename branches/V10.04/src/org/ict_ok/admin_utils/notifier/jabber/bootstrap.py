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
from org.ict_ok.admin_utils.notifier.jabber.interfaces import \
     INotifierJabber
from org.ict_ok.admin_utils.notifier.jabber.jabber import \
     NotifierJabber

logger = logging.getLogger("NotifierJabber")

def createUtils(root_folder, connection=None, dummy_db=None):
    madeSimple = ensureUtility(root_folder, 
                               INotifierJabber,
                               'NotifierJabber', 
                               NotifierJabber,
                               name='Notifier:Jabber',
                               copy_to_zlog=False)

    if isinstance(madeSimple, NotifierJabber):
        logger.info(u"bootstrap: Ensure named NotifierJabber")
        dcore = IWriteZopeDublinCore(madeSimple)
        dcore.title = u"Jabber Notifier"
        dcore.created = datetime.utcnow()
        madeSimple.ikName = dcore.title
        madeSimple.__post_init__()
        sitem = root_folder.getSiteManager()
        utils = [ util for util in sitem.registeredUtilities()
                    if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: made INotifierJabber-Utility")

    transaction.get().commit()
    if connection is not None:
        connection.close()

def bootStrapSubscriberDatabase_step2(event):
    """initialisation of jabber-generator utility on first database startup
    """
    print "bootStrapSubscriberDatabase_step2"
    dummy_db, connection, dummy_root, root_folder = \
            getInformationFromEvent(event)
    # search in global component registry
    sitem = root_folder.getSiteManager()
    utils = [ util for util in sitem.registeredUtilities()
              if util.provided.isOrExtends(INotifierJabber)]
    instIkNotifierJabber = utils[0].component
    if instIkNotifierJabber.enableConnector:
        instIkNotifierJabber.connect_server()
    print "enableConnector: %s" % instIkNotifierJabber.enableConnector
    print "ipv4Connector: %s" % instIkNotifierJabber.ipv4Connector
    print "portConnector: %s" % instIkNotifierJabber.portConnector
    print "lastSeenConnector: %s" % instIkNotifierJabber.lastSeenConnector

def bootStrapSubscriberDatabase_step1(event):
    """initialisation of jabber-generator utility on first database startup
    """
    if appsetup.getConfigContext().hasFeature('devmode'):
        logger.info(u"starting bootStrapSubscriberDatabase (org.ict_ok...)")
    print "bootStrapSubscriberDatabase_step1"
    dummy_db, connection, dummy_root, root_folder = \
            getInformationFromEvent(event)
    createUtils(root_folder, connection, dummy_db)
