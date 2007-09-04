# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
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
from org.ict_ok.admin_utils.util_manager.interfaces import IUtilManager
from org.ict_ok.admin_utils.util_manager.util_manager import UtilManager

logger = logging.getLogger("UtilManager")

def bootStrapSubscriberDatabase(event):
    """initialisation of ict_ok supervisor on first database startup
    """
    if appsetup.getConfigContext().hasFeature('devmode'):
        logger.info(u"starting bootStrapSubscriberDatabase (org.ict_ok...)")
    dummy_db, connection, dummy_root, root_folder = \
            getInformationFromEvent(event)
    madeUtilManager = ensureUtility(root_folder, 
                                    IUtilManager,
                                    'UtilManager', 
                                    UtilManager, '',
                                    copy_to_zlog=False, 
                                    asObject=True)
    
    if isinstance(madeUtilManager, UtilManager):
        logger.info(u"bootstrap: Ensure named UtilManager")
        dcore = IWriteZopeDublinCore(madeUtilManager)
        dcore.title = u"ICT_Ok Utility Manager"
        dcore.creators = (u"bootstrap auto-adder",)
        dcore.created = datetime.utcnow()
        madeUtilManager.__post_init__()
        
    transaction.get().commit()
    connection.close()

