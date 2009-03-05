# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: interfaces.py_cog 465 2009-03-05 02:34:02Z markusleist $
#
# pylint: disable-msg=E0213,W0232
#
"""Interface of DisplayUnit"""


__version__ = "$Id: interfaces.py_cog 465 2009-03-05 02:34:02Z markusleist $"

# zope imports
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, Int, List, TextLine
from zope.app.folder.interfaces import IFolder

_ = MessageFactory('org.ict_ok')


class IDisplayUnit(Interface):
    """A DisplayUnit object."""

    horizontalResolution = Int(
        title = _(u'Horizontal resolution'),
        description = _(u"FlatPanel's horizontal resolution in Pixels."),
        required = False)
        
    verticalResolution = Int(
        title = _(u'Vertical resolution'),
        description = _(u"FlatPanel's vertical resolution in Pixels."),
        required = False)
        
    def trigger_online():
        """
        trigger workflow
        """


class IDisplayUnitFolder(Interface):
    """Container for DisplayUnit objects
    """


class IAddDisplayUnit(Interface):
    """Interface for all Objects"""
    template = Choice(
        title = _("Template"),
        vocabulary="AllDisplayUnitTemplates",
        required = False)
