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
"""Interface of Reminder"""


__version__ = "$Id: interfaces.py_cog 465 2009-03-05 02:34:02Z markusleist $"

# zope imports
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, Int, List, TextLine, Date
from zope.app.folder.interfaces import IFolder

_ = MessageFactory('org.ict_ok')


class IReminder(Interface):
    """A Reminder object."""

    dueDate = Date(
        title = _(u'due date'),
        description = _(u"due date of reminder"),
        required = False)
        
    def trigger_online():
        """
        trigger workflow
        """


class IAddReminder(Interface):
    """Interface for all Objects"""
    template = Choice(
        title = _("Template"),
        vocabulary="AllReminderTemplates",
        required = False)
