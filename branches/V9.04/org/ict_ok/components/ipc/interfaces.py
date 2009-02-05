# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: interfaces.py_cog 424 2009-02-02 23:58:56Z markusleist $
#
# pylint: disable-msg=E0213,W0232
#
"""Interface of IndustrialComputer"""


__version__ = "$Id: interfaces.py_cog 424 2009-02-02 23:58:56Z markusleist $"

# zope imports
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, Date, Int, TextLine

# ict_ok.org imports
from org.ict_ok.components.device.interfaces import IDevice, IDeviceFolder

_ = MessageFactory('org.ict_ok')


class IIndustrialComputer(IDevice):
    """A IndustrialComputer object."""

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
        
    memsize = Int(
        title = _(u'Memory size (MB)'),
        description = _(u'Memory size in MB'),
        required = False)

    cpuType = TextLine(
        title = _(u'CPU type'),
        description = _(u'Text of CPU type'),
        required = False)
        
    hardware = TextLine(
        title = _(u'Hardware'),
        description = _(u'Hardware of the system.'),
        required = False)
        
    serialNumber = TextLine(
        title = _(u'Serial number'),
        description = _(u'Serial number'),
        required = False)
        
    inv_id = TextLine(
        title = _(u'Inventory id'),
        description = _(u'Id of inventory.'),
        required = False)
        
    modelType = TextLine(
        title = _(u'Model type'),
        description = _(u'model type'),
        required = False)
        
    deliveryDate = Date(
        title = _(u'Delivery date'),
        description = _(u'delivery date'),
        required = False)
        
    documentNumber = TextLine(
        title = _(u'Document number'),
        description = _(u'Document number'),
        required = False)
                
    def trigger_online():
        """
        trigger workflow
        """


class IIndustrialComputerFolder(IDeviceFolder):
    """Container for IndustrialComputer objects
    """


class IAddIndustrialComputer(Interface):
    """Interface for all Objects"""
    template = Choice(
        title = _("Template"),
        vocabulary="AllIndustrialComputerTemplates",
        required = False)
