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

filename = r'product'
longpath = r'org.ict_ok.components'
longpath_interface = longpath + r'.%s.interfaces' % (filename)
longpath_file = longpath + r'.%s.%s' % (filename, filename)
longpath_browser_file = longpath + r'.%s.browser.%s' % (filename, filename)
additionalClassImports = []

moduletitle = r'Product'
componentname = r'Product'

purpose = r"""product instance

Product instance will store the product attributes.
"""
# ------------------------------------------

attrTuples = []

# '1'-part of the '1..n'-relation 
connInTuples = []

# 'n'-part of the '1..n'-relation 
connOutTuples = []

connOutTuples.append(('subProducts', u'Sub products', 'Product')) # other mul
connInTuples.append(('mainProduct', u'Main product', 'Product'))  # mul 1
connInTuples.append(('workOrder', u'Work order', 'WorkOrder'))  # mul 1
    

#additionalClassImports.append('from org.ict_ok.schema.ipvalid import NetIpValid')

# '1'-part of the '1..n'-relation 
#additionalClassImports.append('from org.ict_ok.components.interface.interface import Interface_IpAddresses_RelManager')
#additionalClassImports.append('from org.ict_ok.components.interface.interfaces import IInterface')
#additionalClassImports.append('from org.ict_ok.components.ipnet.ipnet import IpNet_IpAddresses_RelManager')
#additionalClassImports.append('from org.ict_ok.components.ipnet.interfaces import IIpNet')
additionalClassImports.append('from org.ict_ok.components.work_order.work_order import WorkOrder_Products_RelManager')
additionalClassImports.append('from org.ict_ok.components.work_order.interfaces import IWorkOrder')

# 'n'-part of the '1..n'-relation 
#additionalClassImports.append('from org.ict_ok.components.patchpanel.interfaces import IPatchPanel')

copyrights = [2009]

if __name__=="__main__":
    print filename + ".py"
