# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0704,W0142
#
"""Configuration adapter for smokeping-config files
"""

__version__ = "$Id$"

# python imports
import os

# zope imports
from zope.interface import implements
from zope.component import adapts
from zope.i18n import translate
from zope.schema import vocabulary
from zope.app import zapi
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory
from org.ict_ok.components.superclass.interfaces import ISuperclass
from org.ict_ok.components.superclass.superclass import Superclass
from org.ict_ok.components.superclass.browser.superclass import \
    SuperclassDetails
from org.ict_ok.components.superclass.interfaces import INavigation
from org.ict_ok.components.superclass.superclass import isOidInCatalog
from org.ict_ok.libs.lib import oid2dcTitle
from org.ict_ok.admin_utils.graphviz.interfaces import \
     IGenGraphvizDot
from org.ict_ok.libs.lib import generateOid

_ = MessageFactory('org.ict_ok')

class RptDot(object):
    """adapter implementation of Superclass -> Dot Report
    """
    
    implements(IGenGraphvizDot)
    adapts(ISuperclass)
    factory = Superclass
    omitFields = ['objectID', '__name__', 'ref', 'history',
                  'dbgLevel', 'ikEventTarget']
    
    attributeList = ['ikName']
    
    def __init__(self, context):
        #self.document = None
        self.context = context
        self.attributeList
        #self.request = None
        #self.files2delete = []
        #self.attributeData = []
        self.parent = None
        self.ikRevision = __version__

    def setParent(self, parent):
        """set Parent-Object
        """
        self.parent = parent

    def traverse4DotGeneratorPre(self,
                                 cfgFile, 
                                 level=0, 
                                 comments=True,
                                 alreadySeenList=None):
        """graphviz configuration preamble
        """
        if comments:
            print >> cfgFile, "%s// Pre (%s,%d) - RptDot" \
                  % ("\t" * level, self.context, level)

    def traverse4DotGeneratorBody(self, cfgFile, level=0,
                                  comments=True, alreadySeenList=None):
        """graphviz configuration data of object
        """
        if comments:
            print >> cfgFile, "%s// Body (%s,%d) - RptDot" \
                  % ("\t" * level, self.context, level)
        dot_str = '%s"%s" [' % ("\t" * level, self.context.objectID)
        dot_str += 'shape="diamond", '
        dot_str += 'label="%s", ' % self.context.ikName
        dot_str += 'fontsize=10.0'
        dot_str += '];'
        print >> cfgFile, dot_str
        if alreadySeenList == None:
            alreadySeenList = []
        alreadySeenList.append(self.context)
        itemNav = INavigation(self.context)
        tuplelist = itemNav.getContextObjList()
        #import pdb
        #pdb.set_trace()
        for (attrName, viewTitle, contextObj) in tuplelist:
                if attrName is not None and viewTitle is not None:
                    if type(attrName) is not type("str"):
                        raise TypeError("Nav_tuple_wrong: %s" % type(attrName))
                    objList = getattr(contextObj, attrName)
                    if objList.__class__ != list:
                        objList = [objList]
                    for obj in objList:
                        if obj not in alreadySeenList:
                            try:
                                adapterGenGraphvizDot = IGenGraphvizDot(obj)
                            except TypeError:
                                adapterGenGraphvizDot = None
                            if adapterGenGraphvizDot:
                                adapterGenGraphvizDot.setParent(self.context)
                                adapterGenGraphvizDot.traverse4DotGenerator(\
                                    cfgFile,
                                    level+1,
                                    comments,
                                    alreadySeenList)
        self.manageEvaluations(self.context, cfgFile, level)
        if self.parent != None:
            print >> cfgFile, '%s"%s" -- "%s"' \
                  % ("\t" * level, self.parent.objectID, self.context.objectID)

    def traverse4DotGeneratorPost(self, cfgFile, level=0, comments=True, alreadySeenList=None):
        """graphviz configurations text after object
        """
        if comments:
            print >> cfgFile, "%s// Post (%s,%d) - RptDot" \
                  % ("\t" * level, self.context, level)


    def traverse4DotGenerator(self, cfgFile, level=0, comments=True,
                              alreadySeenList=None):
        """
        cfgFile: handle to open file
        level: indent-level
        """
        if ISuperclass.providedBy(self.context):
            self.traverse4DotGeneratorPre(cfgFile, level, comments, alreadySeenList)
            self.traverse4DotGeneratorBody(cfgFile, level, comments, alreadySeenList)
            self.traverse4DotGeneratorPost(cfgFile, level, comments, alreadySeenList)
    
    def manageEvaluations(self, obj, cfgFile, level):
        if hasattr(obj, "getEvaluationsDone"):
            evals = obj.getEvaluationsDone()
            if len(evals) > 0:
                table_list = [(_("Evaluation"), _("Evaluator"), _("Value"))]
                for eval in evals:
                    #table_list.append((eval.ikName, eval.evaluator.title, eval.value+' <img src="%s/lib/python/org/ict_ok/skin/pics/mini/tick.gif">' % os.getcwd()))
                    table_list.append((eval.ikName, eval.evaluator.title, eval.value))
                tmpID = "tmp%s" % generateOid()
                dot_str = '%s"%s" [' % ("\t" * level, tmpID)
                dot_str += 'shape="note", '
                dot_str += 'label=<%s>, ' % self.__htmlTable(table_list)
                dot_str += 'fontsize=10.0'
                dot_str += '];\n'
                dot_str += '%s"%s" -- "%s"' % ("\t" * level, tmpID, obj.objectID)
                print >> cfgFile, dot_str
        if hasattr(obj, "getEvaluationsTodo"):
            reqs = obj.getEvaluationsTodo()
            if len(reqs)>0:
                pass

    def __htmlTable(self, table_list):
        """ wants list = [(t1,t2,t3),(z1,z1,z1),(z2,z2,z2)]
        """
        table_str = '<table border="1">'
        for zeile in table_list:
            table_str += '<tr>'
            for s in zeile:
                table_str += '<td>'
                table_str += s
                table_str += '</td>'
            table_str += '</tr>'
        table_str += '</table>'
        return table_str#.replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")



    #def traverse4RptPre(self, level, comments, autoAppend=True):
        #"""pdf report object preamble
        
        #level: indent-level (int 0..)
        #comments: should there comments are in the output?
        #"""
        #if comments:
            #self.writeComment(u"%s## Pre (%s,%d) - SuperclassRptPdfPre" % \
                              #("\t" * level, self.context.ikName, level))
        #if self.document is not None:
            #titleStr = u"%s: %s" % \
                     #(self.context.myFactory.split('.')[-1],
                      #self.context.ikName)
            #title = RptTitle(titleStr,
                             #intype="Heading%d" % level,
                             #doc=self.document,
                             #context=self.context)
##            elemList = [title.genElements()]
            #attrTable = self.getAttributeTable()
            #if attrTable:
                #elemList = [title.genElements(),
                            #self.getAttributeTable(),
                            #Spacer(0, 4 * mm)]
            #else:
                #elemList = [title.genElements(),
                            #Spacer(0, 4 * mm)]
            #elemList.extend(\
                #appendEvaluationList(self.context, self.document))
            #if autoAppend is True:
                #comp = KeepTogether(elemList)
                #self.document.append(comp)
                ##for elem in elemList:
                    ##self.document.append(elem)
            #else:
                #return elemList
        #return None
    
            ##elemList.extend(\
                ##appendEvaluationList(self.context, self.document))

    #def traverse4RptPost(self, level, comments):
        #"""pdf report object postamble
        
        #level: indent-level (int 0..)
        #comments: should there comments are in the output?
        #"""
        #if comments:
            #self.writeComment(u"%s## Post (%s,%d) - SuperclassRptPdfPost" % \
                              #("\t" * level, self.context.ikName, level))

    #def traverse4RptBody(self, level, comments):
        #"""pdf report data of/in object
        
        #level: indent-level (int 0..)
        #comments: should there comments are in the output?
        #"""
        #if comments:
            #self.writeComment(u"%s## Body (%s,%d) - SuperclassRptPdfBody" % \
                              #("\t" * level, self.context.ikName, level))

    #def traverse4Rpt(self, level, comments):
        #"""object pdf report
        
        #level: indent-level (int 0..)
        #comments: should there comments are in the output?
        #"""
        #if ISuperclass.providedBy(self.context):
            #self.traverse4RptPre(level, comments)
            #self.traverse4RptBody(level, comments)
            #self.traverse4RptPost(level, comments)
            #if self.document is not None and \
                #self.document._reporter is not None:
                #self.document._reporter.alreadyReported[self.context.objectID] = self
