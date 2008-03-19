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
    def fileOpen():
        """will open a filehandle to the specific object
        """

    def fileClose():
        """will close the filehandle to the specific object
        """

    def write(text_arg):
        """will write the text_arg into the configuration file
        """

    def traverse4nagiosGeneratorPre(level, comments):
        """graphviz configuration preamble
        
        level: indent-level
        comments: should there comments are in the output?

        """

    def traverse4nagiosGeneratorPost(level, comments):
        """graphviz configurations text after object
        
        level: indent-level
        comments: should there comments are in the output?

        """

    def traverse4nagiosGeneratorBody(level, comments):
        """graphviz configuration data of/in object
        
        level: indent-level
        comments: should there comments are in the output?

        """

    def traverse4nagiosGenerator(level, comments):
        """Configuration generator
        
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

