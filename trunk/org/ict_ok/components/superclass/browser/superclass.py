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

# phython imports
from datetime import datetime

# zope imports
import zope.interface
from zope.app import zapi
from pytz import timezone
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
from zope.component import getMultiAdapter
#import zope.event
from zope.lifecycleevent import Attributes, ObjectModifiedEvent
from zope.app.rotterdam.xmlobject import translate, setNoCacheHeaders
from zope.app.container.interfaces import IOrderedContainer

# z3c imports
from z3c.form import button, field, form, interfaces
from z3c.formui import layout
from z3c.pagelet.interfaces import IPagelet
from z3c.pagelet.browser import BrowserPagelet

# zc imports
from zc.table.column import Column, GetterColumn
from zc.table.table import StandaloneFullFormatter
from zc.table.interfaces import ISortableColumn

# ict_ok import
from org.ict_ok.components.superclass.interfaces import IPickle, ISuperclass
from org.ict_ok.components.superclass.superclass import Superclass
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.components.supernode.interfaces import IState
from org.ict_ok.admin_utils.usermanagement.usermanagement import \
     AdmUtilUserProperties
from org.ict_ok.admin_utils.eventcrossbar.interfaces import \
     IAdmUtilEvent
from org.ict_ok.components.superclass.interfaces import \
     IEventIfSuperclass

# ict_ok imports
from org.ict_ok.skin.menu import GlobalMenuSubItem

_ = MessageFactory('org.ict_ok')
berlinTZ = timezone('Europe/Berlin')


# --------------- helper functions -------------------------


class CheckboxColumn(Column):
    """Special Checkbox Column"""
    def renderCell(self, item, formatter):
        """render a checkbox field"""
        widget = (u'<input type="checkbox" '
                  u'name="selected:list" value="%s">')
        return widget % (item.objectID)

def getActionBottons(item, formatter):
    """Action Buttons for Overview in Web-Browser"""
    #import pdb
    #pdb.set_trace()
    retHtml = u""
    parentIsOrderd = IOrderedContainer.providedBy(item.__parent__)
    resource_path = getAdapter(formatter.request, name='pics')()

    view_url = absoluteURL(item, formatter.request) + '/@@details.html'
    myAdapter = zapi.queryMultiAdapter((item, formatter.request),
                                       name='details.html')
    if myAdapter is not None and canAccess(myAdapter,'render'):
        view_html = u'<a href="%s"><img alt="Info" src="%s/Info.png" /></a>' % \
                  (view_url, resource_path)
    else:
        view_html = u'<img alt="Details" src="%s/Info_gr.png" />' % (resource_path)
    retHtml += view_html

    edit_url = absoluteURL(item, formatter.request) + '/@@edit.html'
    myAdapter = zapi.queryMultiAdapter((item, formatter.request),
                                       name='edit.html')
    if myAdapter is not None and canAccess(myAdapter,'render'):
        edit_html = u'<a href="%s"><img alt="Edit" src="%s/Hand.png" /></a>' % \
                  (edit_url, resource_path)
    else:
        edit_html = u'<img alt="Edit" src="%s/Hand_gr.png" />' % (resource_path)
    retHtml += edit_html

    hist_url = absoluteURL(item, formatter.request) + '/@@history.html'
    myAdapter = zapi.queryMultiAdapter((item, formatter.request),
                                       name='history.html')
    if myAdapter is not None and canAccess(myAdapter,'render'):
        hist_html = u'<a href="%s"><img alt="History" src="%s/Doc.png" /></a>' % \
                  (hist_url, resource_path)
    else:
        hist_html = u'<img alt="History" src="%s/Doc_gr.png" />' % (resource_path)
    retHtml += hist_html

    trash_url = absoluteURL(item, formatter.request) + '/@@delete.html'
    myAdapter = zapi.queryMultiAdapter((item, formatter.request),
                                       name='delete.html')
    if myAdapter is not None and canAccess(myAdapter,'render'):
        trash_html = u'<a href="%s"><img alt="Trash" src="%s/Trash.png" /></a>' % \
                   (trash_url, resource_path)
    else:
        trash_html = u'<img alt="Trash" src="%s/Trash_gr.png" />' % (resource_path)
    retHtml += trash_html

    if parentIsOrderd:
        up_url = absoluteURL(item, formatter.request) + '/@@moveup.html'
        myAdapter = zapi.queryMultiAdapter((item, formatter.request),
                                           name='moveup.html')
        if myAdapter is not None and canAccess(myAdapter,'render') and \
           item.__parent__.keys()[0] != item.objectID: # not the first element
            up_html = u'<a href="%s"><img alt="Up" src="%s/Up.png" /></a>' % \
                       (up_url, resource_path)
        else:
            up_html = u'<img alt="Up" src="%s/Up_gray.png" />' % (resource_path)
        retHtml += up_html

        down_url = absoluteURL(item, formatter.request) + '/@@movedown.html'
        myAdapter = zapi.queryMultiAdapter((item, formatter.request),
                                           name='movedown.html')
        if myAdapter is not None and canAccess(myAdapter,'render') and \
           item.__parent__.keys()[-1] != item.objectID: # not the last element
            down_html = u'<a href="%s"><img alt="Down" src="%s/Down.png" /></a>' % \
                       (down_url, resource_path)
        else:
            down_html = u'<img alt="Down" src="%s/Down_gray.png" />' % (resource_path)
        retHtml += down_html

    return retHtml

def getSize(item, formatter):
    """display size of object"""
    try:
        return translate(ISized(item).sizeForDisplay())
    except AttributeError:
        return "--"

def getModifiedDate(item, formatter):
    """Modified Date for Overview in Web-Browser"""
    try:
        my_formatter = formatter.request.locale.dates.getFormatter(
            'dateTime', 'short')
        timeString = my_formatter.format(berlinTZ.fromutc(
            IZopeDublinCore(item).modified))
        timeStringHTML = timeString.replace(" ", "&nbsp;")
        my_formatter = formatter.request.locale.dates.getFormatter(
            'dateTime', 'long')
        longTimeString = my_formatter.format(
            berlinTZ.fromutc(IZopeDublinCore(item).modified))
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
    return resString + tooltip

def formatEntryDate(entry, formatter):
    """Entry Date for history in Web-Browser"""
    try:
        my_formatter = formatter.request.locale.dates.getFormatter(
            'dateTime', 'short')
        timeString = my_formatter.format(berlinTZ.fromutc(entry.getTime()))
        timeStringHTML = timeString.replace(" ", "&nbsp;")
        my_formatter = formatter.request.locale.dates.getFormatter(
            'dateTime', 'long')
        longTimeString = my_formatter.format(berlinTZ.fromutc(entry.getTime()))
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
    resource_path = getAdapter(formatter.request, name='pics')()
    try:
        icon_name = IState(item).getIconName()
    except Exception, errtxt:
        icon_name = u"Blank_gray.png"
    return u'<img src="%s/%s" />' % (resource_path,
                                       icon_name)

def raw_cell_formatter(value, item, formatter):
    return unicode(value)

def link(view='index.html'):
    """Link to the object for Overview in Web-Browser"""
    def anchor(value, item, formatter):
        """ anchor method will return a html formated anchor"""
        url = absoluteURL(item, formatter.request) + '/' + view
        return u'<a href="%s">%s</a>' % (url, value)
    return anchor

def getTitel(item, formatter):
    """
    Titel for Overview
    """
    try:
        return IBrwsOverview(item).getTitle()
    except TypeError:
        return str(item.__class__.__name__)

def getPosition(item, formatter):
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
        if dm.get() != data[name]:
            dm.set(data[name])
            # Record the change using information required later
            #changes.setdefault(dm.field.interface, []).append(name)
            changes.setdefault(dm.field.interface, {}).setdefault(name, {})['newval'] = data[name]
            changes.setdefault(dm.field.interface, {}).setdefault(name, {})['oldval'] = oldValue
    return changes


# --------------- menu entries -----------------------------


class MSubDetails(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Details')
    viewURL = '@@details.html'
    weight = 10


class MSubOverview(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Overview')
    viewURL = '@@overview.html'
    weight = 10


class MSubHistory(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'History')
    viewURL = '@@history.html'
    weight = 50


class MSubScript(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Script')
    viewURL = '@@python.html'
    weight = 55


class MSubDumpData(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Dump data')
    viewURL = '@@dumpdata.html'
    weight = 60


class MSubExportXmlData(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Export XML')
    viewURL = '@@exportxmldata.html'
    weight = 60


class MSubEdit(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Edit')
    viewURL = '@@edit.html'
    weight = 20


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


# --------------- object details ---------------------------


class SuperclassDetails:
    """ Class for Web-Browser-Details
    """
    omit_viewfields = ['objectID', 'ikNotes', 'ref', 'history',
                      'dbgLevel', 'ikEventTarget']
    omit_addfields = ['objectID', 'ikAuthor', 'ikNotes', 'ref', 'history',
                      'dbgLevel', 'ikEventTarget']
    omit_editfields = ['objectID', 'ikAuthor', 'ikNotes', 'ref', 'history',
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
        
        TODO: migrate to better location
        """
        localTZ = timezone('Europe/Berlin')
        localTimestmp = argdatetime.astimezone(localTZ)
        return localTimestmp.strftime('%d.%m.%Y %H:%M:%S %Z')


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
    fields = field.Fields(ISuperclass).omit(\
        *SuperclassDetails.omit_viewfields)


class AddForm(layout.FormLayoutSupport, form.AddForm):
    """Add form."""

    form.extends(form.AddForm)
    label = _(u'Add Superclass')
    fields = field.Fields(ISuperclass).omit(\
        *SuperclassDetails.omit_addfields)
    # factory stores the class, which will instanciated in AddForm.create()
    factory = Superclass

    def nextURL(self):
        """ forward the browser """
        return absoluteURL(self.context[self._newObjectID],
                           self.request)

    def create(self, data):
        """ will create the object """
        obj = self.factory(**data)
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
        return obj


class EditForm(layout.FormLayoutSupport, form.EditForm):
    """ Edit form """

    form.extends(form.EditForm)
    label = _(u'Edit Superclass')
    fields = field.Fields(ISuperclass).omit(\
        *SuperclassDetails.omit_editfields)
    
    def applyChanges(self, data):
        content = self.getContent()
        changes = applyChanges(self, content, data)
        # ``changes`` is a dictionary; if empty, there were no changes
        if changes:
            #import pdb;pdb.set_trace()
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
        return changes



class DeleteForm(layout.FormLayoutSupport, form.Form):
    """ Delete the net """
    
    form.extends(form.Form)
    label = _(u"Delete this object?")
    
    def getTitel(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this object: '%s'?") % \
               IBrwsOverview(self.context).getTitle()
        
    @button.buttonAndHandler(u'Delete')
    def handleDelete(self, action):
        """delete was pressed"""
        if ISuperclass.providedBy(self.context):
            parent = self.getContent().__parent__
            del parent[self.context.objectID]
            self.deleted = True
            self.context = parent
            url = absoluteURL(parent, self.request)
            self.request.response.redirect(url)

    @button.buttonAndHandler(u'Cancel')
    def handleCancel(self, action):
        """cancel was pressed"""
        url = absoluteURL(self.context, self.request)
        self.request.response.redirect(url)

    def update(self):
        """update all widgets"""
        if ISuperclass.providedBy(self.context):
            self.label = self.getTitel()
        form.Form.update(self)



class Overview(BrowserPagelet):
    """Overview Pagelet"""
    columns = (
        GetterColumn(title="",
                     getter=getStateIcon,
                     cell_formatter=raw_cell_formatter),
        GetterColumn(title=_('Title'),
                     getter=getTitel),
        GetterColumn(title=_('Modified On'),
                     getter=getModifiedDate,
                     subsort=True,
                     cell_formatter=raw_cell_formatter),
        GetterColumn(title=_('Actions'),
                     getter=getActionBottons,
                     cell_formatter=raw_cell_formatter),
        )

    status = None

    def objs(self):
        """List of Content objects"""
        retList = []
        try:
            for obj in self.context.values():
                if ISuperclass.providedBy(obj):
                    retList.append(obj)
        except:
            pass
        return retList

    def table(self):
        """ Properties of table are defined here"""
        columnList = list(self.columns)
        containerIsOrderd = IOrderedContainer.providedBy(self.context)
        directlyProvides(columnList[1], ISortableColumn)
        directlyProvides(columnList[2], ISortableColumn)
        if containerIsOrderd:
            columnList.insert(1, GetterColumn(title=_('Pos'),
                                              getter=getPosition))
            directlyProvides(columnList[3], ISortableColumn)
            formatter = StandaloneFullFormatter(
                self.context, self.request, self.objs(),
                columns=columnList, sort_on=((_('Pos'), False),))
        else:
            formatter = StandaloneFullFormatter(
                self.context, self.request, self.objs(),
                columns=columnList, sort_on=((_('Title'), False),))
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

class DateGetterColumn(GetterColumn):
    """Getter columnt that has locale aware sorting."""
    zope.interface.implements(ISortableColumn)
    def getSortKey(self, item, formatter):
        return item.getTime()

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
                     getter=getTitel,
                     cell_formatter=link('edit.html')),
        GetterColumn(title="",
                     getter=getStateIcon,
                     cell_formatter=raw_cell_formatter),
        GetterColumn(title=_('Modified On'),
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
                    del self.context[myid]
                self.status = _('Objects were successfully deleted.')
            else:
                self.status = _('No objects were selected.')
