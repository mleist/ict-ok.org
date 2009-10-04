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
"""Interface of WorkOrder"""


__version__ = "$Id: interfaces.py_cog 465 2009-03-05 02:34:02Z markusleist $"

# zope imports
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, Int, List, TextLine
from zope.app.folder.interfaces import IFolder

_ = MessageFactory('org.ict_ok')


class IWorkOrder(Interface):
    """A WorkOrder object."""

    mainWorkOrder = Choice(
        title = _(u'Main work order'),
        vocabulary = 'AllWorkOrders',
        required = False)
        

    products = List(
        title = _(u'Products'),
        value_type=Choice(vocabulary='AllUnusedOrUsedWorkOrderProducts'),
        default=[],
        required = False)
        
    contactItems = List(
        title = _(u'Contact Items'),
        value_type=Choice(vocabulary='AllUnusedOrUsedWorkOrderContactItems'),
        default=[],
        required = False)
        
    contacts = List(
        title = _(u'Contacts'),
        value_type=Choice(vocabulary='AllUnusedOrUsedWorkOrderContacts'),
        default=[],
        required = False)
        
    subWorkOrders = List(
        title = _(u'Sub work orders'),
        value_type=Choice(vocabulary='AllUnusedOrUsedWorkOrderWorkOrders'),
        default=[],
        required = False)
        
    def trigger_online():
        """
        trigger workflow
        """


class IWorkOrderFolder(Interface):
    """Container for WorkOrder objects
    """


class IAddWorkOrder(Interface):
    """Interface for all Objects"""
    template = Choice(
        title = _("Template"),
        vocabulary="AllWorkOrderTemplates",
        required = False)
