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
from lxml import etree

# zope imports
from zope.app import zapi
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope import annotation
import zope.app.container.contained
from zope.component import getUtility
from zope.app.catalog.interfaces import ICatalog
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.component.interfaces import ComponentLookupError

# zc imports

# lovely imports
from lovely.relation.property import RelationPropertyIn

# ict_ok.org imports
from org.ict_ok.components.superclass.superclass import Superclass
from org.ict_ok.admin_utils.compliance.interfaces import \
     IRequirement, IAdmUtilCompliance
import schooltool.requirement.requirement
from schooltool.requirement.evaluation import getRequirementList
from schooltool.requirement.scoresystem import \
     GlobalDiscreteValuesScoreSystem, Decimal
from org.ict_ok.admin_utils.categories.rel_managers import \
    Categories_Requirements_RelManager

logger = logging.getLogger("AdmUtilCompliance")

REQUIREMENT_KEY = "org.ict_ok.admin_utils.compliance.requirement"

# TODO: ml nur geparkt
#def getSecondLevelRequirements(self):
#    """ the requirements list in second level
#    """
#    return []

def buildRequirementVocab(inRequirement, inTitlePath=u"",
                          inOidPath=u"", terms=[]):
    newTitlePath = u"%s/%s" % (inTitlePath, inRequirement.ikName)
    newOidPath = u"%s/%s" % (inOidPath, inRequirement.objectID)
    terms.append(SimpleTerm(newOidPath,
                            str(newOidPath),
                            newTitlePath))
    for (oid, oreq) in inRequirement.items():
        buildRequirementVocab(oreq, newTitlePath, newOidPath, terms)

def allRequirementHierVocab(dummy_context):
    """Which locations are there
    """
    terms = []
    try:
        complianceUtil = getUtility(IAdmUtilCompliance,
                                    name='AdmUtilCompliance')
        for (oid, oobj) in complianceUtil.items():
            buildRequirementVocab(oobj, terms=terms)
            #reqList = getRequirementList(oobj)
            #for req in reqList:
                #if IRequirement.providedBy(req):
                    #(titlePath, oidPath) = buildRequirementPath(req)
                    #print "(titlePath, oidPath): ", (titlePath, oidPath)
                    #terms.append(\
                        #SimpleTerm(oidPath,
                                   #str(oidPath),
                                   #titlePath))
                
                #buildingObj = oobj.object.__parent__
                #if IBuilding.providedBy(buildingObj):
                    #locationObj = buildingObj.__parent__
                    #if ILocation.providedBy(locationObj):
                        #myString = u"%s / %s / %s" % (locationObj.getDcTitle(),
                                              #buildingObj.getDcTitle(),
                                              #oobj.object.getDcTitle())
                        #terms.append(\
                            #SimpleTerm(oobj.object.objectID,
                                       #str(oobj.object.objectID),
                                       #myString))
        return SimpleVocabulary(terms)
    except ComponentLookupError:
        return SimpleVocabulary([])
    
def allRequirementVocab(dummy_context, getFirsts=True, getNotFirsts=True):
    """Which locations are there
    """
    terms = []
    my_catalog = zapi.getUtility(ICatalog)
    try:
        reqOidList = []
        complianceUtil = getUtility(IAdmUtilCompliance,
                                    name='AdmUtilCompliance')
        for (oid, oobj) in complianceUtil.items():
            for req in getRequirementList(oobj):
                reqOidList.append(req.objectID)
        reqOidSet = set(reqOidList)
        for reqOid in reqOidSet:
            resultList = my_catalog.searchResults(oid_index=reqOid)
            if len(resultList) > 0:
                req = iter(resultList).next()
                if IRequirement.providedBy(req):
                    parentReq = req.getParent()
                    if parentReq is not None and \
                       IRequirement.providedBy(parentReq):
                        newString = u"%s (%s)" % \
                                  (req.ikName, parentReq.ikName)
                    else:
                        newString = req.ikName
                    appendIt = False
                    if getFirsts and req.validAsFirst:
                        appendIt = True
                    if getNotFirsts and not req.validAsFirst:
                        appendIt = True
                    if appendIt:
                        terms.append( SimpleTerm(req,
                                                 token=getattr(req, 'objectID',
                                                               req.objectID),
                                                 title=newString))
        return SimpleVocabulary(terms)
    except ComponentLookupError:
        return SimpleVocabulary([])

def allValid1stRequirementVocab(dummy_context):
    """Which locations are there
    """
    return allRequirementVocab(dummy_context, True, False)

def allNotValid1stRequirementVocab(dummy_context):
    """Which locations are there
    """
    return allRequirementVocab(dummy_context, False, True)

class Requirement(Superclass,
                  schooltool.requirement.requirement.Requirement):
    """ ict-ok.org wrapper
    """
    implements(IRequirement)
    validAsFirst = FieldProperty(IRequirement['validAsFirst'])
    resubmitDate = FieldProperty(IRequirement['resubmitDate'])
    version = FieldProperty(IRequirement['version'])
    categories = RelationPropertyIn(Categories_Requirements_RelManager)

    def __init__(self, title, **data):
        schooltool.requirement.requirement.Requirement.__init__(self, title)
        Superclass.__init__(self, ikName=title, **data)
        Superclass.__post_init__(self, **data)
        refAttributeNames = ['categories']
        for (name, value) in data.items():
            if name in IRequirement.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        self.ikRevision = __version__

    def store_refs(self, **data):
        refAttributeNames = ['categories']
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)

    def append(self, subObj):
        if hasattr(subObj, 'objectID'):
            self[subObj.objectID] = subObj
        else:
            self[subObj.ikName] = subObj

    def getIndex(self):
        indexList = []
        current = self
        parent = current.getParent()
        while IRequirement.providedBy(parent):
            # prepend to list
            indexList.insert(0, parent.values().index(current)+1)
            current = parent
            parent = current.getParent()
        return indexList
    
    def getIndexString(self):
        try:
            index = self.getIndex()
            return '.'.join(['%d' % i for i in index])
        except TypeError:
            return "-deleted-"
    
    def asXml(self):
        #print u"Pre:", self.title
        #import pdb
        #pdb.set_trace()
        for subReq in self.values():
            subReq.asXml()
        #print u"Post:", self.title

    def asETree(self):
        reqObj = etree.Element("Req")
        titleObj = etree.Element("Title")
        titleObj.text = self.title
        reqObj.append(titleObj)
        for subReq in self.values():
            reqObj.append( subReq.asETree())
        return reqObj


def getRequirement(context):
    """Adapt an ``IHaveRequirement`` object to ``IRequirement``."""
    annotations = annotation.interfaces.IAnnotations(context)
    try:
        return annotations[REQUIREMENT_KEY]
    except KeyError:
        ## TODO: support generic objects without ikName
        requirement = Requirement(getattr(context, "ikName", None))
        annotations[REQUIREMENT_KEY] = requirement
        zope.app.container.contained.contained(
            requirement, context, u'++requirement++')
        return requirement
# Convention to make adapter introspectable
getRequirement.factory = Requirement

PassFail = GlobalDiscreteValuesScoreSystem(
    'PassFail',
    u'Pass/Fail', u'Pass or Fail score system.',
    [(u'Pass', Decimal(1)), (u'Fail', Decimal(0))], u'Pass', u'Pass')
