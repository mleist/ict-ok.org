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

# phython imports

# zope imports
from zope.interface import implements
from zope.component import adapts

# ict_ok.org imports
from org.ict_ok.admin_utils.graphviz.interfaces import \
     IGenGraphvizDot
from org.ict_ok.admin_utils.eventcrossbar.interfaces import IAdmUtilEvent


class AdmUtilEventGenDot(object):
    """Implementation of Graphviz picture adapter
    for an event
    """

    adapts(IAdmUtilEvent)
    implements(IGenGraphvizDot)

    def __init__(self, context):
        self.context = context

    def traverse4DotGeneratorPre(self,
                                 cfgFile, 
                                 level=0, 
                                 comments=True):
        """generate pre-text in graphviz dot-file"""
        if comments:
            print >> cfgFile, "%s// Pre (%s,%d) - AdmUtilEventGenDot" \
                  % ("\t" * level, self.context, level)

    def traverse4DotGeneratorBody(self, \
                                  cfgFile, \
                                  level=0, \
                                  comments=True):
        """Pre-Text in graphviz dot-file"""
        if comments:
            print >> cfgFile, "%s// Body (%s,%d) - AdmUtilEventGenDot" \
                  % ("\t" * level, self.context, level)
        print >> cfgFile, '%s"%s" [' % ("\t" * level, self.context.objectID)
        print >> cfgFile, '%sshape="diamond",' % ("\t" * level)
        print >> cfgFile, '%slabel="%s"' % ("\t" * level, self.context.ikName)
        print >> cfgFile, '%s]' % ("\t" * level)
        print >> cfgFile, '%s// (%s)' % ("\t" * level, self.context.ikName)

    def traverse4DotGeneratorPost(self, 
                                  cfgFile, 
                                  level=0, 
                                  comments=True):
        """generate post-text in graphviz dot-file"""
        if comments:
            print >> cfgFile, "%s// Post (%s,%d) - AdmUtilEventGenDot" \
                  % ("\t" * level, self.context, level)

    def traverse4DotGenerator(self, cfgFile, level=0, comments=True):
        """generate text structure in graphviz dot-file"""
        self.traverse4DotGeneratorPre(cfgFile, level, comments)
        self.traverse4DotGeneratorBody(cfgFile, level, comments)
        self.traverse4DotGeneratorPost(cfgFile, level, comments)
