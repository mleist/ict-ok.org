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
"""Interface of Rack"""


__version__ = "$Id$"

# zope imports
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, Int, List

# ict_ok.org imports

_ = MessageFactory('org.ict_ok')


class IRack(Interface):
    """A Rack object."""

    height = Int(
        title = _(u'Height'),
        description = _(u'Height of the rack'),
        required = False)
        
    patchpanels = List(
        title = _(u'Patchpanel'),
        value_type=Choice(vocabulary='AllUnusedOrUsedRackPatchPanels'),
        default=[],
        required = False)
        
    def trigger_online():
        """
        trigger workflow
        """


class IRackFolder(Interface):
    """Container for Rack objects
    """


class IAddRack(Interface):
    """Interface for all Objects"""
    template = Choice(
        title = _("Template"),
        vocabulary="AllRackTemplates",
        required = False)
