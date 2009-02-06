# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232,W0142
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

# ict_ok.org imports
from org.ict_ok.admin_utils.supervisor.interfaces import \
    IAdmUtilSupervisor
from org.ict_ok.admin_utils.idchooser.interfaces import \
    IAdmUtilIdChooser, IIdChooser
from org.ict_ok.admin_utils.idchooser.idchooser_util import AdmUtilIdChooser
from org.ict_ok.admin_utils.idchooser.idchooser import IdChooser

logger = logging.getLogger("AdmUtilIdChooser")

def bootStrapSubscriberDatabase(event):
    """initialisation of ict_ok supervisor on first database startup
    """
    if appsetup.getConfigContext().hasFeature('devmode'):
        logger.info(u"starting bootStrapSubscriberDatabase (org.ict_ok...)")
    dummy_db, connection, dummy_root, root_folder = \
            getInformationFromEvent(event)

    madeAdmUtilIdChooser = ensureUtility(root_folder, IAdmUtilIdChooser,
                                       'AdmUtilIdChooser',
                                       AdmUtilIdChooser, '',
                                       copy_to_zlog=False, asObject=True)

    if isinstance(madeAdmUtilIdChooser, AdmUtilIdChooser):
        logger.info(u"bootstrap: Ensure named AdmUtilIdChooser")
        sitem = root_folder.getSiteManager()
        dcore = IWriteZopeDublinCore(madeAdmUtilIdChooser)
        dcore.title = u"IdChooser Utility"
        dcore.created = datetime.utcnow()
        madeAdmUtilIdChooser.ikName = dcore.title
        for attrIdChooser in [
            # (name, counterStart, step, format)
            {'ikName': u'inv', 'counter': 0, 'step': 1, 'format': u'ID %05d'},
            ]:
            newIdChooser = IdChooser(**attrIdChooser)
            dcore = IWriteZopeDublinCore(newIdChooser)
            dcore.created = datetime.utcnow()
            dcore.title = attrIdChooser['ikName']
            madeAdmUtilIdChooser[newIdChooser.ikName] = newIdChooser
            sitem.registerUtility(newIdChooser,IIdChooser,
                                  name=newIdChooser.ikName)
        madeAdmUtilIdChooser.__post_init__()
        utils = [ util for util in sitem.registeredUtilities()
                    if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: made IAdmUtilIdChooser-Utility")

    transaction.get().commit()
    connection.close()
