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
from zope.app.catalog.field import FieldIndex
from zope.app.catalog.interfaces import ICatalog
from zope.index.text.interfaces import ISearchableText
from zope.app.component.interfaces import ISite

# ict_ok.org imports
from org.ict_ok.admin_utils.supervisor.interfaces import \
     IAdmUtilSupervisor
from org.ict_ok.admin_utils.esx_vim.interfaces import IAdmUtilEsxVim
from org.ict_ok.admin_utils.esx_vim.esx_vim import AdmUtilEsxVim
from org.ict_ok.admin_utils.esx_vim.esx_vim import globalEsxVimUtility
from org.ict_ok.admin_utils.esx_vim.esx_vim import EsxVimConnectionThread

logger = logging.getLogger("AdmUtilEsxVim")

def recursiveEsxVimSubscriber(obj):
    """distibution of esx_vim event
    """

    if ISite.providedBy(obj):
        sitem = obj.getSiteManager()
        smList = list(sitem.getAllUtilitiesRegisteredFor(IAdmUtilEsxVim))
        for utilObj in smList:
            if IAdmUtilEsxVim.providedBy(utilObj) :
                globalEsxVimUtility.subscribeToEsxVim(utilObj)

def createUtils(root_folder, connection=None, dummy_db=None):
    madeAdmUtilEsxVim = ensureUtility(root_folder, IAdmUtilEsxVim,
                                      'AdmUtilEsxVim', AdmUtilEsxVim,
                                      name='AdmUtilEsxVim',
                                      copy_to_zlog=False, asObject=True)

    if isinstance(madeAdmUtilEsxVim, AdmUtilEsxVim):
        logger.info(u"bootstrap: Ensure named AdmUtilEsxVim")
        dcore = IWriteZopeDublinCore(madeAdmUtilEsxVim)
        dcore.title = u"ESX VIM"
        dcore.created = datetime.utcnow()
        madeAdmUtilEsxVim.ikName = dcore.title
        madeAdmUtilEsxVim.__post_init__()
        #madeAdmUtilEsxVim.connect2VimServer()
        sitem = root_folder.getSiteManager()
        utils = [ util for util in sitem.registeredUtilities()
                    if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: made IAdmUtilEsxVim-Utility")
    sitem = root_folder.getSiteManager()
    # search for ICatalog
    utils = [ util for util in sitem.registeredUtilities()
              if util.provided.isOrExtends(ICatalog)]
    instUtilityICatalog = utils[0].component
    if not "host_esx_uuid_index" in instUtilityICatalog.keys():
        host_esx_uuid_index = FieldIndex(interface=ISearchableText,
                                         field_name='getSearchableEsxUuid',
                                         field_callable=True)
        instUtilityICatalog['host_esx_uuid_index'] = host_esx_uuid_index
        # search for IAdmUtilSupervisor
        utils = [ util for util in sitem.registeredUtilities()
                  if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: ICatalog - create esx uuid index for entry type 'host'")


    recursiveEsxVimSubscriber(root_folder)
    
    transaction.get().commit()
    if connection is not None:
        connection.close()

def bootStrapSubscriberDatabase(event):
    """initialisation of esx_vim utility on first database startup
    """
    if appsetup.getConfigContext().hasFeature('devmode'):
        logger.info(u"starting bootStrapSubscriberDatabase (org.ict_ok...)")
    EsxVimConnectionThread.database = event.database
    dummy_db, connection, dummy_root, root_folder = \
            getInformationFromEvent(event)
    createUtils(root_folder, connection, dummy_db)
