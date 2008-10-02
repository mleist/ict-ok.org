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
"""Adapter implementation for generating graphviz-dot configuration
"""


__version__ = "$Id$"

# python imports
import logging

# zope imports
from zope.app import zapi
from zope.interface import implements
from zope.component import adapts

# ict_ok.org imports
from org.ict_ok.components.interface.interfaces import IInterface
from org.ict_ok.components.latency.interfaces import ILatency
from org.ict_ok.components.supernode.adapter.smokeping import \
     GenSmokePing as ParentGenSmokePing
from org.ict_ok.admin_utils.generators.smokeping.interfaces import \
     IGenSmokePing, IAdmUtilGeneratorSmokePing
from org.ict_ok.version import getIkVersion

logger = logging.getLogger("HostGenSmokePing")


class GenSmokePing(ParentGenSmokePing):
    """adapter implementation of Host -> smokeping
    """

    implements(IGenSmokePing)
    adapts(ILatency)
    
    # modification of this attributes will trigger an new generation of
    # the config file
    attrList = ['objectID', 'hostname', 'ikName', 'genNagios']
    
    def __init__(self, context):
        #print "HostGenSmokePing.__init__"
        ParentGenSmokePing.__init__(self, context)

    def fileOpen(self):
        """will open a filehandle to the specific object
        """
        #import pdb;pdb.set_trace()
        objId = self.context.getObjectId()
        utilSmokePing = zapi.getUtility(IAdmUtilGeneratorSmokePing, '')
        self.fileName = utilSmokePing.pathConfigData + u'/Hosts/%s.cfg' % objId
        ParentGenSmokePing.fileOpen(self)
        
    def wantsCheck(self):
        """object is configured to be checked?
        """
        return True
    
    def traverse4smokepingGeneratorPre(self, level=0, comments=True):
        """graphviz configuration preamble
        """
        valueChanged = False
        try:
            iface = zapi.getParent(self.context)
            host = zapi.getParent(iface)
            ipList = host.getIpList()
        except TypeError:
            return
        if comments:
            self.write(u"%s## Pre (%s,%d) - HostGenSmokePing" % \
                       ("\t" * level, self.context.ikName, level))
        if self.wantsCheck():
            valueChanged = True
            self.write(u"+++ %s\n" % (self.context.objectID))
            self.write(u"menu = %s\n" % (self.context.ikName))
            self.write(u"title = %s\n" % (self.context.ikName))
            if ipList is not None and \
               len(ipList) > 0:
                self.write(u"host = %s\n" % (ipList[0]))
        else:
            self.write(u"# disabled by user\n")
        return valueChanged

    def traverse4smokepingGeneratorBody(self, level=0, comments=True):
        """graphviz configuration data of/in object
        """
        valueChanged = False
        #if self.wantsCheck(from org.ict_ok.version import getIkVersion):
        if self.wantsCheck():
            if ParentGenSmokePing.traverse4smokepingGeneratorBody(self,
                                                         level,
                                                         comments):
                valueChanged = True
        return valueChanged

    def smokepingConfigFileOut(self, forceOutput=False, event=None):
        """SmokePing-Filegenerator
        
        will produce the smokeping configuration files
        
        forceOutput: False will check for a relevant attribute change
        True will alway generate a new config file
        
        event: None or the zope event from lifecycle
        """
        valueChanged = False
        ipv4 = None
        for if_name, if_obj in self.context.items():
            if IInterface.providedBy(if_obj) and \
               if_obj.ipv4List is not None and \
               len (if_obj.ipv4List) > 0:
                ipv4 = if_obj.ipv4List[0]
        if ipv4 is not None and len(ipv4) > 0:
            if ParentGenSmokePing.smokepingConfigFileOut(self,
                                                   forceOutput,
                                                   event):
                valueChanged = True
        return valueChanged


def _test():
    import doctest
    options = doctest.ELLIPSIS
    return doctest.testfile('../../../doctests/smokeping-host.txt', optionflags=options)

if __name__=="__main__":
    _test()
