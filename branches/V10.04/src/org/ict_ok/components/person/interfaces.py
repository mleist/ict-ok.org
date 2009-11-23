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
"""Interface of Person"""


__version__ = "$Id: interfaces.py_cog 465 2009-03-05 02:34:02Z markusleist $"

# zope imports
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, Int, List, TextLine
from zope.app.folder.interfaces import IFolder

_ = MessageFactory('org.ict_ok')


class IPerson(Interface):
    """A Person object."""

    firstName = TextLine(
        title = _(u'first name'),
        description = _(u"first name of the person"),
        required = False)
        
    lastName = TextLine(
        title = _(u'last name'),
        description = _(u"last name of person"),
        required = False)
        
    title = TextLine(
        title = _(u'title'),
        description = _(u"title of person"),
        required = False)
        
#    def trigger_online():
#        """
#        trigger workflow
#        """


class IPersonFolder(Interface):
    """Container for Person objects
    """


class IAddPerson(Interface):
    """Interface for all Objects"""
    template = Choice(
        title = _("Template"),
        vocabulary="AllPersonTemplates",
        required = False)
