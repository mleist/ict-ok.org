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
"""Configuration adapter for smokeping-config files
"""

__version__ = "$Id$"

# python imports
import logging

# zope imports
from zope.interface import implements
from zope.component import adapts

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import ISuperclass
from org.ict_ok.components.supernode.interfaces import ISupernode
from org.ict_ok.components.superclass.adapter.smokeping import \
     GenSmokePing as ParentGenSmokePing
from org.ict_ok.admin_utils.generators.smokeping.interfaces import \
     IGenSmokePing

logger = logging.getLogger("SupernodeGenSmokePing")


class GenSmokePing(ParentGenSmokePing):
    """adapter implementation of Supernode -> smokeping
    """

    implements(IGenSmokePing)
    adapts(ISupernode)
    
    def __init__(self, context):
        #print "SupernodeGenSmokePing.__init__"
        ParentGenSmokePing.__init__(self, context)
    
    def traverse4smokepingGeneratorBody(self, level=0, comments=True):
        """graphviz configuration data of/in object
        """
        if comments:
            self.write("%s## Body (%s,%d) - SupernodeGenSmokePing" % \
                       ("\t" * level, self.context.ikName, level))
        its = self.context.items()
        for (dummy_name, oobj) in its:
            if ISuperclass.providedBy(oobj):
                try:
                    adapterGenSmokePing = IGenSmokePing(oobj)
                    if adapterGenSmokePing:
                        adapterGenSmokePing.parentAdapter = self
                        adapterGenSmokePing.traverse4smokepingGenerator(level + 1,
                                                                  comments)
                except TypeError, errText:
                    logger.error(u"Problem in smokeping adaption: '%s'" % \
                                 errText)

