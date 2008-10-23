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
from org.ict_ok.admin_utils.compliance.interfaces import \
     IEvaluations, IEvaluation
import schooltool.requirement.evaluation
from schooltool.requirement.evaluation import getEvaluations

logger = logging.getLogger("AdmUtilCompliance")

class Evaluation(schooltool.requirement.evaluation.Evaluation):
    """ ict-ok.org wrapper
    """
    implements(IEvaluation)

class Evaluations(schooltool.requirement.evaluation.Evaluations):
    """ ict-ok.org wrapper
    """
    implements(IEvaluations)
