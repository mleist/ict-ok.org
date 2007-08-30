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
"""Configuration adapter for honeyd-config files
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
from org.ict_ok.admin_utils.generators.honeyd.interfaces import \
     IAdmUtilGeneratorHoneyd, IIKGenHoneyd
from org.ict_ok.admin_utils.generators.generators import \
     AdmUtilGenerators

logger = logging.getLogger("AdmUtilGeneratorHoneyd")


class AdmUtilGeneratorHoneyd(AdmUtilGenerators):
    """Implementation of honeyd configuration generator
    """

    implements(IAdmUtilGeneratorHoneyd)

    def __init__(self):
        AdmUtilGenerators.__init__(self)
        self.ikRevision = __version__

    def getConfig(self):
        """make configuration file
        TODO filename or filehandle must be an argument
        """
        cfgFile = open('/tmp/cfgFile', 'w')
        its = zapi.getRoot(self).items()
        for (dummy_name, oobj) in its:
            if ISupernode.providedBy(oobj):
                try:
                    adapterGenHoneyd = IIKGenHoneyd(oobj)
                    if adapterGenHoneyd:
                        adapterGenHoneyd.traverse4honeydGenerator(cfgFile, 
                                                                  level=1, 
                                                                  comments=True)
                except TypeError:
                    logger.error(u"Problem in adaption of honeyd config")
        cfgFile.flush()
        cfgFile.close()
        return "aaa"


class SuperclassGenHoneyd(object):
    """adapter implementation of Superclass -> honeyd
    """
    
    implements(IIKGenHoneyd)
    
    def __init__(self, context):
        self.context = context
        self.ikRevision = __version__
    
    def traverse4honeydGeneratorPre(self, cfgFile, level=0, comments=True):
        """graphviz configuration preamble
        """
        if comments:
            print >> cfgFile, "%s## Pre (%s,%d) - SuperclassGenHoneyd" % \
                  ("\t" * level, self.context.__name__, level)

    def traverse4honeydGeneratorPost(self, cfgFile, level=0, comments=True):
        """graphviz configurations text after object
        """
        if comments:
            print >> cfgFile, "%s## Post (%s,%d) - SuperclassGenHoneyd" % \
                  ("\t" * level, self.context.__name__, level)

    def traverse4honeydGeneratorBody(self, cfgFile, level=0, comments=True):
        """graphviz configuration data of/in object
        """
        if comments:
            print >> cfgFile, "%s## Body (%s,%d) - SuperclassGenHoneyd" % \
                  ("\t" * level, self.context.__name__, level)

    def traverse4honeydGenerator(self, cfgFile, level=0, comments=True):
        """Configuration generator
        
        cfgFile: handle to open file
        level: indent-level
        comments: should there comments are in the output?

        """
        self.traverse4honeydGeneratorPre(cfgFile, level, comments)
        self.traverse4honeydGeneratorBody(cfgFile, level, comments)
        self.traverse4honeydGeneratorPost(cfgFile, level, comments)


class SupernodeGenHoneyd(SuperclassGenHoneyd):
    """adapter implementation of Supernode -> honeyd
    """

    implements(IIKGenHoneyd)
    
    def __init__(self, context):
        SuperclassGenHoneyd.__init__(self, context)
    
    def traverse4honeydGeneratorBody(self, cfgFile, level=0, comments=True):
        """graphviz configuration data of/in object
        """
        if comments:
            print >> cfgFile, "%s## Body (%s,%d) - SupernodeGenHoneyd" % \
                  ("\t" * level, self.context.__name__, level)
        its = self.context.items()
        for (dummy_name, oobj) in its:
            if ISuperclass.providedBy(oobj):
                try:
                    adapterGenHoneyd = IIKGenHoneyd(oobj)
                    if adapterGenHoneyd:
                        adapterGenHoneyd.traverse4honeydGenerator(cfgFile, 
                                                                  level + 1, 
                                                                  comments)
                except TypeError:
                    logger.error(u"Problem in adaption of honeyd config")


class DummyContainerGenHoneyd(SupernodeGenHoneyd):
    """adapter implementation of DummyContainer -> honeyd
    """

    implements(IIKGenHoneyd)
    
    def __init__(self, context):
        SupernodeGenHoneyd.__init__(self, context)
    
    def traverse4honeydGeneratorPre(self, cfgFile, level=0, comments=True):
        """graphviz configuration preamble
        """
        if comments:
            print >> cfgFile, "%s## Pre (%s,%d) - DummyContainerGenHoneyd" % \
                  ("\t" * level, self.context.__name__, level)


class DummyGenHoneyd(SuperclassGenHoneyd):
    """adapter implementation of Dummy -> honeyd
    """

    implements(IIKGenHoneyd)
    
    def __init__(self, context):
        SuperclassGenHoneyd.__init__(self, context)
    
    def traverse4honeydGeneratorPre(self, cfgFile, level=0, comments=True):
        """graphviz configuration preamble
        """
        if comments:
            print >> cfgFile, "%s## Pre (%s,%d) - DummyGenHoneyd" % \
                  ("\t" * level, self.context.__name__, level)
