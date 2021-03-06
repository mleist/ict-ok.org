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
from pytz import timezone
import codecs

# zope imports
from zope.app import zapi
from zope.interface import implements, providedBy
from zope.schema.fieldproperty import FieldProperty
from zope.component import getUtility
from zope.component import adapter
from zope.app.container.interfaces import \
     IObjectAddedEvent, \
     IObjectModifiedEvent, \
     IObjectMovedEvent, \
     IObjectRemovedEvent

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import ISuperclass
from org.ict_ok.components.supernode.interfaces import ISupernode
from org.ict_ok.admin_utils.generators.smokeping.interfaces import \
     IAdmUtilGeneratorSmokePing, IGenSmokePing
from org.ict_ok.admin_utils.generators.generators import \
     AdmUtilGenerators
from org.ict_ok.components.latency.interfaces import ILatency
from org.ict_ok.components.ipnet.interfaces import IIpNet
from org.ict_ok.components.host.interfaces import IHost
from org.ict_ok.components.interface.interfaces import IInterface

from org.ict_ok.version import getIkVersion

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
    pathDataFiles = FieldProperty(\
        IAdmUtilGeneratorSmokePing['pathDataFiles'])
    lastDeamonReload = FieldProperty(\
        IAdmUtilGeneratorSmokePing['lastDeamonReload'])

    def __init__(self):
        self.isRunning = False
        self.lastConfigFileChange = None
        self.lastDeamonReload = None
        self.pathInitScript = u"/etc/init.d/smokeping"
        self.pathConfigData = u"/opt/smokeping/etc/ict_ok"
        self.pathDataFiles = u"/opt/smokeping/data"
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
            cmdString = 'echo "" |sudo -S ' + self.pathInitScript + \
                      ' reload > /dev/null 2>&1'
            retInt = os.system(cmdString)
            if retInt == 0:
                self.lastDeamonReload = datetime.datetime.utcnow()
            else:
                logger.warning(u"reloadDaemon Error No: %d [cmd:%s]",
                               retInt, cmdString)
        
    def allConfigFilesOut(self, forceOutput=False,
                          event=None, genOutput=True):
        """make configuration file
        return True if any value has changed
        """
        valueChanged = forceOutput
        # start config file header
        utcTZ = timezone('UTC')
        starttimeCfg = datetime.datetime.now(utcTZ)
        if genOutput:
            fpCfg = codecs.open(u'/opt/smokeping/etc/ict_ok/ict.cfg', 'w',
                                encoding='utf-8')
            fpCfg.write(u"# generated by ict-ok.org Ver. %s (%s)\n\n" %
                        (getIkVersion(), starttimeCfg))
            fpCfg.write(u"# ----------------------------------------\n")
            fpCfg.close()
        # start config file main parts
        its = zapi.getRoot(self).items()
        for (dummy_name, oobj) in its:
            if ISupernode.providedBy(oobj):
                try:
                    adapterGenSmokePing = IGenSmokePing(oobj)
                    if adapterGenSmokePing:
                        adapterGenSmokePing.genOutput = genOutput
                        if adapterGenSmokePing.smokepingConfigFileOut(\
                            forceOutput, event):
                            valueChanged = True
                except TypeError, errText:
                    logger.error(u"Problem in adaption of smokeping conf: %s" %\
                                 (errText))
        # start config file footer
        if genOutput:
            fpCfg = codecs.open(u'/opt/smokeping/etc/ict_ok/ict.cfg', 'a',
                                encoding='utf-8')
            fpCfg.write(u"\n\n# ----------------------------------------\n")
            utcTZ = timezone('UTC')
            fpCfg.write(u"# ok, generated in %s\n" %
                        (datetime.datetime.now(utcTZ) - starttimeCfg))
            fpCfg.close()
        if valueChanged:
            self.touchLastConfigFile()
        return valueChanged

    def tickerEvent(self):
        """check for changes
        """
        if self.lastDeamonReload is None:
            self.allConfigFilesOut(True)
            self.reloadDaemon()
        elif self.lastConfigFileChange >= self.lastDeamonReload:
            self.allConfigFilesOut(True)
            self.reloadDaemon()

def objEventSupported(instance):
    for tmpInterface in [
        IIpNet,
        IHost,
        IInterface,
        ILatency
        ]:
        if tmpInterface in providedBy(instance):
            return True
    return False

@adapter(ISuperclass, IObjectAddedEvent)
def notifyAddedEvent(instance, event):
    """
    Node was added
    """
    if objEventSupported(event.object):
        #print "generators.smokeping.notifyAddedEvent [%s]" % event.object.ikName
        utilSmokePing = getUtility(IAdmUtilGeneratorSmokePing,
                                   name='AdmUtilGeneratorSmokePing')
        utilSmokePing.allConfigFilesOut(True, event, False)

@adapter(ISuperclass, IObjectModifiedEvent)
def notifyModifiedEvent(instance, event):
    """
    Node was modified
    """
    if objEventSupported(event.object) and \
       len(event.descriptions) > 0:
        #print "generators.smokeping.notifyModifiedEvent [%s]" % event.object.ikName
        smokePingAdapter = IGenSmokePing(event.object)
        if smokePingAdapter is not None:
            if smokePingAdapter.eventModifiesCfgFile(event):
                utilSmokePing = getUtility(IAdmUtilGeneratorSmokePing,
                                           name='AdmUtilGeneratorSmokePing')
                utilSmokePing.allConfigFilesOut(False, event, False)

@adapter(ISuperclass, IObjectMovedEvent)
def notifyMovedEvent(instance, event):
    """
    Node was moved
    """
    #print "generators.smokeping.notifyMovedEvent"

@adapter(ISuperclass, IObjectRemovedEvent)
def notifyRemovedEvent(instance, event):
    """
    Node was removed
    """
    if objEventSupported(event.object):
        #print "generators.smokeping.notifyRemovedEvent [%s]" % event.object.ikName
        utilSmokePing = getUtility(IAdmUtilGeneratorSmokePing)
        utilSmokePing.allConfigFilesOut(True, event, False)
        if ILatency.providedBy(event.object):
            filename = event.object.getRrdFilename()
            try:
                os.remove(filename)
            except:
                pass
            #except OSError, errtext:
                #raise Exception, "No such configfile: '%s'" % filename
