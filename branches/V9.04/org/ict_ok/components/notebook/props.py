#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: props.py 405 2009-01-16 22:03:13Z markusleist $
#

authors = [
   {r'name': r'Markus Leist',
    r'email': r'leist@ikom-online.de'},
    ]

filename = r'notebook'
longpath = r'org.ict_ok.components'
longpath_interface = longpath + r'.%s.interfaces' % (filename)
longpath_file = longpath + r'.%s.%s' % (filename, filename)
longpath_browser_file = longpath + r'.%s.browser.%s' % (filename, filename)

moduletitle = r'Notebook'
componentname = r'Notebook'
#servicename = r'Test'
#serviceport = 65533
#utilityname = r'AdmUtil' + modulename
#loggername = r'AdmUtil' + modulename
#servicetitle = r'%s Service' % servicename

purpose = r"""notebook instances

notebook component will store notebook properties
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

copyrights = [2008, 2009]

if __name__=="__main__":
    print filename + ".py"
