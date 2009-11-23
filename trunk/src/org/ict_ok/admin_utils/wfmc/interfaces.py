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
"""Interface to WFMC generator"""

__version__ = "$Id$"

# zope imports
from zope.interface import Interface
from zope.schema import Choice
from zope.i18nmessageid import MessageFactory

# ict_ok.org imports

_ = MessageFactory('org.ict_ok')


class IAdmUtilWFMC(Interface):
    """
    major component for registration and event distribution 
    """

    graphviz_type = Choice(
        title = _("Output Type"),
        description = _("Output Type"),
        vocabulary = "GraphvizOutputTypes"
    )

    def getIMGFile(self):
        """get Graphviz Picture
        """
        
    def getCmapxText(self):
        """get Graphviz Imagemap
        """


class IGenWFMCDot(Interface):
    """Interface of Graphviz-Adapter
    """
    def traverse4WFMCDotGeneratorPre(self, cfgFile, level):
        """graphviz configuration preamble
        """

    def traverse4WFMCDotGeneratorPost(self, cfgFile, level):
        """graphviz configurations text after object
        """

    def traverse4WFMCDotGeneratorBody(self, cfgFile, level):
        """graphviz configuration data of object
        """

    def traverse4WFMCDotGenerator(self, cfgFile, level):
        """
        cfgFile: handle to open file
        level: indent-level
        """
