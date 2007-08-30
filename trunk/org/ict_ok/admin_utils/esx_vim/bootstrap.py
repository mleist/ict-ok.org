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

def bootStrapSubscriberDatabase(event):
    """initialisation of esx_vim utility on first database startup
    """
    EsxVimConnectionThread.database = event.database
    dummy_db, connection, dummy_root, root_folder = \
            getInformationFromEvent(event)

    madeAdmUtilEsxVim = ensureUtility(root_folder, IAdmUtilEsxVim,
                                        'AdmUtilEsxVim', AdmUtilEsxVim, '',
                                        copy_to_zlog=False, asObject=True)

    if isinstance(madeAdmUtilEsxVim, AdmUtilEsxVim):
        logger.info(u"bootstrap: Ensure named AdmUtilEsxVim")
        dcore = IWriteZopeDublinCore(madeAdmUtilEsxVim)
        dcore.title = u"ESX VIM"
        dcore.created = datetime.utcnow()
        madeAdmUtilEsxVim.__post_init__()
        sitem = root_folder.getSiteManager()
        utils = [ util for util in sitem.registeredUtilities()
                    if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: made IAdmUtilEsxVim-Utility")

    recursiveEsxVimSubscriber(root_folder)
    
    transaction.get().commit()
    connection.close()
