# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0213,W0232
#
"""Interface of PatchPanel"""


__version__ = "$Id$"

# zope imports
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, Int, List

# ict_ok.org imports

_ = MessageFactory('org.ict_ok')


class IPatchPanel(Interface):
    """A PatchPanel object."""

    portCount = Int(
        title = _(u'Port quantity'),
        description = _(u'Quantity of all patch ports'),
        required = False)
        

    rack = Choice(
        title = _(u'Rack'),
        vocabulary = 'AllRacks',
        required = False)
        

    patchports = List(
        title = _(u'Patch ports'),
        value_type=Choice(vocabulary='AllUnusedOrUsedPatchPanelPatchPorts'),
        default=[],
        required = False)
        
    def trigger_online():
        """
        trigger workflow
        """


class IPatchPanelFolder(Interface):
    """Container for PatchPanel objects
    """


class IAddPatchPanel(Interface):
    """Interface for all Objects"""
    template = Choice(
        title = _("Template"),
        vocabulary="AllPatchPanelTemplates",
        required = False)
