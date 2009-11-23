#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#

authors = [
   {r'name': r'Markus Leist',
    r'email': r'leist@ikom-online.de'},
    ]

filename = r'test'
longpath = r'org.ict_ok.components'
longpath_interface = longpath + r'.%s.interfaces' % (filename)
longpath_file = longpath + r'.%s.%s' % (filename, filename)
longpath_browser_file = longpath + r'.%s.browser.%s' % (filename, filename)
additionalClassImports = []

moduletitle = r'Test Component Instance'
componentname = r'TestComponent'
#servicename = r'Test'
#serviceport = 65533
#utilityname = r'AdmUtil' + modulename
#loggername = r'AdmUtil' + modulename
#servicetitle = r'%s Service' % servicename

purpose = r"""test component

A test component will server some tests ...
"""

attrDict = {
    'attr1': 'TextLine',
    'attr2': 'Choice',
    'attr3': 'Date',
    }

attrTuples = [
    # (varName, schema, displayName, displayDescription)
    ('attr1', 'TextLine', u'Text line', u'long description text line'),
    ('attr2', 'Choice', u'display Choice', u'long description choice'),
    ('attr3', 'Date', u'display Date', u'long description date'),
    ]

# '1'-part of the '1..n'-relation 
connInTuples = [
    # (varName, displayName, otherClassName)
    ('conn', u'Conn1', 'Conn'),
    ]

# 'n'-part of the '1..n'-relation 
connOutTuples = [
    # (varName, displayName, otherClassName)
    ('conns', u'ConnN', 'Conn'),
    ]
additionalClassImports.append('from org.ict_ok.components.patchpanel.interfaces import IPatchPanel')

copyrights = [2006, 2007, 2008, 2009]

if __name__=="__main__":
    print filename + ".py"
