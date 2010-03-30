# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101
#
"""startup of ApplicationSoftware"""

__version__ = "$Id$"

# python imports
import logging
import transaction

# zope imports
from zope.app.appsetup import appsetup
from zope.app.appsetup.bootstrap import getInformationFromEvent
from zope.app.catalog.text import TextIndex
from zope.app.catalog.keyword import KeywordIndex
from zope.app.catalog.interfaces import ICatalog
from zope.index.text.interfaces import ISearchableText

# ict_ok.org imports
from org.ict_ok.libs.lib import ensureComponentFolderOnBootstrap
from org.ict_ok.admin_utils.supervisor.interfaces import IAdmUtilSupervisor
from org.ict_ok.components.appsoftware.interfaces import IApplicationSoftwareFolder

logger = logging.getLogger("Compon. ApplicationSoftware")

def createUtils(root_folder, connection=None, dummy_db=None):
    # search in global component registry
    sitem = root_folder.getSiteManager()
    # search for ICatalog
    utils = [ util for util in sitem.registeredUtilities()
              if util.provided.isOrExtends(ICatalog)]
    instUtilityICatalog = utils[0].component
    if not "appsoftware_oid_index" in instUtilityICatalog.keys():
        appsoftware_oid_index = KeywordIndex(interface=ISearchableText,
                                        field_name='getSearchableApplicationSoftwareOid',
                                        field_callable=True)
        instUtilityICatalog['appsoftware_oid_index'] = appsoftware_oid_index
        # search for IAdmUtilSupervisor
        utils = [ util for util in sitem.registeredUtilities()
                  if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: ICatalog - create index for entry type 'appsoftware'")

    ensureComponentFolderOnBootstrap(IApplicationSoftwareFolder,
                 u"ApplicationSoftwares",
                 u'org.ict_ok.components.appsoftware.appsoftware.ApplicationSoftwareFolder',
                 root_folder,
                 sitem)

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
    createUtils(root_folder, connection, dummy_db)
