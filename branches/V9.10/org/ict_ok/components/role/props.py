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
   {r'name': r'Sebastian Napiorkowski',
    r'email': r'leist@ikom-online.de'},
    ]

filename = r'role'
longpath = r'org.ict_ok.components'
longpath_interface = longpath + r'.%s.interfaces' % (filename)
longpath_file = longpath + r'.%s.%s' % (filename, filename)
longpath_browser_file = longpath + r'.%s.browser.%s' % (filename, filename)
additionalClassImports = []

moduletitle = r'Role'
componentname = r'Role'
#servicename = r'Test'
#serviceport = 65533
#utilityname = r'AdmUtil' + modulename
#loggername = r'AdmUtil' + modulename
#servicetitle = r'%s Service' % servicename

purpose = r"""role

The Role object class is used to represent a position or set of
responsibilities within an organization, organizational unit or
other scope, and MAY be filled by a person or persons
(or non-human entities represented by ManagedSystemElement subclasses)
"""

attrTuples = [
    # (varName, schema, displayName, displayDescription)
    ]

# '1'-part of the '1..n'-relation 
connInTuples = [
    # (varName, displayName, otherClassName)
    ]

# 'n'-part of the '1..n'-relation 
connOutTuples = [
    # (varName, displayName, otherClassName)
    ('contactItems', u'Contact items', 'ContactItem'),
    ]
additionalClassImports.append('from org.ict_ok.components.contact_item.interfaces import IContactItem')

copyrights = [2009]

if __name__=="__main__":
    print filename + ".py"
