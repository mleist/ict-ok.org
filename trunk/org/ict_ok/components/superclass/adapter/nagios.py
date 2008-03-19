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
"""Configuration adapter for nagios-config files
"""

__version__ = "$Id$"

# phython imports
import logging

# zope imports
from zope.interface import implements
from zope.component import adapts

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import ISuperclass
from org.ict_ok.admin_utils.generators.nagios.interfaces import \
     IGenNagios

logger = logging.getLogger("SuperclassGenNagios")


class GenNagios(object):
    """adapter implementation of Superclass -> nagios
    """
    
    implements(IGenNagios)
    adapts(ISuperclass)
    
    def __init__(self, context):
        #print "SuperclassGenNagios.__init__"
        self.fpCfg = None
        self.context = context
        self.ikRevision = __version__
        
    def fileOpen(self):
        """will open a filehandle to the specific object
        """
        self.fpCfg = open(u'/opt/nagios/etc/ict_ok/%s.cfg' % \
                          self.context.getObjectId(), 'w')
    
    def fileClose(self):
        """will close the filehandle to the specific object
        """
        if self.fpCfg is not None:
            self.fpCfg.close()

    def write(self, text_arg):
        """will write the text_arg into the configuration file
        """
        if self.fpCfg is not None:
            self.fpCfg.write(text_arg)

    def wantsCheck(self):
        """object is configured to be checked?
        """
        return False

    def traverse4nagiosGeneratorPre(self, level=0, comments=True):
        """graphviz configuration preamble
        """
        if comments:
            self.write(u"%s## Pre (%s,%d) - SuperclassGenNagios" % \
                       ("\t" * level, self.context.ikName, level))

    def traverse4nagiosGeneratorPost(self, level=0, comments=True):
        """graphviz configurations text after object
        """
        if comments:
            self.write(u"%s## Post (%s,%d) - SuperclassGenNagios" % \
                       ("\t" * level, self.context.ikName, level))

    def traverse4nagiosGeneratorBody(self, level=0, comments=True):
        """graphviz configuration data of/in object
        """
        if comments:
            self.write(u"%s## Body (%s,%d) - SuperclassGenNagios" % \
                       ("\t" * level, self.context.ikName, level))

    def traverse4nagiosGenerator(self, level=0, comments=True):
        """Configuration generator
        
        level: indent-level
        comments: should there comments are in the output?

        """
        self.traverse4nagiosGeneratorPre(level, comments)
        self.traverse4nagiosGeneratorBody(level, comments)
        self.traverse4nagiosGeneratorPost(level, comments)
        
    def nagiosConfigFileOut(self):
        """Nagios-Filegenerator for this object
        """
        pass

    def nagiosConfigFileRemove(self):
        """remove old nagios configuration file for this object
        """
        pass
