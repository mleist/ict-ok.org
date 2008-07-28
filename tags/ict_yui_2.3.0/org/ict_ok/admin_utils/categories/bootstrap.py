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


# phython imports
import logging
import transaction
from datetime import datetime

# zope imports
from zope.app.appsetup import appsetup
from zope.app.appsetup.bootstrap import getInformationFromEvent
from zope.app.appsetup.bootstrap import ensureUtility
from zope.dublincore.interfaces import IWriteZopeDublinCore

# ict_ok.org imports
from org.ict_ok.admin_utils.supervisor.interfaces import \
     IAdmUtilSupervisor
from org.ict_ok.admin_utils.categories.interfaces import IAdmUtilCategories
from org.ict_ok.admin_utils.categories.categories import AdmUtilCategories
from org.ict_ok.admin_utils.categories.cat_hostgroup import \
     AdmUtilCatHostGroup

logger = logging.getLogger("AdmUtilCategories")

def bootStrapSubscriberDatabase(event):
    """initialisation of ict_ok supervisor on first database startup
    """
    if appsetup.getConfigContext().hasFeature('devmode'):
        logger.info(u"starting bootStrapSubscriberDatabase (org.ict_ok...)")
    dummy_db, connection, dummy_root, root_folder = \
            getInformationFromEvent(event)

    madeAdmUtilCategories = ensureUtility(root_folder, IAdmUtilCategories,
                                       'AdmUtilCategories',
                                       AdmUtilCategories, '',
                                       copy_to_zlog=False, asObject=True)

    if isinstance(madeAdmUtilCategories, AdmUtilCategories):
        logger.info(u"bootstrap: Ensure named AdmUtilCategories")
        dcore = IWriteZopeDublinCore(madeAdmUtilCategories)
        dcore.title = u"Categories Utility"
        dcore.created = datetime.utcnow()
        madeAdmUtilCategories.ikName = dcore.title
        for strHostGroup in [
            u'DNS-Server',
            u'File-Server',
            u'Miscellaneous-Server',
            u'SMTP-Server',
            u'Terminal-Server',
            u'Utility-Server',
            u'Workstation',
            ]:
            newHostGroup = AdmUtilCatHostGroup()
            newHostGroup.__setattr__("ikName", strHostGroup)
            dcore = IWriteZopeDublinCore(newHostGroup)
            dcore.created = datetime.utcnow()
            dcore.title = strHostGroup
            madeAdmUtilCategories[newHostGroup.objectID] = newHostGroup
        madeAdmUtilCategories.__post_init__()
        sitem = root_folder.getSiteManager()
        utils = [ util for util in sitem.registeredUtilities()
                    if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: made IAdmUtilCategories-Utility")

    transaction.get().commit()
    connection.close()
