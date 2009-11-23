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

filename = r'contract'
longpath = r'org.ict_ok.components'
longpath_interface = longpath + r'.%s.interfaces' % (filename)
longpath_file = longpath + r'.%s.%s' % (filename, filename)
longpath_browser_file = longpath + r'.%s.browser.%s' % (filename, filename)
additionalClassImports = []

moduletitle = r'Contract'
componentname = r'Contract'
#servicename = r'Test'
#serviceport = 65533
#utilityname = r'AdmUtil' + modulename
#loggername = r'AdmUtil' + modulename
#servicetitle = r'%s Service' % servicename

purpose = r"""contract

A contract component will manage all object and their contractors
"""

attrTuples = [
    # (varName, schema, displayName, displayDescription)
    ]

attrTuples.append(\
    ('type', '', u'Contract type', u'Contract type'))
attrTuples.append(\
    ('contractor', 'ContactItem.ContactItem', u'Contractor', u'Contractor'))
attrTuples.append(\
    ('startDate', 'Date', u'start date', u'contract start date'))
attrTuples.append(\
    ('state', '', u'State', u'State'))
attrTuples.append(\
    ('expirationDate', 'Date', u'expiration date', u'expiration of contract'))
attrTuples.append(\
    ('annualCharges', 'PhysicalQuantity', u'annual charges', u'annual charges'))
attrTuples.append(\
    ('internalContractNumber', 'string', u'internal contract number', u'internal contract number'))
attrTuples.append(\
    ('externalContractNumber', 'string', u'external contract number', u'external contract number'))
attrTuples.append(\
    ('responsible', 'ContactItem.ContactItem', u'responsible', u'responsible'))
attrTuples.append(\
    ('periodOfNotice', 'Timedelta', u'period of notice', u'period of notice'))
attrTuples.append(\
    ('minimumTerm', 'Timedelta', u'minimum term', u'minimum term'))

# '1'-part of the '1..n'-relation 
connInTuples = [
    # (varName, displayName, otherClassName)
    ]

connInTuples.append(('component', u'Component', 'Component'))  # mul 1
additionalClassImports.append('from org.ict_ok.components.component.component import Component_Contracts_RelManager')
additionalClassImports.append('from org.ict_ok.components.component.interfaces import IComponent')


# 'n'-part of the '1..n'-relation 
connOutTuples = [
    # (varName, displayName, otherClassName)
    ]
#additionalClassImports.append('from org.ict_ok.components.patchpanel.interfaces import IPatchPanel')

copyrights = [2009]

if __name__=="__main__":
    print filename + ".py"
