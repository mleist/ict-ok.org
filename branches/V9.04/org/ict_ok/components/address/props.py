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

filename = r'address'
longpath = r'org.ict_ok.components'
longpath_interface = longpath + r'.%s.interfaces' % (filename)
longpath_file = longpath + r'.%s.%s' % (filename, filename)
longpath_browser_file = longpath + r'.%s.browser.%s' % (filename, filename)
additionalClassImports = []

moduletitle = r'Address'
componentname = r'Address'

purpose = r"""Address instance
"""
# ------------------------------------------

attrTuples = []

# '1'-part of the '1..n'-relation 
connInTuples = []

# 'n'-part of the '1..n'-relation 
connOutTuples = []

attrTuples.append(\
    ('address1', 'TextLine', u'Address1', u'Address line 1'))
attrTuples.append(\
    ('address2', 'TextLine', u'Address2', u'Address line 2'))
attrTuples.append(\
    ('address3', 'TextLine', u'Address3', u'Address line 3'))
attrTuples.append(\
    ('city', 'TextLine', u'City', u'City'))
attrTuples.append(\
    ('postalCode', 'TextLine', u'Postal code', u'Postal code'))
attrTuples.append(\
    ('country', 'TextLine', u'Country', u'Country'))
    
connInTuples.append(('contactItem', u'Contact item', 'ContactItem'))  # mul 1
    

#additionalClassImports.append('from org.ict_ok.schema.ipvalid import NetIpValid')

# '1'-part of the '1..n'-relation 
#additionalClassImports.append('from org.ict_ok.components.interface.interface import Interface_IpAddresses_RelManager')
#additionalClassImports.append('from org.ict_ok.components.interface.interfaces import IInterface')
#additionalClassImports.append('from org.ict_ok.components.ipnet.ipnet import IpNet_IpAddresses_RelManager')
#additionalClassImports.append('from org.ict_ok.components.ipnet.interfaces import IIpNet')
additionalClassImports.append('from org.ict_ok.components.contact_item.contact_item import ContactItem_Addresss_RelManager')
additionalClassImports.append('from org.ict_ok.components.contact_item.interfaces import IContactItem')

# 'n'-part of the '1..n'-relation 
#additionalClassImports.append('from org.ict_ok.components.patchpanel.interfaces import IPatchPanel')

copyrights = [2009]

if __name__=="__main__":
    print filename + ".py"
