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
"""Interface of Contact"""


__version__ = "$Id: interfaces.py_cog 465 2009-03-05 02:34:02Z markusleist $"

# zope imports
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, Int, List, TextLine
from zope.app.folder.interfaces import IFolder

_ = MessageFactory('org.ict_ok')


class IContact(Interface):
    """A Contact object."""

    workOrder = Choice(
        title = _(u'Work Order'),
        vocabulary = 'AllWorkOrders',
        required = False)
        

    contactItems = List(
        title = _(u'Contact Items'),
        value_type=Choice(vocabulary='AllUnusedOrUsedContactContactItems'),
        default=[],
        required = False)

    mainContact = Choice(
        title = _(u'Main contact'),
        vocabulary = 'AllContacts',
        required = False)
        
    subContacts = List(
        title = _(u'Sub contacts'),
        value_type=Choice(vocabulary='AllContacts'),
        default=[],
        required = False)
        
        
    def trigger_online():
        """
        trigger workflow
        """


class IContactFolder(Interface):
    """Container for Contact objects
    """


class IAddContact(Interface):
    """Interface for all Objects"""
    template = Choice(
        title = _("Template"),
        vocabulary="AllContactTemplates",
        required = False)
