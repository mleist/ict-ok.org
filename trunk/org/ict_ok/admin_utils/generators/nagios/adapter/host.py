# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
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

# zope imports
from zope.interface import implements
from zope.component import adapts

# ict_ok.org imports
from org.ict_ok.components.host.interfaces import IHost
from org.ict_ok.admin_utils.generators.nagios.adapter.supernode import \
     SupernodeGenNagios
from org.ict_ok.admin_utils.generators.nagios.interfaces import \
     IGenNagios

logger = logging.getLogger("HostGenNagios")


class HostGenNagios(SupernodeGenNagios):
    """adapter implementation of Host -> nagios
    """

    implements(IGenNagios)
    adapts(IHost)
    
    def __init__(self, context):
        print "HostGenNagios.__init__"
        SupernodeGenNagios.__init__( self, context)

    def traverse4nagiosGeneratorPre(self, fileDict, level=0, comments=True):
        """graphviz configuration preamble
        """
        if comments:
            print >> fileDict['HostCfg'], \
                  "%s## Pre (%s,%d) - HostGenNagios" % \
                  ("\t" * level, self.context.ikName, level)
        fileDict['HostCfg'].write(u"define host {\n")
        fileDict['HostCfg'].write(u"    use generic-host\n")
        fileDict['HostCfg'].write(u"    host_name %s\n" % \
                                  (self.context.objectID))
        fileDict['HostCfg'].write(u"    alias %s\n" % self.context.hostname)
        #fileDict['HostCfg'].write("    address %s\n" % realObj.ip)
        fileDict['HostGroupCfg'].write(u"%s," % self.context.objectID)
        


    def traverse4nagiosGeneratorPost(self, fileDict, level=0, comments=True):
        """graphviz configurations text after object
        """
        if comments:
            print >> fileDict['HostCfg'], \
                  "%s## Post (%s,%d) - HostGenNagios" % \
                  ("\t" * level, self.context.ikName, level)
        fileDict['HostCfg'].write(u"    check_command check-host-alive\n")
        fileDict['HostCfg'].write(u"    max_check_attempts 3\n")
        fileDict['HostCfg'].write(u"    contact_groups admins\n")
        fileDict['HostCfg'].write(u"    notification_interval 0\n")
        fileDict['HostCfg'].write(u"    notification_period 24x7\n")
        fileDict['HostCfg'].write(u"    notification_options d,u,r\n")
        fileDict['HostCfg'].write(u"}\n\n")
