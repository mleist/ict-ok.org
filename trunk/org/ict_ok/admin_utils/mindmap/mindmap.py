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
# pylint: disable-msg=E1101,E0611
"""Interface of mind map util

the mind map util will display some information from ict-ok in form of a mind map
"""

__version__ = "$Id$"

# python imports
import logging

# zope imports
from zope.app import zapi
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.component import queryUtility
from zope.i18nmessageid import MessageFactory
from zope.app.catalog.interfaces import ICatalog
# zc imports

# ict_ok.org imports
from org.ict_ok.components.supernode.supernode import Supernode
from org.ict_ok.components.superclass.interfaces import INavigation
from org.ict_ok.admin_utils.mindmap.interfaces import \
     IAdmUtilMindMap
from org.ict_ok.admin_utils.mindmap.mm_node import MMNode
from org.ict_ok.libs.lib import generateOid
#schooltool
from schooltool.requirement import interfaces as ischooltool

#_ = MessageFactory('org.ict_ok')

logger = logging.getLogger("AdmUtilMindMap")


class AdmUtilMindMap(Supernode):
    """MindMap Utiltiy
    """

    implements(IAdmUtilMindMap)

    version = FieldProperty(IAdmUtilMindMap['version'])

    def __init__(self, **data):
        """
        constructor of Supernode
        """
        Supernode.__init__(self, **data)
        self.context = None
        self.ikRevision = __version__

    def asMindmap(self, request=None):
        """ generate our mindmap root frame
        """
        admUtilMindMap = queryUtility(IAdmUtilMindMap, name='AdmUtilMindMap')
        params = {}
        params['version'] = admUtilMindMap.version
        params['ikRevision'] = admUtilMindMap.ikRevision
        params['as_mindmapdata'] = zapi.absoluteURL(self.context, request) + u"/@@as_mindmapdata.html"
        return u"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<title>ict-ok MINDMAP</title>
<script type="text/javascript" src="/@@/js/flashobject.js"></script>
<style type="text/css">

               /* hide from ie on mac \*/
               html {
               height: 100%%;
               overflow: hidden;
               }

               #flashcontent {
               height: 100%%;
               }
               /* end hide */

               body {
               height: 100%%;
               margin: 0;
               padding: 0;
               background-color: #9999ff;
               }

</style>
<script language="javascript">
function giveFocus() 
               { 
               document.visorFreeMind.focus();  
               }
</script></head>
<body onLoad="giveFocus();">
               <div id="flashcontent" onmouseover="giveFocus();">
               Flash plugin or Javascript are turned off.
               Activate both  and reload to view the mindmap
               </div>

               <script type="text/javascript">
               // <![CDATA[
               // for allowing using http://.....?mindmap.mm mode
               function getMap(map){
               var result=map;
               var loc=document.location+'';
               if(loc.indexOf(".mm")>0 && loc.indexOf("?")>0){
               result=loc.substring(loc.indexOf("?")+1);
               }
               return result;
               }
               var fo = new FlashObject("/@@/js/visorFreemind.swf", "visorFreeMind", "100%%", "100%%", 6, "#9999ff");
               fo.addParam("quality", "high");
               fo.addParam("bgcolor", "#ffffff");
               fo.addVariable("openUrl", "_blank");
               fo.addVariable("initLoadFile", getMap("%(as_mindmapdata)s"));
               fo.addVariable("startCollapsedToLevel","2")
               fo.addVariable("defaultToolTipWordWrap",200);
               fo.addVariable("min_alpha_buttons",20);
               fo.addVariable("max_alpha_buttons",100);
               fo.addVariable("CSSFile","/@@/js/flashfreemind.css");
               fo.write("flashcontent");
               // ]]>
               </script>
</body>
</html>""" % params
                #fo.addParam("quality", "high");
                #fo.addParam("bgcolor", "#a0a0f0");
                #fo.addVariable("openUrl", "_blank");
                #fo.addVariable("startCollapsedToLevel","2");
                #fo.addVariable("maxNodeWidth","200");
                #//
                #fo.addVariable("mainNodeShape","elipse");
                #fo.addVariable("justMap","false");
                #fo.addVariable("initLoadFile",getMap("%(as_mindmapdata)s"));
                #fo.addVariable("defaultToolTipWordWrap",200);
                #fo.addVariable("offsetX","left");
                #fo.addVariable("offsetY","top");
                #fo.addVariable("buttonsPos","top");
                #fo.addVariable("min_alpha_buttons",20);
                #fo.addVariable("max_alpha_buttons",100);
                #fo.addVariable("scaleTooltips","false");
    
    def style_health(self, obj, node):
        if hasattr(obj, "get_health"):
            health = obj.get_health()
            if health != None:
                if health < 0:
                    health = 0
                elif health>100:
                    health = 100
                if health <= 50:
                    rgbtupel = (255, int(round(health * 5.1,0)), 0)
                else:
                    rgbtupel = ((50 - int(round((health - 50)) * 5.1,0)), 255, 0)
                if health in range(0,34):
                    node.append_builtin_icon("stop")
                if health in range(34,67):
                    node.append_builtin_icon("prepare")
                if health in range(67,101):
                    node.append_builtin_icon("go")
                bgcolor = '#%02x%02x%02x' % rgbtuple
                node.change_style({"background_color":bgcolor})


    def recursiveHelper(self, tupleList, contextdepth, request=None, alreadySeenDict={}):
        if contextdepth > 0:
            contextdepth -= 1
            nodelist = []
            my_catalog = zapi.getUtility(ICatalog)
            for (attrName, viewTitle, contextObj) in tupleList:
                if attrName is not None and viewTitle is not None:
                    if type(attrName) is not type("str"):
                        raise TypeError("Nav_tuple_wrong: %s" % type(attrName))
                    objList = getattr(contextObj, attrName)
                    if type(objList) is not list:
                        objList = [objList]
                    for obj in objList:
                        node = None
                        if obj not in alreadySeenDict.keys():
                            if type(obj) is type("str") or type(obj) is type(u'ustr'):
                                try:
                                    maybe_obj = my_catalog.searchResults(oid_index=obj)
                                    if len(maybe_obj)>0:
                                        maybe_obj = iter(maybe_obj).next()
                                        #hope thats only one ...
                                except:
                                    pass
                                if ischooltool.IRequirement.providedBy(maybe_obj):
                                        #oh its a requiremnt
                                        objList.append(maybe_obj)
                                        continue
                            if not hasattr(obj, "objectID"):
                                Oid = "tmp%s" % generateOid()
                                node = MMNode(Oid, obj)
                                alreadySeenDict[obj] = node
                                print "reursiveHelper %s" % obj
                            else:
                                node = MMNode(obj.objectID, obj.ikName, {"link": zapi.absoluteURL(obj, request), "node_type":"bubble"})
                                self.style_health(obj, node)
                                alreadySeenDict[obj] = node
                                #print "obj: %s" % obj.ikName
                                itemNav = INavigation(obj)
                                sublist = itemNav.getContextObjList()
                                from copy import copy
                                subnodes = self.recursiveHelper(sublist, copy(contextdepth), request, alreadySeenDict)
                                if len(subnodes) > 0:
                                    node.change_style({"cloud_color":"#EFEFEF"})
                                    node.add_nodes(subnodes)
                        else:
                            #arrorw
                            #if not hasattr(obj, "objectID"):
                                #Oid = "tmp%s" % generateOid()
                                #alreadySeenDict[obj].connect_with_node_id(contextObj.objectID, {"COLOR": "#CBCBCB"})
                            #else:
                            alreadySeenDict[obj].connect_with_node_id(contextObj.objectID, {"COLOR": "#CBCBCB"})
                        if node is not None:
                            nodelist.append(node)
            return nodelist
        else:
            return []


    def asMindmapData(self, request=None):
        """ generate our raw mindmap data
        """
        itemNav = INavigation(self.context)
        objList = itemNav.getContextObjList()
        if itemNav is None:
            return u"""
                   <map version="0.8.1">
                   <node ID="0001" TEXT="Error" >
                   </node>
                   </map>
                   """
        root_node = MMNode(self.context.objectID, self.context.ikName)
        root_node.add_nodes(self.recursiveHelper(objList, 10, request, {self.context:root_node}))
        return root_node.generate_map()













