# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611
#
"""Configuration adapter for smokeping-config files
"""

__version__ = "$Id$"

# python imports
import os
import logging
import datetime

# zope imports
from zope.app import zapi
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.component import getUtility

# ict_ok.org imports
from org.ict_ok.components.supernode.interfaces import ISupernode
from org.ict_ok.admin_utils.generators.smokeping.interfaces import \
     IAdmUtilGeneratorSmokePing, IGenSmokePing
from org.ict_ok.admin_utils.generators.generators import \
     AdmUtilGenerators

logger = logging.getLogger("AdmUtilGeneratorSmokePing")


class AdmUtilGeneratorSmokePing(AdmUtilGenerators):
    """Implementation of smokeping configuration generator
    """
    implements(IAdmUtilGeneratorSmokePing)
    
    isRunning = FieldProperty(\
        IAdmUtilGeneratorSmokePing['isRunning'])
    lastConfigFileChange = FieldProperty(\
        IAdmUtilGeneratorSmokePing['lastConfigFileChange'])
    pathInitScript = FieldProperty(\
        IAdmUtilGeneratorSmokePing['pathInitScript'])
    pathConfigData = FieldProperty(\
        IAdmUtilGeneratorSmokePing['pathConfigData'])
    lastDeamonReload = FieldProperty(\
        IAdmUtilGeneratorSmokePing['lastDeamonReload'])

    def __init__(self):
        self.isRunning = False
        self.lastConfigFileChange = None
        self.lastDeamonReload = None
        self.pathInitScript = u"/etc/init.d/smokeping"
        self.pathConfigData = u"/opt/smokeping/etc/ict_ok"
        AdmUtilGenerators.__init__(self)
        self.ikRevision = __version__

    def touchLastConfigFile(self):
        """change timestamp in the utility
        
        will trigger a reload of the smokeping-daemon on cron
        """
        self.lastConfigFileChange = datetime.datetime.utcnow()
        
    def reloadDaemon(self):
        """ reload the smokeping daemon
        """
        smokepingUtil = getUtility(IAdmUtilGeneratorSmokePing)
        if smokepingUtil is not None and \
           smokepingUtil.isRunning:
            retInt = os.system('echo "" |sudo -S ' + self.pathInitScript + \
                               ' reload > /dev/null 2>&1')
            if retInt == 0:
                self.lastDeamonReload = datetime.datetime.utcnow()
            else:
                logger.warning(u"reloadDaemon Error No: %d", retInt)
        
    def allConfigFilesOut(self):
        """make configuration file
        """
        self.touchLastConfigFile()
        its = zapi.getRoot(self).items()
        for (dummy_name, oobj) in its:
            if ISupernode.providedBy(oobj):
                try:
                    adapterGenSmokePing = IGenSmokePing(oobj)
                    if adapterGenSmokePing:
                        adapterGenSmokePing.smokepingConfigFileOut(True, None)
                except TypeError, errText:
                    logger.error(u"Problem in adaption of smokeping config: %s" %\
                                 (errText))

    def tickerEvent(self):
        """check for changes
        """
        if self.lastDeamonReload is None:
            self.reloadDaemon()
        elif self.lastConfigFileChange >= self.lastDeamonReload:
            self.reloadDaemon()
