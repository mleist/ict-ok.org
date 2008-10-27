# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0232,W0142
#
"""implementation of browser class of Host object
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.app import zapi
from zope.i18nmessageid import MessageFactory
from zope.app.catalog.interfaces import ICatalog
from zope.app.security.interfaces import IAuthentication
from zope.component import queryUtility

# z3c imports

# schooltool
from schooltool.requirement.interfaces import IScoreSystem

# ict_ok.org imports
from org.ict_ok.components.superclass.browser.superclass import \
     Overview, getModifiedDate, \
     link, raw_cell_formatter, GetterColumn
from org.ict_ok.components.supernode.browser.supernode import SupernodeDetails
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.admin_utils.compliance.evaluation import \
     getEvaluations, Evaluation
from org.ict_ok.admin_utils.compliance.browser.requirement import \
     getTitle as getReqTitle
from org.ict_ok.admin_utils.compliance.browser.requirement import \
     link as linkReq
from org.ict_ok.admin_utils.compliance.requirement import getRequirementList
from org.ict_ok.admin_utils.compliance.browser.requirement import \
     getRequirementBottons
from org.ict_ok.admin_utils.compliance.browser.evaluation import \
     getEvaluationRequirementTitle, \
     evaluationValue_formatter, \
     getEvaluationBottons, getEvalModifiedDate, \
     getEvaluatorTitle, getEvaluationValue

_ = MessageFactory('org.ict_ok')

# --------------- menu entries -----------------------------


class MSubAddHost(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Host')
    viewURL = 'add_hosts.html'
    weight = 50

class MSubEvaluationsTodo(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Evaluations to do')
    viewURL = 'evaluations_todo.html'
    weight = 100

class MSubEvaluationsDone(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Evaluations done')
    viewURL = 'evaluations_done.html'
    weight = 100

# --------------- object details ---------------------------


class ComponentDetails(SupernodeDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = SupernodeDetails.omit_viewfields + []
    omit_addfields = SupernodeDetails.omit_addfields + []
    omit_editfields = SupernodeDetails.omit_editfields + []
    
    def change_eval_yes(self):
        """ trigger an evaluation process
        """
        requirementId = self.request.get('req_id', default=None)
        evaluations = getEvaluations(self.context)
        if requirementId is not None \
           and evaluations is not None:
            my_catalog = zapi.getUtility(ICatalog)
            res = my_catalog.searchResults(oid_index=requirementId)
            if len(res) > 0:
                requirementObj = iter(res).next()
                principalId = self.request.principal.id.split('.')[1]
                pau_utility = queryUtility(IAuthentication)
                internalPrincipal = pau_utility['principals'][principalId]
                pfSystem = queryUtility(IScoreSystem, name="Comp_Pass/Fail")
                inpVal = 'Pass'
                evaluation = Evaluation(requirementObj, pfSystem,
                                        inpVal, internalPrincipal)
                evaluations.addEvaluation(evaluation)
        nextURL = self.request.get('nextURL', default=None)
        if nextURL is not None:
            return self.request.response.redirect(nextURL)
        else:
            return self.request.response.redirect('./@@details.html')

    def change_eval_no(self):
        """ trigger an evaluation process
        """
        requirementId = self.request.get('req_id', default=None)
        evaluations = getEvaluations(self.context)
        if requirementId is not None \
           and evaluations is not None:
            my_catalog = zapi.getUtility(ICatalog)
            res = my_catalog.searchResults(oid_index=requirementId)
            if len(res) > 0:
                requirementObj = iter(res).next()
                principalId = self.request.principal.id.split('.')[1]
                pau_utility = queryUtility(IAuthentication)
                internalPrincipal = pau_utility['principals'][principalId]
                pfSystem = queryUtility(IScoreSystem, name="Comp_Pass/Fail")
                inpVal = 'Fail'
                evaluation = Evaluation(requirementObj, pfSystem,
                                        inpVal, internalPrincipal)
                evaluations.addEvaluation(evaluation)
        nextURL = self.request.get('nextURL', default=None)
        if nextURL is not None:
            return self.request.response.redirect(nextURL)
        else:
            return self.request.response.redirect('./@@details.html')

class EvaluationsTodoDisplay(Overview):
    """for evaluation which are open
    """
    label = _(u'evaluations to do')
    columns = (
        GetterColumn(title=_('Title'),
                     getter=getReqTitle,
                     cell_formatter=linkReq('overview.html')),
        GetterColumn(title=_('Modified On'),
                     getter=getModifiedDate,
                     subsort=True,
                     cell_formatter=raw_cell_formatter),
        #GetterColumn(title=_('Size'),
                     #getter=getSize,
                     #cell_formatter=raw_cell_formatter),
        GetterColumn(title=_('Actions'),
                     getter=getRequirementBottons,
                     cell_formatter=raw_cell_formatter),
        )
    sort_columns = []
    status = None
    
    def objs(self):
        """List of Content objects"""
        retList = []
        my_catalog = zapi.getUtility(ICatalog)
        if self.context.requirement is not None:
            res = my_catalog.searchResults(oid_index=self.context.requirement)
            if len(res) > 0:
                startReq = iter(res).next()
                allObjReqs = getRequirementList(startReq)
                allObjEvaluations = getEvaluations(self.context)
                alreadyCheckedReqs = [ev[0] for ev in allObjEvaluations.items()]
                retList.extend(set(allObjReqs).difference(alreadyCheckedReqs))
        return retList


class EvaluationsDoneDisplay(Overview):
    """for already done evaluations
    """
    label = _(u'evaluations done')
    columns = (
        GetterColumn(title=_('Requirement'),
                     getter=getEvaluationRequirementTitle,
                     cell_formatter=link('overview.html')),
        GetterColumn(title=_('Evaluator'),
                     getter=getEvaluatorTitle,
                     cell_formatter=link('overview.html')),
        GetterColumn(title=_('Value'),
                     getter=getEvaluationValue,
                     cell_formatter=evaluationValue_formatter),
        GetterColumn(title=_('Modified On'),
                     getter=getEvalModifiedDate,
                     subsort=True,
                     cell_formatter=raw_cell_formatter),
        GetterColumn(title=_('Actions'),
                     getter=getEvaluationBottons,
                     cell_formatter=raw_cell_formatter),
        )
    sort_columns = []
    status = None
    
    def objs(self):
        """List of Content objects"""
        retList = getEvaluations(self.context)
        return [ev[1] for ev in retList.items()]
