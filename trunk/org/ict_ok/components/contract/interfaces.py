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
"""Interface of Contract"""


__version__ = "$Id: interfaces.py_cog 465 2009-03-05 02:34:02Z markusleist $"

# zope imports
from zope.interface import Interface, Invalid, invariant
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, Date, List, TextLine, Timedelta

# ict_ok.org imports
from org.ict_ok.schema.physicalvalid import PhysicalQuantity
from org.ict_ok.libs.physicalquantity import convertQuantity

_ = MessageFactory('org.ict_ok')


class IContract(Interface):
    """A Contract object."""

    type = Choice(
        title = _(u'Contract type'),
        description = _(u"Contract type"),
        required = True,
        vocabulary = "ContractTypes")
        
    startDate = Date(
        title = _(u'start date'),
        description = _(u"contract start date"),
        required = False)
        
    state = Choice(
        title = _(u'State'),
        description = _(u"State"),
        required = False,
        vocabulary = "ContractState")
        
    expirationDate = Date(
        title = _(u'expiration date'),
        description = _(u"expiration of contract"),
        required = False)
        
    annualCharges = PhysicalQuantity(
        title = _(u'annual charges'),
        description = _(u"annual charges"),
        required = False)
        
    internalContractNumber = TextLine(
        title = _(u'internal contract number'),
        description = _(u"internal contract number"),
        required = False)
        
    externalContractNumber = TextLine(
        title = _(u'external contract number'),
        description = _(u"external contract number"),
        required = False)
        
    periodOfNotice = Timedelta(
        title = _(u'period of notice'),
        description = _(u"period of notice"),
        required = False)
        
    minimumTerm = Timedelta(
        title = _(u'minimum term'),
        description = _(u"minimum term"),
        required = False)
        
    contractors = List(
        title = _(u'Contractors'),
        description = _(u"Contractors"),
        value_type=Choice(vocabulary='AllContactItems'),
        default=[],
        required = False)
        
    responsibles = List(
        title = _(u'Responsibles'),
        description = _(u"Responsibles"),
        value_type=Choice(vocabulary='AllContactItems'),
        required = False)

    component = Choice(
        title = _(u'Component'),
        vocabulary = 'AllComponents',
        required = False)
        
    @invariant
    def ensureAnnualChargesUnit(contract):
        if contract.annualCharges is not None:
            annualCharges = convertQuantity(contract.annualCharges)
            if not annualCharges.isCurrency():
                raise Invalid(
                    "No currency specification: '%s'." % \
                    (contract.annualCharges))

    def trigger_online():
        """
        trigger workflow
        """


class IContractFolder(Interface):
    """Container for Contract objects
    """


class IAddContract(Interface):
    """Interface for all Objects"""
    template = Choice(
        title = _("Template"),
        vocabulary="AllContractTemplates",
        required = False)
