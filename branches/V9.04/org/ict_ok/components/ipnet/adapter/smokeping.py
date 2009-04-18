# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: smokeping.py 346M 2009-04-16 11:09:07Z (lokal) $
#
# pylint: disable-msg=E1101,E0611
#
"""Adapter implementation for generating graphviz-dot configuration
"""

__version__ = "$Id: smokeping.py 346M 2009-04-16 11:09:07Z (lokal) $"

# zope imports
from zope.interface import implements
from zope.component import adapts

# ict_ok.org imports
from org.ict_ok.components.ipnet.interfaces import IIpNet
from org.ict_ok.components.supernode.adapter.smokeping import \
     GenSmokePing as ParentGenSmokePing
from org.ict_ok.admin_utils.generators.smokeping.interfaces import \
     IGenSmokePing


class GenSmokePing(ParentGenSmokePing):
    """adapter implementation of Interface -> smokeping
    """

    implements(IGenSmokePing)
    adapts(IIpNet)
    
    # modification of this attributes will trigger an new generation of
    # the config file
    attrList = ['objectID', 'ikName']
    
    def traverse4smokepingGeneratorPre(self, level=0, comments=True):
        """graphviz configuration preamble
        """
        if comments:
            self.write(u"%s## Pre (%s,%d) - IpNetGenSmokePing" % \
                       ("\t" * level, self.context.ikName, level))
        self.write(u"+ %s\n" % (self.context.objectID))
        self.write(u"menu = %s\n" % (self.context.ikName))
        self.write(u"title = %s\n" % (self.context.ikName))
        return True # valueChanged

    def traverse4smokepingGeneratorBody(self, level=0, comments=True):
        """graphviz configuration data of/in object
        """
        ParentGenSmokePing.traverse4smokepingGeneratorBody(self,
                                                           level,
                                                           comments)
        return True # valueChanged
