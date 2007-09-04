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

# zope imports
from zope.app.appsetup import appsetup
from zope.app.appsetup.bootstrap import getInformationFromEvent
from zope.app.catalog.text import TextIndex
from zope.app.catalog.interfaces import ICatalog
from zope.index.text.interfaces import ISearchableText

# ict_ok.org imports
from org.ict_ok.admin_utils.supervisor.interfaces import IAdmUtilSupervisor

logger = logging.getLogger("Compon. Interface")

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
    if not "interface_oid_index" in instUtilityICatalog.keys():
        interface_oid_index = TextIndex(interface=ISearchableText,
                                        field_name='getSearchableInterfaceOid',
                                        field_callable=True)
        instUtilityICatalog['interface_oid_index'] = interface_oid_index
        # search for IAdmUtilSupervisor
        utils = [ util for util in sitem.registeredUtilities()
                  if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: ICatalog - create index for entry type 'interface'")
    if not "interface_ip_index" in instUtilityICatalog.keys():
        interface_ip_index = TextIndex(interface=ISearchableText,
                                       field_name='getSearchableInterfaceIp',
                                       field_callable=True)
        instUtilityICatalog['interface_ip_index'] = interface_ip_index
        # search for IAdmUtilSupervisor
        utils = [ util for util in sitem.registeredUtilities()
                  if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: ICatalog - create ip index for 'interface'")
    if not "interface_mac_index" in instUtilityICatalog.keys():
        interface_mac_index = TextIndex(interface=ISearchableText,
                                        field_name='getSearchableInterfaceMac',
                                        field_callable=True)
        instUtilityICatalog['interface_mac_index'] = interface_mac_index
        # search for IAdmUtilSupervisor
        utils = [ util for util in sitem.registeredUtilities()
                  if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: ICatalog - create mac index for 'interface'")
        
    transaction.get().commit()
    connection.close()
