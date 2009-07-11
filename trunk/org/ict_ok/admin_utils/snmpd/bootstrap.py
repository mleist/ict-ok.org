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
import time
import pickle
import copy
from gzip import GzipFile

# zope imports
from zope.app.appsetup import appsetup
from zope.app.appsetup.bootstrap import getInformationFromEvent
from zope.app.appsetup.bootstrap import ensureUtility
from zope.dublincore.interfaces import IWriteZopeDublinCore

# ict_ok.org imports
from org.ict_ok.admin_utils.snmpd.snmpd import SnmpdThread
from org.ict_ok.admin_utils.supervisor.interfaces import \
     IAdmUtilSupervisor
from org.ict_ok.admin_utils.snmpd.interfaces import IAdmUtilSnmpd
from org.ict_ok.admin_utils.snmpd.snmpd import AdmUtilSnmpd
from org.ict_ok.admin_utils.snmpd.crawl_snmp_mrtg_data import BeautifulSoup, parse_vendors

logger = logging.getLogger("AdmUtilSnmpd")

def getNewMrtgData(madeAdmUtilSnmpd):
    try:
        dbgOut = u" bootstrap: there was an error on mrtg data"
        dataFile = GzipFile("lib/python/org/ict_ok/admin_utils/snmpd/snmp_mrtg_data.gz", "rb")
        if dataFile.readline() == "## mrtg data file for ict_ok.org\n":
            timeStamp = float(dataFile.readline())
            all_templ_data = pickle.load(dataFile)
            dataFile.close()
            madeAdmUtilSnmpd.mrtg_data = copy.deepcopy(all_templ_data)
            madeAdmUtilSnmpd.mrtg_data_timestamp = timeStamp
            dbgOut = u" bootstrap: new mrtg data (%s) loaded" % \
                   (time.strftime("%Y-%m-%d %H:%M:%S +00",time.gmtime(timeStamp)))
    except ValueError:
        dbgOut = u" bootstrap: Hmm, format of mrtg data file incorrect"
    except IOError:
        dbgOut = u" bootstrap: Hmm, no mrtg data file"
    return dbgOut

def updateMrtgData(madeAdmUtilSnmpd):
    try:
        dbgOut = u" bootstrap: there was an error on mrtg data"
        dataFile = GzipFile("lib/python/org/ict_ok/admin_utils/snmpd/snmp_mrtg_data.gz", "rb")
        if dataFile.readline() == "## mrtg data file for ict_ok.org\n":
            timeStamp = float(dataFile.readline())
            if timeStamp > madeAdmUtilSnmpd.mrtg_data_timestamp:
                all_templ_data = pickle.load(dataFile)
                dataFile.close()
                del madeAdmUtilSnmpd.mrtg_data
                madeAdmUtilSnmpd.mrtg_data = copy.deepcopy(all_templ_data)
                madeAdmUtilSnmpd.mrtg_data_timestamp = timeStamp
                dbgOut = u" bootstrap: update mrtg data (%s)" % \
                       (time.strftime("%Y-%m-%d %H:%M:%S +00",time.gmtime(timeStamp)))
            else:
                dbgOut = None
    except ValueError:
        dbgOut = u" bootstrap: Hmm, format of mrtg data file incorrect"
    except IOError:
        dbgOut = u" bootstrap: Hmm, no mrtg data file"
    return dbgOut

def createUtils(root_folder, connection=None, dummy_db=None):
    madeAdmUtilSnmpd = ensureUtility(root_folder, IAdmUtilSnmpd,
                                       'AdmUtilSnmpd', AdmUtilSnmpd,
                                       name='AdmUtilSnmpd',
                                       copy_to_zlog=False, asObject=True)

    if isinstance(madeAdmUtilSnmpd, AdmUtilSnmpd):
        logger.info(u"bootstrap: Ensure named AdmUtilSnmpd")
        dcore = IWriteZopeDublinCore(madeAdmUtilSnmpd)
        dcore.title = u"Snmpd Utility"
        dcore.created = datetime.utcnow()
        madeAdmUtilSnmpd.ikName = dcore.title
        madeAdmUtilSnmpd.__post_init__()
        sitem = root_folder.getSiteManager()
        utils = [ util for util in sitem.registeredUtilities()
                    if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: made IAdmUtilSnmpd-Utility")
        dbgOut = getNewMrtgData(madeAdmUtilSnmpd)
        if dbgOut:
            instAdmUtilSupervisor.appendEventHistory(dbgOut)
    else:
        # search in global component registry
        sitem = root_folder.getSiteManager()
        utils = [ util for util in sitem.registeredUtilities()
                  if util.provided.isOrExtends(IAdmUtilSnmpd)]
        instAdmUtilSnmpd = utils[0].component
        utils = [ util for util in sitem.registeredUtilities()
                  if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        dbgOut = updateMrtgData(instAdmUtilSnmpd)
        if dbgOut:
            instAdmUtilSupervisor.appendEventHistory(dbgOut)

    transaction.get().commit()
    if connection is not None:
        connection.close()

def bootStrapSubscriberDatabase(event):
    """initialisation of ict_ok supervisor on first database startup
    """
    if appsetup.getConfigContext().hasFeature('devmode'):
        logger.info(u"starting bootStrapSubscriberDatabase (org.ict_ok...)")
    SnmpdThread.database = event.database
    dummy_db, connection, dummy_root, root_folder = \
            getInformationFromEvent(event)
    createUtils(root_folder, connection, dummy_db)

