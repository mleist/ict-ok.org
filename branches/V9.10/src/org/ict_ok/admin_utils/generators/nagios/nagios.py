# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0613
#
"""Configuration adapter for nagios-config files
"""

__version__ = "$Id$"

# python imports
import os
import logging
import datetime

# zope imports
from zope.app import zapi
from zope.interface import implements, providedBy
from zope.schema.fieldproperty import FieldProperty
from zope.component import getUtility
from zope.component import adapter
from zope.app.container.interfaces import \
     IObjectAddedEvent, \
     IObjectMovedEvent, \
     IObjectRemovedEvent
from zope.lifecycleevent.interfaces import \
     IObjectModifiedEvent

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import ISuperclass
from org.ict_ok.components.supernode.interfaces import ISupernode
from org.ict_ok.admin_utils.generators.nagios.interfaces import \
     IAdmUtilGeneratorNagios, IGenNagios
from org.ict_ok.admin_utils.generators.generators import \
     AdmUtilGenerators
from org.ict_ok.admin_utils.eventcrossbar.interfaces import \
     IAdmUtilEventCrossbar
from org.ict_ok.components.ipnet.interfaces import IIpNet
from org.ict_ok.components.host.interfaces import IHost
from org.ict_ok.components.interface.interfaces import IInterface
from org.ict_ok.components.service.interfaces import IService

logger = logging.getLogger("AdmUtilGeneratorNagios")


class AdmUtilGeneratorNagios(AdmUtilGenerators):
    """Implementation of nagios configuration generator
    """
    implements(IAdmUtilGeneratorNagios)
    
    isRunning = FieldProperty(\
        IAdmUtilGeneratorNagios['isRunning'])
    lastConfigFileChange = FieldProperty(\
        IAdmUtilGeneratorNagios['lastConfigFileChange'])
    pathInitScript = FieldProperty(\
        IAdmUtilGeneratorNagios['pathInitScript'])
    pathConfigData = FieldProperty(\
        IAdmUtilGeneratorNagios['pathConfigData'])
    lastDeamonReload = FieldProperty(\
        IAdmUtilGeneratorNagios['lastDeamonReload'])

    def __init__(self):
        self.isRunning = False
        self.lastConfigFileChange = None
        self.lastDeamonReload = None
        self.pathInitScript = u"/etc/init.d/nagios"
        self.pathConfigData = u"/opt/nagios/etc/ict_ok"
        AdmUtilGenerators.__init__(self)
        self.ikRevision = __version__

    def touchLastConfigFile(self):
        """change timestamp in the utility
        
        will trigger a reload of the nagios-daemon on cron
        """
        self.lastConfigFileChange = datetime.datetime.utcnow()
        
    def reloadDaemon(self):
        """ reload the nagios daemon
        """
        nagiosUtil = getUtility(IAdmUtilGeneratorNagios)
        if nagiosUtil is not None and \
           nagiosUtil.isRunning:
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
                    adapterGenNagios = IGenNagios(oobj)
                    if adapterGenNagios:
                        adapterGenNagios.nagiosConfigFileOut(True, None)
                except TypeError, errText:
                    logger.error(u"Problem in adaption of nagios config: %s" %\
                                 (errText))

    def tickerEvent(self):
        """check for changes
        """
        if self.lastDeamonReload is None:
            self.reloadDaemon()
        elif self.lastConfigFileChange >= self.lastDeamonReload:
            self.reloadDaemon()
            
def objEventSupported(instance):
    for tmpInterface in [
        IIpNet,
        IHost,
        IInterface,
        IService
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
        valueChanged = False
        #print "generators.nagios.notifyAddedEvent"
        nagiosAdapter = IGenNagios(event.object)
        if nagiosAdapter is not None:
            if nagiosAdapter.nagiosConfigFileOut(True, event):
                valueChanged = True
        #print "valueChanged: ", valueChanged

@adapter(ISuperclass, IObjectModifiedEvent)
def notifyModifiedEvent(instance, event):
    """
    Node was modified
    """
    if objEventSupported(event.object):
        valueChanged = False
        #print "generators.nagios.notifyModifiedEvent"
        allEventObjs = event.object.getAllOutEventObjs()
        utilXbar = getUtility(IAdmUtilEventCrossbar,
                              name='AdmUtilEventCrossbar')
        for eventObj in allEventObjs:
            try:
                utilXbar[eventObj].addOidToInpObjects(event.object.objectID)
            except KeyError:
                pass
        nagiosAdapter = IGenNagios(event.object)
        if nagiosAdapter is not None:
            if nagiosAdapter.nagiosConfigFileOut(False, event):
                valueChanged = True
            if valueChanged:
                utilNagios = getUtility(IAdmUtilGeneratorNagios)
                reloadString = u"%s reload" % utilNagios.pathInitScript
                #print "reloadString: ", reloadString
                os.system(reloadString)
        #print "valueChanged: ", valueChanged

@adapter(ISuperclass, IObjectMovedEvent)
def notifyMovedEvent(instance, event):
    """
    Node was moved
    """
    #print "Superclass.notifyMovedEvent"

@adapter(ISuperclass, IObjectRemovedEvent)
def notifyRemovedEvent(instance, event):
    """
    Node was removed
    """
    if objEventSupported(event.object):
        valueChanged = False
        #print "generators.nagios.notifyRemovedEvent"
        nagiosAdapter = IGenNagios(event.object)
        if nagiosAdapter is not None:
            try:
                if nagiosAdapter.nagiosConfigFileRemove():
                    valueChanged = True
            except Exception: # no such file at this point and/or at this moment
                pass
        #print "valueChanged: ", valueChanged
