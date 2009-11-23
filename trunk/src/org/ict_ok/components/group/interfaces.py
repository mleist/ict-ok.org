# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
#               Sebastian Napiorkowski <i_am@not-there.org>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0213,W0232
#
"""Interface of Group"""


__version__ = "$Id$"

# zope imports
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, Int, List, TextLine
from zope.app.folder.interfaces import IFolder

_ = MessageFactory('org.ict_ok')


class IGroup(Interface):
    """A Group object."""

    contactItems = List(
        title = _(u'Contact items'),
        value_type=Choice(vocabulary='AllContactItems'),
        default=[],
        required = False)
        
    def trigger_online():
        """
        trigger workflow
        """


class IGroupFolder(Interface):
    """Container for Group objects
    """


class IAddGroup(Interface):
    """Interface for all Objects"""
    template = Choice(
        title = _("Template"),
        vocabulary="AllGroupTemplates",
        required = False)
