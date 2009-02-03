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
"""Interface of Rack"""


__version__ = "$Id: interfaces.py_cog 411M 2009-02-02 23:31:12Z (lokal) $"

# zope imports
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, Int, List, TextLine
from zope.app.folder.interfaces import IFolder

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import ISuperclass
from org.ict_ok.components.interfaces import IComponent

_ = MessageFactory('org.ict_ok')


class IRack(IComponent):
    """A Rack object."""

    height = Int(
        title = _(u'Height'),
        description = _(u'Height of the rack'),
        required = False)
        

    room = Choice(
        title = _(u'Room'),
        vocabulary = 'AllRooms',
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


class IRackFolder(ISuperclass, IFolder):
    """Container for Rack objects
    """


class IAddRack(Interface):
    """Interface for all Objects"""
    template = Choice(
        title = _("Template"),
        vocabulary="AllRackTemplates",
        required = False)
