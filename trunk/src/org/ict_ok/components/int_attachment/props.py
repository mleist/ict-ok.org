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

filename = r'int_attachment'
longpath = r'org.ict_ok.components'
longpath_interface = longpath + r'.%s.interfaces' % (filename)
longpath_file = longpath + r'.%s.%s' % (filename, filename)
longpath_browser_file = longpath + r'.%s.browser.%s' % (filename, filename)
additionalClassImports = []

moduletitle = r'Internal Attachment'
componentname = r'InternalAttachment'
#servicename = r'Test'
#serviceport = 65533
#utilityname = r'AdmUtil' + modulename
#loggername = r'AdmUtil' + modulename
#servicetitle = r'%s Service' % servicename

purpose = r"""attachment component

a possible storage for file attachment on superclass objects
"""

attrTuples = [
    # (varName, schema, displayName, displayDescription)
    ('filename', 'TextLine', u'filename', u'long description text line'),
    ('mimeType', 'TextLine', u'mime type', u'long description choice'),
    ('data', 'Byte', u'data', u'long description date'),
    ]

# '1'-part of the '1..n'-relation 
connInTuples = [
    # (varName, displayName, otherClassName)
    ]

# 'n'-part of the '1..n'-relation 
connOutTuples = [
    # (varName, displayName, otherClassName)
    ]

copyrights = [2009]

if __name__=="__main__":
    print filename + ".py"
