# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0613,W0232,W0201,W0142,C0111,R0901,R0201
#
"""implementation of browser class of Site object
"""

__version__ = "$Id$"

# TODO: clean up

# phython imports

# zope imports
from zope.component import queryUtility, getAllUtilitiesRegisteredFor
from zope.i18nmessageid import MessageFactory


# zc imports
from zc.table.column import GetterColumn

# z3c imports
from z3c.form import field

# ict-ok.org imports
from org.ict_ok.components.superclass.interfaces import ISuperclass
from org.ict_ok.components.supernode.interfaces import ISupernode
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     DisplayForm, EditForm
from org.ict_ok.admin_utils.util_manager.interfaces import IUtilManager
from org.ict_ok.admin_utils.supervisor.interfaces import \
     IAdmUtilSupervisor
from org.ict_ok.admin_utils.cron.interfaces import IAdmUtilCron
from org.ict_ok.admin_utils.generators.nagios.interfaces import \
     IAdmUtilGeneratorNagios
from org.ict_ok.admin_utils.graphviz.interfaces import \
     IAdmUtilGraphviz
from org.ict_ok.admin_utils.netscan.interfaces import INetScan
from org.ict_ok.admin_utils.netscan.nmap.interfaces import \
     IAdmUtilNMap
from org.ict_ok.admin_utils.netscan.simple1.interfaces import \
     IAdmUtilSimple1
from org.ict_ok.admin_utils.usermanagement.interfaces import \
     IAdmUtilUserManagement
from org.ict_ok.admin_utils.wfmc.interfaces import \
     IAdmUtilWFMC
from org.ict_ok.components.superclass.browser.superclass import \
     Overview as SuperclassOverview
from org.ict_ok.components.superclass.browser import \
     superclass
from org.ict_ok.admin_utils.eventcrossbar.interfaces import \
     IAdmUtilEventCrossbar
from org.ict_ok.admin_utils.ticker.interfaces import \
     IAdmUtilTicker

_ = MessageFactory('org.ict_ok')

# --------------- menu entries -----------------------------

# --------------- object details ---------------------------


class AdmUtilManagerDetails(SupernodeDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = SupernodeDetails.omit_viewfields + ['ikName']
    omit_editfields = SupernodeDetails.omit_editfields + ['ikName']



#def getStateIcon(item, formatter):
    #resource_path = zope.component.getAdapter(formatter.request, name='pics')()
    #return u'<img src="%s/Blank_gray.png" />' % (resource_path)

#def getSize(item, formatter):
    #sizeAdapter = ISized(item)
    #return sizeAdapter.sizeForDisplay()

#def getActionBottons(item, formatter):
    #resource_path = zope.component.getAdapter(formatter.request, name='pics')()
    #view_url = absoluteURL(item, formatter.request) + '/@@view.html'
    #view_html = u'<a href="%s"><img alt="Info" ' \
              #'src="%s/Info.png" /></a>' % (view_url, resource_path)
    #edit_url = absoluteURL(item, formatter.request) + '/@@edit.html'
    #edit_html = u'<a href="%s"><img alt="Edit" ' \
              #'src="%s/Hand.png" /></a>' % (edit_url, resource_path)
    #hist_url = absoluteURL(item, formatter.request) + '/@@history.html'
    #hist_html = u'<a href="%s"><img alt="History" ' \
              #'src="%s/Doc.png" /></a>' % (hist_url, resource_path)
    #trash_url = absoluteURL(item, formatter.request) + '/@@delete.html'
    #trash_html = u'<a href="%s"><img alt="Trash" ' \
               #'src="%s/Trash.png" /></a>' % (trash_url, resource_path)
    #return view_html + edit_html + hist_html + trash_html

#def getCreationDate(item, formatter):
    #tmpDate = IZopeDublinCore(item).created
    #if tmpDate:
        #short_formatter = formatter.request.locale.dates.getFormatter(\
            #'dateTime', 'short')
        #long_formatter = formatter.request.locale.dates.getFormatter(\
            #'dateTime', 'long')
        #timeShortString = short_formatter.format(berlinTZ.fromutc(tmpDate))
        #timeLongString = long_formatter.format(berlinTZ.fromutc(tmpDate))
        #myid = "id" + str(abs(hash(timeShortString)))
        #tooltip = "<script type=\"text/javascript\">tt_%s = "\
                #"new YAHOO.widget.Tooltip('tt_%s', { "\
                #"autodismissdelay:'15000', context:'%s', text:'%s' });"\
                #"</script>" % (myid, myid, myid, timeLongString)
        #resString = u'<span id="%s">%s</span>' % (id, timeShortString)
        #return resString + tooltip
    #else:
        #return "---"


#def getModifiedDate(item, formatter):
    #tmpDate = IZopeDublinCore(item).modified
    #if tmpDate:
        #short_formatter = formatter.request.locale.dates.getFormatter(\
            #'dateTime', 'short')
        #long_formatter = formatter.request.locale.dates.getFormatter(\
            #'dateTime', 'long')
        #timeShortString = short_formatter.format(berlinTZ.fromutc(tmpDate))
        #timeLongString = long_formatter.format(berlinTZ.fromutc(tmpDate))
        #myid = "id" + str(abs(hash(timeShortString)))
        #tooltip = "<script type=\"text/javascript\">tt_%s = "\
                #"new YAHOO.widget.Tooltip('tt_%s', { "\
                #"autodismissdelay:'15000', context:'%s', text:'%s' });"\
                #"</script>" % (myid, myid, myid, timeLongString)
        #resString = u'<span id="%s">%s</span>' % (id, timeShortString)
        #return resString + tooltip
    #else:
        #return "---"
    
#def link(view='index.html'):
    #def anchor(value, item, formatter):
        #url = absoluteURL(item, formatter.request) + '/' + view
        #return u'<a href="%s">%s</a>' % (url, value)
    #return anchor

#class Overview(BrowserPagelet):
    #columns = (
        #column.GetterColumn(title="",
                            #getter=getStateIcon),
        
        #column.GetterColumn(title=_('Title'),
                            #getter=lambda item, \
                            #f: IZopeDublinCore(item).Title(),
                            #cell_formatter=link()),
        #column.GetterColumn(title=_('Size'),
                            #getter=getSize),
        #column.GetterColumn(title=_('Created On'),
                            #getter=getCreationDate),
        #column.GetterColumn(title=_('Modified On'),
                            #getter=getModifiedDate),
        #column.GetterColumn(title=_('Actions'),
                            #getter=getActionBottons),
        #)

    #status = None

    #def content(self):
        #retList = []
        #tmp_util = queryUtility(IUtilManager)
        #if tmp_util:
            #retList.append(tmp_util)
        #tmp_util = queryUtility(IAdmUtilSupervisor)
        #if tmp_util:
            #retList.append(tmp_util)
        #tmp_util = queryUtility(IAdmUtilCron)
        #if tmp_util:
            #retList.append(tmp_util)
        #tmp_util = queryUtility(IAdmUtilGeneratorNagios)
        #if tmp_util:
            #retList.append(tmp_util)
        #tmp_util = queryUtility(IAdmUtilGraphviz)
        #if tmp_util:
            #retList.append(tmp_util)
        #tmp_util = queryUtility(INetScan)
        #if tmp_util:
            #retList.append(tmp_util)
        #tmp_util = queryUtility(IAdmUtilNMap)
        #if tmp_util:
            #retList.append(tmp_util)
        #tmp_util = queryUtility(IAdmUtilSimple1)
        #if tmp_util:
            #retList.append(tmp_util)
        #tmp_util = queryUtility(IAdmUtilUserManagement)
        #if tmp_util:
            #retList.append(tmp_util)
        #tmp_util = queryUtility(IAdmUtilSupport)
        #if tmp_util:
            #retList.append(tmp_util)
        #tmp_util = queryUtility(IAdmUtilSupportUsr)
        #if tmp_util:
            #retList.append(tmp_util)
        #tmp_util = queryUtility(IAdmUtilWFMC)
        #if tmp_util:
            #retList.append(tmp_util)
        #return retList

    #def table(self):
        #directlyProvides(self.columns[1], ISortableColumn)
        #directlyProvides(self.columns[2], ISortableColumn)
        #directlyProvides(self.columns[3], ISortableColumn)
        #directlyProvides(self.columns[4], ISortableColumn)
        #formatter = table.StandaloneFullFormatter(
            #self.context, self.request, self.content(),
            #columns=self.columns, sort_on=((_('Title'), False),))
        #formatter.cssClasses['table'] = 'listing'
        #return formatter()

    #def update(self):
        #self.util_manager = queryUtility(IUtilManager)
        #self.supervisor = queryUtility(IAdmUtilSupervisor)
        #self.rows = ["1", "2", "3"]


class Overview(SuperclassOverview):
    """Overview Pagelet"""
    columns = (
        GetterColumn(title="",
                     getter=superclass.getStateIcon,
                     cell_formatter=superclass.raw_cell_formatter),
        GetterColumn(title=_('Title'),
                     getter=superclass.getTitel,
                     cell_formatter=superclass.link('')),
        GetterColumn(title=_('Modified On'),
                     getter=superclass.getModifiedDate,
                     cell_formatter=superclass.raw_cell_formatter),
        GetterColumn(title=_('Size'),
                     getter=superclass.getSize),
        GetterColumn(title=_('Actions'),
                     getter=superclass.getActionBottons,
                     cell_formatter=superclass.raw_cell_formatter),
        )

    def objs(self):
        """List of Content objects"""
        return getAllUtilitiesRegisteredFor(ISuperclass)


# --------------- forms ------------------------------------


class ViewAdmUtilManagerForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of utility manager')
    fields = field.Fields(IUtilManager).omit(\
        *AdmUtilManagerDetails.omit_viewfields)


class EditAdmUtilManagerForm(EditForm):
    """ Edit for for net """
    label = _(u'edit utility manager')
    fields = field.Fields(IUtilManager).omit(\
        *AdmUtilManagerDetails.omit_editfields)
