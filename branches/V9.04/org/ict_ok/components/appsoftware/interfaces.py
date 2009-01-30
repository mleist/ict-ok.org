# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: interfaces.py_cog 399 2009-01-08 14:00:17Z markusleist $
#
# pylint: disable-msg=E0213,W0232
#
"""Interface of ApplicationSoftware"""


__version__ = "$Id: interfaces.py_cog 399 2009-01-08 14:00:17Z markusleist $"

# zope imports
from zope.interface import Attribute, Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, Int, List, TextLine
from zope.app.folder.interfaces import IFolder

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import ISuperclass
from org.ict_ok.components.interfaces import IComponent

_ = MessageFactory('org.ict_ok')


class IApplicationSoftware(IComponent):
    """A ApplicationSoftware object."""

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
    otherType = TextLine(
        max_length = 200,
        title = _("Other type"),
        description = _("other type description."),
        required = False)
    targetOperatingSystems = TextLine(
        max_length = 200,
        title = _("Target OS"),
        description = _("target operating systems."),
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


class IApplicationSoftwareFolder(ISuperclass, IFolder):
    """Container for ApplicationSoftware objects
    """


class IAddApplicationSoftware(Interface):
    """Interface for all Objects"""
    template = Choice(
        title = _("Template"),
        vocabulary="AllApplicationSoftwareTemplates",
        required = False)
