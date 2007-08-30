# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0611
#
"""Adapter implementation for generating graphviz-dot configuration
"""

__version__ = "$Id$"

# zope imports
from zope.app import zapi
from zope.interface import implements

# ict_ok.org imports
from org.ict_ok.admin_utils.graphviz.interfaces import IGenGraphvizDot


class SuperclassGenGraphvizDot(object):
    """Implementation of Graphviz picture adapter for Superclass
    """

    implements(IGenGraphvizDot)

    def __init__(self, context):
        self.context = context
        self.parent = None

    def setParent(self, parent):
        """parent object is necessary for root node of graphviz-graph
        """
        self.parent = parent

    def traverse4GraphvizDotGeneratorPre(self,
                                         cfgFile, 
                                         level=0, 
                                         comments=True):
        """generate pre-text in graphviz dot-file"""
        if comments:
            print >> cfgFile, "%s// Pre (%s,%d) - SuperclassGenGraphvizDot" \
                  % ("\t" * level, self.context.__name__, level)
            print >> cfgFile, "%s// Parent = %s" \
                  % ("\t" * level, self.parent.__name__)

    def traverse4GraphvizDotGeneratorPost(self, 
                                          cfgFile, 
                                          level=0, 
                                          comments=True):
        """generate post-text in graphviz dot-file"""
        if comments:
            print >> cfgFile, "%s// Post (%s,%d) - SuperclassGenGraphvizDot" \
                  % ("\t" * level, self.context.__name__, level)
        try:
            print >> cfgFile, '%s"%s" -- "%s"' \
                  % ("\t" * level, self.parent.objectID, self.context.objectID)
        except Exception, err:
            print >> cfgFile, '%s"%s" -- "%s"' \
                  % ("\t" * level, self.parent.__name__, self.context.objectID)

    def traverse4GraphvizDotGeneratorBody(self, 
                                          cfgFile, 
                                          level=0, 
                                          comments=True):
        """generate body-text in graphviz dot-file"""
        if comments:
            print >> cfgFile, "%s// Body (%s,%d) - " \
                  "SuperclassGenGraphvizDot" \
                  % ("\t" * level, self.context.__name__, level)
        print >> cfgFile, '%s"%s" [' % ("\t" * level, self.context.objectID)
        print >> cfgFile, '%sshape = "box",' % ("\t" * (level + 1))
        print >> cfgFile, '%sstyle = "filled,setlinewidth(0)",' \
              % ("\t" * (level + 1))
        print >> cfgFile, '%sfillcolor = chartreuse2,' % ("\t" * (level + 1))
        print >> cfgFile, '%smargin = 0,' % ("\t" * (level + 1))
        print >> cfgFile, '%shref = "%s/@@details.html",' \
              % ("\t" * (level + 1), zapi.getPath(self.context))
        print >> cfgFile, '%slabel = <<TABLE BORDER = "0" CELLBORDER = "0" ' \
              'CELLPADDING = "0" CELLSPACING = "0"><TR><TD>' \
              '<IMG SRC = "/home/markus/Projekte/ICT_Ok-hp/apple-red.png"/>' \
              '</TD></TR><TR><TD><FONT FACE = "Arial" POINT-SIZE = "10">%s' \
              '</FONT></TD></TR></TABLE>>' \
              % ("\t" * (level + 1), self.context.__name__)
        print >> cfgFile, '%s]; // %s' % ("\t" * level, self.context.__name__)

    def traverse4GraphvizDotGenerator(self, cfgFile, level=0, comments=True):
        """generate text structure in graphviz dot-file"""
        self.traverse4GraphvizDotGeneratorPre(cfgFile, level, comments)
        self.traverse4GraphvizDotGeneratorBody(cfgFile, level, comments)
        self.traverse4GraphvizDotGeneratorPost(cfgFile, level, comments)
