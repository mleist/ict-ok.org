# -*- coding: utf-8 -*-
#
# Copyright (c) 2007, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0213,W0232,W0622
#
"""Interface of compliance utility

the compliance utility should store the compliance/requirement-templates
for the host- or service-instances
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Bytes, Datetime, Bool, TextLine, List, Choice

# ict_ok.org imports
from org.ict_ok.schema.date import Date
from schooltool.requirement import interfaces as ischooltool

_ = MessageFactory('org.ict_ok')


class IAdmUtilCompliance(Interface):
    """Compliance Utiltiy
    """
    def generateAllPdf(absFilename, authorStr, versionStr):
        """
        will generate a complete pdf report
        """
    def append(subObj):
        """ append Requirement
        """
    def match_requirements():
        """ match all Components with Categories on all Requirements with
        same Categories
        """
    def delete_requirements():
        """ delete all Categories from Components
        """

#class IRequirement(ischooltool.IRequirement):
class IRequirement(Interface):
    """ ict-ok.org wrapper
    """
    validAsFirst = Bool(
        title = _("Valid as first"),
        description = _("Requirement can be the first requirement with "
                        "more sub-requirement"),
        default = False,
        required = False)

    resubmitDate = Datetime(
        title = _(u'resubmit date'),
        description = _(u'resubmit the workitem on date'),
        required = False)
    
    version = TextLine(
        max_length = 80,
        title = _("Instance version"),
        description = _("Version of the instance."),
        default=u'',
        required = False)
    
    categories = List(
        title = _(u'Categories'),
        #value_type=Choice(vocabulary='AllUnusedOrUsedComponentContracts'),
        value_type=Choice(vocabulary='AllCategories'),
        default=[],
        required = False)



class IHaveRequirement(ischooltool.IHaveRequirement):
    """ ict-ok.org wrapper
    """

class IScoreSystem(ischooltool.IScoreSystem):
    """ ict-ok.org wrapper
    """

class IValuesScoreSystem(ischooltool.IValuesScoreSystem):
    """ ict-ok.org wrapper
    """

class IDiscreteValuesScoreSystem(ischooltool.IDiscreteValuesScoreSystem):
    """ ict-ok.org wrapper
    """

class IRangedValuesScoreSystem(ischooltool.IRangedValuesScoreSystem):
    """ ict-ok.org wrapper
    """

class IHaveEvaluations(ischooltool.IHaveEvaluations):
    """ ict-ok.org wrapper
    """

class IEvaluation(ischooltool.IEvaluation):
    """ ict-ok.org wrapper
    """

class IEvaluations(ischooltool.IEvaluations):
    """ ict-ok.org wrapper
    """

class IEvaluationsQuery(ischooltool.IEvaluationsQuery):
    """ ict-ok.org wrapper
    """

class IImportXmlData(Interface):
    """Interface for all Objects"""
    alldata = Bytes(
        title = _("Data file"),
        required = True)
