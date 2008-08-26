# -*- coding: utf-8 -*-
#
# Copyright (c) 2007, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611
"""Interface of compliance utility

the compliance utility should store the compliance/requirement-templates
for the host- or service-instances
"""

__version__ = "$Id$"

# python imports
import logging

# zope imports
from zope.interface import implements

# zc imports

# ict_ok.org imports
from org.ict_ok.components.supernode.supernode import Supernode
from org.ict_ok.admin_utils.compliance.interfaces import \
     IAdmUtilCompliance

logger = logging.getLogger("AdmUtilCompliance")


class AdmUtilCompliance(Supernode):
    """Compliance Utiltiy
    """
    
    implements(IAdmUtilCompliance)
    