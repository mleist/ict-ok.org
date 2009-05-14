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
"""Interface of ContactItem"""


__version__ = "$Id: interfaces.py_cog 465 2009-03-05 02:34:02Z markusleist $"

# zope imports
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, Int, List, TextLine
from zope.app.folder.interfaces import IFolder

_ = MessageFactory('org.ict_ok')


class IContactItem(Interface):
    """A ContactItem object."""

    contact = Choice(
        title = _(u'Contact'),
        vocabulary = 'AllContacts',
        required = False)
        
    workOrder = Choice(
        title = _(u'WorkOrder'),
        vocabulary = 'AllWorkOrders',
        required = False)
        

    adresses = List(
        title = _(u'Addresses'),
        value_type=Choice(vocabulary='AllUnusedOrUsedContactItemAddresses'),
        default=[],
        required = False)
        
    def trigger_online():
        """
        trigger workflow
        """


class IContactItemFolder(Interface):
    """Container for ContactItem objects
    """


class IAddContactItem(Interface):
    """Interface for all Objects"""
    template = Choice(
        title = _("Template"),
        vocabulary="AllContactItemTemplates",
        required = False)
