# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0702,W0221
#
"""implementation of a "Object-Message-Queue-Utility" 
"""

__version__ = "$Id$"

# python imports

# zope imports

# lovely imports
from lovely.relation.property import FieldRelationManager

# ict_ok.org imports
from org.ict_ok.admin_utils.categories.interfaces import ICategory
from org.ict_ok.admin_utils.compliance.interfaces import IRequirement
from org.ict_ok.components.interfaces import IComponent


Categories_Components_RelManager = \
       FieldRelationManager(ICategory['components'],
                            IComponent['categories'],
                            relType='categories:components')


Categories_Requirements_RelManager = \
       FieldRelationManager(ICategory['requirements'],
                            IRequirement['categories'],
                            relType='categories:requirements')
