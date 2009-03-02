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
"""Interface of Notebook"""


__version__ = "$Id: interfaces.py_cog 399 2009-01-08 14:00:17Z markusleist $"

# zope imports
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, Date, Int, TextLine

# ict_ok.org imports

_ = MessageFactory('org.ict_ok')


class INotebook(Interface):
    """A Notebook object."""

    def trigger_online():
        """
        trigger workflow
        """


class INotebookFolder(Interface):
    """Container for Notebook objects
    """

class IAddNotebook(Interface):
    """Interface for all Objects"""
    template = Choice(
        title = _("Template"),
        vocabulary="AllNotebookTemplates",
        required = False)
