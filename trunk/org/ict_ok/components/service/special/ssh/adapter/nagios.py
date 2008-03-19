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
"""Adapter implementation for generating nagios configuration
"""

__version__ = "$Id$"

# phython imports
import logging

# zope imports
from zope.app import zapi
from zope.interface import implements
from zope.component import adapts

# ict_ok.org imports
from org.ict_ok.components.service.special.ssh.interfaces import IServiceSsh
from org.ict_ok.admin_utils.generators.nagios.adapter.supernode import \
     GenNagios as ParentGenNagios
from org.ict_ok.admin_utils.generators.nagios.interfaces import \
     IGenNagios

logger = logging.getLogger("ServiceGenNagios")


class GenNagios(ParentGenNagios):
    """adapter implementation of SSH-Service -> nagios
    """

    implements(IGenNagios)
    adapts(IServiceSsh)
    
    def __init__(self, context):
        ParentGenNagios.__init__( self, context)

    def traverse4nagiosGeneratorPre(self, fileDict, level=0, comments=True):
        """graphviz configuration preamble
        """
        tmp_interface = zapi.getParent(self.context)
        tmp_host = zapi.getParent(tmp_interface)
        if comments:
            print >> fileDict['ServiceCfg'], \
                  "%s## Pre (%s,%d) - ServiceGenNagios" % \
                  ("\t" * level, self.context.ikName, level)
        fileDict['ServiceCfg'].write( "define service {\n")
        fileDict['ServiceCfg'].write( "    use generic-service\n")
        fileDict['ServiceCfg'].write( "    host_name %s\n" % tmp_host.objectID)
        fileDict['ServiceCfg'].write( "    service_description %s\n" % \
                                      (self.context.getDcTitle()))
        fileDict['ServiceCfg'].write( "    contact_groups    admins\n")
        fileDict['ServiceCfg'].write( "    check_period    24x7\n")
        fileDict['ServiceCfg'].write( "    notification_interval    0\n")
        fileDict['ServiceCfg'].write( "    notification_options    w,u,c,r\n")
        fileDict['ServiceCfg'].write( "    notification_period    24x7\n")
        fileDict['ServiceCfg'].write( \
            "    check_command    check_ssh_ict!5!%d\n" % self.context.port)
        fileDict['ServiceCfg'].write( "    max_check_attempts    3\n")
        fileDict['ServiceCfg'].write( "    normal_check_interval    5\n")
        fileDict['ServiceCfg'].write( "    retry_check_interval    1\n")
        fileDict['ServiceCfg'].write( "}\n\n")

    def traverse4nagiosGeneratorPost(self, fileDict, level=0, comments=True):
        """graphviz configurations text after object
        """
        if comments:
            print >> fileDict['ServiceCfg'], \
                  "%s## Post (%s,%d) - ServiceGenNagios" % \
                  ("\t" * level, self.context.ikName, level)
