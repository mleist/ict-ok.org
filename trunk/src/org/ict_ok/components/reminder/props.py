#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: props.py 465 2009-03-05 02:34:02Z markusleist $
#

authors = [
   {r'name': r'Markus Leist',
    r'email': r'leist@ikom-online.de'},
    ]

filename = r'reminder'
longpath = r'org.ict_ok.components'
longpath_interface = longpath + r'.%s.interfaces' % (filename)
longpath_file = longpath + r'.%s.%s' % (filename, filename)
longpath_browser_file = longpath + r'.%s.browser.%s' % (filename, filename)
additionalClassImports = []

moduletitle = r'Reminder'
componentname = r'Reminder'
#servicename = r'Test'
#serviceport = 65533
#utilityname = r'AdmUtil' + modulename
#loggername = r'AdmUtil' + modulename
#servicetitle = r'%s Service' % servicename

purpose = r"""Reminder

A reminder component will generate a reminder letter to some persons
"""

attrTuples = [
    # (varName, schema, displayName, displayDescription)
    ]

attrTuples.append(\
            ('dueDate', 'Date', u'due date', u'due date of reminder'))
            

# '1'-part of the '1..n'-relation 
connInTuples = [
    # (varName, displayName, otherClassName)
    ]
#connInTuples.append(('component', u'Component', 'Component'))  # mul 1
#additionalClassImports.append('from org.ict_ok.components.work_order.work_order import WorkOrder_Contact_RelManager')
#additionalClassImports.append('from org.ict_ok.components.work_order.interfaces import IWorkOrder')


# 'n'-part of the '1..n'-relation 
connOutTuples = [
    # (varName, displayName, otherClassName)
    ]
#additionalClassImports.append('from org.ict_ok.components.patchpanel.interfaces import IPatchPanel')

copyrights = [2009]

if __name__=="__main__":
    print filename + ".py"
