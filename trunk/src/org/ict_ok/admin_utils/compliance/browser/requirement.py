# -*- coding: utf-8 -*-
#
# Copyright (c) 2007, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0232,W0142
"""Interface of compliance utility

the compliance utility should store the compliance/requirement-templates
for the host- or service-instances
implementation of browser class of eventCrossbar handler
"""

__version__ = "$Id$"

# python imports
from datetime import datetime

# zope imports
from zope.traversing.browser import absoluteURL
from zope.i18nmessageid import MessageFactory
from zope.component import getAdapter
from zope.app.pagetemplate.urlquote import URLQuote

# zc imports
from zc.table.column import GetterColumn

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory
from org.ict_ok.admin_utils.compliance.interfaces import IRequirement
from org.ict_ok.admin_utils.compliance.requirement import Requirement
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     DisplayForm, EditForm, AddForm, DeleteForm
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.components.superclass.browser.superclass import \
     Overview, getModifiedDate, raw_cell_formatter, \
     link, getActionBottons, getSize
from org.ict_ok.components.superclass.browser.superclass import \
     getActionBotton_Detail, getTitle
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.admin_utils.usermanagement.usermanagement import \
     getUserTimezone

_ = MessageFactory('org.ict_ok')

# --------------- helper functions -------------------------


def getRequirementBotton_Cross(item, formatter):
    """Action Buttons for Overview in Web-Browser
    """
    if type(item) is dict:
        obj = item["obj"]
        item = item["req"]
    fromURLq = URLQuote(formatter.request['PATH_INFO']).quote()
    urlExt = '/@@change_eval_no?nextURL=%s&req_id=%s&obj_id=%s' % \
           (fromURLq, item.getObjectId(), obj.objectID)
    resource_path = getAdapter(formatter.request, name='pics')()
    ttid = u"tick" + obj.objectID + item.objectID
    view_url = absoluteURL(obj,
                           formatter.request) \
             + urlExt
    if True:
        view_html = u'<a href="%s">' %  (view_url) + \
                  u'<img id="%s" alt="Info" src="%s/Cross.png" /></a>' % \
                  (ttid, resource_path)
        tooltip_text = _(u'check requirement to <b>no</b>')
    else:
        view_html = u'<img id="%s" alt="Details" src="%s/Cross_gr.png" />' % \
                  (ttid, resource_path)
        tooltip_text = _(u'checking requirement to <b>no</b> is not permitted')
    tooltip = u"<script type=\"text/javascript\">tt_%s = new YAHOO." \
            u"widget.Tooltip('tt_%s', { autodismissdelay:'15000', " \
            u"context:'%s', text:'%s' });</script>" \
            % (ttid, ttid, ttid, tooltip_text)
    return view_html + tooltip

def getRequirementBotton_Tick(item, formatter):
    """Action Buttons for Overview in Web-Browser
    """
    if type(item) is dict:
        obj = item["obj"]
        item = item["req"]
    fromURLq = URLQuote(formatter.request['PATH_INFO']).quote()
    urlExt = '/@@change_eval_yes?nextURL=%s&req_id=%s&obj_id=%s' % \
           (fromURLq, item.getObjectId(), obj.objectID)
    resource_path = getAdapter(formatter.request, name='pics')()
    ttid = u"tick" + obj.objectID + item.objectID
    view_url = absoluteURL(obj,
                           formatter.request) \
             + urlExt
    if True:
        view_html = u'<a href="%s">' %  (view_url) + \
                  u'<img id="%s" alt="Info" src="%s/Tick.png" /></a>' % \
                  (ttid, resource_path)
        tooltip_text = _(u'check requirement to <b>yes</b>')
    else:
        view_html = u'<img id="%s" alt="Details" src="%s/Tick_gr.png" />' % \
                  (ttid, resource_path)
        tooltip_text = _(u'checking requirement to <b>yes</b> is not permitted')
    tooltip = u"<script type=\"text/javascript\">tt_%s = new YAHOO." \
            u"widget.Tooltip('tt_%s', { autodismissdelay:'15000', " \
            u"context:'%s', text:'%s' });</script>" \
            % (ttid, ttid, ttid, tooltip_text)
    return view_html + tooltip


def getRequirementBottons(item, formatter):
    """Action Buttons for Overview in Web-Browser
    """
    retHtml = u""
    retHtml += getActionBotton_Detail(item['req'], formatter,
                                      isRequirement=True)
    retHtml += getRequirementBotton_Tick(item, formatter)
    retHtml += getRequirementBotton_Cross(item, formatter)
    return retHtml

def getRequirementTitle(item, formatter):
    """
    Titel for Overview
    """
    if type(item) is dict:
        item = item["req"]
    try:
        return item.ikName
    except TypeError:
        return str(item.__class__.__name__)

def getReqModifiedDate(item, formatter):
    if type(item) is dict:
        item = item["req"]
    getModifiedDate(item, formatter)

# --------------- menu entries -----------------------------

class MSubDisplayRequirements(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Requirements')
    viewURL = 'display_reqs.html'
    weight = 80

class MSubAllRequirements(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'All Requirements')
    viewURL = 'allreqs.html'
    weight = 80

class MSubAddRequirement(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Requirement')
    viewURL = 'add_requirement.html'
    weight = 50


# --------------- details -----------------------------

class AdmUtilRequirementDetails(SupernodeDetails):
    """Requirement Utiltiy
    """
    
    omit_viewfields = SupernodeDetails.omit_viewfields + \
                    ['__name__', '__parent__', 'title']
    omit_addfields = SupernodeDetails.omit_addfields + \
                    ['__name__', '__parent__', 'title']
    omit_editfields = SupernodeDetails.omit_editfields + \
                    ['__name__', '__parent__', 'title']

    def overResubmitDate(self):
        userTZ = getUserTimezone()
        nowTS = userTZ.fromutc(datetime.utcnow())
        
# --------------- forms ------------------------------------


class DetailsAdmUtilRequirementForm(Overview):
    """ Display form for the object """
    
    label = _(u'settings of Requirement')
    factory = Requirement
    omitFields = AdmUtilRequirementDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)
    columns = (
        GetterColumn(title=_('Title'),
                     getter=getTitle,
                     cell_formatter=link('overview.html')),
        GetterColumn(title=_('Modified'),
                     getter=getModifiedDate,
                     subsort=True,
                     cell_formatter=raw_cell_formatter),
        GetterColumn(title=_('Size'),
                     getter=getSize,
                     cell_formatter=raw_cell_formatter),
        GetterColumn(title=_('Actions'),
                     getter=getActionBottons,
                     cell_formatter=raw_cell_formatter),
        )
    pos_colum_index = 3
    sort_columns = [1]
    status = None
    
    def objs(self):
        """List of Content objects"""
        return [obj
                for obj in self.context.values()
                if IRequirement.providedBy(obj)]

class OverviewAdmUtilRequirementForm(DetailsAdmUtilRequirementForm):
    """for overview
    """
    
    
class AdmUtilRequirementDisplayAll(DisplayForm):
    """for all Requirements
    """
    label = _(u'display all requirements')


class AddAdmUtilRequirementForm(AddForm):
    """Add form."""
    label = _(u'add Requirement')
    factory = Requirement
    omitFields = AdmUtilRequirementDetails.omit_addfields
    fields = fieldsForFactory(factory, omitFields)
    
    def create(self, data):
        """ will create the object """
        # arg1 must be title for schooltool requirement
        # this will be reused later by ikName=arg1
        titleArg = data.pop('ikName')
        obj = self.factory(titleArg, **data)
        self.newdata = data
        IBrwsOverview(obj).setTitle(titleArg)
        obj.__post_init__()
        return obj
    
    def nextURL(self):
        """ don't forward the browser """
        return absoluteURL(self.context, self.request)

    
class EditAdmUtilRequirementForm(EditForm):
    """ Display form for the object """
    
    label = _(u'edit Requirement properties')
    factory = Requirement
    omitFields = AdmUtilRequirementDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)


class DeleteAdmUtilRequirementForm(DeleteForm):
    """ Delete the Requirement """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this Requirement: '%s'?") % \
               self.context.ikName
