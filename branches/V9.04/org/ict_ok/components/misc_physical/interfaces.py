# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: interfaces.py_cog 467 2009-03-05 04:28:59Z markusleist $
#
# pylint: disable-msg=E0213,W0232
#
"""Interface of MiscPhysical"""


__version__ = "$Id: interfaces.py_cog 467 2009-03-05 04:28:59Z markusleist $"

# zope imports
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, Int, List, TextLine
from zope.app.folder.interfaces import IFolder

_ = MessageFactory('org.ict_ok')


class IMiscPhysical(Interface):
    """A MiscPhysical object."""
    def trigger_online():
        """
        trigger workflow
        """


class IMiscPhysicalFolder(Interface):
    """Container for MiscPhysical objects
    """


class IAddMiscPhysical(Interface):
    """Interface for all Objects"""
    template = Choice(
        title = _("Template"),
        vocabulary="AllMiscPhysicalTemplates",
        required = False)
