# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0213,W0232
#
"""Interface of OperatingSoftware"""


__version__ = "$Id$"

# zope imports
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, Int, TextLine

# ict_ok.org imports

_ = MessageFactory('org.ict_ok')


class IOperatingSoftware(Interface):
    """A OperatingSoftware object."""

    device = Choice(
        title=_(u'Device'),
        vocabulary='AllDevices',
        required=False
        )
        
    manufacturer = TextLine(
        max_length = 200,
        title = _("Manufacturer"),
        description = _("Name/Address of the manufacturer."),
        required = False)
    osType = TextLine(
        max_length = 200,
        title = _("OS type"),
        description = _("type of operating system."),
        required = False)
    otherType = TextLine(
        max_length = 200,
        title = _("Other type"),
        description = _("other type description."),
        required = False)
    versionText = TextLine(
        max_length = 200,
        title = _("Version text"),
        required = False)
    licenseKey = TextLine(
        max_length = 200,
        title = _("License key"),
        required = False)
    language = TextLine(
        max_length = 200,
        title = _("Language"),
        required = False)
    majorVersion = Int(
        title = _("Major version"),
        required = False)
    minorVersion = Int(
        title = _("Minor version"),
        required = False)
    revisionNumber = Int(
        title = _("Revision number"),
        required = False)
    buildNumber = Int(
        title = _("Build number"),
        required = False)

    def trigger_online():
        """
        trigger workflow
        """


class IOperatingSoftwareFolder(Interface):
    """Container for OperatingSoftware objects
    """

class IAddOperatingSoftware(Interface):
    """Interface for all Objects"""
    template = Choice(
        title = _("Template"),
        vocabulary="AllOperatingSoftwareTemplates",
        required = False)
