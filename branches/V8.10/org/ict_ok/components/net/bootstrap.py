# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611
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
from zope.app.catalog.text import TextIndex
from zope.app.catalog.interfaces import ICatalog
from zope.index.text.interfaces import ISearchableText
from zope.dublincore.interfaces import IZopeDublinCore
from zope.lifecycleevent import ObjectCreatedEvent
from zope.event import notify
from zope.component import createObject

# ict_ok.org imports
from org.ict_ok.admin_utils.supervisor.interfaces import IAdmUtilSupervisor

logger = logging.getLogger("Compon. Net")

def createLocalSystem(root_folder):
    pass

def bootStrapSubscriber(event):
    """initialisation of IntId utility on first database startup
    """
    if appsetup.getConfigContext().hasFeature('devmode'):
        logger.info(u"starting bootStrapSubscriberDatabase (org.ict_ok...)")
    dummy_db, connection, dummy_root, root_folder = \
            getInformationFromEvent(event)
    # search in global component registry
    sitem = root_folder.getSiteManager()
    # search for ICatalog
    utils = [ util for util in sitem.registeredUtilities()
              if util.provided.isOrExtends(ICatalog)]
    instUtilityICatalog = utils[0].component
    if not "net_oid_index" in instUtilityICatalog.keys():
        net_oid_index = TextIndex(interface=ISearchableText,
                                  field_name='getSearchableNetOid',
                                  field_callable=True)
        instUtilityICatalog['net_oid_index'] = net_oid_index
        # search for IAdmUtilSupervisor
        utils = [ util for util in sitem.registeredUtilities()
                  if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: ICatalog - create index for entry type 'net'")
    if not "net_ip_index" in instUtilityICatalog.keys():
        net_ip_index = TextIndex(interface=ISearchableText,
                                 field_name='getSearchableNetIp',
                                 field_callable=True)
        instUtilityICatalog['net_ip_index'] = net_ip_index
        # search for IAdmUtilSupervisor
        utils = [ util for util in sitem.registeredUtilities()
                  if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: ICatalog - create ip index for 'net'")

    createLocalSystem(root_folder)

    transaction.get().commit()
    connection.close()
