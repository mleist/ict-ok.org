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
from zope.annotation.interfaces import IAnnotations
from zope.location import location
from zope.proxy import removeAllProxies

# zc imports

# ict_ok.org imports
from org.ict_ok.components.superclass.superclass import Superclass
from org.ict_ok.admin_utils.compliance.interfaces import \
     IEvaluations, IEvaluation
import schooltool.requirement.evaluation
#from schooltool.requirement.evaluation import getEvaluations

logger = logging.getLogger("AdmUtilCompliance")
EVALUATIONS_KEY = "org.ict_ok.components.evaluations"


class Evaluation(Superclass,
                 schooltool.requirement.evaluation.Evaluation):
    """ ict-ok.org wrapper
    """
    implements(IEvaluation)
    def __init__(self, requirement, scoreSystem, value, evaluator, **data):
        schooltool.requirement.evaluation.Evaluation.__init__(
            self, requirement, scoreSystem, value, evaluator)
        Superclass.__init__(self, ikName=requirement.ikName, **data)
        Superclass.__post_init__(self, **data)

class Evaluations(schooltool.requirement.evaluation.Evaluations):
    """ ict-ok.org wrapper
    """
    implements(IEvaluations)

def getEvaluations(context):
    """Adapt an ``IHaveEvaluations`` object to ``IEvaluations``."""
    annotations = IAnnotations(removeAllProxies(context))
    try:
        return annotations[EVALUATIONS_KEY]
    except KeyError:
        evaluations = Evaluations()
        annotations[EVALUATIONS_KEY] = evaluations
        location.locate(evaluations, removeAllProxies(context),
                        '++evaluations++')
        return evaluations
# Convention to make adapter introspectable
getEvaluations.factory = Evaluations
