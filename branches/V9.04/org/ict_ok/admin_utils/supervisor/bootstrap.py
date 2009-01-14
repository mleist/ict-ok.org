# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232
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
from zope.app.intid import IntIds
from zope.app.intid.interfaces import IIntIds
from zope.app.catalog.catalog import Catalog
from zope.app.catalog.text import TextIndex
from zope.app.catalog.interfaces import ICatalog
from zope.index.text.interfaces import ISearchableText

from lovely.relation.app import O2OStringTypeRelationships
from lovely.relation.interfaces import IO2OStringTypeRelationships
from lovely.relation.event import o2oIntIdRemoved

# ict_ok.org imports
from org.ict_ok.version import getIkVersion
from org.ict_ok.admin_utils.supervisor.interfaces import IAdmUtilSupervisor
from org.ict_ok.admin_utils.supervisor.supervisor import AdmUtilSupervisor

logger = logging.getLogger("AdmUtilSupervisor")

def bootStrapSubscriberDatabase(event):
    """initialisation of ict_ok supervisor on first database startup
    """
    if appsetup.getConfigContext().hasFeature('devmode'):
        logger.info(u"starting bootStrapSubscriberDatabase (org.ict_ok...)")
    dummy_db, connection, dummy_root, root_folder = \
            getInformationFromEvent(event)
    madeAdmUtilSupervisor = ensureUtility(root_folder, 
                                          IAdmUtilSupervisor,
                                          'AdmUtilSupervisor', 
                                          AdmUtilSupervisor, '',
                                          copy_to_zlog=False, 
                                          asObject=True)

    if isinstance(madeAdmUtilSupervisor, AdmUtilSupervisor):
        logger.info(u"bootstrap: Ensure named AdmUtilSupervisor")
    
        instAdmUtilSupervisor = madeAdmUtilSupervisor
        # attribute is defined readonly, so first toggle this
        IAdmUtilSupervisor['nbrStarts'].readonly = False
        instAdmUtilSupervisor.nbrStarts += 1
        IAdmUtilSupervisor['nbrStarts'].readonly = True
        instAdmUtilSupervisor.appendEventHistory(u"'web service' started (Vers. %s)" \
                                                 % getIkVersion())
        dcore = IWriteZopeDublinCore(madeAdmUtilSupervisor)
        dcore.title = u"ICT_Ok Supervisor"
        dcore.created = datetime.utcnow()
        madeAdmUtilSupervisor.ikName = dcore.title
        madeAdmUtilSupervisor.__post_init__()
    else:
        # search in global component registry
        sitem = root_folder.getSiteManager()
        utils = [ util for util in sitem.registeredUtilities()
                  if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        # attribute is defined readonly, so first toggle this
        IAdmUtilSupervisor['nbrStarts'].readonly = False
        instAdmUtilSupervisor.nbrStarts += 1
        IAdmUtilSupervisor['nbrStarts'].readonly = True
        instAdmUtilSupervisor.appendEventHistory(\
            u"'web service' started (Vers. %s) (%d bytes) (%d objects)" \
            % (getIkVersion(), dummy_db.getSize(), dummy_db.objectCount()))
        dcore = IWriteZopeDublinCore(instAdmUtilSupervisor)
        dcore.title = u"ICT_Ok Supervisor"
        dcore.modified = datetime.utcnow()
        
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
        dcore.title = u"ICT_Ok Object Id Manager"
        dcore.created = datetime.utcnow()
        sitem = root_folder.getSiteManager()
        utils = [ util for util in sitem.registeredUtilities()
                    if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: made IIntIds-Utility")
        
    madeUtilityO2ORels = ensureUtility(root_folder, 
                                       IO2OStringTypeRelationships, 
                                       '', 
                                       O2OStringTypeRelationships, 
                                       '', 
                                       copy_to_zlog=False, 
                                       asObject=True)

    if isinstance(madeUtilityO2ORels, O2OStringTypeRelationships):
        logger.info(u"bootstrap: made O2ORels-Utility")
        #dcore = IWriteZopeDublinCore(madeUtilityO2ORels)
        #dcore.title = u"ICT_Ok Object Relation Manager"
        #dcore.created = datetime.utcnow()
        sitem = root_folder.getSiteManager()
        utils = [ util for util in sitem.registeredUtilities()
                    if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: made O2ORels-Utility")

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
        dcore.title = u"ICT_Ok Search Manager"
        dcore.created = datetime.utcnow()
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
    if not "all_fulltext_index" in instUtilityICatalog.keys():
        all_fulltext_index = TextIndex(interface=ISearchableText,
                                        field_name='getSearchableFullText',
                                        field_callable=True)
        instUtilityICatalog['all_fulltext_index'] = all_fulltext_index
        # search for IAdmUtilSupervisor
        utils = [ util for util in sitem.registeredUtilities()
                  if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: ICatalog - create index for all fulltext")

        
    transaction.get().commit()
    connection.close()
