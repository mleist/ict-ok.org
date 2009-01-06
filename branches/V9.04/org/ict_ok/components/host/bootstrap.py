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
from zope.app.catalog.field import FieldIndex
from zope.app.catalog.text import TextIndex
from zope.app.catalog.interfaces import ICatalog
from zope.index.text.interfaces import ISearchableText
from zope.dublincore.interfaces import IZopeDublinCore
from zope.lifecycleevent import ObjectCreatedEvent
from zope.event import notify
from zope.component import createObject

# ict_ok.org imports
from org.ict_ok.admin_utils.supervisor.interfaces import IAdmUtilSupervisor
from org.ict_ok.components.host.interfaces import IHost

logger = logging.getLogger("Compon. Host")

def createLocalSystem(root_folder):
    dateNow = datetime.utcnow()
    newHost = createObject(u'org.ict_ok.components.host.host.Host')
    notify(ObjectCreatedEvent(newHost))
    root_folder.__setitem__(newHost.getObjectId(), 
                            newHost)
    dcore = IZopeDublinCore(newHost, None)
    dcore.creators = [u'first bootstrap']
    newHost.ikComment += u"bootstrap on %s" % (dateNow)
    newHost.__setattr__("ikName", u'Local System')
    newHost.__setattr__("hostname", u'Local System')
    dcore.title = u'Local System'
    newHost.__setattr__("ikDesc", u'this is the ict-ok.org management-system')
    newHost.__setattr__("manufacturer", u'see ict-ok.org')
    newHost.__setattr__("vendor", u'see ict-ok.org')
    newHost.__setattr__("genNagios", True)
    dcore.created = dateNow

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
    if not "host_oid_index" in instUtilityICatalog.keys():
        host_oid_index = FieldIndex(interface=ISearchableText,
                                    field_name='getSearchableHostOid',
                                    field_callable=True)
        instUtilityICatalog['host_oid_index'] = host_oid_index
        # search for IAdmUtilSupervisor
        utils = [ util for util in sitem.registeredUtilities()
                  if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: ICatalog - create oid index for entry type 'host'")
    if not "host_hostname_index" in instUtilityICatalog.keys():
        host_hostname_index = FieldIndex(interface=ISearchableText,
                                         field_name='getSearchableHostHostname',
                                         field_callable=True)
        instUtilityICatalog['host_hostname_index'] = host_hostname_index
        # search for IAdmUtilSupervisor
        utils = [ util for util in sitem.registeredUtilities()
                  if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: ICatalog - create hostname index for entry type 'host'")
    if not "host_room_oid_index" in instUtilityICatalog.keys():
        host_room_oid_index = TextIndex(interface=ISearchableText,
                                        field_name='getSearchableHostRoomOid',
                                        field_callable=True)
        instUtilityICatalog['host_room_oid_index'] = host_room_oid_index
        # search for IAdmUtilSupervisor
        utils = [ util for util in sitem.registeredUtilities()
                  if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: ICatalog - create room index for entry type 'host'")

    # creates and stores the local system in ZODB
    # createLocalSystem(root_folder)
    
    transaction.get().commit()
    connection.close()
