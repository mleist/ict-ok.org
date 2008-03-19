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

# phython imports
import logging
from datetime import datetime
from pytz import timezone

# zope imports
from zope.interface import implements
from zope.component import adapts

# ict_ok.org imports
from org.ict_ok.components.interface.interfaces import IInterface
from org.ict_ok.components.host.interfaces import IHost
from org.ict_ok.components.supernode.adapter.nagios import \
     GenNagios as ParentGenNagios
from org.ict_ok.admin_utils.generators.nagios.interfaces import \
     IGenNagios
from org.ict_ok.version import getIkVersion

logger = logging.getLogger("HostGenNagios")


class GenNagios(ParentGenNagios):
    """adapter implementation of Host -> nagios
    """

    implements(IGenNagios)
    adapts(IHost)
    
    def __init__(self, context):
        #print "HostGenNagios.__init__"
        ParentGenNagios.__init__(self, context)

    def wantsCheck(self):
        """object is configured to be checked?
        """
        return self.context.genNagios

    def traverse4nagiosGeneratorPre(self, level=0, comments=True):
        """graphviz configuration preamble
        """
        if comments:
            self.write(u"%s## Pre (%s,%d) - HostGenNagios" % \
                       ("\t" * level, self.context.ikName, level))
        if self.wantsCheck():
            self.write(u"define host {\n")
            self.write(u"    use generic-host\n")
            self.write(u"    host_name %s\n" % (self.context.objectID))
            self.write(u"    alias %s\n" % self.context.hostname)

    def traverse4nagiosGeneratorPost(self, level=0, comments=True):
        """graphviz configurations text after object
        """
        if comments:
            self.write(u"%s## Post (%s,%d) - HostGenNagios" % \
                       ("\t" * level, self.context.ikName, level))
        if self.wantsCheck():
            self.write(u"    check_command check-host-alive\n")
            self.write(u"    max_check_attempts 3\n")
            self.write(u"    contact_groups admins\n")
            self.write(u"    notification_interval 0\n")
            self.write(u"    notification_period 24x7\n")
            self.write(u"    notification_options d,u,r\n")
            self.write(u"}\n\n")

    def traverse4nagiosGeneratorBody(self, level=0, comments=True):
        """graphviz configuration data of/in object
        """
        #if self.wantsCheck(from org.ict_ok.version import getIkVersion):
        if self.wantsCheck():
            ParentGenNagios.traverse4nagiosGeneratorBody(self,
                                                         level, comments)

    
    def nagiosConfigFileOut(self):
        """Nagios-Filegenerator for this host object
        """
        print "HostGenNagios.nagiosConfigFileOut [%s]  -----------------------" % self.context.ikName
        berlinTZ = timezone('Europe/Berlin')
        dtHostCfg = datetime.now(berlinTZ)
        ihostn = self.context.getObjectId() # internal object id as filename
        #fpHostCfg = open(u'/opt/ikomtrol/etc/Host.cfg', 'w+')
        fpHostCfg = open(u'/opt/nagios/etc/ict_ok/'+ ihostn +'.cfg', 'w')
        fpHostCfg.write(u"# " + ihostn + ".cfg\n")
        fpHostCfg.write(u"# generated by ict-ok.org Ver. %s (%s)\n\n" %
                        (getIkVersion(), dtHostCfg))
        ipv4 = None
        for if_name, if_obj in self.context.items():
            if IInterface.providedBy(if_obj):
                ipv4 = if_obj.ipv4List
        if ipv4 is not None and len(ipv4):
            fileDict = {'HostCfg': fpHostCfg}
            self.traverse4nagiosGenerator(fileDict,
                                          level=1, 
                                          comments=False)
        fpHostCfg.write(u"\n\n# ok, generated in %s\n" %
                        (datetime.now(berlinTZ) - dtHostCfg))
        fpHostCfg.close()

    def nagiosConfigFileRemove(self):
        """remove old nagios configuration file for this object
        """
        print "HostGenNagios.nagiosConfigFileRemove [%s]  -----------------------" % self.context.ikName
        ihostn = self.context.getObjectId() # internal object id as filename
        import os
        try:
            os.remove(u'/opt/nagios/etc/ict_ok/'+ ihostn +'.cfg')
        except OSError, errtext:
            print "----------------------------------- %s" % errtext