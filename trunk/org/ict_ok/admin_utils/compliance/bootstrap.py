# -*- coding: utf-8 -*-
#
# Copyright (c) 2007, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101
#
"""compliance utility

the compliance utility should store the compliance/requirement-templates
for the host- or service-instances
"""

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
from zope.app.component.interfaces import ISite
from zope.app.container.interfaces import IContainer

# ict_ok.org imports
from org.ict_ok.admin_utils.supervisor.interfaces import \
     IAdmUtilSupervisor
from org.ict_ok.admin_utils.compliance.interfaces import \
     IAdmUtilCompliance
from org.ict_ok.admin_utils.compliance.compliance import \
     AdmUtilCompliance

logger = logging.getLogger("AdmUtilCompliance")

def bootStrapSubscriberDatabase(event):
    """initialisation of eventcrossbar utility on first database startup
    """
    if appsetup.getConfigContext().hasFeature('devmode'):
        logger.info(u"starting bootStrapSubscriberDatabase (org.ict_ok...)")
    dummy_db, connection, dummy_root, root_folder = \
            getInformationFromEvent(event)

    madeAdmUtilCompliance = ensureUtility(root_folder, IAdmUtilCompliance,
                                       'AdmUtilCompliance', AdmUtilCompliance, '',
                                       copy_to_zlog=False, asObject=True)

    if isinstance(madeAdmUtilCompliance, AdmUtilCompliance):
        logger.info(u"bootstrap: Ensure named AdmUtilCompliance")
        dcore = IWriteZopeDublinCore(madeAdmUtilCompliance)
        dcore.title = u"Compliance Utiltiy"
        dcore.created = datetime.utcnow()
        madeAdmUtilCompliance.ikName = dcore.title
        madeAdmUtilCompliance.__post_init__()
        sitem = root_folder.getSiteManager()
        utils = [util for util in sitem.registeredUtilities()
                 if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: made Compliance Utiltiy")

    transaction.get().commit()
    connection.close()
