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

# python imports

# zope imports
from zope.interface import implements
from zope.component import adapts
from zope.wfmc.interfaces import ITransitionDefinition

# ict_ok.org imports
from org.ict_ok.admin_utils.wfmc.interfaces import  IGenWFMCDot
#from org.ict_ok.admin_utils.wfmc.interfaces import IIKGenWFMCDot


class TransitionDefinitionGenDot(object):
    """Implementation of Graphviz picture adapter
    for WFMC TransitionDefinition
    """

    adapts(ITransitionDefinition)
    implements(IGenWFMCDot)

    def __init__(self, context):
        self.context = context

    def traverse4DotGeneratorPre(self,
                                 cfgFile, 
                                 level=0, 
                                 comments=True):
        """generate pre-text in graphviz dot-file"""
        if comments:
            print >> cfgFile, "%s// Pre (%s,%d) - TransitionDefinitionGenDot" \
                  % ("\t" * level, self.context, level)
            
    def traverse4DotGeneratorBody(self, \
                                  cfgFile, \
                                  level=0, \
                                  comments=True):
        """Pre-Text in graphviz dot-file"""
        if comments:
            print >> cfgFile, "%s// Body (%s,%d) (id:%s) (cond:%s) - TransitionDefinitionGenDot" \
                  % ("\t" * level, self.context, level,
                     self.context.id, self.context.condition)
        print >> cfgFile, '%s"%s" -> "%s"' \
              % ("\t" * level, self.context.from_, self.context.to)

        #print >> cfgFile, '%s"%s" [' % ("\t" * level, self.context.objectID)
        #print >> cfgFile, '%sshape="box",' % ("\t" * (level + 1))
        #print >> cfgFile, '%sstyle="filled,setlinewidth(0)",' \
              #% ("\t" * (level + 1))
        #print >> cfgFile, '%sfillcolor = chartreuse2,' % ("\t" * (level + 1))
        #print >> cfgFile, '%smargin = 0,' % ("\t" * (level + 1))
        #print >> cfgFile, '%shref = "%s/@@details.html",' \
              #% ("\t" * (level + 1), zapi.absoluteURL(self.context, self.request))
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
            print >> cfgFile, "%s// Post (%s,%d) - TransitionDefinitionGenDot" \
                  % ("\t" * level, self.context, level)

    def traverse4DotGenerator(self, cfgFile, level=0, comments=True):
        """generate text structure in graphviz dot-file"""
        self.traverse4DotGeneratorPre(cfgFile, level, comments)
        self.traverse4DotGeneratorBody(cfgFile, level, comments)
        self.traverse4DotGeneratorPost(cfgFile, level, comments)
