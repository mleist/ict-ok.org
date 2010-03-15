# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0613,W0612,W0232,W0142
#
"""implementation of browser class of Host object
"""

__version__ = "$Id$"

# python imports
import os
import csv
from datetime import datetime
import tempfile

# zope imports
from zope.app import zapi
from zope.i18nmessageid import MessageFactory
from zope.app.catalog.interfaces import ICatalog
from zope.app.security.interfaces import IAuthentication
from zope.component import queryUtility, queryMultiAdapter, \
    getUtilitiesFor
from zope.traversing.browser import absoluteURL
from zope.session.interfaces import ISession
from zope.app.rotterdam.xmlobject import setNoCacheHeaders

# z3c imports
from z3c.form import button, field, form, interfaces
from z3c.formui import layout

# schooltool
from schooltool.requirement.interfaces import IScoreSystem

# ict_ok.org imports
from org.ict_ok.components.superclass.browser.superclass import \
     Overview, \
     link, raw_cell_formatter, GetterColumn
from org.ict_ok.components.supernode.browser.supernode import SupernodeDetails
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.admin_utils.compliance.evaluation import \
     getEvaluationsDone, Evaluation, getEvaluationsTodo
from org.ict_ok.admin_utils.compliance.browser.requirement import \
     link as linkReq
from org.ict_ok.admin_utils.compliance.browser.requirement import \
     getRequirementBottons, getReqModifiedDate, getRequirementTitle
from org.ict_ok.admin_utils.compliance.browser.evaluation import \
     getEvaluationRequirementTitle, \
     evaluationValue_formatter, \
     getEvaluationBottons, getEvalModifiedDate, \
     getEvaluatorTitle, getEvaluationValue
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, getTitle
from org.ict_ok.components.interfaces import \
    IImportCsvData, IImportXlsData
from org.ict_ok.admin_utils.idchooser.interfaces import IIdChooser
from org.ict_ok.osi.interfaces import IOSIModel
from org.ict_ok.osi.interfaces import IPhysicalLayer
from org.ict_ok.components.superclass.superclass import objectsWithInterface

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
        objectId = self.request.get('obj_id', default=None)
        my_catalog = zapi.getUtility(ICatalog)
        if objectId != None:
            obj = my_catalog.searchResults(oid_index=objectId)
            obj = iter(obj).next()
        else:
            obj = self.context
        evaluations = getEvaluationsDone(obj)
        if requirementId is not None \
           and evaluations is not None:
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
        objectId = self.request.get('obj_id', default=None)
        my_catalog = zapi.getUtility(ICatalog)
        if objectId != None:
            obj = my_catalog.searchResults(oid_index=objectId)
            obj = iter(obj).next()
        else:
            obj = self.context
        evaluations = getEvaluationsDone(obj)
        if requirementId is not None \
           and evaluations is not None:
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

    def exportCsvData(self):
        """get CSV file for all folder objects"""
        fields = self.fields
        attrList = [ fname for fname, fval in fields.items()]
        writerFile = os.tmpfile()
        writer = csv.writer(writerFile, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(attrList)
        itemList = self.context.items()
        for item_n, item_v in itemList:
            valueList = []
            for attr in attrList:
                value = getattr(item_v, attr)
                valueList.append(value)
            writer.writerow(valueList)
        writerFile.seek(0)
        tmpText = writerFile.read()
        #writerFile.close()
        self.request.response.setHeader('Content-Type', 'application/vnd.ms-excel')
        self.request.response.setHeader(\
            'Content-Disposition',
            'attachment; filename=\"%s.csv\"' % self.attrInterface.__name__)
        setNoCacheHeaders(self.request.response)
        return tmpText
    
    def exportXlsData(self, sheetName=u'ict', wbook=None, filename='ict.xls'):
        """get XLS file for all folder objects"""
        import cProfile, pstats


#        (filename, dataMem) = self.context.exportXlsData(self.request,
#                                                         sheetName=sheetName,
#                                                         wbook=wbook)

        print ----------------------------------1
        pr = cProfile.Profile()
        print ----------------------------------2
        (filename, dataMem) = pr.runcall(self.context.exportXlsData,
                                         self.request,
                                         sheetName=sheetName,
                                         wbook=wbook)
        pr.print_stats()
        print ----------------------------------3
#        p = pstats.Stats('cprof.out')
#        p.sort_stats('time').print_stats(10)

        self.request.response.setHeader('Content-Type', 'application/vnd.ms-excel')
        self.request.response.setHeader(\
            'Content-Disposition',
            'attachment; filename=\"%s\"' % filename)
        setNoCacheHeaders(self.request.response)
        return dataMem

    def connectedComponentsOnPhysicalLayer(self):
        Components = []
        osiModelAdapter = IOSIModel(self.context)
        if osiModelAdapter:
            osiModelAdapter.connectedComponentsOnLayer(\
                (IPhysicalLayer,), Components, 10)
        return Components

    def todoHref(self):
        return "%s/evaluations_todo.html" % zapi.absoluteURL(self.context, self.request)
    
    def passHref(self):
        return "%s/evaluations_done.html" % zapi.absoluteURL(self.context, self.request)

    def failHref(self):
        return "%s/evaluations_done.html" % zapi.absoluteURL(self.context, self.request)

    def resumee(self):
        allObjEvaluations = getEvaluationsDone(self.context)
        reqs = allObjEvaluations.items()
        reqs_ok = 0
        reqs_fail = 0
        for req_tupel in reqs:
            if req_tupel[1].value == "Pass":
                reqs_ok += 1
            elif req_tupel[1].value == "Fail":
                reqs_fail += 1
        reqs_todo = len(getEvaluationsTodo(self.context))
        return (reqs_todo, reqs_ok, reqs_fail)


class EvaluationsTodoDisplay(Overview):
    """for evaluation which are open
    """
    label = _(u'evaluations to do')
    columns = (
        GetterColumn(title=_('Title'),
                     getter=getRequirementTitle,
                     cell_formatter=linkReq('overview.html')),
        GetterColumn(title=_('Component'),
                     getter=getTitle,
                     cell_formatter=link('overview.html')),
        GetterColumn(title=_('Modified'),
                     getter=getReqModifiedDate,
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
    
    def reqList1stLevel(self):
        """List of Content objects"""
        retList = []
        evaluations = self.context.getEvaluationsTodo()
        for ev in evaluations:
            retList.append({"req": ev, "obj": self.context})
        return retList

    def reqList2ndLevel(self):
        """List of Content objects"""
        attrs = self.context.getRefAttributeNames()
        retList = []
        for attr in attrs:
            objs = getattr(self.context, attr)
            if type(objs) is not list:
                objs = [objs]
            for obj in objs:
                if hasattr(obj, "requirements"):
                    evaluations = self.context.getEvaluationsTodo()
                    for ev in evaluations:
                        retList.append({"req": ev, "obj": self.context})
        return retList


class EvaluationsDoneDisplay(Overview):
    """for already done evaluations
    """
    label = _(u'evaluations done')
    columns = (
        GetterColumn(title=_('Requirement'),
                     getter=getEvaluationRequirementTitle,
                     cell_formatter=link('overview.html')),
        GetterColumn(title=_('Component'),
                     getter=getTitle,
                     cell_formatter=link('overview.html')),
        GetterColumn(title=_('Evaluator'),
                     getter=getEvaluatorTitle,
                     cell_formatter=link('overview.html')),
        GetterColumn(title=_('Value'),
                     getter=getEvaluationValue,
                     cell_formatter=evaluationValue_formatter),
        GetterColumn(title=_('Modified'),
                     getter=getEvalModifiedDate,
                     subsort=True,
                     cell_formatter=raw_cell_formatter),
        GetterColumn(title=_('Actions'),
                     getter=getEvaluationBottons,
                     cell_formatter=raw_cell_formatter),
        )
    sort_columns = []
    status = None
    firstSortOn = _("Component")

    def reqList1stLevel(self):
        """List of Content objects"""
        retList = []
        evaluations = self.context.getEvaluationsDone()
        for ev in evaluations:
            retList.append({"eval": ev, "obj": self.context})
        return retList

    def reqList2ndLevel(self):
        """List of Content objects"""
        attrs = self.context.getRefAttributeNames()
        retList = []
        for attr in attrs:
            objs = getattr(self.context, attr)
            if type(objs) is not list:
                objs = [objs]
            for obj in objs:
                if hasattr(obj, "requirements"):
                    evaluations = self.context.getEvaluationsDone()
                    for ev in evaluations:
                        retList.append({"eval": ev, "obj": self.context})
        return retList

class AddComponentForm(AddForm):
    """ template add form """
    
    def templatesOutThere(self):
        templatesOutThere = False
        for object in objectsWithInterface(self.attrInterface):
            if object.isTemplate:
                templatesOutThere = True
                break
        return templatesOutThere
    
    def update(self):
        if self.templatesOutThere():
            session = ISession(self.request)[self._session_key]
            try:
#                print "eee: ", session['state']
                if session['state'] == "templateOk":
                    self.fields = self.allFields
                elif session['state'] == "done":
                    del session['state']
                    self.fields = self.addFields
                elif session['state'] == "novalue":
                    self.fields = self.allFields
                else:
                    pass
            except KeyError:
                self.fields = self.addFields
        else:
            self.fields = self.allFields
        return AddForm.update(self)
    
    @button.buttonAndHandler(u'Cancel')
    def handleCancel(self, action):
        """cancel was pressed"""
        session = ISession(self.request)[self._session_key]
        try:
            del session['state']
        except KeyError:
            pass
        url = absoluteURL(self.context, self.request)
        self.request.response.redirect(url)
        
    @button.buttonAndHandler(_('Add'), name='add')
    def handleAdd(self, action):
        """submit was pressed"""
        #import pdb
        #pdb.set_trace()
        session = ISession(self.request)[self._session_key]
        if 'template' in self.widgets and \
            self.widgets['template'] is not None and \
            len(self.widgets['template'].value) > 0:
            if self.widgets['template'].value[0] == u'--NOVALUE--':
                url = absoluteURL(self, self.request)
                session['state'] = "novalue" 
                return self.request.response.redirect(url)
            addObjId = str(self.widgets['template'].value[0])
            my_catalog = zapi.getUtility(ICatalog)
            obj = my_catalog.searchResults(oid_index=addObjId)
            addObj = iter(obj).next()
            #addObjIntId = int(self.widgets['template'].value[0])
            #intIdUtil = queryUtility(IIntIds)
            #addObj = intIdUtil.queryObject(addObjIntId)
            if addObj is not None:
                self.context = addObj
                session['state'] = "templateOk" 
                self.fields = self.allFields
                self.updateWidgets()
                for field_n in self.fields:
                    i_widgets = self.widgets[field_n]
                    i_dc = queryMultiAdapter((i_widgets.field,i_widgets),
                                             interfaces.IDataConverter)
                    i_val = getattr(addObj, field_n)
                    i_wval = i_dc.toWidgetValue(i_val)
                    if i_val is not None and \
                        field_n != "isTemplate":
                        self.widgets[field_n].value = i_wval
                    if interfaces.IOrderedSelectWidget.providedBy(i_widgets):
                        for value in i_wval:
                            for item in i_widgets.items:
                                if value in item["value"]:
                                    i_widgets.selectedItems.append(item)
                        i_widgets.notselectedItems = i_widgets.deselect()
                        #import pdb
                        #pdb.set_trace()
        else:
            self.fields = self.allFields
            data, errors = self.extractData()
            if not hasattr(data, 'isTemplate') or \
               not data['isTemplate']:
                idChoosers = list(getUtilitiesFor(IIdChooser))
                for (i_key, i_val) in data.items():
                    if type(i_val) is type(u''):
                        for (ch_name, idChooser) in idChoosers:
                            if i_val.count(u'[$%s$]' % ch_name) > 0:
                                data[i_key] = i_val.replace(u'[$%s$]' % ch_name,
                                                      idChooser.incrementId())
            session['state'] = "dataExtracted" 
            if errors:
                self.status = self.formErrorsMessage
                return
            obj = self.createAndAdd(data)
            if obj is not None:
                # mark only as finished if we get the new object
                self._finishedAdd = True
                session['state'] = "done" 
            url = absoluteURL(self, self.request)
            self.request.response.redirect(url)


class ImportCsvDataComponentForm(layout.FormLayoutSupport, form.Form):
    """ Delete the net """
    
    form.extends(form.Form)
    label = _(u"Import CSV data")
    fields = field.Fields(IImportCsvData)
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return u"aaa"
        
    @button.buttonAndHandler(u'Submit')
    def handleSubmit(self, action):
        """submit was pressed"""
        if 'csvdata' in self.widgets:
            fileWidget=self.widgets['csvdata']
            fileUpload = fileWidget.extract()
            reader = csv.reader(fileUpload.readlines(), 
                                delimiter=';', 
                                quoting=csv.QUOTE_NONNUMERIC)
#            for row in reader:
#                print '> ', row
        url = absoluteURL(self.context, self.request)
        self.request.response.redirect(url)

    @button.buttonAndHandler(u'Cancel')
    def handleCancel(self, action):
        """cancel was pressed"""
        url = absoluteURL(self.context, self.request)
        self.request.response.redirect(url)

    def update(self):
        """update all widgets"""
        #if ISuperclass.providedBy(self.context):
            #self.label = self.getTitle()
        form.Form.update(self)


class ImportXlsDataComponentForm(layout.FormLayoutSupport, form.Form):
    """ Delete the net """
    
    form.extends(form.Form)
    label = _(u"Import XLS data")
    fields = field.Fields(IImportXlsData)
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return u"aaa"

    @button.buttonAndHandler(u'Submit')
    def handleSubmit(self, action):
        """submit was pressed"""
        #import pdb
        #pdb.set_trace()
        if 'xlsdata' in self.widgets:
            codepage=self.widgets['codepage'].value[0]
            fileWidget=self.widgets['xlsdata']
            fileUpload = fileWidget.extract()
            filename = datetime.now().strftime('in_%Y%m%d%H%M%S.xls')
            f_handle, f_name = tempfile.mkstemp(filename)
            outf = open(f_name, 'wb')
            outf.write(fileUpload.read())
            outf.close()
            try:
                self.context.importXlsData(self.request, f_name, codepage)
            finally:
                os.remove(f_name)
        url = absoluteURL(self.context, self.request)
        self.request.response.redirect(url)

    @button.buttonAndHandler(u'Cancel')
    def handleCancel(self, action):
        """cancel was pressed"""
        url = absoluteURL(self.context, self.request)
        self.request.response.redirect(url)

    def update(self):
        """update all widgets"""
        #if ISuperclass.providedBy(self.context):
            #self.label = self.getTitle()
        form.Form.update(self)
