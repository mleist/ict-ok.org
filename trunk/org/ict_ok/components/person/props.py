#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: generation_settings 518 2009-05-09 10:42:45Z markusleist $
#
# pylint: disable-msg=
#

authors = [
   {r'name': r'Markus Leist',
    r'email': r'leist@ikom-online.de'},
    ]

filename = r'person'
longpath = r'org.ict_ok.components'
longpath_interface = longpath + r'.%s.interfaces' % (filename)
longpath_file = longpath + r'.%s.%s' % (filename, filename)
longpath_browser_file = longpath + r'.%s.browser.%s' % (filename, filename)
additionalClassImports = []

moduletitle = r'Person'
componentname = r'Person'

purpose = r"""person instance

Person instance will store direct personal attributes.
"""
# ------------------------------------------

attrTuples = []

# '1'-part of the '1..n'-relation 
connInTuples = []

# 'n'-part of the '1..n'-relation 
connOutTuples = []

attrTuples.append(\
    ('firstName', 'TextLine', u'first name', u'first name of the person'))
attrTuples.append(\
    ('lastName', 'TextLine', u'last name', u'last name of person'))
attrTuples.append(\
    ('title', 'TextLine', u'title', u'title of person'))


#additionalClassImports.append('from org.ict_ok.schema.ipvalid import NetIpValid')

# '1'-part of the '1..n'-relation 
#additionalClassImports.append('from org.ict_ok.components.interface.interface import Interface_IpAddresses_RelManager')
#additionalClassImports.append('from org.ict_ok.components.interface.interfaces import IInterface')
#additionalClassImports.append('from org.ict_ok.components.ipnet.ipnet import IpNet_IpAddresses_RelManager')
#additionalClassImports.append('from org.ict_ok.components.ipnet.interfaces import IIpNet')

# 'n'-part of the '1..n'-relation 
#additionalClassImports.append('from org.ict_ok.components.patchpanel.interfaces import IPatchPanel')

copyrights = [2009]

if __name__=="__main__":
    print filename + ".py"
