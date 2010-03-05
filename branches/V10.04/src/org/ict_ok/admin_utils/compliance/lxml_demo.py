# -*- coding: utf-8 -*-
#
# Copyright (c) 2007, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611
"""some demo code with lxml
"""

__version__ = "$Id$"

# python imports

# zope imports

# zc imports

# ict_ok.org imports
from org.ict_ok.admin_utils.compliance.requirement import Requirement

def lxmlDemo():
#    print "#" * 80
    
    reqMainList = []
    
        
    reqCompany = Requirement(
        u"M. GmbH",
        ikComment = u"vollständiger Requirement-Katalog")
    
    reqMainList.append(reqCompany)
    
    reqInfrastruktur = Requirement(
        u"Infrastruktur",
        ikComment = u"""Requirement-Katalog
        """)
    
    reqOrganisation = Requirement(
        u"Organisation",
        ikComment = u"""Requirement-Katalog
        """)
    
    reqPersonal = Requirement(
        u"Personal",
        ikComment = u"""Requirement-Katalog
        """)

    reqCompany.append(reqInfrastruktur)
    reqCompany.append(reqOrganisation)
    reqCompany.append(reqPersonal)

    reqFirewallKonzept01 = Requirement(
        u"Konzept für Sicherheitsgateways",
        ikComment = u"""Das Sicherheitsgateway muss
        
        * auf einer umfassenden Sicherheitsrichtlinie aufsetzen
        
        * im IT-Sicherheitskonzept der Organisation eingebettet sein
        
        * korrekt installiert
        
        * korrekt administriert werden
        """)
    reqOrganisation.append(reqFirewallKonzept01)

    
#    print reqMainList
#    print "-" * 80
    for reqMain in reqMainList:
        reqMain.asXml()
#    print "#" * 80
