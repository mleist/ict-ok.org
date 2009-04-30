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

filename = r'rack'
longpath = r'org.ict_ok.components'
longpath_interface = longpath + r'.%s.interfaces' % (filename)
longpath_file = longpath + r'.%s.%s' % (filename, filename)
longpath_browser_file = longpath + r'.%s.browser.%s' % (filename, filename)
additionalClassImports = []

moduletitle = r'Device rack'
componentname = r'Rack'
#servicename = r'Test'
#serviceport = 65533
#utilityname = r'AdmUtil' + modulename
#loggername = r'AdmUtil' + modulename
#servicetitle = r'%s Service' % servicename

purpose = r"""device rack

there are devices and patch panels in a rack
"""

attrDict = {
    'height': 'Int',
    }

attrTuples = [
    # (varName, schema, displayName, displayDescription)
    ('height', 'Int', u'Height', u'Height of the rack'),
    ]

# '1'-part of the '1..n'-relation 
connInTuples = [
    # (varName, displayName, otherClassName)
    ('room', u'Room', 'Room'),
    ]
additionalClassImports.append('from org.ict_ok.components.room.room import Room_Racks_RelManager')
additionalClassImports.append('from org.ict_ok.components.room.interfaces import IRoom')

# 'n'-part of the '1..n'-relation 
connOutTuples = [
    # (varName, displayName, otherClassName)
    ('patchpanels', u'Patchpanel', 'PatchPanel'),
    ]
additionalClassImports.append('from org.ict_ok.components.patchpanel.interfaces import IPatchPanel')


copyrights = [2009]

if __name__=="__main__":
    print filename + ".py"
