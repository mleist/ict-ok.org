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

# zope imports
from zope.interface import implements
from zope.component import adapts

# ict_ok.org imports
from org.ict_ok.components.interface.interfaces import IInterface
from org.ict_ok.admin_utils.generators.nagios.adapter.supernode import \
     SupernodeGenNagios
from org.ict_ok.admin_utils.generators.nagios.interfaces import \
     IGenNagios

logger = logging.getLogger("InterfaceGenNagios")


class InterfaceGenNagios(SupernodeGenNagios):
    """adapter implementation of Interface -> nagios
    """

    implements(IGenNagios)
    adapts(IInterface)
    
    def __init__(self, context):
        print "InterfaceGenNagios.__init__"
        SupernodeGenNagios.__init__( self, context)

    def traverse4nagiosGeneratorPre(self, fileDict, level=0, comments=True):
        """graphviz configuration preamble
        """
        if comments:
            print >> fileDict['HostCfg'], \
                  "%s## Pre (%s,%d) - InterfaceGenNagios" % \
                  ("\t" * level, self.context.ikName, level)
        if len(self.context.ipv4List) > 0:
            fileDict['HostCfg'].write("    address %s\n" % \
                                      self.context.ipv4List[0])


    def traverse4nagiosGeneratorPost(self, fileDict, level=0, comments=True):
        """graphviz configurations text after object
        """
        if comments:
            print >> fileDict['HostCfg'], \
                  "%s## Post (%s,%d) - InterfaceGenNagios" % \
                  ("\t" * level, self.context.ikName, level)
