# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
"""Adapter implementation for generating graphviz-dot configuration
"""

__version__ = "$Id$"

# zope imports
from zope.interface import implements

# ict_ok.org imports
from org.ict_ok.admin_utils.graphviz.interfaces import IGenGraphvizDot
from org.ict_ok.admin_utils.graphviz.adapter.supernode import \
     SupernodeGenGraphvizDot


class DummyContainerGenGraphvizDot(SupernodeGenGraphvizDot):
    """Implementation of Graphviz picture adapter for DummyContainer
    """

    implements(IGenGraphvizDot)

    def traverse4DotGeneratorPre(self, 
                                         cfgFile, 
                                         level=0, 
                                         comments=True):
        """Pre-Text in graphviz dot-file"""
        if comments:
            print >> cfgFile, "%s// Pre (%s,%d) DummyContainerGenGraphvizDot" \
                  % ("\t" * level, self.context.__name__, level)
            print >> cfgFile, "%s// Parent = %s" \
                  % ("\t" * level, self.parent.__name__)
