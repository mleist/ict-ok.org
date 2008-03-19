# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0213,E0211,W0232,W0622
#
"""Interface to nagios generator"""

__version__ = "$Id$"

# zope imports
from zope.interface import Interface

# ict_ok.org imports
from org.ict_ok.admin_utils.generators.interfaces import \
     IAdmUtilGenerators


class IAdmUtilGeneratorNagios(IAdmUtilGenerators):
    """
    major component for registration and event distribution 
    """
    def getConfig(self):
        """make configuration file
        TODO filename or filehandle must be an argument
        """


class IGenNagios(Interface):
    """Interface of nagios-Adapter
    """
    def traverse4nagiosGeneratorPre(cfgFile, level, comments):
        """graphviz configuration preamble
        
        cfgFile: handle to open file
        level: indent-level
        comments: should there comments are in the output?

        """

    def traverse4nagiosGeneratorPost(cfgFile, level, comments):
        """graphviz configurations text after object
        
        cfgFile: handle to open file
        level: indent-level
        comments: should there comments are in the output?

        """

    def traverse4nagiosGeneratorBody(cfgFile, level, comments):
        """graphviz configuration data of/in object
        
        cfgFile: handle to open file
        level: indent-level
        comments: should there comments are in the output?

        """

    def traverse4nagiosGenerator(cfgFile, level, comments):
        """Configuration generator
        
        cfgFile: handle to open file
        level: indent-level
        comments: should there comments are in the output?

        """

    def nagiosConfigFileOut():
        """Nagios-Filegenerator
        
        will produce the nagios configuration files
        """
        
    def nagiosConfigFileRemove():
        """remove old nagios configuration file for this object
        """
        pass
