#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: props.py 467 2009-03-05 04:28:59Z markusleist $
#

authors = [
   {r'name': r'Markus Leist',
    r'email': r'leist@ikom-online.de'},
    ]

filename = r'ip_address'
longpath = r'org.ict_ok.components'
longpath_interface = longpath + r'.%s.interfaces' % (filename)
longpath_file = longpath + r'.%s.%s' % (filename, filename)
longpath_browser_file = longpath + r'.%s.browser.%s' % (filename, filename)
additionalClassImports = []

moduletitle = r'IP address'
componentname = r'IpAddress'
#servicename = r'Test'
#serviceport = 65533
#utilityname = r'AdmUtil' + modulename
#loggername = r'AdmUtil' + modulename
#servicetitle = r'%s Service' % servicename

purpose = r"""test component

An IP address instance will store some IP settings
"""

attrDict = {
#    'attr1': 'TextLine',
#    'attr2': 'Choice',
#    'attr3': 'Date',
    }

attrTuples = [
    # (varName, schema, displayName, displayDescription)
#    ('attr1', 'TextLine', u'Text line', u'long description text line'),
#    ('attr2', 'Choice', u'display Choice', u'long description choice'),
    ('ipv4', 'NetIpValid', u'IP Address', u'IP address of the device.'),
    ]
additionalClassImports.append('from org.ict_ok.schema.ipvalid import NetIpValid')

# '1'-part of the '1..n'-relation 
connInTuples = [
    # (varName, displayName, otherClassName)
    ('interface', u'Interface', 'Interface'),
    ('ipNet', u'IP Net', 'IpNet'),
    ]
additionalClassImports.append('from org.ict_ok.components.interface.interface import Interface_IpAddresses_RelManager')
additionalClassImports.append('from org.ict_ok.components.interface.interfaces import IInterface')
additionalClassImports.append('from org.ict_ok.components.ipnet.ipnet import IpNet_IpAddresses_RelManager')
additionalClassImports.append('from org.ict_ok.components.ipnet.interfaces import IIpNet')

# 'n'-part of the '1..n'-relation 
connOutTuples = [
    # (varName, displayName, otherClassName)
    #('conns', u'ConnN', 'Conn'),
    ]
#additionalClassImports.append('from org.ict_ok.components.patchpanel.interfaces import IPatchPanel')

copyrights = [2009]

if __name__=="__main__":
    print filename + ".py"
