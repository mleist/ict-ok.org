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
from zope.app import zapi
from zope.interface import implements
from zope.annotation.interfaces import IAnnotations
from zope.location import location
from zope.proxy import removeAllProxies
from zope.app.catalog.interfaces import ICatalog
from zope.app.container.btree import BTreeContainer

# ict_ok.org imports
from org.ict_ok.components.superclass.superclass import Superclass
from org.ict_ok.admin_utils.compliance.interfaces import \
     IEvaluations, IEvaluation
from org.ict_ok.admin_utils.compliance.requirement import getRequirementList
import schooltool.requirement.evaluation

logger = logging.getLogger("AdmUtilCompliance")
EVALUATIONS_KEY = "org.ict_ok.components.evaluations"


class Evaluation(BTreeContainer, Superclass,
                 schooltool.requirement.evaluation.Evaluation):
    """ ict-ok.org wrapper
    """
    implements(IEvaluation)
    def __init__(self, requirement, scoreSystem, value, evaluator, **data):
        BTreeContainer.__init__(self)
        schooltool.requirement.evaluation.Evaluation.__init__(
            self, requirement, scoreSystem, value, evaluator)
        Superclass.__init__(self, ikName=requirement.ikName, **data)
        Superclass.__post_init__(self, **data)

class Evaluations(schooltool.requirement.evaluation.Evaluations):
    """ ict-ok.org wrapper
    """
    implements(IEvaluations)

def getEvaluationsDone(context):
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

def getEvaluationsTodo(context):
    """List of Content objects"""
    #retList = []
    retSet = set([])
    my_catalog = zapi.getUtility(ICatalog)
    if hasattr(context, "requirements"):
        requirements = removeAllProxies(context.requirements)
        if requirements is not None:
            for requirement in requirements:
                res = my_catalog.searchResults(oid_index=requirement.objectID)
                if len(res) > 0:
                    startReq = iter(res).next()
                    allObjReqs = []
                    allTmpObjReqs = getRequirementList(startReq)
                    for req in allTmpObjReqs:
                        if req.validAsFirst and len(req) > 0:
                            pass
                        else:
                            allObjReqs.append(req)
                    allObjEvaluations = getEvaluationsDone(context)
                    alreadyCheckedReqs = [ev[0] for ev in allObjEvaluations.items()]
                    #retList.extend(set(allObjReqs).difference(alreadyCheckedReqs))
                    retSet = retSet.union(set(allObjReqs).difference(alreadyCheckedReqs))
    #        return retList
    retList = list(retSet)
    retList.sort()
    return retList

# Convention to make adapter introspectable
getEvaluationsDone.factory = Evaluations
