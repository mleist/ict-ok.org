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
from zope.app import zapi
from zope.interface import implements

# ict_ok.org imports
from org.ict_ok.components.supernode.interfaces import ISupernode
from org.ict_ok.components.superclass.interfaces import ISuperclass
from org.ict_ok.admin_utils.generators.nagios.interfaces import \
     IAdmUtilGeneratorNagios, IIKGenNagios
from org.ict_ok.admin_utils.generators.generators import \
     AdmUtilGenerators

logger = logging.getLogger("AdmUtilGeneratorNagios")


class AdmUtilGeneratorNagios(AdmUtilGenerators):
    """Implementation of nagios configuration generator
    """

    implements(IAdmUtilGeneratorNagios)

    def __init__(self):
        AdmUtilGenerators.__init__(self)
        self.ikRevision = __version__

    def getConfig(self):
        """make configuration file
        TODO filename or filehandle must be an argument
        """
        cfgFile = open('/tmp/cfgNagiosFile', 'w')
        its = zapi.getRoot(self).items()
        for (dummy_name, oobj) in its:
            if ISupernode.providedBy(oobj):
                try:
                    adapterGenNagios = IIKGenNagios(oobj)
                    if adapterGenNagios:
                        adapterGenNagios.traverse4nagiosGenerator(cfgFile, 
                                                                  level=1, 
                                                                  comments=True)
                except TypeError:
                    logger.error(u"Problem in adaption of nagios config")
        cfgFile.flush()
        cfgFile.close()
        return "aaa"


class SuperclassGenNagios(object):
    """adapter implementation of Superclass -> nagios
    """
    
    implements(IIKGenNagios)
    
    def __init__(self, context):
        self.context = context
        self.ikRevision = __version__
    
    def traverse4nagiosGeneratorPre(self, cfgFile, level=0, comments=True):
        """graphviz configuration preamble
        """
        if comments:
            print >> cfgFile, "%s## Pre (%s,%d) - SuperclassGenNagios" % \
                  ("\t" * level, self.context.ikName, level)

    def traverse4nagiosGeneratorPost(self, cfgFile, level=0, comments=True):
        """graphviz configurations text after object
        """
        if comments:
            print >> cfgFile, "%s## Post (%s,%d) - SuperclassGenNagios" % \
                  ("\t" * level, self.context.ikName, level)

    def traverse4nagiosGeneratorBody(self, cfgFile, level=0, comments=True):
        """graphviz configuration data of/in object
        """
        if comments:
            print >> cfgFile, "%s## Body (%s,%d) - SuperclassGenNagios" % \
                  ("\t" * level, self.context.ikName, level)

    def traverse4nagiosGenerator(self, cfgFile, level=0, comments=True):
        """Configuration generator
        
        cfgFile: handle to open file
        level: indent-level
        comments: should there comments are in the output?

        """
        self.traverse4nagiosGeneratorPre(cfgFile, level, comments)
        self.traverse4nagiosGeneratorBody(cfgFile, level, comments)
        self.traverse4nagiosGeneratorPost(cfgFile, level, comments)


class SupernodeGenNagios(SuperclassGenNagios):
    """adapter implementation of Supernode -> nagios
    """

    implements(IIKGenNagios)
    
    def __init__(self, context):
        SuperclassGenNagios.__init__(self, context)
    
    def traverse4nagiosGeneratorBody(self, cfgFile, level=0, comments=True):
        """graphviz configuration data of/in object
        """
        if comments:
            print >> cfgFile, "%s## Body (%s,%d) - SupernodeGenNagios" % \
                  ("\t" * level, self.context.ikName, level)
        its = self.context.items()
        for (dummy_name, oobj) in its:
            if ISuperclass.providedBy(oobj):
                try:
                    adapterGenNagios = IIKGenNagios(oobj)
                    if adapterGenNagios:
                        adapterGenNagios.traverse4nagiosGenerator(cfgFile, 
                                                                  level + 1, 
                                                                  comments)
                except TypeError:
                    logger.error(u"Problem in adaption of nagios config")


class DummyContainerGenNagios(SupernodeGenNagios):
    """adapter implementation of DummyContainer -> nagios
    """

    implements(IIKGenNagios)
    
    def __init__(self, context):
        SupernodeGenNagios.__init__(self, context)
    
    def traverse4nagiosGeneratorPre(self, cfgFile, level=0, comments=True):
        """graphviz configuration preamble
        """
        if comments:
            print >> cfgFile, "%s## Pre (%s,%d) - DummyContainerGenNagios" % \
                  ("\t" * level, self.context.ikName, level)


class DummyGenNagios(SuperclassGenNagios):
    """adapter implementation of Dummy -> nagios
    """

    implements(IIKGenNagios)
    
    def __init__(self, context):
        SuperclassGenNagios.__init__(self, context)
    
    def traverse4nagiosGeneratorPre(self, cfgFile, level=0, comments=True):
        """graphviz configuration preamble
        """
        if comments:
            print >> cfgFile, "%s## Pre (%s,%d) - DummyGenNagios" % \
                  ("\t" * level, self.context.ikName, level)
