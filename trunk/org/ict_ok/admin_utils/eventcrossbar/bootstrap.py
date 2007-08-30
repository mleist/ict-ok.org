# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
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
from zope.app.appsetup.bootstrap import getInformationFromEvent
from zope.app.appsetup.bootstrap import ensureUtility
from zope.dublincore.interfaces import IWriteZopeDublinCore
from zope.app.component.interfaces import ISite
from zope.app.container.interfaces import IContainer

# ict_ok.org imports
from org.ict_ok.admin_utils.supervisor.interfaces import \
     IAdmUtilSupervisor
from org.ict_ok.admin_utils.eventcrossbar.interfaces import IAdmUtilEventCrossbar
from org.ict_ok.admin_utils.eventcrossbar.eventcrossbar import AdmUtilEventCrossbar
from org.ict_ok.admin_utils.eventcrossbar.eventcrossbar import globalEventCrossbarUtility
from org.ict_ok.admin_utils.eventcrossbar.eventcrossbar import ContentDDD

logger = logging.getLogger("AdmUtilEventCrossbar")

def recursiveEventCrossbarSubscriber(obj):
    """distibution of eventcrossbar event
    """

    if ISite.providedBy(obj):
        sitem = obj.getSiteManager()
        smList = list(sitem.getAllUtilitiesRegisteredFor(IAdmUtilEventCrossbar))
        for utilObj in smList:
            if IAdmUtilEventCrossbar.providedBy(utilObj) :
                globalEventCrossbarUtility.subscribeToEventCrossbar(utilObj)
    if IContainer.providedBy(obj):
        for (dummy_name, subObject) in obj.items():
            recursiveEventCrossbarSubscriber(subObject)

def bootStrapSubscriberDatabase(event):
    """initialisation of eventcrossbar utility on first database startup
    """
    dummy_db, connection, dummy_root, root_folder = \
            getInformationFromEvent(event)

    madeAdmUtilEventCrossbar = ensureUtility(root_folder, IAdmUtilEventCrossbar,
                                        'AdmUtilEventCrossbar', AdmUtilEventCrossbar, '',
                                        copy_to_zlog=False, asObject=True)

    if isinstance(madeAdmUtilEventCrossbar, AdmUtilEventCrossbar):
        logger.info(u"bootstrap: Ensure named AdmUtilEventCrossbar")
        contentDDD = ContentDDD()
        setattr(madeAdmUtilEventCrossbar, 'ddd', contentDDD)
        
        from zope.app.container.contained import contained, setitem
        madeAdmUtilEventCrossbar['ddd'] = contentDDD
        dcore = IWriteZopeDublinCore(madeAdmUtilEventCrossbar)
        dcore.title = u"Event Crossbar"
        dcore.created = datetime.utcnow()
        madeAdmUtilEventCrossbar.__post_init__()
        sitem = root_folder.getSiteManager()
        utils = [ util for util in sitem.registeredUtilities()
                    if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: made IAdmUtilEventCrossbar-Utility")

    recursiveEventCrossbarSubscriber(root_folder)
    
    transaction.get().commit()
    connection.close()
