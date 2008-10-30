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
"""Adapter implementation for generating graphviz-dot configuration
"""

__version__ = "$Id$"

# python imports
import logging

# zope imports
from zope.app import zapi
from zope.interface import implements

# ict_ok.org imports
from org.ict_ok.admin_utils.graphviz.interfaces import IGenGraphvizDot
from org.ict_ok.admin_utils.graphviz.adapter.superclass import \
     SuperclassGenGraphvizDot
from org.ict_ok.components.superclass.interfaces import ISuperclass


class SupernodeGenGraphvizDot(SuperclassGenGraphvizDot):
    """Implementation of Graphviz picture adapter for Supernode
    """

    implements(IGenGraphvizDot)

    def __init__(self, context):
        SuperclassGenGraphvizDot.__init__(self, context)
        self.parent = None

    def setParent(self, parent):
        """parent object is necessary for root node of graphviz-graph
        """
        self.parent = parent

    def traverse4DotGeneratorBody(self, \
                                  cfgFile, \
                                  level=0, \
                                  comments=True,
                                  signalsOutput=False,
                                  recursive=True):
        """Pre-Text in graphviz dot-file"""
        if comments:
            print >> cfgFile, "%s// Body (%s,%d) - SupernodeGenGraphvizDot" \
                  % ("\t" * level, self.context.__name__, level)

        print >> cfgFile, '%s"%s" [' % ("\t" * level, self.context.objectID)
        print >> cfgFile, '%sshape="plaintext",' % ("\t" * (level + 1))
        print >> cfgFile, '%sstyle="filled,setlinewidth(0)",' \
              % ("\t" * (level + 1))
        print >> cfgFile, '%sfillcolor = chartreuse2,' % ("\t" * (level + 1))
        print >> cfgFile, '%smargin = 0,' % ("\t" * (level + 1))
        print >> cfgFile, '%shref = "%s/@@details.html",' \
              % ("\t" * (level + 1), zapi.getPath(self.context))

        #print >> cfgFile, '%slabel = <<TABLE BORDER = "0" CELLBORDER = "0" ' \
              #'CELLPADDING = "0" CELLSPACING = "0"><TR><TD>' \
              #'<IMG SRC = "/home/markus/Projekte/IKOMtrol-hp/apple-red.png"/>' \
              #'</TD></TR><TR><TD><FONT FACE = "Arial" POINT-SIZE = "10">%s' \
              #'</FONT></TD></TR></TABLE>>' \
              #% ("\t" * (level + 1), self.context.ikName)

        print >> cfgFile, '%slabel = <' % ("\t" * (level + 1))
        print >> cfgFile, '%s<TABLE BORDER="0" CELLBORDER="1" CELLPADDING = "2" CELLSPACING = "0">' % ("\t" * (level + 1))
        print >> cfgFile, '%s<TR><TD WIDTH="120px">%s</TD></TR>' % ("\t" * (level + 1), self.context.ikName)
        if signalsOutput:
            allInpNamesDict = self.context.getAllInpEventNames()
            for inpName in allInpNamesDict.keys():
                print >> cfgFile, '%s<TR><TD ALIGN="LEFT" PORT="%s" '\
                      'BGCOLOR="yellow">%s</TD></TR>' % \
                      ("\t" * (level + 1), inpName, inpName)
            allOutNamesDict = self.context.getAllOutEventNames()
            for outName in allOutNamesDict.keys():
                print >> cfgFile, '%s<TR><TD ALIGN="RIGHT" PORT="%s" '\
                      'BGCOLOR="orange">%s</TD></TR>' % \
                      ("\t" * (level + 1), outName, outName)
        #print >> cfgFile, '%s<TR><TD ALIGN="LEFT" PORT="sig_inp1" BGCOLOR="yellow">sig_inp1</TD></TR>' % ("\t" * (level + 1))
        #print >> cfgFile, '%s<TR><TD ALIGN="LEFT" PORT="sig_inp2" BGCOLOR="yellow">sig_inp2</TD></TR>' % ("\t" * (level + 1))
        #print >> cfgFile, '%s<TR><TD ALIGN="RIGHT" PORT="sig_out1" BGCOLOR="orange">sig_out1</TD></TR>' % ("\t" * (level + 1))
        print >> cfgFile, '%s</TABLE>>' % ("\t" * (level + 1))
        print >> cfgFile, '%s]; // %s' % ("\t" * level, self.context.__name__)
        if recursive:
            its = self.context.items()
        else:
            its = []
        for (dummy_name, oobj) in its:
            if ISuperclass.providedBy(oobj):
                try:
                    adapterGenGraphvizDot = IGenGraphvizDot(oobj)
                    if adapterGenGraphvizDot:
                        adapterGenGraphvizDot.setParent(self.context)
                        adapterGenGraphvizDot.traverse4DotGenerator(\
                            cfgFile, level + 1, comments, signalsOutput)
                except TypeError, err:
                    logging.error("Error in AdmUtilGraphviz::getRootDot()"\
                                  % err)
