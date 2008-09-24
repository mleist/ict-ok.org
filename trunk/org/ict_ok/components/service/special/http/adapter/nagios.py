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

# python imports
import logging

# zope imports
from zope.app import zapi
from zope.interface import implements
from zope.component import adapts

# ict_ok.org imports
from org.ict_ok.components.service.special.http.interfaces import IServiceHttp
from org.ict_ok.components.service.adapter.nagios import \
     GenNagios as ParentGenNagios
from org.ict_ok.admin_utils.generators.nagios.interfaces import \
     IGenNagios

logger = logging.getLogger("ServiceGenNagios")


class GenNagios(ParentGenNagios):
    """adapter implementation of HTTP-Service -> nagios
    """

    implements(IGenNagios)
    adapts(IServiceHttp)
    
    def __init__(self, context):
        ParentGenNagios.__init__( self, context)

    def traverse4nagiosGeneratorPre(self, level=0, comments=True):
        """graphviz configuration preamble
        """
        tmp_interface = zapi.getParent(self.context)
        tmp_host = zapi.getParent(tmp_interface)
        if comments:
            self.write(u"%s## Pre (%s,%d) - ServiceGenNagios" % \
                       ("\t" * level, self.context.ikName, level))
        self.write(u"define service {\n")
        self.write(u"    use generic-service\n")
        self.write(u"    host_name %s\n" % tmp_host.objectID)
        self.write(u"    service_description %s\n" % (self.context.objectID))
        self.write(u"    display_name %s\n" % (self.context.ikName))
        self.write(u"    contact_groups    admins\n")
        self.write(u"    check_period    24x7\n")
        self.write(u"    notification_interval    0\n")
        self.write(u"    notification_options    w,u,c,r\n")
        self.write(u"    notification_period    24x7\n")
        self.write(u"    check_command    check_http_ict!5!%d\n" % \
                    self.context.port)
        self.write(u"    max_check_attempts    3\n")
        self.write(u"    normal_check_interval    5\n")
        self.write(u"    retry_check_interval    1\n")
        self.write(u"}\n\n")

    def traverse4nagiosGeneratorPost(self, level=0, comments=True):
        """graphviz configurations text after object
        """
        if comments:
            self.write(u"%s## Post (%s,%d) - ServiceGenNagios" % \
                       ("\t" * level, self.context.ikName, level))
