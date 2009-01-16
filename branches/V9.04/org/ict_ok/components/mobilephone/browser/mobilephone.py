# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: template.py_cog 396 2009-01-08 00:21:51Z markusleist $
#
# pylint: disable-msg=E1101,W0232,W0142
#
from zope.component._api import getUtility
from zope.app.intid.interfaces import IIntIds
from docutils.nodes import field_name
"""implementation of browser class of MobilePhone"""

__version__ = "$Id: template.py_cog 396 2009-01-08 00:21:51Z markusleist $"

# python imports
import os
import csv
from datetime import datetime
import tempfile
from pyExcelerator import Workbook, XFStyle, Font, Alignment, Formula
import pyExcelerator as xl

# zope imports
from zope.app import zapi
from zope.traversing.browser import absoluteURL
from zope.i18nmessageid import MessageFactory
from zope.app.rotterdam.xmlobject import setNoCacheHeaders
import zope.component
from zope.component import getUtility
from zope.lifecycleevent import ObjectCreatedEvent
from zope.event import notify
from zope.session.interfaces import ISession
from zope.schema.interfaces import IChoice, ICollection, IDate

# z3c imports
from z3c.form import button, field, form, interfaces, util
from z3c.formui import layout
from z3c.pagelet.interfaces import IPagelet
from z3c.pagelet.browser import BrowserPagelet
from z3c.form import datamanager
from z3c.form import converter
from z3c.form import widget

# ict_ok.org imports
from org.ict_ok.components.mobilephone.interfaces import \
    IMobilePhone, IAddMobilePhones
from org.ict_ok.components.interfaces import \
    IImportCsvData, IImportXlsData
from org.ict_ok.components.mobilephone.mobilephone import MobilePhone
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditForm

_ = MessageFactory('org.ict_ok')
SESSION_KEY = 'org.ict_ok.components.mobilephone'


# --------------- menu entries -----------------------------


class MSubAddMobilePhone(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Mobile phone')
    viewURL = 'add_mobilephone.html'

    weight = 50

# --------------- object details ---------------------------


class MobilePhoneDetails(ComponentDetails):
    """ Class for MobilePhone details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + ['requirement']
    omit_addfields = ComponentDetails.omit_addfields + ['requirement']
    omit_editfields = ComponentDetails.omit_editfields + ['requirement']


class MobilePhoneFolderDetails(ComponentDetails):
    """ Class for MobilePhone details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + ['requirement']
    omit_addfields = ComponentDetails.omit_addfields + ['requirement']
    omit_editfields = ComponentDetails.omit_editfields + ['requirement']

    def exportCsvData(self):
        """get CSV file for all folder objects"""
        fields = field.Fields(IMobilePhone).omit(*MobilePhoneDetails.omit_viewfields)
        attrList = [ fname for fname, fval in fields.items()]
        #writerFile = open("/tmp/1111.csv", "wb")
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
            'attachment; filename=\"%s.csv\"' % IMobilePhone.__name__)
        setNoCacheHeaders(self.request.response)
        return tmpText
    
    def exportXlsData(self):
        """get CSV file for all folder objects"""
        filename = datetime.now().strftime('ict_%Y%m%d%H%M%S.xls')
        f_handle, f_name = tempfile.mkstemp(filename)
        wbook = Workbook()
        wb_hosts = wbook.add_sheet('ddd')
        style0 = XFStyle()
        font0 = Font()
        font0.height = 6*20
        style0.num_format_str = '@'
        style0.font = font0
        style1 = XFStyle()
        font1 = Font()
        font1.height = 6*20
        style1.num_format_str = '@'
        style1.font = font1
        heading_pattern = xl.Pattern()
        heading_pattern.pattern = xl.Pattern.SOLID_PATTERN
        heading_pattern.pattern_back_colour = 0x5
        heading_pattern.pattern_fore_colour = 0x5   
#        wb_hosts.write(1, 0, 'ddd2')
        fields = field.Fields(IMobilePhone).omit(*MobilePhoneDetails.omit_viewfields)
        attrList = [ fname for fname, fval in fields.items()]
        #writerFile = open("/tmp/1111.csv", "wb")
#        writerFile = os.tmpfile()
#        writer = csv.writer(writerFile, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
#        writer.writerow(attrList)
        itemList = self.context.items()
        pos_y = 0
        pos_x = 0
        for attr in attrList:
            wb_data = Formula(u'"%s"' % attr)
            style0.pattern = heading_pattern 
            wb_hosts.write(pos_y, pos_x, wb_data, style0)
            pos_x += 1
        # objectID
        wb_data = Formula(u'"objectID"')
        wb_hosts.write(pos_y, pos_x, wb_data, style0)
        wb_hosts.col(pos_x).width *= 3
        pos_x += 1
        pos_y = 1
        for item_n, item_v in itemList:
            pos_x = 0
#            valueList = []
#            widgets = zope.component.getMultiAdapter(
#                (self, self.request, self.context), interfaces.IWidgets)
#            widget = zope.component.getMultiAdapter((field, self.request),
#                                                    interfaces.IFieldWidget)

            for attr in attrList:
                attrField = IMobilePhone[attr]
                attrDm = datamanager.AttributeField(item_v, attrField)
                v_style = XFStyle()
                v_font = Font()
                v_font.height = 6*20
                v_style.font = v_font
                value = None
                if IChoice.providedBy(attrField):
                    v_style.num_format_str = '@'
                    #value = getattr(item_v, attr)
#                    import pdb
#                    pdb.set_trace()
                    dateValue = attrDm.get()
                    v_widget = zope.component.getMultiAdapter(\
                                    (attrField,self.request),
                                    interfaces.IFieldWidget)
                    v_dataconverter = zope.component.queryMultiAdapter(\
                                    (attrDm.field, v_widget),
                                    interfaces.IDataConverter)
                    value = v_dataconverter.toWidgetValue(dateValue)[0]
                elif ICollection.providedBy(attrField):
                    v_style.num_format_str = '@'
                    value = getattr(item_v, attr)
                else:
                    v_style.num_format_str = '@'
                    dateValue = attrDm.get()
                    v_widget = zope.component.getMultiAdapter(\
                                    (attrField,self.request),
                                    interfaces.IFieldWidget)
                    v_dataconverter = zope.component.queryMultiAdapter(\
                                    (attrDm.field, v_widget),
                                    interfaces.IDataConverter)
                    value = v_dataconverter.toWidgetValue(dateValue)
#                elif IDate.providedBy(attrField):
#                    v_style.num_format_str = 'M/D/YYYY'
#                    import pdb
#                    pdb.set_trace()
#                    www = zope.component.getMultiAdapter(\
#                             (attrField,self.request),
#                             interfaces.IFieldWidget)
##                    c2 = converter.DateDataConverter(attrDm.field, www)
##                    dm2 = zope.component.getMultiAdapter((item_v, attrField), interfaces.IDataManager)
#                    dc2 = zope.component.queryMultiAdapter((attrDm.field, www), interfaces.IDataConverter)
#                    dateValue = attrDm.get()
#                    value = datetime(dateValue.year,
#                                     dateValue.month,
#                                     dateValue.day)
#                    value = dc2.toWidgetValue(dateValue)
#                else:
#                    v_style.num_format_str = '@'
##                    www=widget.Widget(self.request)
##                    www = zope.component.getMultiAdapter(\
##                             (attrField,self.request),
##                             interfaces.IFieldWidget)
##                    ccc = converter.FieldDataConverter(attrDm.field, www)
##                    print ccc.toWidgetValue(attrDm.get())
#                    value = attrDm.get()
##                value = getattr(item_v, attr)
                if value is not None:
                    #wb_data = Formula(u'"%s"' % value)
#                    wb_hosts.write(pos_y, pos_x, wb_data, style0)
                    wb_hosts.write(pos_y, pos_x, value, v_style)
                pos_x += 1
            # objectID
            wb_data = Formula(u'"%s"' % item_v.objectID)
            wb_hosts.write(pos_y, pos_x, wb_data, style0)
            pos_x += 1
            pos_y += 1
#            writer.writerow(valueList)
#        writerFile.seek(0)
#        tmpText = writerFile.read()
        #writerFile.close()
        wbook.save(f_name)
        self.request.response.setHeader('Content-Type', 'application/vnd.ms-excel')
        self.request.response.setHeader(\
            'Content-Disposition',
            'attachment; filename=\"%s\"' % filename)
        setNoCacheHeaders(self.request.response)
        datafile = open(f_name, "r")
        dataMem = datafile.read()
        datafile.close()
        os.remove(f_name)
        return dataMem

# --------------- forms ------------------------------------


# TODO: delete this form
class DetailsMobilePhoneForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Mobile phone')
    fields = field.Fields(IMobilePhone).omit(*MobilePhoneDetails.omit_viewfields)


class AddMobilePhoneForm(AddForm):
    """Add Mobile phone form"""
    label = _(u'Add Mobile phone')
    fields = field.Fields(IMobilePhone).omit(*MobilePhoneDetails.omit_addfields)
    factory = MobilePhone
        


class EditMobilePhoneForm(EditForm):
    """ Edit for Mobile phone """
    label = _(u'Mobile phone Edit Form')
    fields = field.Fields(IMobilePhone).omit(*MobilePhoneDetails.omit_editfields)


class DeleteMobilePhoneForm(DeleteForm):
    """ Delete the Mobile phone """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this MobilePhone: '%s'?") % \
               IBrwsOverview(self.context).getTitle()



#class AddMobilePhones(layout.FormLayoutSupport, form.Form):
#class AddMobilePhones(layout.FormLayoutSupport, form.AddForm):
class AddMobilePhones(AddForm):
    """ Delete the net """
    
    #form.extends(form.AddForm)
    label = _(u"Add Mobile Phones")
    #fields = field.Fields(IMobilePhone).omit(*MobilePhoneDetails.omit_addfields)
    fields = field.Fields(IAddMobilePhones)
    factory = MobilePhone
    _templChoice = False
    _dataExtracted = False
    
#    def __call__(self):
#        print "###### __call__() (%s) (%s)" % (self.templChoice, self.dataExtracted)
#        if self.templChoice or \
#            self.dataExtracted:
#            self.fields = field.Fields(IMobilePhone).omit(*MobilePhoneDetails.omit_addfields)
#        import pdb
#        pdb.set_trace()
#        return AddForm.__call__(self)

    def update(self):
        """update all widgets"""
        session = ISession(self.request)[SESSION_KEY]
        print "###### update() (%s) (%s)" % (self._templChoice, self._dataExtracted)
        print "> :", session
#        import pdb
#        pdb.set_trace()
        try:
            if session['state'] == "templateOk":
                print "------------ 1"
                self.fields = field.Fields(IMobilePhone).omit(*MobilePhoneDetails.omit_addfields)
            elif session['state'] == "dataExtracted":
                print "------------ 2"
                #self.fields = field.Fields(IMobilePhone).omit(*MobilePhoneDetails.omit_addfields)
            elif session['state'] == "done":
                print "------------ 3"
                #self.fields = field.Fields(IMobilePhone).omit(*MobilePhoneDetails.omit_addfields)
                del session['state']
            else:
                print "------------ 4"
                #self.fields = field.Fields(IMobilePhone).omit(*MobilePhoneDetails.omit_addfields)
        except KeyError:
            print "++++++++++++ 5"
            self.fields = field.Fields(IAddMobilePhones)
        return AddForm.update(self)
#        
##        if self.templChoice or \
##            self.dataExtracted:
#        if not self._templChoice:
#            self.fields = field.Fields(IAddMobilePhones)
#        else:
#            self.fields = field.Fields(IMobilePhone).omit(*MobilePhoneDetails.omit_addfields)
#        return AddForm.update(self)
    
    @button.buttonAndHandler(u'Cancel')
    def handleCancel(self, action):
        """cancel was pressed"""
        session = ISession(self.request)[SESSION_KEY]
        try:
            del session['state']
        except KeyError:
            pass
        url = absoluteURL(self.context, self.request)
        self.request.response.redirect(url)
        
#    @button.buttonAndHandler(u'Add from template')
#    def handleAdd(self, action):
    @button.buttonAndHandler(_('Add'), name='add')
    def handleAdd(self, action):
        """submit was pressed"""
#        import pdb
#        pdb.set_trace()
        session = ISession(self.request)[SESSION_KEY]
        if 'template' in self.widgets and \
            self.widgets['template'] is not None and \
            len(self.widgets['template'].value) > 0:
            print "............... 5"
            #action.value = u"Add1"
#            import pdb
#            pdb.set_trace()
            print "iii: ", self.widgets['template']
            addObjIntId = int(self.widgets['template'].value[0])
            intIdUtil = getUtility(IIntIds)
            addObj = intIdUtil.queryObject(addObjIntId)
            if addObj is not None:
#                import pdb
#                pdb.set_trace()
#                print addObj.ikName
                self.context = addObj
                session['state'] = "templateOk" 
                #self._templChoice = True
                self.fields = field.Fields(IMobilePhone).omit(*MobilePhoneDetails.omit_addfields)
#                self.factory = MobilePhone
#                form.extends(form.AddForm)
                self.updateWidgets()
#                self.update()
#                for field_n, field_o in self.fields.items():
                for field_n in self.fields:
                    if field_n == "user":
                        import pdb
                        pdb.set_trace()
                    w21=self.widgets[field_n]
                    f21=self.fields[field_n]
                    dc21=zope.component.queryMultiAdapter((w21.field,w21),interfaces.IDataConverter)
                    val21 = getattr(addObj, field_n)
                    wval21 = dc21.toWidgetValue(val21)
                    if val21 is not None and \
                        field_n != "isTemplate":
                        self.widgets[field_n].value = wval21
                    
##                    attrField = IMobilePhone[attr]
##                    attrDm = datamanager.AttributeField(item_v, attrField)
#                    attrDm = datamanager.AttributeField(addObj, field_o)
#                    dateValue = attrDm.get()
#                    v_widget = zope.component.getMultiAdapter(\
#                                    (field_o.field,self.request),
#                                    interfaces.IFieldWidget)
#                    #(self, self.request, self.getContent())
#                    v_dataconverter = zope.component.queryMultiAdapter(\
#                                    (attrDm.field, v_widget),
#                                    interfaces.IDataConverter)
#                    if v_dataconverter is not None:
#                        import pdb
#                        pdb.set_trace()
#                        i_val = v_dataconverter.toWidgetValue(dateValue)
#                    else:
#                        i_val = getattr(addObj, field_n)
#                    if i_val is not None and \
#                        field_n != "isTemplate":
#                        self.widgets[field_n].value = i_val
#                        print "uuu: ", i_val
##                import pdb
##                pdb.set_trace()
##                self.update()
#                self._templChoice = True
#                #return self.render()
        else:
            print "............... 4"
            #action.value = u"Add2"
            self.fields = field.Fields(IMobilePhone).omit(*MobilePhoneDetails.omit_addfields)
            data, errors = self.extractData()
            session['state'] = "dataExtracted" 
            self._dataExtracted = True
#            import pdb
#            pdb.set_trace()
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


class ImportCsvDataForm(layout.FormLayoutSupport, form.Form):
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
        import pdb
        pdb.set_trace()
        if 'csvdata' in self.widgets:
            fileWidget=self.widgets['csvdata']
            fileUpload = fileWidget.extract()
            reader = csv.reader(fileUpload.readlines(), 
                                delimiter=';', 
                                quoting=csv.QUOTE_NONNUMERIC)
            for row in reader:
                print '> ', row
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


class ImportXlsDataForm(layout.FormLayoutSupport, form.Form):
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
        import pyExcelerator
        if 'xlsdata' in self.widgets:
            from pprint import pprint
            from zope.schema.interfaces import IChoice, ICollection, IDate
            from zope.component import createObject
            fields = field.Fields(IMobilePhone)
#            import pdb
#            pdb.set_trace()
            codepage=self.widgets['codepage'].value[0]
            fileWidget=self.widgets['xlsdata']
            fileUpload = fileWidget.extract()
            filename = datetime.now().strftime('in_%Y%m%d%H%M%S.xls')
            f_handle, f_name = tempfile.mkstemp(filename)
            outf = open(f_name, 'wb')
            outf.write(fileUpload.read())
            outf.close()
            parseRet = pyExcelerator.parse_xls(f_name, codepage)
            os.remove(f_name)
            for sheet_name, values in parseRet:
                matrix = [[]]
                for row_idx, col_idx in sorted(values.keys()):
                    v = values[(row_idx, col_idx)]
                    if isinstance(v, unicode):
                        v = u"%s" % v # v.encode(codepage, 'backslashreplace')
                    else:
                        v = `v`
                    v = u'%s' % v.strip()
                    last_row, last_col = len(matrix), len(matrix[-1])
                    while last_row <= row_idx:
                        matrix.extend([[]])
                        last_row = len(matrix)
    
                    while last_col < col_idx:
                        matrix[-1].extend([''])
                        last_col = len(matrix[-1])
    
                    matrix[-1].extend([v])
                attrNameList = matrix[0]
                attrValMatrix = matrix[1:]
                for attrValVector in attrValMatrix:
                    attrDict = {}
                    for attrIndex, attrVal in enumerate(attrValVector):
                        attrDict[attrNameList[attrIndex]] = attrVal
                    # ---------------------------------------
                    if attrDict.has_key('objectID'):
                        attrObjectID = attrDict.pop('objectID')
                        oldObj = self.context[attrObjectID]
#                        import pdb
#                        pdb.set_trace()
                        for attrName, newValString in attrDict.items():
                            attrField = IMobilePhone[attrName]
                            if IChoice.providedBy(attrField):
                                v_widget = zope.component.getMultiAdapter(\
                                                (attrField,self.request),
                                                interfaces.IFieldWidget)
                                v_dataconverter = zope.component.queryMultiAdapter(\
                                                (attrField, v_widget),
                                                interfaces.IDataConverter)
                                newVal = v_dataconverter.toFieldValue([newValString])
                            else:
                                v_widget = zope.component.getMultiAdapter(\
                                                (attrField,self.request),
                                                interfaces.IFieldWidget)
                                v_dataconverter = zope.component.queryMultiAdapter(\
                                                (attrField, v_widget),
                                                interfaces.IDataConverter)
                                newVal = v_dataconverter.toFieldValue(newValString)
                            if getattr(oldObj, attrName) != newVal:
                                setattr(oldObj, attrName, newVal)
                    else:
                        newObj = createObject(\
                            u'org.ict_ok.components.mobilephone.mobilephone.MobilePhone')
                        newObj.__post_init__()
                        for attrName, newValString in attrDict.items():
                            attrField = IMobilePhone[attrName]
                            if IChoice.providedBy(attrField):
                                v_widget = zope.component.getMultiAdapter(\
                                                (attrField,self.request),
                                                interfaces.IFieldWidget)
                                v_dataconverter = zope.component.queryMultiAdapter(\
                                                (attrField, v_widget),
                                                interfaces.IDataConverter)
                                newVal = v_dataconverter.toFieldValue([newValString])
                            else:
                                v_widget = zope.component.getMultiAdapter(\
                                                (attrField,self.request),
                                                interfaces.IFieldWidget)
                                v_dataconverter = zope.component.queryMultiAdapter(\
                                                (attrField, v_widget),
                                                interfaces.IDataConverter)
                                newVal = v_dataconverter.toFieldValue(newValString)
                            setattr(newObj, attrName, newVal)
                        self.context.__setitem__(newObj.objectID, newObj)
                        notify(ObjectCreatedEvent(newObj))
                    # ---------------------------------------
                    
#                for row_idx, col_idx in sorted(values.keys()):
#                    v = values[(row_idx, col_idx)]
#                    print v
#            reader = csv.reader(fileUpload.readlines(), 
#                                delimiter=';', 
#                                quoting=csv.QUOTE_NONNUMERIC)
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
