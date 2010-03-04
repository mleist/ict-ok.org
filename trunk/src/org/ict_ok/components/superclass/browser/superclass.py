# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1111,E1101,E0611,W0613,W0232,W0201,W0142,R0901
#
"""implementation of browser class of Net object
"""

__version__ = "$Id$"

# python imports
import os
from datetime import datetime
import tempfile
import operator

# zope imports
import zope.interface
from zope.app import zapi
from zope.traversing.browser import absoluteURL
from zope.i18nmessageid import MessageFactory
from zope.i18n import translate
from zope.dublincore.interfaces import IZopeDublinCore
from zope.interface import directlyProvides
from zope.component import getAdapter
from zope.proxy import removeAllProxies
from zope.app.applicationcontrol.interfaces import IRuntimeInfo
from zope.size.interfaces import ISized
from zope.security.checker import canAccess
from zope.component import queryUtility
from zope.app.intid.interfaces import IIntIds
from zope.component import getMultiAdapter
from zope.lifecycleevent import Attributes, ObjectModifiedEvent
from zope.app.rotterdam.xmlobject import translate, setNoCacheHeaders
from zope.app.container.interfaces import IOrderedContainer
from zope.schema import vocabulary
from zope.app.pagetemplate.urlquote import URLQuote
from zope.component.interfaces import ComponentLookupError

# z3c imports
from z3c.form import button, field, form, interfaces
from z3c.formui import layout
from z3c.pagelet.interfaces import IPagelet
from z3c.pagelet.browser import BrowserPagelet
from z3c.form.converter import CalendarDataConverter

# zc imports
from zc.table.column import Column, GetterColumn
from zc.table.table import StandaloneFullFormatter
from zc.table.batching import Formatter as BatchedFormatter
from zc.table.interfaces import ISortableColumn

# ict_ok import
from org.ict_ok.libs.lib import fieldsForFactory, fieldsForInterface
from org.ict_ok.version import getIkVersion
from org.ict_ok.components.superclass.interfaces import \
    IPickle, ISuperclass, IFocus
from org.ict_ok.components.superclass.superclass import Superclass
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.components.supernode.interfaces import IState
from org.ict_ok.components.interfaces import IComponent
from org.ict_ok.admin_utils.usermanagement.usermanagement import \
     getUserTimezone, convert2UserTimezone, AdmUtilUserProperties
from org.ict_ok.admin_utils.eventcrossbar.interfaces import \
     IAdmUtilEvent
from org.ict_ok.components.superclass.interfaces import \
     IEventIfSuperclass
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.schema.IPy import IP
from org.ict_ok.admin_utils.mindmap.interfaces import IAdmUtilMindMap
from org.ict_ok.admin_utils.mac_address_db.interfaces import \
     IAdmUtilMacAddressDb

_ = MessageFactory('org.ict_ok')

CalendarDataConverter.length = 'medium'

# --------------- helper functions -------------------------


class CheckboxColumn(Column):
    """Special Checkbox Column"""
    def renderCell(self, item, formatter):
        """render a checkbox field"""
        widget = (u'<input type="checkbox" '
                  u'name="selected:list" value="%s">')
        return widget % (item.objectID)

def getActionBotton_Detail(item, formatter):
    """Action Buttons for Overview in Web-Browser
    """
    if type(item) is dict:
        item = item["obj"]
    resource_path = getAdapter(formatter.request, name='pics')()
    ttid = u"details" + item.getObjectId()
    view_url = absoluteURL(item, formatter.request) + '/@@details.html'
    myAdapter = zapi.queryMultiAdapter((item, formatter.request),
                                       name='details.html')
    if myAdapter is not None and canAccess(myAdapter,'render'):
        view_html = u'<a href="%s">' %  (view_url) + \
                  u'<img id="%s" alt="Info" src="%s/Info.png" /></a>' % \
                  (ttid, resource_path)
        tooltip_text = _(u'details of this object')
    else:
        view_html = u'<img id="%s" alt="Details" src="%s/Info_gr.png" />' % \
                  (ttid, resource_path)
        tooltip_text = _(u'viewing details is not permitted')
    tooltip = u"<script type=\"text/javascript\">tt_%s = new YAHOO." \
            u"widget.Tooltip('tt_%s', { autodismissdelay:'15000', " \
            u"context:'%s', text:'%s' });</script>" \
            % (ttid, ttid, ttid, tooltip_text)
    return view_html + tooltip

def getActionBotton_Edit(item, formatter):
    """Action Buttons for Overview in Web-Browser
    """
    if type(item) is dict:
        item = item["obj"]
    resource_path = getAdapter(formatter.request, name='pics')()
    ttid = u"edit" + item.getObjectId()
    edit_url = absoluteURL(item, formatter.request) + '/@@edit.html'
    myAdapter = zapi.queryMultiAdapter((item, formatter.request),
                                       name='edit.html')
    if myAdapter is not None and canAccess(myAdapter,'render'):
        edit_html = u'<a href="%s">' %  (edit_url) + \
                  u'<img id="%s" alt="Edit" src="%s/Hand.png" /></a>' % \
                  (ttid, resource_path)
        tooltip_text = _(u'edit this object')
    else:
        edit_html = u'<img id="%s" alt="Edit" src="%s/Hand_gr.png" />' % \
                  (ttid, resource_path)
        tooltip_text = _(u'editing is not permitted')
    tooltip = u"<script type=\"text/javascript\">tt_%s = new YAHOO." \
            u"widget.Tooltip('tt_%s', { autodismissdelay:'15000', " \
            u"context:'%s', text:'%s' });</script>" \
            % (ttid, ttid, ttid, tooltip_text)
    return edit_html + tooltip

def getActionBotton_History(item, formatter):
    """Action Buttons for Overview in Web-Browser
    """
    if type(item) is dict:
        item = item["obj"]
    resource_path = getAdapter(formatter.request, name='pics')()
    ttid = u"history" + item.getObjectId()
    hist_url = absoluteURL(item, formatter.request) + '/@@history.html'
    myAdapter = zapi.queryMultiAdapter((item, formatter.request),
                                       name='history.html')
    if myAdapter is not None and canAccess(myAdapter,'render'):
        hist_html = u'<a href="%s">' %  (hist_url) + \
                  u'<img id="%s" alt="History" src="%s/Doc.png" /></a>' % \
                  (ttid, resource_path)
        tooltip_text = _(u'history this object')
    else:
        hist_html = u'<img id="%s" alt="History" src="%s/Doc_gr.png" />' % \
                  (ttid, resource_path)
        tooltip_text = _(u'viewing the history is not permitted')
    tooltip = u"<script type=\"text/javascript\">tt_%s = new YAHOO." \
            u"widget.Tooltip('tt_%s', { autodismissdelay:'15000', " \
            u"context:'%s', text:'%s' });</script>" \
            % (ttid, ttid, ttid, tooltip_text)
    return hist_html + tooltip

def getActionBotton_Delete(item, formatter):
    """Action Buttons for Overview in Web-Browser
    """
    if type(item) is dict:
        item = item["obj"]
    resource_path = getAdapter(formatter.request, name='pics')()
    ttid = u"delete" + item.getObjectId()
    trash_url = absoluteURL(item, formatter.request) + '/@@delete.html'
    myAdapter = zapi.queryMultiAdapter((item, formatter.request),
                                       name='delete.html')
    if myAdapter is not None and canAccess(myAdapter,'render') \
       and item.canBeDeleted():
        trash_html = u'<a href="%s">' %  (trash_url) + \
                  u'<img id="%s" alt="Trash" src="%s/Trash.png" /></a>' % \
                   (ttid, resource_path)
        tooltip_text = _(u'delete this object')
    else:
        trash_html = u'<img id="%s" alt="Trash" src="%s/Trash_gr.png" />' % \
                   (ttid, resource_path)
        tooltip_text = _(u'deleting this object is not permitted')
        if not item.canBeDeleted():
            tooltip_text += _(u',<br/>referenced by other objects')
    tooltip = u"<script type=\"text/javascript\">tt_%s = new YAHOO." \
            u"widget.Tooltip('tt_%s', { autodismissdelay:'15000', " \
            u"context:'%s', text:'%s' });</script>" \
            % (ttid, ttid, ttid, tooltip_text)
    return trash_html + tooltip

def getActionBotton_UpDown(item, formatter):
    """Action Buttons for Overview in Web-Browser
    """
    if type(item) is dict:
        item = item["obj"]
    retHtml = u""
    parentIsOrderd = IOrderedContainer.providedBy(item.__parent__)
    resource_path = getAdapter(formatter.request, name='pics')()
    if parentIsOrderd:
        up_url = absoluteURL(item, formatter.request) + '/@@moveup.html'
        myAdapter = zapi.queryMultiAdapter((item, formatter.request),
                                           name='moveup.html')
        if myAdapter is not None and canAccess(myAdapter,'render') and \
           item.__parent__.keys()[0] != item.objectID: # not the first element
            up_html = u'<a href="%s">' %  (up_url) + \
                    u'<img alt="Up" src="%s/Up.png" /></a>' % \
                    (resource_path)
        else:
            up_html = u'<img alt="Up" src="%s/Up_gray.png" />' % \
                    (resource_path)
        retHtml += up_html

        down_url = absoluteURL(item, formatter.request) + '/@@movedown.html'
        myAdapter = zapi.queryMultiAdapter((item, formatter.request),
                                           name='movedown.html')
        if myAdapter is not None and canAccess(myAdapter,'render') and \
           item.__parent__.keys()[-1] != item.objectID: # not the last element
            down_html = u'<a href="%s">' %  (down_url) + \
                      u'<img alt="Down" src="%s/Down.png" /></a>' % \
                      (resource_path)
        else:
            down_html = u'<img alt="Down" src="%s/Down_gray.png" />' %\
                      (resource_path)
        retHtml += down_html
    return retHtml

def getActionBottons(item, formatter):
    """Action Buttons for Overview in Web-Browser
    """
    if type(item) is dict:
        item = item["obj"]
    retHtml = u""
    retHtml += getActionBotton_Detail(item, formatter)
    retHtml += getActionBotton_Edit(item, formatter)
    retHtml += getActionBotton_History(item, formatter)
    retHtml += getActionBotton_Delete(item, formatter)
    retHtml += getActionBotton_UpDown(item, formatter)
    return retHtml

def getSize(item, formatter):
    """display size of object"""
    if type(item) is dict:
        item = item["obj"]
    try:
        return translate(ISized(item).sizeForDisplay())
    except AttributeError:
        return "--"
    except TypeError:
        return "--"

def getModifiedDate(item, formatter):
    """Modified Date for Overview in Web-Browser"""
    if type(item) is dict:
        item = item["obj"]
    try:
        userTZ = getUserTimezone()
        my_formatter = formatter.request.locale.dates.getFormatter(
            'dateTime', 'short')
        timeString = my_formatter.format(userTZ.fromutc(
            IZopeDublinCore(item).modified))
        timeStringHTML = timeString.replace(" ", "&nbsp;")
        my_formatter = formatter.request.locale.dates.getFormatter(
            'dateTime', 'long')
        longTimeString = my_formatter.format(
            userTZ.fromutc(IZopeDublinCore(item).modified))
        #ttid = u"id" + str(abs(hash(timeString)))
        ttid = u"modt" + item.getObjectId()
        tooltip = u"<script type=\"text/javascript\">tt_%s = new YAHOO." \
                u"widget.Tooltip('tt_%s', { autodismissdelay:'15000', " \
                u"context:'%s', text:'%s' });</script>" \
                % (ttid, ttid, ttid, longTimeString)
        resString = u'<span id="%s">%s</span>' % (ttid, timeStringHTML)
    except AttributeError:
        resString = u"---"
        tooltip = u""
    except TypeError:
        resString = u"---"
        tooltip = u""
    return resString + tooltip

def formatEntryDate(entry, formatter):
    """Entry Date for history in Web-Browser"""
    try:
        userTZ = getUserTimezone()
        my_formatter = formatter.request.locale.dates.getFormatter(
            'dateTime', 'short')
        timeString = my_formatter.format(userTZ.fromutc(entry.getTime()))
        timeStringHTML = timeString.replace(" ", "&nbsp;")
        my_formatter = formatter.request.locale.dates.getFormatter(
            'dateTime', 'long')
        longTimeString = my_formatter.format(userTZ.fromutc(entry.getTime()))
        ttid = u"id" + str(abs(hash(entry)))
        tooltip = u"<script type=\"text/javascript\">tt_%s = new YAHOO." \
                u"widget.Tooltip('tt_%s', { autodismissdelay:'15000', " \
                u"context:'%s', text:'%s' });</script>" \
                % (ttid, ttid, ttid, longTimeString)
        resString = u'<span id="%s">%s</span>' % (ttid, timeStringHTML)
    except AttributeError:
        resString = u"---"
        tooltip = u""
    return resString + tooltip

def formatEntryTextSplit(full_text, split_size):
    for line in full_text.splitlines(False):
        pos = 0
        while pos < len(line):
            pos = pos + split_size
            yield line[pos-split_size:pos]+"\n"

def formatEntryText(entry, formatter):
    """Entry Date for history in Web-Browser"""
    textList = entry.getList(['level', 'text'])
    return u"<pre class='history %s' >%s</pre>" % \
           (textList[0],
            u"".join(formatEntryTextSplit(textList[1].strip(), 60)))

def formatEntryLevel(entry, formatter):
    """Entry Date for history in Web-Browser"""
    return entry.getLevel()

def formatEntryRepeatCounter(entry, formatter):
    """Entry Repeat Counter for a history entry"""
    if entry.getRepeatCounter() > 0:
        return str(entry.getRepeatCounter())
    else:
        return ""

def getStateIcon(item, formatter):
    """State Icon of Object"""
    if type(item) is dict:
        item = item["obj"]
    resource_path = getAdapter(formatter.request, name='pics')()
    try:
        icon_name = IState(item).getIconName()
    except Exception, errtxt:
        icon_name = u"Blank_gray.png"
    return u'<img src="%s/%s" />' % (resource_path,
                                       icon_name)

def raw_cell_formatter(value, item, formatter):
    if value is None:
        return u''
    return unicode(value)

def link(view='index.html'):
    """Link to the object for Overview in Web-Browser"""
    def anchor(value, item, formatter):
        """ anchor method will return a html formated anchor"""
        if value is None:
            return u''
        if ISuperclass.providedBy(value):
            item = value
            value = item.ikName
        try:
            myAdapter = zapi.queryMultiAdapter((item, formatter.request),
                                               name=view)
            if myAdapter is not None and canAccess(myAdapter,'render'):
                url = absoluteURL(item, formatter.request) + '/' + view
                return u'<a href="%s">%s</a>' % (url, value)
            else:
#                view = "details.html"
                myAdapter = zapi.queryMultiAdapter((item, formatter.request),
                                                   name="details.html")
                if myAdapter is not None and canAccess(myAdapter,'render'):
                    url = absoluteURL(item, formatter.request) + '/' + "details.html"
                    return u'<a href="%s">%s</a>' % (url, value)
                else:
                    return u'%s' % (value)
        except Exception:
            return u'%s' % (value)
    return anchor

def getTitle(item, formatter):
    """
    Titel for Overview
    """
    if type(item) is dict:
        item = item["obj"]
    try:
        return IBrwsOverview(item).getTitle()
    except TypeError:
        return str(item.__class__.__name__)

def getTypeName(item, formatter):
    """
    Type name of object for Overview
    """
    if type(item) is dict:
        item = item["obj"]
    textTransl = translate(item.shortName,
                           domain='org.ict_ok',
                           context=formatter.request)
    return textTransl

def getHealth(item, formatter):
    if type(item) is dict:
        item = item["obj"]
    """State Icon of Object"""
    if IComponent.providedBy(item):
        try:
            return u"%3.0f %%" % (100.0 * item.get_health())
        except TypeError:
            return u"-"

def getPosition(item, formatter):
    if type(item) is dict:
        item = item["obj"]
    """
    Titel for Overview
    """
    return item.__parent__.keys().index(item.objectID)

def applyChanges(form, content, data):
    # copied from z3c.form.form
    changes = {}
    for name, field in form.fields.items():
        # If the field is not in the data, then go on to the next one
        if name not in data:
            continue
        # Get the datamanager and get the original value
        dm = getMultiAdapter(
            (content, field.field), interfaces.IDataManager)
        oldValue = dm.get()
        # Only update the data, if it is different
        if data[name] is interfaces.NOT_CHANGED:
            pass
        else:
            if dm.get() != data[name]:
                dm.set(data[name])
                # Record the change using information required later
                #changes.setdefault(dm.field.interface, []).append(name)
                changes.setdefault(dm.field.interface, {}).setdefault(name, {})['newval'] = data[name]
                changes.setdefault(dm.field.interface, {}).setdefault(name, {})['oldval'] = oldValue
    return changes

class DateGetterColumn(GetterColumn):
    """Getter columnt that has locale aware sorting."""
    zope.interface.implements(ISortableColumn)
    def getSortKey(self, item, formatter):
        if hasattr(item, 'getTime'):
            return item.getTime()
        else:
            return IZopeDublinCore(item).modified

class TitleGetterColumn(GetterColumn):
    """Getter columnt that has locale aware sorting."""
    zope.interface.implements(ISortableColumn)
    def getSortKey(self, item, formatter):
        return getTitle(item, formatter).upper()
    
class IPsGetterColumn(GetterColumn):
    """Getter columnt that has locale aware sorting."""
    zope.interface.implements(ISortableColumn)
    def getSortKey(self, item, formatter):
        hostIpList = item.getIpList()
        if len(hostIpList) > 0:
            return IP(hostIpList[0])
        return None


# --------------- menu entries -----------------------------


class MSubDetails(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Details')
    viewURL = '@@details.html'
    weight = 10


class MSubSmartView(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Smart view')
    viewURL = '@@smartview.html'
    weight = 12


class MSubOverview(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Overview')
    viewURL = '@@overview.html'
    weight = 10
    def render(self):
        try:
            if len(self.context) > 0:
                return GlobalMenuSubItem.render(self)
        except:
            return None


class MSubReportPdf(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'normal PDF')
    viewURL = '@@reportPdf.html'
    weight = 60


class MSubReportXML(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'report XML')
    viewURL = '@@reportXML.html'
    weight = 70


class MSubHistory(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'History')
    viewURL = '@@history.html'
    weight = 60


class MSubScript(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Script')
    viewURL = '@@python.html'
    weight = 55


class MSubDumpData(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Dump data')
    viewURL = '@@dumpdata.html'
    weight = 69


class MSubExportXmlData(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Export XML')
    viewURL = '@@exportxmldata.html'
    weight = 62


class MSubExportCsvData(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Export CSV')
    viewURL = '@@exportcsvdata.html'
    weight = 62


class MSubExportXlsData(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Export XLS')
    viewURL = '@@exportxlsdata.html'
    weight = 62


class MSubImportCsvData(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Import CSV')
    viewURL = '@@importcsvdata.html'
    weight = 60


class MSubImportXlsData(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Import XLS')
    viewURL = '@@importxlsdata.html'
    weight = 60

class MSubExportAllXlsData(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Export All XLS')
    viewURL = '@@exportallxlsdata.html'
    weight = 55

class MSubImportAllXlsData(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Import All XLS')
    viewURL = '@@importallxlsdata.html'
    weight = 53


class MSubEdit(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Edit')
    viewURL = '@@edit.html'
    weight = 20


class MSubDelete(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Delete')
    viewURL = '@@delete.html'
    weight = 21


class MSubEditEventIf(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Event Interface')
    viewURL = '@@edit_event_if.html'
    weight = 25


class MSubEditContent(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Edit Content')
    viewURL = '@@edit_content.html'
    weight = 30


class MSubAsMindMap(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'as mind map')
    viewURL = '@@as_mindmap.html'
    weight = 100


# --------------- object details ---------------------------


class SuperclassDetails:
    """ Class for Web-Browser-Details
    """
    omit_viewfields = ['objectID', '__name__', 'ref', 'history',
                      'dbgLevel', 'ikEventTarget']
    omit_addfields = ['objectID', 'ikAuthor', '__name__', 'ref', 'history',
                      'dbgLevel', 'ikEventTarget']
    omit_editfields = ['objectID', 'ikAuthor', '__name__', 'ref', 'history',
                       'dbgLevel', 'ikEventTarget']
    _zopeRuntimeInfoFields = (
        "ZopeVersion",
        "PythonVersion",
        "PythonPath",
        "SystemPlatform",
        "PreferredEncoding",
        "FileSystemEncoding",
        "CommandLine",
        "ProcessId"
        )
    _zopeRuntimeInfoUnavailable = _("Unavailable")

    def getHistory(self):
        """
        special format list of the history for web-view
        """
        retList = []
        obj = removeAllProxies(self.context)
        historyList = obj.history
        for entry in historyList:
            tmpList = entry.getList(['date', 'text', 'level', \
                                     'version', 'bgcolor'])
            retList.append(tmpList )
        retList.sort(lambda a, b: cmp(b[0], a[0]))
        return retList

    def dumpData(self):
        """
        pretty print for web-interface
        """
        import pprint
        #obj = removeAllProxies(self.context)
        obj = self.context
        #print "1------------------------------->", obj
        pickleAdapter = IPickle(obj)
        if pickleAdapter:
            return pprint.pformat(pickleAdapter.exportAsDict(), \
                                   width=80, depth=3)
        else:
            return _(u"no pickle adapter")

    def exportXmlData(self):
        """
        export data as XML to the web browser
        """
        from zope.xmlpickle import toxml
        import pickle
        obj = self.context
        pickleAdapter = IPickle(obj)
        if pickleAdapter:
            self.request.response.setHeader('Content-Type', 'application/ict-xml')
            filename = datetime.now().strftime('ictxml_%Y%m%d%H%M%S.xml')
            self.request.response.setHeader('Content-Disposition', 'attachment; filename=\"%s\"' % filename)
            setNoCacheHeaders(self.request.response)
            pickleDump = pickle.dumps(pickleAdapter.exportAsDict())
            #return xmlEscapeWithCData(
                    ##u'<?xml version="1.0" encoding="ISO-8859-1"?>'
                    ##u'<datadump>%s</datadump>',
                    #toxml(pickleDump))
            #return pprint.pformat(pickleAdapter.exportAsDict(), \
                                   #width=60, depth=6)
            return toxml(pickleDump)
        else:
            return _(u"no pickle adapter")

    def getZopeRuntimeInfo(self):
        """get Runtime information from Zope system
        """
        try:
            runtimeinfo = IRuntimeInfo(self.context)
        except TypeError:
            formatted = dict.fromkeys(self._zopeRuntimeInfoFields, 
                                      self._zopeRuntimeInfoUnavailable)
            formatted["Uptime"] = self._zopeRuntimeInfoUnavailable
        else:
            formatted = self._getInfo(runtimeinfo)
        return formatted

    def convertToLocalTimeString(self, argdatetime):
        """Converts to local time
        """
        userTimestmp = convert2UserTimezone(argdatetime)
        return userTimestmp.strftime('%d.%m.%Y %H:%M:%S %Z')
    
    def getModifiedTime(self):
        modTS = IZopeDublinCore(self.context).modified
        if modTS is not None:
            return convert2UserTimezone(IZopeDublinCore(self.context).modified)
        else:
            return None
    
    def convert2UserTimezone(self, timest):
        return convert2UserTimezone(timest)

    def vocabValue(self, vocabName=None, token=None):
        if vocabName is None:
            return None
        if token is None:
            return None
        vocabReg = vocabulary.getVocabularyRegistry()
        if vocabReg is not None:
            vocab = vocabReg.get(self.request, vocabName)
            if vocab is not None:
                try:
                    vocabTerm = vocab.getTerm(token)
                    if vocabTerm:
                        return vocabTerm.title
                except LookupError:
                    return None
        return None
    
    def getHrefTitle(self, obj, displayShort=False):
        href = zapi.absoluteURL(obj, self.request)
        if hasattr(obj, 'getDisplayTitle'):
            title = obj.getDisplayTitle()
        else:
            title = obj.ikName
        if displayShort and hasattr(obj, 'shortName'):
            return u'<a href="%s">%s [%s]</a>' % (href, title, obj.shortName)
        else:
            return u'<a href="%s">%s</a>' % (href, title)

    def getStateIconClass(self, obj):
        try:
            stateAdapter = getAdapter(obj, IState)
            if stateAdapter:
                stateNum = stateAdapter.getStateOverview(-1)
                if stateNum >= 0:
                    return u"icon-%s%d" % (obj.getShortname(), stateNum)
                else:
                    return u"icon-%s" % (obj.getShortname())
        except ComponentLookupError, err:
            return u"icon-%s" % (obj.getShortname())
        except AttributeError, err:
            return u"icon-%s" % (obj.getShortname())
        return u"icon-%s" % (obj.getShortname())

    def fsearchLink(self, text, arg_key=None):
        if arg_key:
            key = arg_key
        else:
            key = u'%s' % (text)
        quoter = URLQuote(key)
        return u'<a href="/@@fsearch?key=%s">%s</a>' % (quoter.quote(), text)
        

    def getTabClass(self):
        if hasattr(self.request, 'tabClass'):
            return self.request.tabClass
        return 'cb_wht'

    def getNextTabClass(self):
        if hasattr(self.request, 'tabClass'):
            if self.request.tabClass == 'cb_wht':
                self.request.tabClass = 'cb_ixl'
            else:
                self.request.tabClass = 'cb_wht'
        else:
            self.request.tabClass = 'cb_wht'
        return self.request.tabClass

    def reportPdf(self):
        filename = datetime.now().strftime('ictrpt_%Y%m%d%H%M%S.pdf')
        f_handle, f_name = tempfile.mkstemp(filename)
        authorStr = self.request.principal.title
        my_formatter = self.request.locale.dates.getFormatter(
            'dateTime', 'medium')
        userTZ = getUserTimezone()
        longTimeString = my_formatter.format(\
            userTZ.fromutc(datetime.utcnow()))
        versionStr = "%s [%s]" % (longTimeString, getIkVersion())
        self.context.generatePdf(f_name, authorStr, versionStr,request=self.request)
        self.request.response.setHeader('Content-Type', 'application/pdf')
        self.request.response.setHeader(\
            'Content-Disposition',
            'attachment; filename=\"%s\"' % filename)
        setNoCacheHeaders(self.request.response)
        datafile = open(f_name, "r")
        dataMem = datafile.read()
        datafile.close()
        os.remove(f_name)
        return dataMem
    
    def reportXML(self):
        filename = datetime.now().strftime('ict_%Y%m%d%H%M%S.xml')
        f_handle, f_name = tempfile.mkstemp(filename)
        authorStr = self.request.principal.title
        my_formatter = self.request.locale.dates.getFormatter(
            'dateTime', 'medium')
        userTZ = getUserTimezone()
        longTimeString = my_formatter.format(\
            userTZ.fromutc(datetime.utcnow()))
        versionStr = "%s [%s]" % (longTimeString, getIkVersion())
        self.context.generateXML(f_name, authorStr, versionStr)
        self.request.response.setHeader('Content-Type', 'application/xml')
        self.request.response.setHeader(\
            'Content-Disposition',
            'attachment; filename=\"%s\"' % filename)
        setNoCacheHeaders(self.request.response)
        datafile = open(f_name, "r")
        dataMem = datafile.read()
        datafile.close()
        os.remove(f_name)
        return dataMem
    
    def getFocusContent(self):
        return (1000,
                self.__class__.__name__,
                self,
                self.context,
                u"<div>%s</div>" % self.context.ikName)

    def asMindmap(self):
        self.request.response.setHeader('Content-Type', 'text/html')
        mindMapUtil = queryUtility(IAdmUtilMindMap, name="AdmUtilMindMap")
        from zope.proxy import removeAllProxies
        mindMapUtil.context = removeAllProxies(self.context)
        return mindMapUtil.asMindmap(request=self.request)
    
    def asMindmapData(self):
        #self.request.response.setHeader('Content-Type', 'text/html')
        mindMapUtil = queryUtility(IAdmUtilMindMap, name="AdmUtilMindMap")
        from zope.proxy import removeAllProxies
        mindMapUtil.context = removeAllProxies(self.context)
        return mindMapUtil.asMindmapData(request=self.request)

    def getOrganizationForMacAddress(self, macAddress):
        macAddressDb = queryUtility(IAdmUtilMacAddressDb, name="AdmUtilMacAddressDb")
        return macAddressDb
        #return u'Apfel'

    def macAddressUtility(self):
        return queryUtility(IAdmUtilMacAddressDb, name="AdmUtilMacAddressDb")


class IctGetterColumn(GetterColumn):
    def getSortKey(self, item, formatter):
        if ISuperclass.providedBy(self.getter(item, formatter)):
            key = self.getter(item, formatter).ikName
            if key is not None:
                key = key.lower()
            else:
                key = u'\xffff' * 80
            return key
        else:
            key = self.getter(item, formatter)
            if key is not None:
                key = key.lower()
            else:
                key = u'\xffff' * 80
            return key


class FocusDetails(SuperclassDetails):
    """
    """
    def getHtmlList(self):
        retList = []
        uidutil = queryUtility(IIntIds)
        for (oid, oobj) in uidutil.items():
            if IFocus.providedBy(oobj.object):
                try:
                    obj_view = getMultiAdapter((oobj.object, self.request), name='focus.html')
                    retList.append(obj_view.getFocusContent())
                except ComponentLookupError, err:
                    pass
        retList.sort(key=operator.itemgetter(0))
        return retList


class DumpData:
    """ Class for Web-Browser-Details
    """
    def dumpData(self):
        """
        pretty print for web-interface
        """
        import pprint
        obj = removeAllProxies(self.context)
        pickleAdapter = IPickle(obj)
        if pickleAdapter:
            return pprint.pformat(pickleAdapter.exportAsDict(), \
                                   width = 60, depth = 6)
        else:
            return _(u"no pickle adapter")

class MoveUp(BrowserPagelet):
    def update(self):
        parentObj = self.context.__parent__
        itemIndex = parentObj.keys().index(self.context.objectID)
        if itemIndex > 0:
            keyList = [i for i in parentObj.keys()]
            keyList.remove(self.context.objectID)
            keyList.insert(itemIndex - 1, self.context.objectID)
            dd1=parentObj
            d2=IOrderedContainer(dd1)
            parentObj.updateOrder(keyList)
    def render(self):
        parentObj = self.context.__parent__
        parentUrl = absoluteURL(parentObj, self.request) + '/@@overview.html'
        return self.request.response.redirect(parentUrl)

class MoveDown(BrowserPagelet):
    def update(self):
        parentObj = self.context.__parent__
        itemIndex = parentObj.keys().index(self.context.objectID)
        if itemIndex + 1 < len(parentObj):
            keyList = [i for i in parentObj.keys()]
            keyList.remove(self.context.objectID)
            keyList.insert(itemIndex + 1, self.context.objectID)
            parentObj.updateOrder(keyList)
    def render(self):
        parentObj = self.context.__parent__
        parentUrl = absoluteURL(parentObj, self.request) + '/@@overview.html'
        return self.request.response.redirect(parentUrl)

class AddDashboard(BrowserPagelet):
    def update(self):
        userProps = AdmUtilUserProperties(self.request.principal)
        userProps.dashboard_objs.add(self.context, self.request)
        userProps.mapping._p_changed = True

    def render(self):
        return self.request.response.redirect('./@@overview.html')


class DelDashboard(BrowserPagelet):
    def update(self):
        userProps = AdmUtilUserProperties(self.request.principal)
        userProps.dashboard_objs.remove(self.context, self.request)
        userProps.mapping._p_changed = True
        
    def render(self):
        return self.request.response.redirect('./@@overview.html')


# --------------- forms ------------------------------------


class DisplayForm(layout.FormLayoutSupport, form.DisplayForm):
    """Widgets in Display-Mode"""
    form.extends(form.DisplayForm)
    label = _(u'View Superclass')
    factory = Superclass
    omitFields = SuperclassDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class AddForm(layout.FormLayoutSupport, form.AddForm):
    """Add form."""

    form.extends(form.AddForm)
    label = _(u'Add Superclass')
    factory = Superclass
    omitFields = SuperclassDetails.omit_addfields
    fields = fieldsForFactory(factory, omitFields)

    def nextURL(self):
        """ forward the browser """
        return absoluteURL(self.context[self._newObjectID],
                           self.request)

    def create(self, data):
        """ will create the object """
        obj = self.factory(**data)
        self.newdata = data
        IBrwsOverview(obj).setTitle(data['ikName'])
        obj.__post_init__()
        return obj
    
    def add(self, obj):
        """ will store the new one in object tree """
        travp = self.context
        # store obj id for nextURL()
        self._newObjectID = obj.objectID
        while IPagelet.providedBy(travp):
            travp = self.context.__parent__
        travp[obj.objectID] = obj
        if hasattr(obj, "store_refs"):
            obj.store_refs(**self.newdata)
        # workaround for gocept.objectquery
        #import transaction
        #transaction.savepoint()
        return obj


class EditForm(layout.FormLayoutSupport, form.EditForm):
    """ Edit form """

    form.extends(form.EditForm)
    label = _(u'Edit Superclass')
    factory = Superclass
    omitFields = SuperclassDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)
    
    def applyChanges(self, data):
        content = self.getContent()
        changes = applyChanges(self, content, data)
        # ``changes`` is a dictionary; if empty, there were no changes
        if changes:
            # Construct change-descriptions for the object-modified event
            descriptions = []
            for interface, attrs in changes.items():
                if interface == IAdmUtilEvent:
                    #print "##### Event #######"
                    pass
                elif IEventIfSuperclass.isEqualOrExtendedBy(interface):
                    #print "##### Superclass #######"
                    pass
                names = attrs.keys()
                #for attr in attrs:
                    #print "attr: %s (I:%s)" % (attr, interface)
                    #print "   old: ", attrs[attr]['oldval']
                    #print "   new: ", attrs[attr]['newval']
                descriptions.append(Attributes(interface, *names))
            # Send out a detailed object-modified event
            zope.event.notify(ObjectModifiedEvent(content, *descriptions))
        # workaround for gocept.objectquery
        import transaction
        transaction.savepoint()
        return changes



class DeleteForm(layout.FormLayoutSupport, form.Form):
    """ Delete the net """
    
    form.extends(form.Form)
    label = _(u"Delete this object?")
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this object: '%s'?") % \
               IBrwsOverview(self.context).getTitle()
        
    @button.buttonAndHandler(u'Delete')
    def handleDelete(self, action):
        """delete was pressed"""
        if ISuperclass.providedBy(self.context):
            parent = self.context.__parent__
            del parent[self.context.objectID]
            self.deleted = True
            self.context = parent
            url = absoluteURL(parent, self.request)
            self.request.response.redirect(url)
            # workaround for gocept.objectquery
            import transaction
            transaction.savepoint()

    @button.buttonAndHandler(u'Cancel')
    def handleCancel(self, action):
        """cancel was pressed"""
        url = absoluteURL(self.context, self.request)
        self.request.response.redirect(url)

    def update(self):
        """update all widgets"""
        if ISuperclass.providedBy(self.context):
            self.label = self.getTitle()
        form.Form.update(self)


class DeleteFolderForm(layout.FormLayoutSupport, form.Form):
    """
    """
    @button.buttonAndHandler(u'Cancel')
    def handleCancel(self, action):
        """cancel was pressed"""
        url = absoluteURL(self.context, self.request)
        self.request.response.redirect(url)

    @button.buttonAndHandler(u'Delete')
    def handleDelete(self, action):
        """delete was pressed"""
        if ISuperclass.providedBy(self.context):
            parent = self.context.__parent__
            parentList = list(parent.items())
            oname = [oname for oname, oobj in parentList \
                     if oobj == self.context][0]
            del parent[oname]
            self.deleted = True
            self.context = parent
            url = absoluteURL(parent, self.request)
            self.request.response.redirect(url)

    def update(self):
        """update all widgets"""
        if ISuperclass.providedBy(self.context):
            self.label = self.context.ikName
        form.Form.update(self)


class Overview(BrowserPagelet):
    """Overview Pagelet"""
    columns = (
        GetterColumn(title="",
                     getter=getStateIcon,
                     cell_formatter=raw_cell_formatter),
        GetterColumn(title=_('Health'),
                     getter=getHealth),
        #TitleGetterColumn(title=_('Title'),
                          #getter=getTitle),
        IctGetterColumn(title=_('Title'),
                     getter=getTitle,
                     cell_formatter=link('overview.html')),
        GetterColumn(title=_('Modified'),
                     getter=getModifiedDate,
                     subsort=True,
                     cell_formatter=raw_cell_formatter),
        GetterColumn(title=_('Actions'),
                     getter=getActionBottons,
                     cell_formatter=raw_cell_formatter),
        )
    pos_column_index = 1
    sort_columns = [1, 2, 3]
    status = None
    firstSortOn = _('Title') 
    
    def convert2UserTimezone(self, argTS):
        if argTS is not None:
            return convert2UserTimezone(argTS)
        else:
            return None

    def getTabClass(self):
        if hasattr(self.request, 'tabClass'):
            return self.request.tabClass
        return 'cb_wht'

    def getNextTabClass(self):
        if hasattr(self.request, 'tabClass'):
            if self.request.tabClass == 'cb_wht':
                self.request.tabClass = 'cb_ixl'
            else:
                self.request.tabClass = 'cb_wht'
        else:
            self.request.tabClass = 'cb_wht'
        return self.request.tabClass
    
    def objs(self):
        """List of Content objects"""
        retList = []
#        try:
        for obj in self.context.values():
            #if ISuperclass.providedBy(obj):
            retList.append(obj)
#        except:
#            pass
        return retList

    def table(self, arg_objList=None):
        """ Properties of table are defined here"""
        if arg_objList is None:
            objList = self.objs()
        else:
            if type(arg_objList) is list:
                objList = arg_objList
            else:
                objList = []
        columnList = list(self.columns)
        containerIsOrderd = IOrderedContainer.providedBy(self.context)
        if containerIsOrderd:
            getterC = GetterColumn(title=_('Pos'), getter=getPosition)
            #directlyProvides(getterC, ISortableColumn)
            columnList.insert(self.pos_column_index, getterC)
            #directlyProvides(columnList[3], ISortableColumn)
            #StandaloneFullFormatter
            #BatchedFormatter
            formatter = BatchedFormatter(
                self.context, self.request, objList,
                columns=columnList,
                sort_on=((_('Pos'), False),),
                batch_size=50)
        else:
            for i in self.sort_columns:
                directlyProvides(columnList[i], ISortableColumn)
            #formatter = StandaloneFullFormatter(
                #self.context, self.request, self.objs(),
                #columns=columnList, sort_on=((_('Title'), False),))
            #StandaloneFullFormatter
            #BatchedFormatter
            formatter = BatchedFormatter(
                self.context, self.request, objList,
                columns=columnList,
                sort_on=((self.firstSortOn, False),),
                batch_size=50)
        formatter.cssClasses['table'] = 'listing'
        return formatter()



class ViewDashboard(Overview):
    label = _(u"Dashboard")
    def update(self):
        self.label = _(u"Dashboard of %s") % \
            self.request.principal.title
        Overview.update(self)
    def objs(self):
        """List of Content objects"""
        retList = []
        userProps = AdmUtilUserProperties(self.request.principal)
        for dashboardItem in userProps.dashboard_objs:
            myObj = dashboardItem.getObject(some_obj=self,
                                            arg_request=self.request)
            if myObj is not None:
                retList.append(myObj)
        return retList

class History(BrowserPagelet):
    """History Pagelet"""
    columns = (
        GetterColumn(title=_('Level'),
                     getter=formatEntryLevel),
        DateGetterColumn(title=_('Date'),
                     getter=formatEntryDate,
                     cell_formatter=raw_cell_formatter),
        GetterColumn(title=_('R'),
                     getter=formatEntryRepeatCounter),
        GetterColumn(title=_('Text'),
                     getter=formatEntryText,
                     cell_formatter=raw_cell_formatter),
                     )
    def objs(self):
        """List of Content objects"""
        obj = removeAllProxies(self.context)
        historyList = obj.history.get()
        return historyList

    def table(self):
        """ Properties of table are defined here"""
        directlyProvides(self.columns[0], ISortableColumn)
        #directlyProvides(self.columns[1], ISortableColumn)
        directlyProvides(self.columns[3], ISortableColumn)
        formatter = StandaloneFullFormatter(
            self.context, self.request, self.objs(),
            columns=self.columns, sort_on=((_('Date'), True),))
        formatter.cssClasses['table'] = 'listing'
        return formatter()


class EditContent(BrowserPagelet):
    """Overview Pagelet"""
    columns = (
        CheckboxColumn(_(' ')),
        GetterColumn(title=_('Title'),
                     getter=getTitle,
                     cell_formatter=link('edit.html')),
        GetterColumn(title="",
                     getter=getStateIcon,
                     cell_formatter=raw_cell_formatter),
        GetterColumn(title=_('Modified'),
                     getter=getModifiedDate,
                     cell_formatter=raw_cell_formatter),
        )

    status = None

    def objs(self):
        """List of Content objects"""
        return [obj
                for obj in self.context.values()
                if ISuperclass.providedBy(obj)]

    def table(self):
        """ Properties of table are defined here"""
        directlyProvides(self.columns[1], ISortableColumn)
        directlyProvides(self.columns[3], ISortableColumn)
        formatter = StandaloneFullFormatter(
            self.context, self.request, self.objs(),
            columns=self.columns, sort_on=((_('Title'), False),))
        formatter.cssClasses['table'] = 'listing'
        return formatter()
    
    def update(self):
        """update all widgets"""
        if 'DELETE' in self.request:
            if self.request.get('confirm_delete') != 'yes':
                self.status = _('You did not confirm the deletion correctly.')
                return
            if 'selected' in self.request:
                for myid in self.request['selected']:
                    try:
                        del self.context[myid]
                    except KeyError:
                        pass
                self.status = _('Objects were successfully deleted.')
            else:
                self.status = _('No objects were selected.')
