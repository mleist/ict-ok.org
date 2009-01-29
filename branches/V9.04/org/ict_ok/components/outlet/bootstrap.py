# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: bootstrap.py 273 2008-08-26 13:23:57Z markusleist $
#
# pylint: disable-msg=E1101
#
"""startup of Outlet"""

__version__ = "$Id: bootstrap.py 273 2008-08-26 13:23:57Z markusleist $"

# python imports
import logging
import transaction

# zope imports
from zope.app.appsetup import appsetup
from zope.app.appsetup.bootstrap import getInformationFromEvent
from zope.app.catalog.text import TextIndex
from zope.app.catalog.interfaces import ICatalog
from zope.index.text.interfaces import ISearchableText
from zope.dublincore.interfaces import IZopeDublinCore
from zope.component import createObject

# ict_ok.org imports
from org.ict_ok.admin_utils.supervisor.interfaces import IAdmUtilSupervisor

logger = logging.getLogger("Compon. Outlet")

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
    if not "outlet_oid_index" in instUtilityICatalog.keys():
        outlet_oid_index = TextIndex(interface=ISearchableText,
                                        field_name='getSearchableOutletOid',
                                        field_callable=True)
        instUtilityICatalog['outlet_oid_index'] = outlet_oid_index
        # search for IAdmUtilSupervisor
        utils = [ util for util in sitem.registeredUtilities()
                  if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: ICatalog - create index for entry type 'outlet'")
        
    folderName = u"Outlets"
    if folderName not in root_folder.keys():
        #newFolder = TestComponentFolder()
        newFolder = createObject(u'org.ict_ok.components.outlet.outlet.OutletFolder')
        root_folder[folderName] = newFolder
        dcore = IZopeDublinCore(newFolder, None)
        #dcore.creators = [u'ikportscan']
        #newFolder.ikComment += u"scanner: %s" % (dateNow)
        newFolder.__setattr__("ikName", folderName)
        dcore.title = folderName

    transaction.get().commit()
    connection.close()
