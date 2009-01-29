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
from zope.interface import Attribute, Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, Date, Int, List, TextLine
from zope.app.folder.interfaces import IFolder

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import ISuperclass
from org.ict_ok.components.interfaces import IComponent

_ = MessageFactory('org.ict_ok')


class INotebook(IComponent):
    """A Notebook object."""

#    conns = List(title=u"Conns 0..n",
#                 #value_type=Object(IObject),
#                 value_type=Choice(vocabulary='AllNotebooks'),
#                 required=False,
#                 default=[])
#    conn = Choice(
#        title=u'Conn 0..1',
#        vocabulary='AllNotebooks',
#        required=False
#        )
    #related = schema.List(
            #title=u"Related",
            #value_type=schema.Choice(vocabulary='demo.documentsInParent'),
            #required=False,
            #default=[])

    user = Choice(
        title = _("User"),
        description = _("User of the mobile phone"),
        vocabulary="AllLdapUser",
        required = False)
    manufacturer = TextLine(
        max_length = 200,
        title = _("Manufacturer"),
        description = _("Name/Address of the manufacturer."),
        required = True)
    vendor = TextLine(
        max_length = 500,
        title = _("Vendor"),
        description = _("Name/Address of the vendor."),
        default = u"",
        required = False)
    productionState = Choice(
        title = _("Production state"),
        vocabulary="AllHostProductionStates",
        default = 'production',
        readonly = False,
        required = True)
    hardware = TextLine(
        max_length = 500,
        title = _("Hardware"),
        description = _("Hardware of the system."),
        default = u"",
        required = False)
    serialNumber = TextLine(
        max_length = 80,
        title = _("Serial number"),
        description = _("Serial number"),
        required = False)
    inv_id = TextLine(
        max_length = 500,
        title = _("inventory id"),
        description = _("Id of inventory."),
        default = u"",
        required = False)
    modelType = TextLine(
        max_length = 200,
        title = _("model type"),
        required = False)
    deliveryDate = Date(
        title = _("delivery date"),
        description = _("delivery date"),
        required = False)

    appSoftware = List(title=_(u"Applicaton software"),
        value_type=Choice(vocabulary='AllUnusedOrSelfApplicationSoftwares'),
        required=False,
        default=[])

    def trigger_online():
        """
        trigger workflow
        """


class INotebookFolder(ISuperclass, IFolder):
    """Container for Notebook objects
    """

class IAddNotebook(Interface):
    """Interface for all Objects"""
    template = Choice(
        title = _("Template"),
        vocabulary="AllNotebookTemplates",
        required = False)
