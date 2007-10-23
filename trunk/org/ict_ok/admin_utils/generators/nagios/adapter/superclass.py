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
"""Configuration adapter for nagios-config files
"""

__version__ = "$Id$"

# phython imports
import logging

# zope imports
from zope.interface import implements

# ict_ok.org imports
from org.ict_ok.admin_utils.generators.nagios.interfaces import \
     IGenNagios

logger = logging.getLogger("SuperclassGenNagios")


class SuperclassGenNagios(object):
    """adapter implementation of Superclass -> nagios
    """
    
    implements(IGenNagios)
    
    def __init__(self, context):
        print "SuperclassGenNagios.__init__"
        self.context = context
        self.ikRevision = __version__
    
    def traverse4nagiosGeneratorPre(self, fileDict, level=0, comments=True):
        """graphviz configuration preamble
        """
        if comments:
            print >> fileDict['HostCfg'], \
                  "%s## Pre (%s,%d) - SuperclassGenNagios" % \
                  ("\t" * level, self.context.ikName, level)

    def traverse4nagiosGeneratorPost(self, fileDict, level=0, comments=True):
        """graphviz configurations text after object
        """
        if comments:
            print >> fileDict['HostCfg'], \
                  "%s## Post (%s,%d) - SuperclassGenNagios" % \
                  ("\t" * level, self.context.ikName, level)

    def traverse4nagiosGeneratorBody(self, fileDict, level=0, comments=True):
        """graphviz configuration data of/in object
        """
        if comments:
            print >> fileDict['HostCfg'], \
                  "%s## Body (%s,%d) - SuperclassGenNagios" % \
                  ("\t" * level, self.context.ikName, level)

    def traverse4nagiosGenerator(self, fileDict, level=0, comments=True):
        """Configuration generator
        
        cfgFile: handle to open file
        level: indent-level
        comments: should there comments are in the output?

        """
        self.traverse4nagiosGeneratorPre(fileDict, level, comments)
        self.traverse4nagiosGeneratorBody(fileDict, level, comments)
        self.traverse4nagiosGeneratorPost(fileDict, level, comments)
