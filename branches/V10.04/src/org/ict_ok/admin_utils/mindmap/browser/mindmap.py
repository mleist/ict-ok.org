# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
#               Sebastian Napiorkowski <s.napiorkowski@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0232,W0142
"""Interface of mind map util

the mind map util will display some information from ict-ok in form of a mind map
"""
"""implementation of browser class of eventCrossbar handler
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory
from zope.dublincore.interfaces import IZopeDublinCore

# zc imports
from zc.table.column import GetterColumn
from zc.table.table import StandaloneFullFormatter

# z3c imports
from z3c.form import field
from z3c.pagelet.browser import BrowserPagelet

# ict_ok.org imports
from org.ict_ok.admin_utils.mindmap.interfaces import \
     IAdmUtilMindMap
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DisplayForm, EditForm
from org.ict_ok.skin.menu import GlobalMenuSubItem

_ = MessageFactory('org.ict_ok')

# --------------- menu entries -----------------------------


class AdmUtilMindMapDetails(SupernodeDetails):
    """MindMap Utiltiy
    """

    omit_viewfields = SupernodeDetails.omit_viewfields + ['ikName']
    omit_editfields = SupernodeDetails.omit_editfields + ['ikName']



class AdmUtilMindMapFrame(SupernodeDetails):
    """MindMap Utiltiy
    """
        #return """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
#<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
#<head>
#<script type="text/javascript" src="http://localhost:8080/@@/js/flashobject.js"></script>
#</head>
#<body>
#<script language="javascript">
#function giveFocus() 
    #{ 
        #document.visorFreeMind.focus();  
    #}
#</script>
#<div id="flashcontent" onmouseover="giveFocus();">
    #Flash plugin or Javascript are turned off.
    #Activate both  and reload to view the mindmap
#</div>

#<script type="text/javascript">
    #// <![CDATA[
    #// for allowing using http://.....?mindmap.mm mode
    #function getMap(map){
        #var result=map;
        #var loc=document.location+'';
        #if(loc.indexOf(".mm")>0 && loc.indexOf("?")>0){
            #result=loc.substring(loc.indexOf("?")+1);
        #}
        #return result;
    #}
    #var fo = new FlashObject("http://localhost:8080/@@/js/visorFreemind.swf", "visorFreeMind", "100%%", "100%%", 6, "#9999ff");
    #fo.addParam("quality", "high");
    #fo.addParam("bgcolor", "#a0a0f0");
    #fo.addVariable("openUrl", "_blank");
    #fo.addVariable("startCollapsedToLevel","2");
    #fo.addVariable("maxNodeWidth","200");
    #//
    #fo.addVariable("mainNodeShape","elipse");
    #fo.addVariable("justMap","false");
    #fo.addVariable("initLoadFile",getMap("/@@/js/test.mm"));
    #fo.addVariable("defaultToolTipWordWrap",200);
    #fo.addVariable("offsetX","left");
    #fo.addVariable("offsetY","top");
    #fo.addVariable("buttonsPos","top");
    #fo.addVariable("min_alpha_buttons",20);
    #fo.addVariable("max_alpha_buttons",100);
    #fo.addVariable("scaleTooltips","false");
    #fo.write("flashcontent");
    #// ]]>
#</script>
#</body>
#</html>
#<!-- mm genrator ict-ok.org (%(ikRevision)s) -->""" % params
# --------------- forms ------------------------------------


class DetailsAdmUtilMindMapForm(DisplayForm):
    """ Display form for the object """

    label = _(u'settings of MindMap')
    fields = field.Fields(IAdmUtilMindMap).omit(
        *AdmUtilMindMapDetails.omit_viewfields)


class EditAdmUtilMindMapForm(EditForm):
    """ Display form for the object """

    label = _(u'edit MindMap properties')
    fields = field.Fields(IAdmUtilMindMap).omit(
        *AdmUtilMindMapDetails.omit_editfields)
