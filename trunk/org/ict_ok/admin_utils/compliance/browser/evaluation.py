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

"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.app import zapi
from zope.traversing.browser import absoluteURL
from zope.i18nmessageid import MessageFactory
from zope.dublincore.interfaces import IZopeDublinCore
from zope.security.checker import canAccess
from zope.component import getAdapter
from zope.app.pagetemplate.urlquote import URLQuote

# zc imports
from zc.table.column import GetterColumn
from zc.table.table import StandaloneFullFormatter

# z3c imports
from z3c.form import field
from z3c.pagelet.browser import BrowserPagelet

# ict_ok.org imports
from org.ict_ok.admin_utils.compliance.interfaces import \
     IEvaluation, IEvaluations
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DisplayForm, EditForm
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.admin_utils.usermanagement.usermanagement import \
     getUserTimezone, convert2UserTimezone, AdmUtilUserProperties

_ = MessageFactory('org.ict_ok')


# --------------- helper functions -------------------------


def getEvaluationBotton_Cross(item, formatter):
    """Action Buttons for Overview in Web-Browser
    """
    evaluations = item.getParent()
    evalObj = evaluations.__parent__
    fromURLq = URLQuote(formatter.request['PATH_INFO']).quote()
    urlExt = '/@@change_eval_no?nextURL=%s&req_id=%s' % \
           (fromURLq, item.requirement.getObjectId())
    resource_path = getAdapter(formatter.request, name='pics')()
    ttid = u"evcross" + evalObj.getObjectId()
    view_url = absoluteURL(formatter.context,
                           formatter.request) \
             + urlExt
    #view_url = absoluteURL(evalObj, formatter.request) + '/@@change_eval_no'
    #myAdapter = zapi.queryMultiAdapter((evalObj, formatter.request),
                                       #name='change_eval_no')
    #if myAdapter is not None and canAccess(myAdapter,'render'):
    if not item.value == 'Fail':
        view_html = u'<a href="%s">' %  (view_url) + \
                  u'<img id="%s" alt="Info" src="%s/Cross.png" /></a>' % \
                  (ttid, resource_path)
        tooltip_text = _(u"change evaluation to <b>no</b>")
    else:
        view_html = u'<img id="%s" alt="Details" src="%s/Cross_gr.png" />' % \
                  (ttid, resource_path)
        tooltip_text = _(u"changing evaluation to <b>no</b> is not permitted")
    tooltip = u"<script type=\"text/javascript\">tt_%s = new YAHOO." \
            u"widget.Tooltip('tt_%s', { autodismissdelay:'15000', " \
            u"context:'%s', text:'%s' });</script>" \
            % (ttid, ttid, ttid, tooltip_text)
    return view_html + tooltip

def getEvaluationBotton_Tick(item, formatter):
    """Action Buttons for Overview in Web-Browser
    """
    evaluations = item.getParent()
    evalObj = evaluations.__parent__
    fromURLq = URLQuote(formatter.request['PATH_INFO']).quote()
    urlExt = '/@@change_eval_yes?nextURL=%s&req_id=%s' % \
           (fromURLq, item.requirement.getObjectId())
    resource_path = getAdapter(formatter.request, name='pics')()
    ttid = u"evtick" + evalObj.getObjectId()
    view_url = absoluteURL(formatter.context,
                           formatter.request) \
             + urlExt
    #myAdapter = zapi.queryMultiAdapter((evalObj, formatter.request),
                                       #name='change_eval_yes')
    #if myAdapter is not None and canAccess(myAdapter,'render'):
    if not item.value == 'Pass':
        view_html = u'<a href="%s">' %  (view_url) + \
                  u'<img id="%s" alt="Info" src="%s/Tick.png" /></a>' % \
                  (ttid, resource_path)
        tooltip_text = _(u"change evaluation to <b>yes</b>")
    else:
        view_html = u'<img id="%s" alt="Details" src="%s/Tick_gr.png" />' % \
                  (ttid, resource_path)
        tooltip_text = _(u"changing evaluation to <b>yes</b> is not permitted")
    tooltip = u"<script type=\"text/javascript\">tt_%s = new YAHOO." \
            u"widget.Tooltip('tt_%s', { autodismissdelay:'15000', " \
            u"context:'%s', text:'%s' });</script>" \
            % (ttid, ttid, ttid, tooltip_text)
    return view_html + tooltip

def getRequirementTitle(item, formatter):
    """
    Titel for Overview
    """
    try:
        return item.requirement.ikName
    except TypeError:
        return str(item.__class__.__name__)

def getEvaluatorTitle(item, formatter):
    """
    Titel for Overview
    """
    try:
        return item.evaluator.title
    except TypeError:
        return str(item.__class__.__name__)
    
def getEvaluationValue(item, formatter):
    """
    Titel for Overview
    """
    #self.scoreSystem = scoreSystem
    return item.value

def evaluationValue_formatter(value, item, formatter):
    if item.scoreSystem.title == u'Pass/Fail':
        if value == u'Pass':
            return u'<B CLASS="cb_ig">%s</b>' % (value)
        else:
            return u'<B CLASS="cb_ir">%s</b>' % (value)
    else:
        return unicode(value)

def getEvalModifiedDate(item, formatter):
    """Modified Date for Overview in Web-Browser"""
    try:
        #self.scoreSystem = scoreSystem
        #item.time
        userTZ = getUserTimezone()
        my_formatter = formatter.request.locale.dates.getFormatter(
            'dateTime', 'short')
        timeString = my_formatter.format(userTZ.fromutc(item.time))
        timeStringHTML = timeString.replace(" ", "&nbsp;")
        my_formatter = formatter.request.locale.dates.getFormatter(
            'dateTime', 'long')
        longTimeString = my_formatter.format(
            userTZ.fromutc(item.time))
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


# --------------- menu entries -----------------------------


# --------------- details -----------------------------

class AdmUtilEvaluationDetails(SupernodeDetails):
    """Evaluation Utiltiy
    """
    
    omit_viewfields = SupernodeDetails.omit_viewfields + ['ikName']
    omit_editfields = SupernodeDetails.omit_editfields + ['ikName']


class AdmUtilEvaluationsDetails(SupernodeDetails):
    """Evaluation Utiltiy
    """
    
    omit_viewfields = SupernodeDetails.omit_viewfields + ['ikName']
    omit_editfields = SupernodeDetails.omit_editfields + ['ikName']


# --------------- forms ------------------------------------


# --------- Evaluation

#class DetailsAdmUtilEvaluationForm(DisplayForm):
    #""" Display form for the object """
    
    #label = _(u'settings of Evaluation')
    #fields = field.Fields(IEvaluation).omit(
       #*AdmUtilEvaluationDetails.omit_viewfields)
    
    #def update(self):
        #DisplayForm.update(self)
    


#class EditAdmUtilEvaluationForm(EditForm):
    #""" Display form for the object """
    
    #label = _(u'edit Evaluation properties')
    #fields = field.Fields(IEvaluation).omit(
       #*AdmUtilEvaluationDetails.omit_editfields)

# --------- Evaluations

#class DetailsAdmUtilEvaluationsForm(DisplayForm):
    #""" Display form for the object """
    
    #label = _(u'settings of Evaluations')
    #fields = field.Fields(IEvaluations).omit(
       #*AdmUtilEvaluationsDetails.omit_viewfields)
    
    #def update(self):
        #DisplayForm.update(self)
    


#class EditAdmUtilEvaluationsForm(EditForm):
    #""" Display form for the object """
    
    #label = _(u'edit Evaluations properties')
    #fields = field.Fields(IEvaluations).omit(
       #*AdmUtilEvaluationsDetails.omit_editfields)
