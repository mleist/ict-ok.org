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
from org.ict_ok.components.supernode.interfaces import ISupernode
from org.ict_ok.components.superclass.adapter.nagios import \
     GenNagios as ParentGenNagios
from org.ict_ok.admin_utils.generators.nagios.interfaces import \
     IGenNagios

logger = logging.getLogger("SupernodeGenNagios")


class GenNagios(ParentGenNagios):
    """adapter implementation of Supernode -> nagios
    """

    implements(IGenNagios)
    adapts(ISupernode)
    
    def __init__(self, context):
        #print "SupernodeGenNagios.__init__"
        ParentGenNagios.__init__(self, context)
    
    def traverse4nagiosGeneratorBody(self, level=0, comments=True):
        """graphviz configuration data of/in object
        """
        if comments:
            self.write("%s## Body (%s,%d) - SupernodeGenNagios" % \
                       ("\t" * level, self.context.ikName, level))
        its = self.context.items()
        for (dummy_name, oobj) in its:
            if ISuperclass.providedBy(oobj):
                try:
                    adapterGenNagios = IGenNagios(oobj)
                    if adapterGenNagios:
                        adapterGenNagios.parentAdapter = self
                        adapterGenNagios.traverse4nagiosGenerator(level + 1,
                                                                  comments)
                except TypeError, errText:
                    logger.error(u"Problem in nagios adaption: '%s'" % \
                                 errText)

