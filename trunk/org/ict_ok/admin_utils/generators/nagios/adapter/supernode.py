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
from org.ict_ok.components.superclass.interfaces import ISuperclass
from org.ict_ok.admin_utils.generators.nagios.adapter.superclass import \
     SuperclassGenNagios
from org.ict_ok.admin_utils.generators.nagios.interfaces import \
     IGenNagios

logger = logging.getLogger("SupernodeGenNagios")


class SupernodeGenNagios(SuperclassGenNagios):
    """adapter implementation of Supernode -> nagios
    """

    implements(IGenNagios)
    
    def __init__(self, context):
        print "SupernodeGenNagios.__init__"
        SuperclassGenNagios.__init__(self, context)
    
    def traverse4nagiosGeneratorBody(self, fileDict, level=0, comments=True):
        """graphviz configuration data of/in object
        """
        if comments:
            print >> fileDict['HostCfg'], \
                  "%s## Body (%s,%d) - SupernodeGenNagios" % \
                  ("\t" * level, self.context.ikName, level)
        its = self.context.items()
        for (dummy_name, oobj) in its:
            if ISuperclass.providedBy(oobj):
                try:
                    adapterGenNagios = IGenNagios(oobj)
                    if adapterGenNagios:
                        adapterGenNagios.traverse4nagiosGenerator(fileDict,
                                                                  level + 1,
                                                                  comments)
                except TypeError:
                    logger.error(u"Problem in adaption of nagios config")

