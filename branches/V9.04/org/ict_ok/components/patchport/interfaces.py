# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: interfaces.py_cog 411M 2009-02-02 23:31:12Z (lokal) $
#
# pylint: disable-msg=E0213,W0232
#
"""Interface of PatchPort"""


__version__ = "$Id: interfaces.py_cog 411M 2009-02-02 23:31:12Z (lokal) $"

# zope imports
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, Int, List, TextLine

# ict_ok.org imports
from org.ict_ok.components.physical_connector.interfaces import \
    IPhysicalConnector, IPhysicalConnectorFolder

_ = MessageFactory('org.ict_ok')


class IPatchPort(IPhysicalConnector):
    """A PatchPort object."""

    patchpanel = Choice(
        title = _(u'Patch panel'),
        vocabulary = 'AllPatchPanels',
        required = False)
        
    def trigger_online():
        """
        trigger workflow
        """


class IPatchPortFolder(IPhysicalConnectorFolder):
    """Container for PatchPort objects
    """


class IAddPatchPort(Interface):
    """Interface for all Objects"""
    template = Choice(
        title = _("Template"),
        vocabulary="AllPatchPortTemplates",
        required = False)
