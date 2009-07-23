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
"""Interface of Printer"""


__version__ = "$Id$"

# zope imports
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, Int, List, TextLine
from zope.app.folder.interfaces import IFolder

_ = MessageFactory('org.ict_ok')


class IPrinter(Interface):
    """A Printer object."""

    paperTypesAvailable = TextLine(
        title = _(u'Available paper types'),
        description = _(u"An array of free-form strings specifying the types and sizes of paper that are currently available on the Printer."),
        required = False)
        
    def trigger_online():
        """
        trigger workflow
        """


class IPrinterFolder(Interface):
    """Container for Printer objects
    """


class IAddPrinter(Interface):
    """Interface for all Objects"""
    template = Choice(
        title = _("Template"),
        vocabulary="AllPrinterTemplates",
        required = False)
