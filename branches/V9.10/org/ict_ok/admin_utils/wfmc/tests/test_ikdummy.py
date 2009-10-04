# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0221,W0212,R0904
#

__version__ = "$Id$"

# python imports
import os
import unittest

# zope imports
from zope.app.testing import ztapi
from zope.app.component.testing import PlacefulSetup
from zope.app.testing import setup

# ict_ok.org imports
#from org.ict_ok.ikdummy.interfaces import IDummy
#from org.ict_ok.ikdummy.ikdummy import Dummy
from org.ict_ok.admin_utils.graphviz.interfaces import IGenGraphvizDot
#from org.ict_ok.admin_utils.graphviz.adapter.ikdummy import \
     #DummyGenGraphvizDot


class AdminGraphvizIkDummyTestCase(PlacefulSetup, unittest.TestCase):

    def setUp(self):
        pass
        #PlacefulSetup.setUp(self, False, False)
        #self.root = root = setup.placefulSetUp(site = True)
        #self.ikdummy11 = Dummy()
        #self.ikdummy11.ikName = u"ikdummy1.1"
        #root[u'ikdummy1.1'] = self.ikdummy11
        #self.ikdummy12 = Dummy()
        #self.ikdummy12.ikName = u"ikdummy1.2"
        #root[u'ikdummy1.2'] = self.ikdummy12
        #self.ikdummy13 = Dummy()
        #self.ikdummy13.ikName = u"ikdummy1.3"
        #root[u'ikdummy1.3'] = self.ikdummy13
        #ztapi.provideAdapter(IDummy, IIkGenGraphvizDot, \
                             #DummyGenGraphvizDot)

    #def test_genOut_ikdummy11(self):
        #tmpFile = os.tmpfile()
        #adapterGenGraphvizDot = IIkGenGraphvizDot(self.ikdummy11)
        #adapterGenGraphvizDot.setParent(self.root)
        #adapterGenGraphvizDot.traverse4DotGenerator(tmpFile, \
                                                            #level=1, \
                                                            #comments=False)
        #tmpFile.seek(0)
        #genOut = tmpFile.read()
        #testOut = u'''\t"ikdummy1.1" [\n''' \
            #'''\t\tshape = "box",\n''' \
            #'''\t\tstyle = "filled,setlinewidth(0)",\n''' \
            #'''\t\tfillcolor = chartreuse2,\n''' \
            #'''\t\tmargin = 0,\n''' \
            #'''\t\thref = "/ikdummy1.1/@@details.html",\n''' \
            #'''\t\tlabel = <<TABLE BORDER = "0" CELLBORDER = "0" ''' \
            #'''CELLPADDING = "0" CELLSPACING = "0">''' \
            #'''<TR><TD><IMG SRC = "/home/markus/Projekte/''' \
            #'''ICT_Ok-hp/apple-red.png"/></TD></TR><TR><TD>''' \
            #'''<FONT FACE = "Arial" POINT-SIZE = "10">ikdummy1.1</FONT>''' \
            #'''</TD></TR></TABLE>>\n''' \
            #'''\t]; // ikdummy1.1\n''' \
            #'''\t"None" -- "ikdummy1.1"\n'''
        #self.assertEqual(genOut, testOut)

    #def test_genOut_ikdummy12(self):
        #tmpFile = os.tmpfile()
        #adapterGenGraphvizDot = IIkGenGraphvizDot(self.ikdummy12)
        #adapterGenGraphvizDot.setParent(self.root)
        #adapterGenGraphvizDot.traverse4DotGenerator(tmpFile, \
                                                            #level=1, \
                                                            #comments=False)
        #tmpFile.seek(0)
        #genOut = tmpFile.read()
        #testOut = u'''\t"ikdummy1.2" [\n''' \
            #'''\t\tshape = "box",\n''' \
            #'''\t\tstyle = "filled,setlinewidth(0)",\n''' \
            #'''\t\tfillcolor = chartreuse2,\n''' \
            #'''\t\tmargin = 0,\n''' \
            #'''\t\thref = "/ikdummy1.2/@@details.html",\n''' \
            #'''\t\tlabel = <<TABLE BORDER = "0" CELLBORDER = "0" ''' \
            #'''CELLPADDING = "0" CELLSPACING = "0">''' \
            #'''<TR><TD><IMG SRC = "/home/markus/Projekte/''' \
            #'''ICT_Ok-hp/apple-red.png"/></TD></TR><TR><TD>''' \
            #'''<FONT FACE = "Arial" POINT-SIZE = "10">ikdummy1.2</FONT>''' \
            #'''</TD></TR></TABLE>>\n''' \
            #'''\t]; // ikdummy1.2\n''' \
            #'''\t"None" -- "ikdummy1.2"\n'''
        #self.assertEqual(genOut, testOut)

    #def test_genOut_ikdummy13(self):
        #tmpFile = os.tmpfile()
        #adapterGenGraphvizDot = IIkGenGraphvizDot(self.ikdummy13)
        #adapterGenGraphvizDot.setParent(self.root)
        #adapterGenGraphvizDot.traverse4DotGenerator(tmpFile, \
                                                            #level=1, \
                                                            #comments=False)
        #tmpFile.seek(0)
        #genOut = tmpFile.read()
        #testOut = u'''\t"ikdummy1.3" [\n''' \
            #'''\t\tshape = "box",\n''' \
            #'''\t\tstyle = "filled,setlinewidth(0)",\n''' \
            #'''\t\tfillcolor = chartreuse2,\n''' \
            #'''\t\tmargin = 0,\n''' \
            #'''\t\thref = "/ikdummy1.3/@@details.html",\n''' \
            #'''\t\tlabel = <<TABLE BORDER = "0" CELLBORDER = "0" ''' \
            #'''CELLPADDING = "0" CELLSPACING = "0">''' \
            #'''<TR><TD><IMG SRC = "/home/markus/Projekte/''' \
            #'''ICT_Ok-hp/apple-red.png"/></TD></TR><TR><TD>''' \
            #'''<FONT FACE = "Arial" POINT-SIZE = "10">ikdummy1.3</FONT>''' \
            #'''</TD></TR></TABLE>>\n''' \
            #'''\t]; // ikdummy1.3\n''' \
            #'''\t"None" -- "ikdummy1.3"\n'''
        #self.assertEqual(genOut, testOut)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(AdminGraphvizIkDummyTestCase))
    return suite

if __name__ == '__main__':
    unittest.main()
