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
"""Interface of IndustrialComputer"""


__version__ = "$Id$"

# zope imports
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, Date, Int, TextLine

# ict_ok.org imports

_ = MessageFactory('org.ict_ok')


class IIndustrialComputer(Interface):
    """A IndustrialComputer object."""

    def trigger_online():
        """
        trigger workflow
        """


class IIndustrialComputerFolder(Interface):
    """Container for IndustrialComputer objects
    """


class IAddIndustrialComputer(Interface):
    """Interface for all Objects"""
    template = Choice(
        title = _("Template"),
        vocabulary="AllIndustrialComputerTemplates",
        required = False)
