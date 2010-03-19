# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: template.py_cog 465 2009-03-05 02:34:02Z markusleist $
#
# pylint: disable-msg=E1101,W0142
#
"""implementation of Contract"""

__version__ = "$Id: template.py_cog 465 2009-03-05 02:34:02Z markusleist $"

# python imports

# zope imports

# lovely imports
from lovely.relation.property import FieldRelationManager

# ict_ok.org imports
from org.ict_ok.components.contract.interfaces import IContract
from org.ict_ok.components.contact_item.interfaces import IContactItem
from org.ict_ok.components.interfaces import IComponent

ClosedContracts_ContactItems_RelManager = \
       FieldRelationManager(IContract['contractors'],
                            IContactItem['closedContracts'],
                            relType='closedContracts:contractors')

Responsible4Contracts_ContactItems_RelManager = \
       FieldRelationManager(IContract['responsibles'],
                            IContactItem['responsible4Contracts'],
                            relType='responsible4Contracts:responsibles')

Contracts_Component_RelManager = \
       FieldRelationManager(IContract['component'],
                            IComponent['contracts'],
                            relType='contracts:component')
