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

# zope imports
from zope.app.appsetup import appsetup
from zope.app.appsetup.bootstrap import getInformationFromEvent
from zope.app.catalog.text import TextIndex
from zope.app.intid.interfaces import IIntIds
from zope.app.catalog.interfaces import ICatalog
from zope.index.text.interfaces import ISearchableText

# ict_ok.org imports
from org.ict_ok.libs.lib import ensureComponentFolderOnBootstrap
from org.ict_ok.admin_utils.supervisor.interfaces import IAdmUtilSupervisor
from org.ict_ok.components.net.interfaces import INetFolder 

logger = logging.getLogger("Compon. Net")

def createLocalSystem(root_folder):
    pass

def createUtils(root_folder, connection=None, dummy_db=None):
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

    ensureComponentFolderOnBootstrap(\
         INetFolder,
         u"Nets",
         u'org.ict_ok.components.net.net.NetFolder',
         root_folder,
         sitem)

    transaction.get().commit()
    if connection is not None:
        connection.close()

def deleteUtils(root_folder, connection=None, dummy_db=None):
    # search in global component registry
    sitem = root_folder.getSiteManager()
    # search for ICatalog
    utils = [ util for util in sitem.registeredUtilities()
              if util.provided.isOrExtends(ICatalog)]
    instUtilityICatalog = utils[0].component
    utils = [ util for util in sitem.registeredUtilities()
              if util.provided.isOrExtends(IIntIds)]
    instUtilityIIntIds = utils[0].component
    if "net_oid_index" in instUtilityICatalog.keys():
        indx = instUtilityICatalog['net_oid_index']
        indx.clear()
        del instUtilityICatalog['net_oid_index']
        # search for IAdmUtilSupervisor
        utils = [ util for util in sitem.registeredUtilities()
                  if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: ICatalog - delete index for entry type 'net'")
        
    if "net_ip_index" in instUtilityICatalog.keys():
        indx = instUtilityICatalog['net_ip_index']
        indx.clear()
        del instUtilityICatalog['net_ip_index']
        # search for IAdmUtilSupervisor
        utils = [ util for util in sitem.registeredUtilities()
                  if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: ICatalog - delete ip index for 'net'")

    allSubFolders = [folder for folder in root_folder.values()
                     if INetFolder.providedBy(folder)]
    for i_subFolder in allSubFolders:
        instUtilityIIntIds.unregister(i_subFolder)
        i_subFolder.disconnectFromEventXbar()
        del i_subFolder
    if 'Nets' in root_folder.keys():
        root_folder['Nets'].disconnectFromEventXbar()
        del root_folder['Nets']

    transaction.get().commit()
    if connection is not None:
        connection.close()

def bootStrapSubscriber(event):
    """initialisation of IntId utility on first database startup
    """
    if appsetup.getConfigContext().hasFeature('devmode'):
        logger.info(u"starting bootStrapSubscriberDatabase (org.ict_ok...)")
    dummy_db, connection, dummy_root, root_folder = \
            getInformationFromEvent(event)
    deleteUtils(root_folder, connection, dummy_db)
