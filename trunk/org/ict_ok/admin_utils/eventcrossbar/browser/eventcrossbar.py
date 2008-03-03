# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0232,W0142
#
"""implementation of browser class of eventCrossbar handler
"""

__version__ = "$Id$"

# phython imports

# zope imports
from zope.app import zapi
from zope.i18nmessageid import MessageFactory
from zope.dublincore.interfaces import IZopeDublinCore
from zope.app.catalog.interfaces import ICatalog

# zc imports
from zc.table.column import GetterColumn
from zc.table.table import StandaloneFullFormatter

# z3c imports
from z3c.form import field
from z3c.pagelet.browser import BrowserPagelet

# ict_ok.org imports
from org.ict_ok.admin_utils.eventcrossbar.interfaces import \
     IAdmUtilEventCrossbar
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DisplayForm, EditForm
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.admin_utils.graphviz.interfaces import \
     IGenGraphvizDot
from org.ict_ok.admin_utils.eventcrossbar.interfaces import IAdmUtilEvent
from org.ict_ok.admin_utils.eventcrossbar.interfaces import \
     IEventLogic
from org.ict_ok.components.interfaces import IComponent

_ = MessageFactory('org.ict_ok')

# --------------- menu entries -----------------------------


class MSubCrossBar(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Crossbar')
    viewURL = 'crossbar.html'
    weight = 20


class MSubCrossBarSignalGraph(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Signal Graph')
    viewURL = 'signalgraph.html'
    weight = 30



class AdmUtilEventCrossbarDetails(SupernodeDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = SupernodeDetails.omit_viewfields + ['ikName']
    omit_editfields = SupernodeDetails.omit_editfields + ['ikName']

    def getInstanceCounter(self):
        """convert instance counter for display
        """
        return self.context.getInstanceCounter()

    def getEventCrossbarTime(self):
        """convert eventcrossbar timestamp for display
        """
        return self.context.getEventCrossbarTime()

    def getIMGFile(self):
        """get dot file and convert to png
        """
        imgtype = self.request.get('type', default='png')
        mode = self.request.get('mode', default=None)
        if mode and mode.lower() == "fview":
            self.request.response.setHeader('content-type',
                                            'image/%s' % imgtype)
            self.request.response.setHeader('content-disposition',
                                            'attachment; filename=\"signals.%s\"'\
                                            % (imgtype))
        return self.context.getIMGFile(imgtype, mode)

    #def getCmapxText(self):
        #"""get dot file and convert to client side image map
        #"""
        #return self.context.getCmapxText(zapi.getRoot(self))



class CrossBar(BrowserPagelet):
    label = _(u'event crossbar')
    mytest = [u'a', u'b', u'c', u'd', u'e', u'f', u'g']
    def update(self):
        self.columns = (\
            GetterColumn(title="1111",
                         ),
            GetterColumn(title="2222",
                         ),
            GetterColumn(title="3333",
                         ),
        )
    def objs(self):
        """List of Content objects"""
        retList = []
        try:
            for obj in self.mytest:
                retList.append(obj)
        except:
            pass
        #try:
            #for obj in self.context.values():
                #if ISuperclass.providedBy(obj):
                    #retList.append(obj)
        #except:
            #pass
        return retList
    def table(self):
        """ Properties of table are defined here"""
        formatter = StandaloneFullFormatter(
            self.context, self.request, self.objs(),
            columns=self.columns)
        formatter.cssClasses['table'] = 'listing'
        return formatter()


class SignalGraph(BrowserPagelet):
    label = _(u'Signal Overview')
    #def genDotFile(self):
        #print "genDotFile"
        #my_catalog = zapi.getUtility(ICatalog)
        #objIdSet = set()
        #objSet = set()
        #eventSet = set()
        ##print "all items."
        #for (oid, oobj) in self.context.items():
            #objIdSet.add(oid)
            ##print "%s: %s" % (oid, oobj)
        ##print "inp queue 1:"
        #for objId in self.context.inpEQueues:
            #objIdSet.add(objId)
            ##print "%s: %s" % (objId, self.context.inpEQueues[objId])
        ##print "inp queue 2:"
        ##for inpObjId in iter(self.context.inpEQueues):
            ##print "%s" % (type(inpObjId))
            ##for result in my_catalog.searchResults(oid_index=inpObjId):
                ##print "result: %s [%s]" % (result, type(result))
        ##print "out queue:"
        #for objId in self.context.outEQueues:
            #objIdSet.add(objId)
            ##print "%s: %s" % (objId, self.context.outEQueues[objId])
        #for objId in objIdSet:
            #for result in my_catalog.searchResults(oid_index=objId):
                #if IAdmUtilEvent.providedBy(result):
                    #eventSet.add(result)
                #elif IEventLogic.providedBy(result):
                    #objSet.add(result)
                #elif IEventLogic.providedBy(result):
                    #objSet.add(result)
                #elif IComponent.providedBy(result):
                    #if result.isConnectedToEvent():
                        #objSet.add(result)
                #else:
                    #pass
        #dotFile = open("/tmp/dotSignals.dot", 'w')
        #print >> dotFile, '// GraphViz DOT-File'
        #print >> dotFile, 'digraph "%s" {' % (zapi.getRoot(self).__name__)
        ##print >> dotFile, '\tgraph [bgcolor="#E5FFF9", size="6.2,5.2",' +\
        ##' splines="true", ratio = "auto", dpi="100.0"];'
        #print >> dotFile, '\tgraph [bgcolor="#E5FFF9", dpi="100.0"];'
        #print >> dotFile, '\tnode [fontname = "Helvetica",fontsize = 10];'
        #print >> dotFile, '\tedge [style = "setlinewidth(2)", color = black];'
        #print >> dotFile, '\trankdir = LR;'
        #print >> dotFile, '\t// objects ----------------------------------'
        #for obj in objSet:
            ##print >> dotFile, '\t"%s" [' % (obj.objectID)
            ##print >> dotFile, '\t ]'
            #objGraphvizDot = IGenGraphvizDot(obj)
            ##try:
            #objGraphvizDot.traverse4DotGenerator(dotFile, level=1,
                                                 #comments=True,
                                                 #signalsOutput=True,
                                                 #recursive=False)
            ##except AttributeError:
                ##print >> dotFile, '\t ^^ (%s)' % objGraphvizDot
        #print >> dotFile, '\t// events ----------------------------------'
        #for event in eventSet:
            ##for inp in event.inpObjects:
                ##print >> dotFile, "\t//\tinp: %s" % (inp)
            ##for out in event.outObjects:
                ##print >> dotFile, "\t//\tout: %s" % (out)
            #eventGraphvizDot = IGenGraphvizDot(event)
            #eventGraphvizDot.traverse4DotGenerator(dotFile, level=1, comments=True)
            ##try:
                ##eventGraphvizDot.traverse4DotGenerator(dotFile, level=1, comments=True)
            ##except AttributeError:
                ##print >> dotFile, '\t ^^ (%s)' % objGraphvizDot
                
        ##for obj in objSet:
            ##print >> dotFile, '\t//getAllOutEventObjs:'
            ##for i in obj.getAllOutEventObjs():
                ##print >> dotFile, '\t//\t -> %s' % i
                ##print >> dotFile, '\t "%s"-> "%s"' % (obj.objectID, i)
            ##print >> dotFile, '\t//getAllInpEventObjs:'
            ##for i in obj.getAllInpEventObjs():
                ##print >> dotFile, '\t//\t -> %s' % i
                ##print >> dotFile, '\t "%s"-> "%s"' % (i, obj.objectID)

        #for obj in objSet:
            #allInpNamesDict = obj.getAllInpEventNames()
            #allOutNamesDict = obj.getAllOutEventNames()
            ##import pdb; pdb.set_trace()
            #for inpName in allInpNamesDict.keys():
                #for iObj in allInpNamesDict[inpName]:
                    #print >> dotFile, '\t "%s"-> "%s":"%s"' % (iObj, obj.objectID, inpName)
            #for outName in allOutNamesDict.keys():
                #for iObj in allOutNamesDict[outName]:
                    #print >> dotFile, '\t "%s":"%s"-> "%s"' % (obj.objectID, outName, iObj)
        #print >> dotFile, '}'
        #dotFile.flush()
        #dotFile.close()

    def getValuePngHref(self):
        """get path of object as string
        """
        #from zope.proxy import removeAllProxies
        #obj = removeAllProxies(self.context)
        #return zapi.getPath(obj)
        return zapi.getPath(self.context)


# --------------- forms ------------------------------------


class DetailsAdmUtilEventCrossbarForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Event')
    fields = field.Fields(IAdmUtilEventCrossbar).omit(\
        *AdmUtilEventCrossbarDetails.omit_viewfields) + \
           field.Fields(IZopeDublinCore).select('modified')


class EditAdmUtilEventCrossbarForm(EditForm):
    """ Edit form for the object """
    label = _(u'edit crossbar properties')
    fields = field.Fields(IAdmUtilEventCrossbar).omit(\
        *AdmUtilEventCrossbarDetails.omit_editfields)
