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
from pytz import timezone

# zope imports
from zope.app.appsetup import appsetup
from zope.app.appsetup.bootstrap import getInformationFromEvent
from zope.app.appsetup.bootstrap import ensureUtility
from zope.dublincore.interfaces import IWriteZopeDublinCore
from zope.app.intid import IntIds
from zope.app.intid.interfaces import IIntIds
from zope.app.catalog.catalog import Catalog
from zope.app.catalog.text import TextIndex
from zope.app.catalog.interfaces import ICatalog
from zope.index.text.interfaces import ISearchableText

# ict_ok.org imports
from org.ict_ok.admin_utils.supervisor.interfaces import \
     IAdmUtilSupervisor

logger = logging.getLogger("Compon. Supernode")
berlinTZ = timezone('Europe/Berlin')

def bootStrapSubscriber(event):
    """initialisation of IntId utility on first database startup
    """
    if appsetup.getConfigContext().hasFeature('devmode'):
        logger.info(u"starting bootStrapSubscriberDatabase (org.ict_ok...)")
    dummy_db, connection, dummy_root, root_folder = \
            getInformationFromEvent(event)

    madeUtilityIIntIds = ensureUtility(root_folder, 
                                       IIntIds, 
                                       '', 
                                       IntIds, 
                                       '', 
                                       copy_to_zlog=False, 
                                       asObject=True)

    if isinstance(madeUtilityIIntIds, IntIds):
        logger.info(u"bootstrap: made IIntIds-Utility")
        dcore = IWriteZopeDublinCore(madeUtilityIIntIds)
        dcore.title = u"Object Id Manager"
        dcore.created = datetime.now(berlinTZ)
        sitem = root_folder.getSiteManager()
        utils = [ util for util in sitem.registeredUtilities()
                    if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: made IIntIds-Utility")

    madeUtilityICatalog = ensureUtility(root_folder, 
                                        ICatalog, 
                                        '', 
                                        Catalog, 
                                        '', 
                                        copy_to_zlog=False, 
                                        asObject=True)

    if isinstance(madeUtilityICatalog, Catalog):
        logger.info(u"bootstrap: made ICatalog-Utility")
        dcore = IWriteZopeDublinCore(madeUtilityICatalog)
        dcore.title = u"Search Manager"
        dcore.created = datetime.now(berlinTZ)
        oid_index = TextIndex(interface=ISearchableText,
                               field_name='getSearchableOid',
                               field_callable=True)
        madeUtilityICatalog['oid_index'] = oid_index
        sitem = root_folder.getSiteManager()
        utils = [ util for util in sitem.registeredUtilities()
                    if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: made ICatalog-Utility")
        
    # search in global component registry
    sitem = root_folder.getSiteManager()
    # search for ICatalog
    utils = [ util for util in sitem.registeredUtilities()
              if util.provided.isOrExtends(ICatalog)]
    instUtilityICatalog = utils[0].component
    if not "all_comments_index" in instUtilityICatalog.keys():
        all_comments_index = TextIndex(interface=ISearchableText,
                                        field_name='getSearchableComments',
                                        field_callable=True)
        instUtilityICatalog['all_comments_index'] = all_comments_index
        # search for IAdmUtilSupervisor
        utils = [ util for util in sitem.registeredUtilities()
                  if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: ICatalog - create index for all comments")
    if not "all_notes_index" in instUtilityICatalog.keys():
        all_notes_index = TextIndex(interface=ISearchableText,
                                        field_name='getSearchableNotes',
                                        field_callable=True)
        instUtilityICatalog['all_notes_index'] = all_notes_index
        # search for IAdmUtilSupervisor
        utils = [ util for util in sitem.registeredUtilities()
                  if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: ICatalog - create index for all notes")


    transaction.get().commit()
    connection.close()
