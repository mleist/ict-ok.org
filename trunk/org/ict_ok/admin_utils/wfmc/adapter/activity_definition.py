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

# phython imports

# zope imports
from zope.interface import implements
from zope.component import adapts
from zope.wfmc.interfaces import IActivityDefinition

# ict_ok.org imports
from org.ict_ok.admin_utils.wfmc.interfaces import  IGenWFMCDot


class ActivityDefinitionGenDot(object):
    """Implementation of Graphviz picture adapter
    for WFMC ActivityDefinition
    """

    adapts(IActivityDefinition)
    implements(IGenWFMCDot)

    def __init__(self, context):
        self.context = context

    def traverse4DotGeneratorPre(self,
                                 cfgFile, 
                                 level=0, 
                                 comments=True):
        """generate pre-text in graphviz dot-file"""
        if comments:
            print >> cfgFile, "%s// Pre (%s,%d) - ActivityDefinitionGenDot" \
                  % ("\t" * level, self.context, level)

    def traverse4DotGeneratorBody(self, \
                                  cfgFile, \
                                  level=0, \
                                  comments=True):
        """Pre-Text in graphviz dot-file"""
        if comments:
            print >> cfgFile, "%s// Body (%s,%d) - ActivityDefinitionGenDot" \
                  % ("\t" * level, self.context, level)
        performer = self.context.performer
        participant = self.context.process.participants[performer]
        print >> cfgFile, '%ssubgraph "cluster_%s" {' % \
              ("\t" * level, performer)
        print >> cfgFile, '%scolor="#7DD0BC";' % \
              ("\t" * (level + 1))
        print >> cfgFile, '%sfontname="Arial";' % \
              ("\t" * (level + 1))
        print >> cfgFile, '%sfontsize="10.0";' % \
              ("\t" * (level + 1))
        print >> cfgFile, '%sfontcolor="#008263";' % \
              ("\t" * (level + 1))
        print >> cfgFile, '%slabel="%s";' % \
              ("\t" * (level + 1), participant.__name__)
        print >> cfgFile, '%s"%s" [' % ("\t" * (level + 1), self.context.id)
        print >> cfgFile, '%sshape="box",' % ("\t" * (level + 2))
        print >> cfgFile, '%sstyle="filled,setlinewidth(0)",' \
              % ("\t" * (level + 2))
        print >> cfgFile, '%sfillcolor = "#7DD0BC",' % ("\t" * (level + 2))
        print >> cfgFile, '%smargin = 0,' % ("\t" * (level + 2))
        print >> cfgFile, '%slabel=<<TABLE BORDER="0" CELLBORDER="0" ' \
              'CELLPADDING="1px" CELLSPACING="3px"><TR><TD VALIGN="TOP">' \
              '<IMG SRC="/home/markus/Projekte/ICT_Ok-hp/activitytool.gif"/>' \
              '</TD><TD ALIGN="LEFT" VALIGN="TOP" HEIGHT="30px" WIDTH="50px" BGCOLOR="#E5FFF9">'\
              '<FONT FACE="arial,helvetica,clean,sans-serif" POINT-SIZE="10px">' \
              '%s</FONT></TD></TR></TABLE>>' \
              % ("\t" * (level + 2), self.context.__name__)
        print >> cfgFile, '%s]; // %s' % ("\t" * (level + 1), self.context.__name__)
        print >> cfgFile, '%s}; // %s' % ("\t" * (level), self.context.__name__)
        #print >> cfgFile, '%s"%s" [' % ("\t" * level, self.context.objectID)
        #print >> cfgFile, '%sshape="box",' % ("\t" * (level + 1))
        #print >> cfgFile, '%sstyle="filled,setlinewidth(0)",' \
              #% ("\t" * (level + 1))
        #print >> cfgFile, '%sfillcolor = chartreuse2,' % ("\t" * (level + 1))
        #print >> cfgFile, '%smargin = 0,' % ("\t" * (level + 1))
        #print >> cfgFile, '%shref = "%s/@@details.html",' \
              #% ("\t" * (level + 1), zapi.getPath(self.context))
        #print >> cfgFile, '%slabel=<<TABLE BORDER="0" CELLBORDER="0" ' \
              #'CELLPADDING="0" CELLSPACING="0"><TR><TD>' \
              #'<IMG SRC="/home/markus/Projekte/ICT_Ok-hp/apple-red.png"/>' \
              #'</TD></TR><TR><TD><FONT FACE="Arial" POINT-SIZE="10">' \
              #'%s</FONT></TD></TR></TABLE>>' \
              #% ("\t" * (level + 1), self.context.__name__)
        #print >> cfgFile, '%s]; // %s' % ("\t" * level, self.context.__name__)

    def traverse4DotGeneratorPost(self, 
                                  cfgFile, 
                                  level=0, 
                                  comments=True):
        """generate post-text in graphviz dot-file"""
        if comments:
            print >> cfgFile, "%s// Post (%s,%d) - ActivityDefinitionGenDot" \
                  % ("\t" * level, self.context, level)

    def traverse4DotGenerator(self, cfgFile, level=0, comments=True):
        """generate text structure in graphviz dot-file"""
        self.traverse4DotGeneratorPre(cfgFile, level, comments)
        self.traverse4DotGeneratorBody(cfgFile, level, comments)
        self.traverse4DotGeneratorPost(cfgFile, level, comments)
