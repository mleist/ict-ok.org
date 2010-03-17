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
from zope.schema import Datetime, TextLine, Bool
from org.ict_ok.schema.datetime import IctDatetime
from zope.i18nmessageid import MessageFactory

# ict_ok.org imports
from org.ict_ok.admin_utils.generators.interfaces import \
     IAdmUtilGenerators

_ = MessageFactory('org.ict_ok')


class IAdmUtilGeneratorNagios(IAdmUtilGenerators):
    """
    major component for registration and event distribution 
    """
    isRunning = Bool(
        title = _("nagios is running"),
        default = False)

    pathInitScript = TextLine(
        max_length = 200,
        title = _(u"init script"),
        description = _(u"nagios init script with path"),
        default = _(u"/etc/init.d/nagios"),
        required = True)

    pathConfigData = TextLine(
        max_length = 200,
        title = _(u"path to configuration"),
        default = u"/opt/nagios/etc/ict_ok",
        required = True)

    lastConfigFileChange = IctDatetime(
        title=_(u"last change"),
        description=_(u"last change of configuration file"),
        required=False)

    lastDeamonReload = IctDatetime(
        title=_(u"last reload"),
        description=_(u"last reload of nagios deamon"),
        required=False)

    def touchLastConfigFile():
        """change timestamp in the utility
        
        will trigger a reload of the nagios-daemon on cron
        """

    def reloadDaemon():
        """ reload the nagios daemon
        """

    def allConfigFilesOut():
        """make all configuration files
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

    def nagiosConfigFileOut(forceOutput=False, event=None):
        """Nagios-Filegenerator
        
        will produce the nagios configuration files
        
        forceOutput: False will check for a relevant attribute change
        True will alway generate a new config file
         
        event: None or the zope event from lifecycle
       """

    def nagiosConfigFileRemove():
        """remove old nagios configuration file for this object
        """

    def eventModifiesCfgFile(event):
        """check for attribute changes
        """


class INagiosCheck(Interface):
    """ Interface for all Object whoch should support nagios checks
    """
    genNagios = Bool(
        title = _("for Nagios"),
        description = _("enabled in Nagios"),
        default = False,
        required = False)
