# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=F0401,E1101,E0611,W0612,W0232,W0201,W0142
#
"""implementation of browser class of Latency object
"""

__version__ = "$Id$"

# python imports
from tempfile import _RandomNameSequence as RandomNameSequence
import os
import time

# zope imports
from zope.app import zapi
from zope.i18nmessageid import MessageFactory

# zc imports

# z3c imports
from z3c.form import field
from z3c.form.browser import checkbox

# ict_ok.org imports
from org.ict_ok.components.latency.interfaces import ILatency, IAddLatency
from org.ict_ok.components.latency.latency import Latency
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditForm
from org.ict_ok.components.browser.component import AddComponentForm
from org.ict_ok.components.browser.component import ImportCsvDataComponentForm
from org.ict_ok.components.browser.component import ImportXlsDataComponentForm

_ = MessageFactory('org.ict_ok')

# --------------- menu entries -----------------------------

class MSubAddLatency(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add latency check')
    viewURL = 'add_latency.html'
    weight = 50

class MSubDisplayLatency(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Display latency check')
    viewURL = 'display.html'
    weight = 9

# --------------- object details ---------------------------


class LatencyDetails(ComponentDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []

    def getValuePngHref(self):
        """Url to picture"""
        obj = self.context
        return zapi.getPath(obj)

    def getValuePngDeltaT(self):
        """get Picture for special time interval"""
        hours = float(self.request.get('hours', default="1"))
        try:
            width = int(self.request.get('width', default=None))
        except ValueError:
            width = None
        except TypeError:
            width = None
        try:
            height = int(self.request.get('height', default=None))
        except ValueError:
            height = None
        except TypeError:
            height = None
        currtime = time.time()
        params = {}
        params['imgtype'] = "PNG"
        params['nameext'] = "_%dh" % hours
        params['starttime'] = currtime - 3600 * hours
        params['endtime'] = currtime
        if width is None:
            params['width'] = 540
        else:
            params['width'] = width
        if height is None:
            params['height'] = 120
        else:
            params['height'] = height
        return self.getValuePng(params)

    def getValuePng(self, params=None):
        """get Picture"""
        fileExt = RandomNameSequence().next()
        rrdFile = self.context.getRrdFilename()
        if not os.path.exists(rrdFile):
            return None
        params['targetname'] = str("/tmp/%s%s_%s.png" % \
                                   (str(self.context.objectID),
                                    params['nameext'],
                                    fileExt))
        self.context.generateValuePng(params)
        self.request.response.setHeader('Content-Type', 'image/png')
        pic = open(params['targetname'], "r")
        picMem = pic.read()
        pic.close()
        os.remove(params['targetname'])
        return picMem


class LatencyFolderDetails(ComponentDetails):
    """ Class for MobilePhone details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + ['requirement']
    omit_addfields = ComponentDetails.omit_addfields + ['requirement']
    omit_editfields = ComponentDetails.omit_editfields + ['requirement']
    fields = field.Fields(ILatency).omit(*LatencyDetails.omit_viewfields)
    attrInterface = ILatency


class LatencyDisplay(LatencyDetails):
    """
    """
    pass

# --------------- forms ------------------------------------


class DetailsLatencyForm(DisplayForm):
    """ Display form for the object """
    label = _(u'Details of Snmp value')
    fields = field.Fields(ILatency).omit(*LatencyDetails.omit_viewfields)
    
    def update(self):
        DisplayForm.update(self)


#class AddLatencyForm(AddForm):
#    """Add form."""
#    label = _(u'Add Latency')
#    fields = field.Fields(ILatency).omit(*LatencyDetails.omit_addfields)
#    factory = Latency
    
class AddLatencyForm(AddComponentForm):
    label = _(u'Add Latency')
    addFields = field.Fields(IAddLatency)
    allFields = field.Fields(ILatency).omit(*LatencyDetails.omit_addfields)
    allFields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget
    factory = Latency
    attrInterface = ILatency
    _session_key = 'org.ict_ok.components.latency'


class EditLatencyForm(EditForm):
    """ Edit for for net """
    label = _(u'Latency Edit Form')
    fields = field.Fields(ILatency).omit(*LatencyDetails.omit_editfields)
    fields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget


class DeleteLatencyForm(DeleteForm):
    """ Delete the net """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this latency: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportCsvDataForm(ImportCsvDataComponentForm):
    pass


class ImportXlsDataForm(ImportXlsDataComponentForm):
    allFields = field.Fields(ILatency)
    attrInterface = ILatency
    factoryId = u'org.ict_ok.components.latency.latency.Latency'
