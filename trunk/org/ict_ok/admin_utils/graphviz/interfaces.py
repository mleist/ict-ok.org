# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0213,W0232,W0622
#
"""Interface to Graphviz generator"""

__version__ = "$Id$"

# zope imports
from zope.interface import Interface
from zope.schema import Choice
from zope.i18nmessageid import MessageFactory

# ict_ok.org imports
from org.ict_ok.components.supernode.interfaces import ISupernode

_ = MessageFactory('org.ict_ok')


class IAdmUtilGraphviz(ISupernode):
    """
    major component for registration and event distribution 
    """

    graphviz_type = Choice(
        title = _("Output Type"),
        description = _("Output Type"),
        vocabulary = "GraphvizOutputTypes"
    )

    def getPngFile(self):
        """get Graphviz Picture
        """
        
    def getCmapxText(self):
        """get Graphviz Imagemap
        """


class IGenGraphvizDot(Interface):
    """Interface of Graphviz-Adapter
    """
    def setParent(self, parent):
        """set Parent-Object
        """

    def traverse4DotGeneratorPre(self, cfgFile, level):
        """graphviz configuration preamble
        """

    def traverse4DotGeneratorPost(self, cfgFile, level):
        """graphviz configurations text after object
        """

    def traverse4DotGeneratorBody(self, cfgFile, level):
        """graphviz configuration data of object
        """

    def traverse4DotGenerator(self, cfgFile, level):
        """
        cfgFile: handle to open file
        level: indent-level
        """
