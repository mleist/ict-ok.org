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

filename = r'patchpanel'
longpath = r'org.ict_ok.components'
longpath_interface = longpath + r'.%s.interfaces' % (filename)
longpath_file = longpath + r'.%s.%s' % (filename, filename)
longpath_browser_file = longpath + r'.%s.browser.%s' % (filename, filename)
additionalClassImports = []

moduletitle = r'Patch panel'
componentname = r'PatchPanel'
#servicename = r'Test'
#serviceport = 65533
#utilityname = r'AdmUtil' + modulename
#loggername = r'AdmUtil' + modulename
#servicetitle = r'%s Service' % servicename

purpose = r"""patch panel

A patch panel will contain n patch ports
"""

attrTuples = [
    # (varName, schema, displayName, displayDescription)
    #('attr1', 'TextLine', u'Text line', u'long description text line'),
    #('attr2', 'Choice', u'display Choice', u'long description choice'),
    #('attr3', 'Date', u'display Date', u'long description date'),
    ('portCount', 'Int', u'Port quantity', u'Quantity of all patch ports'),
    ]

# '1'-part of the '1..n'-relation 
connInTuples = [
    # (varName, displayName, otherClassName)
    ('rack', u'Rack', 'Rack'),
    ]
additionalClassImports.append('from org.ict_ok.components.rack.rack import Rack_PatchPanels_RelManager')
additionalClassImports.append('from org.ict_ok.components.rack.interfaces import IRack')

# 'n'-part of the '1..n'-relation 
connOutTuples = [
    # (varName, displayName, otherClassName)
    ('patchports', u'Patch ports', 'PatchPort'),
    ]
additionalClassImports.append('from org.ict_ok.components.patchport.interfaces import IPatchPort')

copyrights = [2009]

if __name__=="__main__":
    print filename + ".py"
