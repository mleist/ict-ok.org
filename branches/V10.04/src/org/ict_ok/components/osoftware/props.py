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

filename = r'osoftware'
longpath = r'org.ict_ok.components'
longpath_interface = longpath + r'.%s.interfaces' % (filename)
longpath_file = longpath + r'.%s.%s' % (filename, filename)
longpath_browser_file = longpath + r'.%s.browser.%s' % (filename, filename)

moduletitle = r'Operating Software Instance'
componentname = r'OperatingSoftware'
#servicename = r'Test'
#serviceport = 65533
#utilityname = r'AdmUtil' + modulename
#loggername = r'AdmUtil' + modulename
#servicetitle = r'%s Service' % servicename

purpose = r"""operating software component

A software component which will hold information about the operating systems
"""

attrDict = {
    'manufacturer': 'TextLine',
    'osType': 'TextLine',
    'otherType': 'TextLine',
    'manufacturer': 'TextLine',
    'versionText': 'TextLine',
    'licenseKey': 'TextLine',
    'language': 'TextLine',
    'majorVersion': 'Int',
    'minorVersion': 'Int',
    'revisionNumber': 'Int',
    'buildNumber': 'Int',
    }

copyrights = [2008, 2009]

if __name__=="__main__":
    print filename + ".py"
