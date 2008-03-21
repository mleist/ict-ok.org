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
from org.ict_ok.components.service.adapter.nagios import \
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

    def traverse4nagiosGeneratorPre(self, level=0, comments=True):
        """graphviz configuration preamble
        """
        tmp_interface = zapi.getParent(self.context)
        tmp_host = zapi.getParent(tmp_interface)
        if comments:
            self.write("%s## Pre (%s,%d) - ServiceGenNagios" % \
                        ("\t" * level, self.context.ikName, level))
        self.write("define service {\n")
        self.write("    use generic-service\n")
        self.write("    host_name %s\n" % \
                   tmp_host.objectID)
        self.write("    service_description %s\n" % \
                   (self.context.getDcTitle()))
        self.write("    contact_groups    admins\n")
        self.write("    check_period    24x7\n")
        self.write("    notification_interval    0\n")
        self.write("    notification_options    w,u,c,r\n")
        self.write("    notification_period    24x7\n")
        self.write("    check_command    check_ssh_ict!5!%d\n" % \
                   self.context.port)
        self.write("    max_check_attempts    3\n")
        self.write("    normal_check_interval    5\n")
        self.write("    retry_check_interval    1\n")
        self.write("}\n\n")

    def traverse4nagiosGeneratorPost(self, level=0, comments=True):
        """graphviz configurations text after object
        """
        if comments:
            self.write("%s## Post (%s,%d) - ServiceGenNagios" % \
                       ("\t" * level, self.context.ikName, level))
