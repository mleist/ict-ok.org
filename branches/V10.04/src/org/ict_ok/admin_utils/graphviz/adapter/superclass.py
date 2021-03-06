# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
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

    def traverse4DotGeneratorPre(self,
                                 cfgFile, 
                                 level=0, 
                                 comments=True,
                                 signalsOutput=False):
        """generate pre-text in graphviz dot-file"""
        if comments:
            print >> cfgFile, "%s// Pre (%s,%d) - SuperclassGenGraphvizDot" \
                  % ("\t" * level, self.context.__name__, level)
            if hasattr(self, "parent") and self.parent is not None:
                print >> cfgFile, "%s// Parent = %s" \
                      % ("\t" * level, self.parent.__name__)

    def traverse4DotGeneratorPost(self, 
                                  cfgFile, 
                                  level=0, 
                                  comments=True,
                                  signalsOutput=False):
        """generate post-text in graphviz dot-file"""
        if comments:
            print >> cfgFile, "%s// Post (%s,%d) - SuperclassGenGraphvizDot" \
                  % ("\t" * level, self.context.__name__, level)
        #if hasattr(self, "parent") and self.parent is not None:
            #try:
                #print >> cfgFile, '%s"%s" -- "%s"' \
                      #% ("\t" * level, self.parent.objectID, self.context.objectID)
            #except Exception, err:
                #print >> cfgFile, '%s"%s" -- "%s"' \
                      #% ("\t" * level, self.parent.__name__, self.context.objectID)
        #else:
            #print >> cfgFile, '%s -- "%s"' \
                  #% ("\t" * level, self.context.objectID)

    def traverse4DotGeneratorBody(self, 
                                  cfgFile, 
                                  level=0, 
                                  comments=True,
                                  signalsOutput=False,
                                  recursive=True):
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
              % ("\t" * (level + 1), zapi.absoluteURL(self.context, self.request))
        print >> cfgFile, '%slabel = <<TABLE BORDER = "0" CELLBORDER = "0" ' \
              'CELLPADDING = "0" CELLSPACING = "0"><TR><TD>' \
              '<IMG SRC = "/home/markus/Projekte/IKOMtrol-hp/apple-red.png"/>' \
              '</TD></TR><TR><TD><FONT FACE = "Arial" POINT-SIZE = "10">%s' \
              '</FONT></TD></TR></TABLE>>' \
              % ("\t" * (level + 1), self.context.ikName)
        print >> cfgFile, '%s]; // %s' % ("\t" * level, self.context.__name__)

    def traverse4DotGenerator(self, cfgFile, level=0,
                              comments=True, signalsOutput=False,
                              recursive=True):
        """generate text structure in graphviz dot-file"""
        self.traverse4DotGeneratorPre(cfgFile, level,
                                      comments, signalsOutput)
        self.traverse4DotGeneratorBody(cfgFile, level,
                                       comments, signalsOutput, recursive)
        self.traverse4DotGeneratorPost(cfgFile, level,
                                       comments, signalsOutput)
