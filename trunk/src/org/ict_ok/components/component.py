# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0612,W0142
#
"""superclass for all content-objects
"""

__version__ = "$Id$"

# python imports
import os
from datetime import datetime
import tempfile
from pyExcelerator import Workbook, XFStyle, Font, Formula
import pyExcelerator as xl

# zope imports
from zope.traversing.browser import absoluteURL
from zope.interface import implements, implementedBy
from zope.component import getUtility
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IField, IChoice
from zope.component import queryMultiAdapter, getMultiAdapter
from zope.app.folder import Folder

# z3c imports
from z3c.form import button, field, form, interfaces
from z3c.formui import layout
from z3c.form import datamanager
from z3c.form.browser import checkbox

# lovely imports
from lovely.relation.property import RelationPropertyIn
from lovely.relation.property import RelationPropertyOut

# ict_ok.org imports
from org.ict_ok.admin_utils.supervisor.interfaces import IAdmUtilSupervisor
from org.ict_ok.components.superclass.superclass import Superclass
from org.ict_ok.libs.interfaces import IDocumentAddable
from org.ict_ok.libs.history.entry import Entry
from org.ict_ok.libs.lib import fieldsForFactory
from org.ict_ok.components.superclass.interfaces import ISuperclass
from org.ict_ok.components.interfaces import IComponent, IComponentFolder
from org.ict_ok.components.supernode.supernode import Supernode
from org.ict_ok.admin_utils.compliance.evaluation import \
     getEvaluationsDone, getEvaluationsTodo
from org.ict_ok.components.interfaces import IImportXlsData
from org.ict_ok.components.superclass.superclass import objectsWithInterface
from org.ict_ok.admin_utils.categories.rel_managers import \
    Categories_Components_RelManager
from org.ict_ok.components.contract.rel_managers import \
    Contracts_Component_RelManager

from plone.memoize import instance
from plone.memoize import forever


#@instance.memoize
def AllComponentTemplates(dummy_context, interface):
    """Which MobilePhone templates exists
    """
#    print "AllComponentTemplates() ->", interface
    terms = []
    for object in objectsWithInterface(interface):
        if object.isTemplate:
            myString = u"%s [T]" % (object.getDcTitle())
            terms.append(SimpleTerm(object,
                                    token=getattr(object, 'objectID',
                                                  object.objectID),
                                    title=myString))
    terms.sort(lambda l, r: cmp(l.title.lower(), r.title.lower()))
    return SimpleVocabulary(terms)


#@instance.memoize
def AllComponents(dummy_context, interface=IComponent,
                  includeSelf=True, *additionalAttrNames):
    """In which production state a host may be
    """
#    print "AllComponents(%s, %s, %s, %s) ->" % (dummy_context, interface,
#                                                additionalAttrNames,
#                                                includeSelf)
    terms = []
    for object in objectsWithInterface(interface):
        myString = u"%s" % (object.ikName)
        for additionalAttrName in additionalAttrNames:
            additionalAttribute = getattr(object, additionalAttrName, None)
            if additionalAttribute is not None:
                if hasattr(additionalAttribute, 'ikName'):
                    if len(additionalAttribute.ikName) > 70:
                        dotted = u'...)'
                    else:
                        dotted = u')'
                    myString = myString + u" (%s" % \
                        additionalAttribute.ikName[:70] + dotted
                else:
                    if len(additionalAttribute) > 70:
                        dotted = u'...)'
                    else:
                        dotted = u')'
                    myString = myString + u" (%s" % \
                        additionalAttribute[:70] + dotted
        if object == dummy_context:
            if includeSelf:
                terms.append(\
                    SimpleTerm(object,
                               token=getattr(object, 'objectID', object.objectID),
                               title=myString))
        else:
            terms.append(\
                SimpleTerm(object,
                           token=getattr(object, 'objectID', object.objectID),
                           title=myString))
    terms.sort(lambda l, r: cmp(l.title.lower(), r.title.lower()))
    return SimpleVocabulary(terms)


#def All_y_UnusedOrSelfComponents(dummy_context, interface,
#                              obj_attr_name, *additionalAttrNames):
#    import cProfile
#    from datetime import datetime
#    print "----------------------------------1"
#    pr = cProfile.Profile()
#    print "----------------------------------2"
#    tmpRet = pr.runcall(All_x_UnusedOrSelfComponents,
#                        dummy_context, interface,
#                        obj_attr_name, *additionalAttrNames)
#    filename = datetime.now().strftime('/tmp/ict_3_%Y%m%d%H%M%S.profile')
#    pr.dump_stats(filename)
#    print "----------------------------------3"
#    return tmpRet


def AllUnusedOrSelfComponents(dummy_context, interface,
                              obj_attr_name, *additionalAttrNames):
    """In which production state a host may be
    """
    terms = []
    for object in objectsWithInterface(interface):
        obj_attr = getattr(object, obj_attr_name, None)
        if obj_attr is None or \
            len(obj_attr) == 0:
            myString = object.ikName
            for additionalAttrName in additionalAttrNames:
                additionalAttribute = getattr(object, additionalAttrName, None)
                if additionalAttribute is not None:
                    if hasattr(additionalAttribute, 'ikName'):
                        if len(additionalAttribute.ikName) > 70:
                            dotted = u'...)'
                        else:
                            dotted = u')'
                        myString = myString + u" (%s" % \
                            additionalAttribute.ikName[:70] + dotted
                    else:
                        if len(additionalAttribute) > 70:
                            dotted = u'...)'
                        else:
                            dotted = u')'
                        myString = myString + u" (%s" % \
                            additionalAttribute[:70] + dotted
            terms.append(\
                SimpleTerm(object,
                           token=getattr(object, 'objectID', object.objectID),
                           title=myString))
        else:
            if obj_attr == dummy_context or \
                dummy_context in obj_attr:
                myString = u"%s" % (object.ikName)
                for additionalAttrName in additionalAttrNames:
                    additionalAttribute = getattr(object, additionalAttrName, None)
                    if additionalAttribute is not None:
                        if hasattr(additionalAttribute, 'ikName'):
                            if len(additionalAttribute.ikName) > 70:
                                dotted = u'...)'
                            else:
                                dotted = u')'
                            myString = myString + u" (%s" % \
                                additionalAttribute.ikName[:70] + dotted
                        else:
                            if len(additionalAttribute) > 70:
                                dotted = u'...)'
                            else:
                                dotted = u')'
                            myString = myString + u" (%s" % \
                                additionalAttribute[:70] + dotted
                terms.append(\
                    SimpleTerm(object,
                               token=getattr(object, 'objectID', object.objectID),
                               title=myString))
    terms.sort(lambda l, r: cmp(l.title.lower(), r.title.lower()))
    return SimpleVocabulary(terms)


#@instance.memoize
def ComponentsFromObjList(dummy_context, obj_list, additionalAttrNames=None):
    """In which production state a host may be
    """
#    print "ComponentsFromObjList()"
    terms = []
    for i_obj in obj_list:
        myString = u"%s" % (i_obj.ikName)
        for additionalAttrName in additionalAttrNames:
            additionalAttribute = getattr(object, additionalAttrName, None)
            if additionalAttribute is not None:
                if hasattr(additionalAttribute, 'ikName'):
                    if len(additionalAttribute.ikName) > 70:
                        dotted = u'...)'
                    else:
                        dotted = u')'
                    myString = myString + u" (%s" % \
                        additionalAttribute.ikName[:70] + dotted
                else:
                    if len(additionalAttribute) > 70:
                        dotted = u'...)'
                    else:
                        dotted = u')'
                    myString = myString + u" (%s" % \
                        additionalAttribute[:70] + dotted
        terms.append(\
            SimpleTerm(i_obj,
                       token=i_obj.objectID,
                       title=myString))
    terms.sort(lambda l, r: cmp(l.title.lower(), r.title.lower()))
    return SimpleVocabulary(terms)    


class Component(Supernode):
    """
    the general component instance
    """

    implements(IComponent, IDocumentAddable)
    containerIface = None
    isTemplate = FieldProperty(IComponent['isTemplate'])
#    requirement = FieldProperty(IComponent['requirement'])
    requirements = FieldProperty(IComponent['requirements'])
    categories = RelationPropertyIn(Categories_Components_RelManager)
    contracts = RelationPropertyIn(Contracts_Component_RelManager)

    fullTextSearchFields = []
    fullTextSearchFields.extend(Supernode.fullTextSearchFields)

    def __init__(self, **data):
        """
        constructor of the object
        """
        Supernode.__init__(self, **data)
        self.requirements = []
        refAttributeNames = getRefAttributeNames(Component)
        for (name, value) in data.items():
            if name in IComponent.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        self.ikRevision = __version__

    def store_refs(self, **data):
        refAttributeNames = self.getRefAttributeNames()
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)
    
    def getRefAttributeNames(self):
        return getRefAttributeNames(Component)

    def getEvaluationsTodo(self):
        """ returns: [Requirement(u'ReqA1'), Requirement(u'ReqA2')]
        """
        return getEvaluationsTodo(self)

    def getEvaluationsDone(self):
        """returns [<Evaluation for Requirement(u'ReqA1'), value='Fail'>),
        <Evaluation for Requirement(u'ReqA2'), value='Pass'>]
        """
        retList = []
        evaluations = getEvaluationsDone(self)
        for ev in evaluations.items():
            retList.append(ev[1])
        return retList

    def getFirstContainer(self):
        """
        """
        if self.containerIface is not None:
            return objectsWithInterface(self.containerIface).pop(0)
        else:
            return None

    def get_health(self):
        """
        output of health, 0-1 (float)
        !!!!!! has to be implemented by subclass !!!!!!
        """
        #raise Exception, 'Not implemented yet'
        return None
    
    def get_wcnt(self):
        """
        weighted count of accesses
        !!!!!! has to be implemented by subclass !!!!!!
        """
        #raise Exception, 'Not implemented yet'
        return None

    def _getAllExportData_Step0(self):
        """return a list of meta-attribute-dict
        [{'myFactory': 'bla bla',
          'objectID': '1234...',
         },
        ]
        """
        retDict = {}
        retDict['myFactory'] = self.myFactory
        retDict['shortName'] = self.shortName
        retDict['ikRevision'] = self.ikRevision
        historyDictList = []
#        import pdb
#        pdb.set_trace()
        for historyEvent in self.history.data:
            historyDictList.append(historyEvent.exportAsDict())
        retDict['events'] = historyDictList
        return retDict

    def _getAllExportData_Step1(self):
        """return a list of attribute-dict ict-objects _without_ all
        references by lovely.relation in form of
        [{'ikName': 'bla bla',
          'objectID': '1234...',
         },
        ]
        """
        retDict = {}
        metaDataDict = self._getAllExportData_Step0()
        retDict['meta'] = metaDataDict
#        import pdb
#        pdb.set_trace()
        valAttributeNames = getValAttributeNames(self)
        for (name, value) in self.__dict__.items():
            if name in valAttributeNames:
                retDict[name] = value
        return [retDict]

    def _getAllExportData_Step2(self):
        """return a list of relation-tuples by lovely.relation
        in form of
        [ (('obj1Id'. 'obj1AttrName'), ('obj2Id'. 'obj2AttrName')),
        ]
        """
        retList = []
        refAttributeNames = self.getRefAttributeNames()
        for attr_name in refAttributeNames:
            if hasattr(self, attr_name):
                objList = getattr(self, attr_name)
                if type(objList) != type([]):
                    objList = [objList]
                for obj in objList:
                    if IComponent.providedBy(obj):
                        rel_manager = getattr(self.__class__, attr_name)._manager
                        retList.append(
                            ((self.objectID, attr_name), (obj.objectID, rel_manager.relType))
                        )
        return retList

    def getAllExportData(self, dataStructure):
        """returns a python data structure
        """
        #if self.len() > 0:
        #    for obj in self:
        #        if hasattr(obj, 'getAllExportData'):
        #            obj.getAllExportData(dataStructure)
        objDataList = self._getAllExportData_Step1()
        connDataList = self._getAllExportData_Step2()
        for newConntuple in connDataList:
            for oldConntuple in dataStructure['conns']:
                oldConnObjId = oldConntuple[1][0]
                oldConnRelMan = oldConntuple[1][1]
                newConnObjId = newConntuple[0][0]
                newConnRelMan = newConntuple[1][1]
                #import pdb
                #pdb.set_trace()
                if oldConnObjId == newConnObjId and \
                   oldConnRelMan == newConnRelMan:
                    print "DRIN: ", newConntuple[0]
                    tmplist = list(oldConntuple)
                    tmplist[1] = newConntuple[0]
                    oldConntuple = tuple(tmplist)
                    print "eee: ", oldConntuple
#        print "ddd: ", self.ikName
        dataStructure['objects'].extend(objDataList)
        dataStructure['conns'].extend(connDataList)
#        print "1:", dataStructure['objects']
#        print "2:", dataStructure['conns']

    def _importAllData_Step0(self, metaData):
        """imports a list of meta-attribute-dict
        """
        print "############ meta :"
        if metaData.has_key('ikRevision'):
            self.ikRevision = metaData['ikRevision']
        if metaData.has_key('events'):
            for eventEntry in metaData['events']:
                print "Event-Entry: ", eventEntry
                newEntry = Entry(eventEntry, self)
                self.history.append(newEntry)
        try:
            #ISlave['objectID'].readonly = False
            for attrName, attrVal in metaData.items():
                print "attr:  %s = %s" % (attrName, attrVal)
                #newObj.__setattr__(i, msgObj['listAttr'][i])
        finally:
            pass
            #ISlave['objectID'].readonly = True
        pass
        
    def _importAllData_Step1(self, objData):
        """return a list of attribute-dict ict-objects _without_ all
        references by lovely.relation in form of
        """
        print "############ obj :"
        try:
            ISuperclass['objectID'].readonly = False
            #valAttributeNames = getValAttributeNames(self)
            for attrName, attrVal in objData.items():
                #if attrName in valAttributeNames:
                print "attr:  %s = %s  (SET)" % (attrName, attrVal)
                self.__setattr__(attrName, attrVal)
                #else:
                #    print "attr:  %s = %s  (NOSET)" % (attrName, attrVal)
        finally:
            ISuperclass['objectID'].readonly = True

    def _importAllData_Step2(self):
        """return a list of relation-tuples by lovely.relation
        in form of
        [ (('obj1Id'. 'obj1AttrName'), ('obj2Id'. 'obj2AttrName')),
        ]
        """
        

    def importAllData(self, argData):
        objData = argData
        metaData = objData.pop('meta')
        self._importAllData_Step0(metaData)
        self._importAllData_Step1(objData)


class ComponentFolder(Superclass, Folder):
    implements(IComponentFolder, 
               IImportXlsData)
    def __init__(self, **data):
        """
        constructor of the object
        """
        Superclass.__init__(self, **data)
        Folder.__init__(self)

    def exportXlsData(self, request, sheetName=u'ict', wbook=None):
        """get XLS file for all folder objects"""
        if wbook is None:
            localWbook = True
            filename = datetime.now().strftime('ict_%Y%m%d%H%M%S.xls')
            f_handle, f_name = tempfile.mkstemp(filename)
            wbook = Workbook()
        else:
            localWbook = False
        wb_hosts = wbook.add_sheet(getattr(self, 'ikName', sheetName))
        style0 = XFStyle()
        font0 = Font()
        font0.height = 6*20
        #style0.num_format_str = '@'
        style0.font = font0
        style1 = XFStyle()
        font1 = Font()
        font1.height = 6*20
        #style1.num_format_str = '@'
        style1.font = font1
        heading_pattern = xl.Pattern()
        heading_pattern.pattern = xl.Pattern.SOLID_PATTERN
        heading_pattern.pattern_back_colour = 0x5
        heading_pattern.pattern_fore_colour = 0x5   
        fields = fieldsForFactory(self.contentFactory, ['objectID'])
        attrList = [ fname for fname, fval in fields.items()]
        itemList = self.items()
        pos_y = 0
        pos_x = 0
        for attr in attrList:
            style0.pattern = heading_pattern 
            wb_hosts.write(pos_y, pos_x, attr, style0)
            pos_x += 1
        # objectID
        wb_hosts.write(pos_y, pos_x, "objectID", style0)
        wb_hosts.col(pos_x).width *= 3
        pos_x += 1
        pos_y = 1
        #
        allAttributes = {}
        for interface in implementedBy(self.contentFactory):
            for i_attrName in interface:
                i_attr = interface[i_attrName]
                if IField.providedBy(i_attr):
                    allAttributes[i_attrName] = i_attr
        #
        for item_n, item_v in itemList:
            pos_x = 0
            for attr in attrList:
                attrField = allAttributes[attr]
                attrDm = datamanager.AttributeField(item_v, attrField)
                v_style = XFStyle()
                v_font = Font()
                v_font.height = 6*20
                v_style.font = v_font
                value = None
                if IChoice.providedBy(attrField):
                    v_style.num_format_str = '@'
#                    try:
                    dateValue = attrDm.get()
                    v_widget = getMultiAdapter(\
                                    (attrField,request),
                                    interfaces.IFieldWidget)
                    v_widget.context = item_v
                    v_dataconverter = queryMultiAdapter(\
                                    (attrDm.field, v_widget),
                                    interfaces.IDataConverter)
#                    except AttributeError, errText:
#                        print "Error2:  ### ", errText
#                        print "item_v: ", item_v
#                        print "item_v.ikName: ", item_v.ikName
#                        print "attr: ", attr
#                        dateValue = None
#                        #import pdb
#                        #pdb.set_trace()
                    if dateValue is not None:
#                        try:
                        valueVector = v_dataconverter.toWidgetValue(dateValue)
                        if len(valueVector) > 0:
                            value = valueVector[0]
#                        except IndexError, errText:
#                            print "Error3:  ### ", errText
#                            print "item_v: ", item_v
#                            print "item_v.ikName: ", item_v.ikName
#                            print "attr: ", attr
                else:
                    v_style.num_format_str = '@'
                    try:
#                        import pdb
#                        pdb.set_trace()
                        dateValue = attrDm.get()
                        v_widget = getMultiAdapter(\
                                        (attrField,request),
                                        interfaces.IFieldWidget)
                        v_widget.context = item_v
                        v_dataconverter = queryMultiAdapter(\
                                        (attrDm.field, v_widget),
                                        interfaces.IDataConverter)
                    except AttributeError, errText:
                        print "Error1:  ### ", errText
                        print "item_v: ", item_v
                        print "item_v.ikName: ", item_v.ikName
                        print "attr: ", attr
                        dateValue = None
                    if dateValue is not None:
                        try:
                            value = v_dataconverter.toWidgetValue(dateValue)
                        except AttributeError, errText:
                            print "Error4:  ### ", errText
                            print "item_v: ", item_v
                            print "item_v.ikName: ", item_v.ikName
                            print "attr: ", attr
                            value = None
                    if type(value) is list:
                        value = u";".join(value)
                if value is not None:
                    wb_hosts.write(pos_y, pos_x, value, v_style)
                pos_x += 1
            # objectID
            wb_hosts.write(pos_y, pos_x, item_v.objectID, style0)
            pos_x += 1
            pos_y += 1
        if localWbook is True:
            wbook.save(f_name)
            datafile = open(f_name, "r")
            dataMem = datafile.read()
            datafile.close()
            os.remove(f_name)
            return (filename, dataMem)

    def importXlsData(self, request, f_name, codepage):
        """set data from XLS file on new or modified folder objects"""
        supervisorUtil = getUtility(IAdmUtilSupervisor,
                                    name='AdmUtilSupervisor')
        supervisorUtil.importAllXlsData(request, f_name, codepage)


        
#    def importXlsData(self, request, f_name, codepage):
#        """set data from XLS file on new or modified folder objects"""
#        #import pdb
#        #pdb.set_trace()
#        fields = fieldsForFactory(self.contentFactory, ['objectID'])
#        parseRet = xl.parse_xls(f_name, codepage)
#        from pprint import pprint
#        pprint(parseRet)
#        #
#        allAttributes = {}
#        for interface in implementedBy(self.contentFactory):
#            for i_attrName in interface:
#                i_attr = interface[i_attrName]
#                if IField.providedBy(i_attr):
#                    allAttributes[i_attrName] = i_attr
#        #
#        for sheet_name, values in parseRet:
#            matrix = [[]]
#            for row_idx, col_idx in sorted(values.keys()):
#                v = values[(row_idx, col_idx)]
#                if isinstance(v, unicode):
#                    v = u"%s" % v # v.encode(codepage, 'backslashreplace')
#                else:
#                    v = `v`
#                v = u'%s' % v.strip()
#                last_row, last_col = len(matrix), len(matrix[-1])
#                while last_row <= row_idx:
#                    matrix.extend([[]])
#                    last_row = len(matrix)
#                while last_col < col_idx:
#                    matrix[-1].extend([''])
#                    last_col = len(matrix[-1])
#                matrix[-1].extend([v])
#            attrNameList = matrix[0]
#            attrValMatrix = matrix[1:]
#            for attrValVector in attrValMatrix:
#                attrDict = {}
#                for attrIndex, attrVal in enumerate(attrValVector):
#                    attrDict[attrNameList[attrIndex]] = attrVal
#                # ---------------------------------------
##                    if attrDict.has_key('IntID'):
##                        attrDict.pop('IntID')
#                if attrDict.has_key('objectID') and \
#                   attrDict['objectID'] in self:
#                    attrObjectID = attrDict.pop('objectID')
#                    oldObj = self.context[attrObjectID]
#                    for attrName, newValString in attrDict.items():
#                        #print u"ddd4-> %s" % (attrName)
#                        attrField = allAttributes[attrName]
#                        #print u"type(%s): %s" % (attrField, type(attrField))
##                            if attrName == "rooms":
#                        if IChoice.providedBy(attrField):
#                            v_widget = getMultiAdapter(\
#                                            (attrField,request),
#                                            interfaces.IFieldWidget)
#                            v_widget.context = oldObj
#                            v_dataconverter = queryMultiAdapter(\
#                                            (attrField, v_widget),
#                                            interfaces.IDataConverter)
#                            if len(newValString) > 0:
#                                newVal = v_dataconverter.toFieldValue([newValString])
#                            else:
#                                newVal = v_dataconverter.toFieldValue([])
#                        else:
#                            if attrName == "isTemplate":
#                                v_widget = checkbox.SingleCheckBoxFieldWidget(\
#                                            attrField,request)
#                            else:
#                                v_widget = getMultiAdapter(\
#                                                (attrField,request),
#                                                interfaces.IFieldWidget)
#                            v_widget.context = oldObj
#                            v_dataconverter = queryMultiAdapter(\
#                                            (attrField, v_widget),
#                                            interfaces.IDataConverter)
#                            if ICollection.providedBy(attrField):
#                                if len(newValString) > 0:
#                                    newVal = v_dataconverter.toFieldValue(newValString.split(';'))
#                                else:
#                                    newVal = v_dataconverter.toFieldValue([])
#                            else:
#                                newVal = v_dataconverter.toFieldValue(newValString)
#                        if getattr(oldObj, attrName) != newVal:
#                            setattr(oldObj, attrName, newVal)
#                            dcore = IWriteZopeDublinCore(oldObj)
#                            dcore.modified = datetime.utcnow()
#                            if attrName == "ikName":
#                                IBrwsOverview(oldObj).setTitle(newVal)
#                else:
#                    oldObj = None
#                    # new Object
##                        newObj = createObject(self.factoryId)
##                        newObj.__post_init__()
#                    dataVect = {}
#                    for attrName, newValString in attrDict.items():
#                        attrField = allAttributes[attrName]
#                        if IChoice.providedBy(attrField):
#                            v_widget = getMultiAdapter(\
#                                            (attrField,request),
#                                            interfaces.IFieldWidget)
#                            v_dataconverter = queryMultiAdapter(\
#                                            (attrField, v_widget),
#                                            interfaces.IDataConverter)
#                            if len(newValString) > 0:
#                                try:
#                                    newVal = v_dataconverter.toFieldValue([newValString])
#                                except LookupError:
#                                    newVal = v_dataconverter.toFieldValue([])
#                            else:
#                                newVal = v_dataconverter.toFieldValue([])
#                        else:
#                            if attrName == "isTemplate":
#                                v_widget = checkbox.SingleCheckBoxFieldWidget(\
#                                            attrField,request)
#                            else:
#                                v_widget = getMultiAdapter(\
#                                                (attrField,request),
#                                                interfaces.IFieldWidget)
#                            v_dataconverter = queryMultiAdapter(\
#                                            (attrField, v_widget),
#                                            interfaces.IDataConverter)
#                            if ICollection.providedBy(attrField):
#                                if len(newValString) > 0:
#                                    newVal = v_dataconverter.toFieldValue(newValString.split(';'))
#                                else:
#                                    newVal = v_dataconverter.toFieldValue([])
#                            else:
#                                newVal = v_dataconverter.toFieldValue(newValString)
#                        dataVect[str(attrName)] = newVal
#                        #setattr(newObj, attrName, newVal)
#                    #self.context.__setitem__(newObj.objectID, newObj)
#                    #print "dataVect: ", dataVect
#                    newObj = self.contentFactory(**dataVect)
#                    # new Object, but already have an object id
#                    if attrDict.has_key('objectID'):
#                        newObj.setObjectId(attrDict['objectID'])
#                    newObj.__post_init__()
#                    if oldObj is not None:
#                        dcore = IWriteZopeDublinCore(oldObj)
#                        dcore.modified = datetime.utcnow()
#                    IBrwsOverview(newObj).setTitle(dataVect['ikName'])
#                    self[newObj.objectID] = newObj
#                    if hasattr(newObj, "store_refs"):
#                        newObj.store_refs(**dataVect)
#                    notify(ObjectCreatedEvent(newObj))

    def renderAddObjectButton(self, request):
        """ render html code for a generic add button
        """
        if hasattr(self.contentFactory, 'shortName'):
            view_url = absoluteURL(self, request)\
                        + '/@@add_%s.html' % self.contentFactory.shortName
            return u'<a href="%s">Add %s</a>' % (view_url,
                                                 self.contentFactory.shortName)
        else:
            return u''



def AllXlsCodepages(dummy_context):
    """Which MobilePhone are there
    """
    terms = []
    encodings = {
        0x016F: 'ascii',     #ASCII
        0x01B5: 'cp437',     #IBM PC CP-437 (US)
        0x02D0: 'cp720',     #IBM PC CP-720 (OEM Arabic)
        0x02E1: 'cp737',     #IBM PC CP-737 (Greek)
        0x0307: 'cp775',     #IBM PC CP-775 (Baltic)
        0x0352: 'cp850',     #IBM PC CP-850 (Latin I)
        0x0354: 'cp852',     #IBM PC CP-852 (Latin II (Central European))
        0x0357: 'cp855',     #IBM PC CP-855 (Cyrillic)
        0x0359: 'cp857',     #IBM PC CP-857 (Turkish)
        0x035A: 'cp858',     #IBM PC CP-858 (Multilingual Latin I with Euro)
        0x035C: 'cp860',     #IBM PC CP-860 (Portuguese)
        0x035D: 'cp861',     #IBM PC CP-861 (Icelandic)
        0x035E: 'cp862',     #IBM PC CP-862 (Hebrew)
        0x035F: 'cp863',     #IBM PC CP-863 (Canadian (French))
        0x0360: 'cp864',     #IBM PC CP-864 (Arabic)
        0x0361: 'cp865',     #IBM PC CP-865 (Nordic)
        0x0362: 'cp866',     #IBM PC CP-866 (Cyrillic (Russian))
        0x0365: 'cp869',     #IBM PC CP-869 (Greek (Modern))
        0x036A: 'cp874',     #Windows CP-874 (Thai)
        0x03A4: 'cp932',     #Windows CP-932 (Japanese Shift-JIS)
        0x03A8: 'cp936',     #Windows CP-936 (Chinese Simplified GBK)
        0x03B5: 'cp949',     #Windows CP-949 (Korean (Wansung))
        0x03B6: 'cp950',     #Windows CP-950 (Chinese Traditional BIG5)
        0x04B0: 'utf_16_le', #UTF-16 (BIFF8)
        0x04E2: 'cp1250',    #Windows CP-1250 (Latin II) (Central European)
        0x04E3: 'cp1251',    #Windows CP-1251 (Cyrillic)
        0x04E4: 'cp1252',    #Windows CP-1252 (Latin I) (BIFF4-BIFF7)
        0x04E5: 'cp1253',    #Windows CP-1253 (Greek)
        0x04E6: 'cp1254',    #Windows CP-1254 (Turkish)
        0x04E7: 'cp1255',    #Windows CP-1255 (Hebrew)
        0x04E8: 'cp1256',    #Windows CP-1256 (Arabic)
        0x04E9: 'cp1257',    #Windows CP-1257 (Baltic)
        0x04EA: 'cp1258',    #Windows CP-1258 (Vietnamese)
        0x0551: 'cp1361',    #Windows CP-1361 (Korean (Johab))
        0x2710: 'mac_roman', #Apple Roman
    }
    for codepage in encodings.values():
        terms.append(SimpleTerm(codepage,
                                token=codepage,
                                title=codepage))
    return SimpleVocabulary(terms)

def getClassInheritancePath(startClass, endClass=None):
    """Class inheritance path in form of list
    """
    retList = []
    if endClass == None:
        endClass = Component
    if startClass is not endClass:
        for i_class in startClass.__bases__:
            if issubclass(i_class, endClass):
                retList.append(i_class)
                retList.extend(getClassInheritancePath(i_class, endClass))
    return retList

def getRefAttributeNames(arg_class):
    """return a string list of class attribute names with
    RelationPropertyIn- or RelationPropertyOut-type
    """
    retList = []
    classInheritancePath = getClassInheritancePath(arg_class,
                                                   endClass=Component)
    classInheritancePath.append(arg_class)
    for i_class in classInheritancePath:
        for attrName, attrValue in i_class.__dict__.items():
            if type(attrValue)==RelationPropertyIn or \
               type(attrValue)==RelationPropertyOut:
                retList.append(attrName)
    return retList

#def getRefAttributeNamesTypes(arg_class):
    #"""return a tuple list of class attribute names with
    #RelationPropertyIn- or RelationPropertyOut-type
    #[(attrname, reltype),]
    #"""
    #retList = []
    #class_parents = getClassParents(arg_class)
    #class_parents.append(arg_class)
    #for arg_class in class_parents:
        #for attrName, attrValue in arg_class.__dict__.items():
            #if type(attrValue)==RelationPropertyIn or \
               #type(attrValue)==RelationPropertyOut:
                #retList.append((attrName, attrValue._relType))
    #return retList

def getValAttributeNames(arg_instance):
    """return a string list of instance attribute names
    """
    classOfInstance = arg_instance.__class__
    #(Pdb) pp classOfInstance.__dict__['address1']
    #<zope.schema.fieldproperty.FieldProperty object at 0xb86d1ec>
    #(Pdb) getattr(classOfInstance, attrName)
    #*** AttributeError: type object 'Address' has no attribute '__annotations__'
    #(Pdb) hasattr(classOfInstance, attrName)
    #False
    retList = []
    classInheritancePath = getClassInheritancePath(classOfInstance,
                                                   endClass=Superclass)
    classInheritancePath.append(classOfInstance)
    print "classInheritancePath: ", classInheritancePath
    askAttributes = []
    allAttributesList = [i_class.__dict__.keys() for i_class in classInheritancePath]
    for j_attrList in allAttributesList:
        askAttributes.extend(j_attrList)

    from zope.interface import Attribute
    for attrName, attrValue in arg_instance.__dict__.items():
        if hasattr(classOfInstance, attrName):
            classField = getattr(classOfInstance, attrName)
            #print "%s: (%s): %s" % (attrName, classField, isinstance(classField, Attribute))
            if IField.providedBy(classField) and \
               attrName in askAttributes:
                retList.append(attrName)
    #print "dumdidumm: ", retList
    return retList
