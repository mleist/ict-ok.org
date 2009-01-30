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
from zope.schema import Choice, Date, List, TextLine

# ict_ok.org imports
from org.ict_ok.components.device.interfaces import IDevice, IDeviceFolder

_ = MessageFactory('org.ict_ok')


class INotebook(IDevice):
    """A Notebook object."""

    user = Choice(
        title = _("User"),
        description = _("User of the mobile phone"),
        vocabulary="AllLdapUser",
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

    def trigger_online():
        """
        trigger workflow
        """


class INotebookFolder(IDeviceFolder):
    """Container for Notebook objects
    """

class IAddNotebook(Interface):
    """Interface for all Objects"""
    template = Choice(
        title = _("Template"),
        vocabulary="AllNotebookTemplates",
        required = False)
