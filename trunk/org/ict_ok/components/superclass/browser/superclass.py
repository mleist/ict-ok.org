# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
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

# zope imports
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
from zope.app.catalog.interfaces import ICatalog
from zope.app.intid.interfaces import IIntIds

# z3c imports
from z3c.form import button, field, form
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
     AdmUtilUserDashboardItem, AdmUtilUserDashboardSet, AdmUtilUserProperties

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
    resource_path = getAdapter(formatter.request, name='pics')()

    view_url = absoluteURL(item, formatter.request) + '/@@details.html'
    myAdapter = zapi.queryMultiAdapter((item, formatter.request),
                                       name='details.html')
    if myAdapter is not None and canAccess(myAdapter,'render'):
        view_html = u'<a href="%s"><img alt="Info" src="%s/Info.png" /></a>' % \
                  (view_url, resource_path)
    else:
        view_html = u'<img alt="Info" src="%s/Info_gr.png" />' % (resource_path)

    edit_url = absoluteURL(item, formatter.request) + '/@@edit.html'
    myAdapter = zapi.queryMultiAdapter((item, formatter.request),
                                       name='edit.html')
    if myAdapter is not None and canAccess(myAdapter,'render'):
        edit_html = u'<a href="%s"><img alt="Edit" src="%s/Hand.png" /></a>' % \
                  (edit_url, resource_path)
    else:
        edit_html = u'<img alt="Info" src="%s/Hand_gr.png" />' % (resource_path)

    hist_url = absoluteURL(item, formatter.request) + '/@@history.html'
    myAdapter = zapi.queryMultiAdapter((item, formatter.request),
                                       name='history.html')
    if myAdapter is not None and canAccess(myAdapter,'render'):
        hist_html = u'<a href="%s"><img alt="History" src="%s/Doc.png" /></a>' % \
                  (hist_url, resource_path)
    else:
        hist_html = u'<img alt="Info" src="%s/Doc_gr.png" />' % (resource_path)

    trash_url = absoluteURL(item, formatter.request) + '/@@delete.html'
    myAdapter = zapi.queryMultiAdapter((item, formatter.request),
                                       name='delete.html')
    if myAdapter is not None and canAccess(myAdapter,'render'):
        trash_html = u'<a href="%s"><img alt="Trash" src="%s/Trash.png" /></a>' % \
                   (trash_url, resource_path)
    else:
        trash_html = u'<img alt="Info" src="%s/Trash_gr.png" />' % (resource_path)
    return view_html + edit_html + hist_html + trash_html

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
        resString = u'<span id="%s">%s</span>' % (ttid, timeString)
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
        my_formatter = formatter.request.locale.dates.getFormatter(
            'dateTime', 'long')
        longTimeString = my_formatter.format(berlinTZ.fromutc(entry.getTime()))
        ttid = u"id" + str(abs(hash(timeString)))
        tooltip = u"<script type=\"text/javascript\">tt_%s = new YAHOO." \
                u"widget.Tooltip('tt_%s', { autodismissdelay:'15000', " \
                u"context:'%s', text:'%s' });</script>" \
                % (ttid, ttid, ttid, longTimeString)
        resString = u'<span id="%s">%s</span>' % (ttid, timeString)
    except AttributeError:
        resString = u"---"
        tooltip = u""
    return resString + tooltip

def formatEntryText(entry, formatter):
    """Entry Date for history in Web-Browser"""
    return entry.getText()

def formatEntryLevel(entry, formatter):
    """Entry Date for history in Web-Browser"""
    return entry.getLevel()

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


# --------------- menu entries -----------------------------


class MSubDetails(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Details')
    viewURL = 'details.html'
    weight = 10


class MSubOverview(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Overview')
    viewURL = 'overview.html'
    weight = 10


class MSubHistory(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'History')
    viewURL = 'history.html'
    weight = 50


class MSubEdit(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Edit')
    viewURL = 'edit.html'
    weight = 20


class MSubEditContent(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Edit Content')
    viewURL = 'edit_content.html'
    weight = 30


# --------------- object details ---------------------------


class SuperclassDetails:
    """ Class for Web-Browser-Details
    """
    omit_viewfields = ['ikNotes', 'ref', 'history',
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
        obj = removeAllProxies(self.context)
        #print "1------------------------------->", obj
        pickleAdapter = IPickle(obj)
        if pickleAdapter:
            return pprint.pformat(pickleAdapter.exportAsDict(), \
                                   width=60, depth=6)
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
                                   width=60, depth=6)
        else:
            return _(u"no pickle adapter")


class AddDashboard(BrowserPagelet):
    def update(self):
        #import pdb; pdb.set_trace()
        #testObjId = self.context.getObjectId()
        userProps = AdmUtilUserProperties(self.request.principal)
        #userProps.dashboard_obj_ids.add(testObjId)
        userProps.dashboard_objs.add(self.context, self.request)
        userProps.mapping._p_changed=True

    def render(self):
        return self.request.response.redirect('./overview.html')


class DelDashboard(BrowserPagelet):
    def update(self):
        #import pdb; pdb.set_trace()
        #testObjId = self.context.getObjectId()
        userProps = AdmUtilUserProperties(self.request.principal)
        #if testObjId in userProps.dashboard_obj_ids:
            #userProps.dashboard_obj_ids.remove(testObjId)
            #userProps.mapping._p_changed=True
        userProps.dashboard_objs.remove(self.context, self.request)
        userProps.mapping._p_changed=True
        
    def render(self):
        return self.request.response.redirect('./overview.html')


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
                     getter=getTitel,
                     cell_formatter=link('overview.html')),
        GetterColumn(title=_('Modified On'),
                     getter=getModifiedDate,
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
        directlyProvides(self.columns[1], ISortableColumn)
        directlyProvides(self.columns[2], ISortableColumn)
        formatter = StandaloneFullFormatter(
            self.context, self.request, self.objs(),
            columns=self.columns, sort_on=((_('Title'), False),))
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
        #print "oid_list: ", list(userProps.dashboard_objs)
        for dashboardItem in userProps.dashboard_objs:
            myObj = dashboardItem.getObject(some_obj=self,
                                            arg_request=self.request)
            if myObj is not None:
                retList.append(myObj)
        #my_catalog = zapi.getUtility(ICatalog)
        #uidutil = zapi.getUtility(IIntIds)
        #for obj_id in userProps.dashboard_objs:
            #retList.extend(list(my_catalog.searchResults(oid_index=obj_id)))
        print "retList: ", retList
        return retList


class History(BrowserPagelet):
    """History Pagelet"""
    columns = (
        GetterColumn(title=_('Level'),
                     getter=formatEntryLevel),
        GetterColumn(title=_('Date'),
                     getter=formatEntryDate,
                     cell_formatter=raw_cell_formatter),
        GetterColumn(title=_('Text'),
                     getter=formatEntryText),
                     )
    def objs(self):
        """List of Content objects"""
        obj = removeAllProxies(self.context)
        historyList = obj.history
        #return [entry.getList(['date', 'text', 'level', 'version', 'bgcolor'])\
                #for entry in historyList]
        return historyList

    def table(self):
        """ Properties of table are defined here"""
        directlyProvides(self.columns[0], ISortableColumn)
        directlyProvides(self.columns[1], ISortableColumn)
        directlyProvides(self.columns[2], ISortableColumn)
        formatter = StandaloneFullFormatter(
            self.context, self.request, self.objs(),
            columns=self.columns, sort_on=((_('Date'), False),))
        formatter.cssClasses['table'] = 'listing'
        return formatter()
    #def getHistory(self):
        #"""
        #special format list of the history for web-view
        #"""
        #retList = []
        #obj = removeAllProxies(self.context)
        #historyList = obj.history
        #for entry in historyList:
            #tmpList = entry.getList(['date', 'text', 'level', \
                                     #'version', 'bgcolor'])
            #retList.append(tmpList )
        #retList.sort(lambda a, b: cmp(b[0], a[0]))
        #return retList


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
                    #print "delete myid: ", myid
                    #print "       obj: ", self.context[myid]
                    del self.context[myid]
                self.status = _('Objects were successfully deleted.')
            else:
                self.status = _('No objects were selected.')
