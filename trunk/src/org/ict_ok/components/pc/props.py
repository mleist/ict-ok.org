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

filename = r'pc'
longpath = r'org.ict_ok.components'
longpath_interface = longpath + r'.%s.interfaces' % (filename)
longpath_file = longpath + r'.%s.%s' % (filename, filename)
longpath_browser_file = longpath + r'.%s.browser.%s' % (filename, filename)
additionalClassImports = []

moduletitle = r'Personal Computer'
componentname = r'PersonalComputer'
#servicename = r'Test'
#serviceport = 65533
#utilityname = r'AdmUtil' + modulename
#loggername = r'AdmUtil' + modulename
#servicetitle = r'%s Service' % servicename

purpose = r"""PC instances

PC component will store personal computer properties
"""

attrDict = {
    'manufacturer': 'TextLine',
    'vendor': 'TextLine',
    'productionState': 'TextLine',
    'hardware': 'TextLine',
    'serialNumber': 'TextLine',
    'inv_id': 'TextLine',
    'modelType': 'TextLine',
    'deliveryDate': 'Date',
    }


attrTuples = [
    # (varName, schema, displayName, displayDescription)
    ('productionState', 'Choice', u'Production state', u'Production state of PC'),
    ('hardware', 'TextLine', u'Hardware', u'Hardware of the system.'),
    ('serialNumber', 'TextLine', u'Serial number', u'Serial number'),
    ('inv_id', 'TextLine', u'Inventory id', u'Id of inventory.'),
    ('modelType', 'TextLine', u'Model type', u'model type'),
    ('deliveryDate', 'Date', u'Delivery date', u'delivery date'),
    ('documentNumber', 'TextLine', u'Document number', u'Document number'),
    ('user', 'Choice', u'User', u'User of the PC'),
    ]

# '1'-part of the '1..n'-relation 
connInTuples = [
    # (varName, displayName, otherClassName)
    #('user', u'User', ''),
    ]

# 'n'-part of the '1..n'-relation 
connOutTuples = [
    # (varName, displayName, otherClassName)
    #('conns', u'ConnN', 'Conn'),
    ]
#additionalClassImports.append('from org.ict_ok.components.patchpanel.interfaces import IPatchPanel')

copyrights = [2009]

if __name__=="__main__":
    print filename + ".py"
