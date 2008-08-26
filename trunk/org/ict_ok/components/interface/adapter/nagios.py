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
from zope.interface import implements
from zope.component import adapts
from zope.app import zapi

# ict_ok.org imports
from org.ict_ok.components.interface.interfaces import IInterface
from org.ict_ok.components.supernode.adapter.nagios import \
     GenNagios as ParentGenNagios
from org.ict_ok.admin_utils.generators.nagios.interfaces import \
     IGenNagios

logger = logging.getLogger("InterfaceGenNagios")


class GenNagios(ParentGenNagios):
    """adapter implementation of Interface -> nagios
    """

    implements(IGenNagios)
    adapts(IInterface)
    
    def __init__(self, context):
        #print "InterfaceGenNagios.__init__"
        ParentGenNagios.__init__( self, context)

    # modification of this attributes will trigger an new generation of
    # the config file
    attrList = ['objectID', 'ipv4List']

    def fileOpen(self):
        """will open a filehandle to the specific object
        """
        if self.parentAdapter is not None:
            self.fpCfg = self.parentAdapter.fpCfg
    
    def fileClose(self):
        """will close the filehandle to the specific object
        """
        pass

    def traverse4nagiosGeneratorPre(self, level=0, comments=True):
        """graphviz configuration preamble
        """
        if comments:
            self.write(u"%s## Pre (%s,%d) - InterfaceGenNagios" % \
                       ("\t" * level, self.context.ikName, level))
        if len(self.context.ipv4List) > 0:
            #ipv4List should be a list
            #fileDict['HostCfg'].write("    address %s\n" % \
                                      #self.context.ipv4List[0])
            self.write("    address %s\n" % self.context.ipv4List)

    def traverse4nagiosGeneratorPost(self, level=0, comments=True):
        """graphviz configurations text after object
        """
        if comments:
            self.write(u"%s## Post (%s,%d) - InterfaceGenNagios" % \
                       ("\t" * level, self.context.ikName, level))

    def nagiosConfigFileOut(self, forceOutput=False, event=None):
        """Nagios-Filegenerator
        
        will produce the nagios configuration files
        
        forceOutput: False will check for a relevant attribute change
        True will alway generate a new config file
         
        event: None or the zope event from lifecycle
        """
        try:
            host = zapi.getParent(self.context)
        except TypeError:
            return
        nagiosAdapter = IGenNagios(host)
        if nagiosAdapter is not None:
            nagiosAdapter.nagiosConfigFileOut(True, event)

    def nagiosConfigFileRemove(self):
        """remove old nagios configuration file for this object
        """
        host = zapi.getParent(self.context)
        nagiosAdapter = IGenNagios(host)
        if nagiosAdapter is not None:
            nagiosAdapter.nagiosConfigFileOut(True, None)
