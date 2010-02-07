# -*- coding: utf-8 -*-
#
# Copyright (c) 2007, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101
#
"""compliance utility

the compliance utility should store the compliance/requirement-templates
for the host- or service-instances
"""

__version__ = "$Id$"

# python imports
import logging
import transaction
from datetime import datetime

# zope imports
from zope.app.appsetup import appsetup
from zope.app.appsetup.bootstrap import getInformationFromEvent
from zope.app.appsetup.bootstrap import ensureUtility
from zope.dublincore.interfaces import IWriteZopeDublinCore
from zope.location.interfaces import ISite
from zope.app.container.interfaces import IContainer

# ict_ok.org imports
from org.ict_ok.admin_utils.supervisor.interfaces import \
     IAdmUtilSupervisor
from org.ict_ok.admin_utils.compliance.interfaces import \
     IAdmUtilCompliance
from org.ict_ok.admin_utils.compliance.compliance import \
     AdmUtilCompliance
from org.ict_ok.admin_utils.compliance.requirement import Requirement

logger = logging.getLogger("AdmUtilCompliance")

#from org.ict_ok.admin_utils.compliance.req_imports import fillUtilitiyWithReqs
def fillUtilitiyWithReqs(context):
    managementOBJ = context
    delKeys = [key for key in managementOBJ.keys()]
    for delKey in delKeys:
        del managementOBJ[delKey]
    #
    # sorry, only a very first draft in german
    #
    # ###################################################################
    # ##########  vollständiger Requirement-Katalog  ####################
    # ###################################################################
    # ##########  detaillierte Übersicht für Mitarbeiter
    
    reqItMediaVentures = Requirement(
        u"IT-Anforderungen M. GmbH",
        ikComment = u"vollständiger Requirement-Katalog")
    managementOBJ.append(reqItMediaVentures)
    
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
    
    reqHardwareSoftware = Requirement(
        u"Hardware und Software",
        ikComment = u"""Requirement-Katalog
        """)
    
    reqKommunikation = Requirement(
        u"Kommunikation",
        ikComment = u"""Requirement-Katalog
        """)
    
    reqNotfallvorsorge = Requirement(
        u"Notfallvorsorge",
        ikComment = u"""Requirement-Katalog
        """)
    
    
    reqItMediaVentures.append(reqInfrastruktur)
    reqItMediaVentures.append(reqOrganisation)
    reqItMediaVentures.append(reqPersonal)
    reqItMediaVentures.append(reqHardwareSoftware)
    reqItMediaVentures.append(reqKommunikation)
    reqItMediaVentures.append(reqNotfallvorsorge)
    
    
    # ###################################################################
    # ###################################################################
    # ###################################################################
    
    
    # ###################################################################
    
    #
    # ##########  Doku: Verantwortlichkeiten, Stellvertretungen, Organisation
    #
    reqDokuVerantwortlichkeiten = Requirement(
        u"Doku: Verantwortlichkeiten",
        ikComment = u"""Doku:
        
        * Verantwortlichkeiten
        
        * Stellvertretungen
        
        * Organisation
        """)
    reqOrganisation.append(reqDokuVerantwortlichkeiten)
    
    # ###################################################################
    
    #
    # ##########  Doku: externe Ansprechpartner, Anlagen, Verträge
    #
    reqDokuExterne = Requirement(
        u"Doku: externe Ansprechpartner",
        ikComment = u"""Doku:
        
        * externe Ansprechpartner
        
        * Anlagen
        
        * Verträge
        """)
    reqOrganisation.append(reqDokuExterne)
    
    # ###################################################################
    
    #
    # ##########  Doku: Richtlinien, Handlungsanweisungen
    #
    reqDokuRichtlinien = Requirement(
        u"Doku: Richtlinien, Handlungsanweisungen",
        ikComment = u"""Doku:
        
        * Richtlinien
        
        * Handlungsanweisungen
        """)
    reqOrganisation.append(reqDokuRichtlinien)
    
    # ###################################################################
    
    #
    # ##########  Doku: Systeme
    #
    reqDokuSysteme = Requirement(
        u"Doku: Systeme",
        ikComment = u"""Doku:
        
        * Host-Systeme
        
        * Netzwerke (Ebene 1, 2; Ethernet)
        
        * Netzwerke (Ebene 3, 4; IP, TCP)
        
        * Dienste (Ebene 7; Anwendungen)
        """)
    reqOrganisation.append(reqDokuSysteme)
    
    # ###################################################################
    
    #
    # ##########  Monitoring
    #
    reqMonitoring = Requirement(
        u"Monitoring",
        ikComment = u"""Netzwerk-Monitoring:
        
        * Host-Verfügbarkeiten
        
        * Dienste-Verfügbarkeiten
        """)
    reqHardwareSoftware.append(reqMonitoring)
    
    # ###################################################################
    
    #
    # ##########  Changemanagement
    #
    reqChangemanagement = Requirement(
        u"Changemanagement",
        ikComment = u"""Changemanagement, Konzepte und deren Umsetzungen
        
        Ein hoher Anteil von kostenintensiven IT-Service-Störungen lässt sich
        häufig auf schlecht koordinierte oder unzureichend gesteuerte
        Veränderungen an der IT-Servicelandschaft zurückverfolgen.
        Diese Störungen können bei der heutigen Verknüpfung der IT mit den
        führenden Prozessen eines Unternehmens durchaus enorme wirtschaftliche
        Kosten nach sich ziehen. Dies rechtfertigt Investitionen in Prozesse,
        in welchen der Bedarf für einen Change und die möglichen negativen
        Auswirkungen geprüft und die Störungen durch entsprechende Maßnahmen
        auf ein akzeptables Minimum reduziert werden.
    
        Es ist die Aufgabe des Change-Managements, sicherzustellen, dass
        standardisierte Methoden und Verfahren zur Durchführung von 
        Veränderungen existieren und effizient genutzt werden.
        """)
    reqOrganisation.append(reqChangemanagement)
    
    reqChangemanagement01 = Requirement(
        u"Change-Management-Prozess",
        ikComment = u"""Es existiert ein definierter Change-Management-Prozess
        
        Der prinzipielle Ablauf ist unabhängig davon, ob es sich um einen kleinen
        Change, wie vielleicht das Erweitern des Arbeitsspeichers eines Servers,
        oder ein Projekt mit erheblicher Auswirkung auf den bestehenden Betrieb
        handelt. Auch die Dringlichkeit hat keinen Einfluss auf den Ablauf selbst,
        jedoch sind die Ablaufgeschwindigkeiten und Prioritäten unterschiedlich.
        """)
    
    reqChangemanagement01_RFC = Requirement(
        u"Request for Change",
        ikComment = u"""Teil des Change-Management-Prozesses:
        
        RFC - zu deutsch Änderungsantrag.
        
        Mit der formellen Registrierung des Antrages beginnt der Lebenszyklus
        eines Changes. Der RFC ist das eigentliche Logbuch, also die Sammlung
        aller Aktivitäten dieses Lebenszyklus. Alle Aktivitäten, Diskussionen,
        Beschreibungen, Analysen, Dokumentationen und Entscheidungen bezüglich
        einer Veränderung werden hier festgehalten.
        """)
    
    reqChangemanagement01_Registrierung = Requirement(
        u"Registrierung und Klassifizierung",
        ikComment = u"""Teil des Change-Management-Prozesses:
        
        Sammeln der benötigten Informationen, um Entscheidungen darüber zu
        treffen, was geändert werden muss, in welche Kategorie der Change fällt
        und welche Auswirkungen er hat, um die Genehmigung angemessen durchführen
        zu können. Eine Priorität und Kategorie wird dem Change basierend auf
        dessen Auswirkung zugewiesen. Risikoabschätzung ist in diesem Stadium von
        entscheidender Bedeutung.
        """)
    
    reqChangemanagement01_Planung = Requirement(
        u"Überwachung und Planung",
        ikComment = u"""Teil des Change-Management-Prozesses:
        
        Alle Changes werden unter der Verantwortung des Change-Managements
        geplant und wenn dies für die optimale Kontrolle des/der Changes
        notwendig ist, wird ein kompletter Zeitplan (mit Meilensteinen)
        bereitgestellt.
        """)
    
    reqChangemanagement01_Genehmigung = Requirement(
        u"Genehmigung",
        ikComment = u"""Teil des Change-Management-Prozesses:
        
        Entscheidung, ob der Change durchgeführt wird oder nicht.
        """)
    
    reqChangemanagement01_Test = Requirement(
        u"Ausarbeitung und Test",
        ikComment = u"""Teil des Change-Management-Prozesses:
        
        Genehmigte Changes werden zur Ausarbeitung an die entsprechenden
        Mitarbeiter/Dienstleister weitergegeben. Das Change-Management übernimmt -
        unterstützt durch Release-Management und normales Linien-Management -
        die Koordination, um sicherzustellen, dass die Aktivitäten sowohl die
        erforderlichen Ressourcen bekommen als auch innerhalb des vorgegebenen
        Zeitplans durchgeführt werden. Um zu verhindern, dass die Changes
        schwerwiegende Auswirkungen auf die Service-Qualität haben, wird
        empfohlen, die Changes vor der Implementierung genauestens zu Testen und
        Back-Out-Pläne vorzusehen.
        """)
    
    reqChangemanagement01_Freigabe = Requirement(
        u"Freigabe der Implementierung",
        ikComment = u"""Teil des Change-Management-Prozesses:
        
        Nach einem geeigneten Test und der Überprüfung, dass alle notwendigen
        Aktionen durchgeführt wurden, zum Beispiel Prüfung auf Vorhandensein 
        eines Back-Out-Plans, kann der Change zur Durchführung freigegeben werden.
        """)
    
    reqChangemanagement01_Implementierung = Requirement(
        u"Implementierung",
        ikComment = u"""Teil des Change-Management-Prozesses:
        
        Es ist die Aufgabe des Change-Managements dafür zu sorgen, dass die
        Changes im vorgesehenen Zeitrahmen implementiert werden. Dies wird
        jedoch meistens die Koordination des Changes bedeuten, da die eigentliche
        Ausführung in der Verantwortung von Anderen liegt (z. B. werden Hardware-
        und Software-Änderungen von Administratoren bzw. durch entsprechende
        Dienstleister durchgeführt.).
        """)
    
    reqChangemanagement.append(reqChangemanagement01)
    
    reqChangemanagement01.append(reqChangemanagement01_RFC)
    reqChangemanagement01.append(reqChangemanagement01_Registrierung)
    reqChangemanagement01.append(reqChangemanagement01_Planung)
    reqChangemanagement01.append(reqChangemanagement01_Genehmigung)
    reqChangemanagement01.append(reqChangemanagement01_Test)
    reqChangemanagement01.append(reqChangemanagement01_Freigabe)
    reqChangemanagement01.append(reqChangemanagement01_Implementierung)
    
    
    # ###################################################################
    
    
    # ###################################################################
    
    #
    # ##########  Firewall
    # 
    
    reqFirewallKonzept01 = Requirement(
        u"Konzept für Sicherheitsgateways",
        ikComment = u"""Das Sicherheitsgateway muss
        
        * auf einer umfassenden Sicherheitsrichtlinie aufsetzen
        
        * im IT-Sicherheitskonzept der Organisation eingebettet sein
        
        * korrekt installiert
        
        * korrekt administriert werden
        """)
    reqOrganisation.append(reqFirewallKonzept01)
    
    # ###################################################################
    
    #
    # ##########  Performance Messungen
    #
    reqPerformance = Requirement(
        u"Performance Messungen",
        ikComment = u"""Messungen von
        
        * Bandbreiten
        
        * Latenzen
        """)
    reqKommunikation.append(reqPerformance)
    
    # ###################################################################
    
    #
    # ##########  Protokollierungen
    #
    reqProtokollierungen = Requirement(
        u"Protokollierungen",
        ikComment = u"""Protokollierungen von
        
        * Störungen
        
        * Missbrauch
        """)
    reqHardwareSoftware.append(reqProtokollierungen)
    
    # ###################################################################
    
    #
    # ##########  Systemkonfiguration
    #
    reqSystemkonfiguration = Requirement(
        u"Systemkonfiguration",
        ikComment = u"""Systemkonfiguration von
        
        * Host-Systemen
        
        * Diensten
        """)
    reqHardwareSoftware.append(reqSystemkonfiguration)
    
    # ###################################################################
    
    #
    # ##########  Auditierungen / Überprüfungen
    #
    reqAuditierungen = Requirement(
        u"Auditierungen / Überprüfungen",
        ikComment = u"""Auditierungen
        
        * automatisch
        
        * händisch
        """)
    reqOrganisation.append(reqAuditierungen)
    
    # ###################################################################
    
    #
    # ##########  Änderungsdokumentation
    #
    reqDokuAenderungen = Requirement(
        u"Änderungsdokumentation",
        ikComment = u"""Änderungsdokumentation
        
        * vollautomatisch
        
        * halbautomatisch
        
        * händisch
        """)
    reqHardwareSoftware.append(reqDokuAenderungen)
    
    # ###################################################################
    
    #
    # ##########  Antiviren-Konzept
    #
    reqAntiviren = Requirement(
        u"Antiviren",
        ikComment = u"""Antiviren-Konzepte und deren Umsetzung
        
        Einsatz eines Anti-Viren-Programms
        """)
    reqHardwareSoftware.append(reqAntiviren)
    
    # ###################################################################
    
    #
    # ##########  Backup
    #
    reqBackup = Requirement(
        u"Backup",
        ikComment = u"Backup-Konzepte und deren Umsetzungen")
    reqNotfallvorsorge.append(reqBackup)
    
    # ###################################################################
    
    #
    # ##########  Nutzer-Authentifierung
    #
    reqAuthentifierung = Requirement(
        u"Nutzer-Authentifierung",
        ikComment = u"""Nutzer-Authentifierung
        
        * Konzepte
        
        * Verfahren
        """)
    reqHardwareSoftware.append(reqAuthentifierung)
    
    # ###################################################################
    
    #
    # ##########  Verschlüsselung
    #
    reqVerschluesselung = Requirement(
        u"Verschlüsselung",
        ikComment = u"""Verschlüsselung für
        
        * Arbeitsplatz-Rechner
        
        * Notebooks
        
        * Server-Laufwerke
        
        * Server-Dateien
        """)
    reqHardwareSoftware.append(reqVerschluesselung)
    
    # ###################################################################
    
    #
    # ##########  Template
    #
    reqTemplate = Requirement(
        u"Template",
        ikComment = u"""Template:
        
        * Punkt1
        
        * Punkt2
        """)
    
    # ###################################################################
    # ###################################################################
    # ###################################################################
    
    # ###################################################################
    # ##########  IT-Sicherheitskonzept            ######################
    # ###################################################################
    # ##########  Übersicht für Wirtschaftsprüfer u.a.
    
    reqItSicherheitskonzept = Requirement(
        u"IT-Sicherheitskonzept",
        ikComment = u"speziell die Kurzdarstellung")
    managementOBJ.append(reqItSicherheitskonzept)
    
    reqStoerungenMissbrauch = Requirement(
        u"Störungen und Missbrauch verhindern",
        ikComment = u"innerhalb der Kurzdarstellung")
    reqItSicherheitskonzept.append(reqStoerungenMissbrauch)
    
    reqStoerungenMissbrauch.append(reqDokuSysteme)
    reqStoerungenMissbrauch.append(reqChangemanagement)
    reqStoerungenMissbrauch.append(reqFirewallKonzept01)
    reqStoerungenMissbrauch.append(reqProtokollierungen)
    reqStoerungenMissbrauch.append(reqDokuAenderungen)
    reqStoerungenMissbrauch.append(reqAntiviren)
    reqStoerungenMissbrauch.append(reqAuthentifierung)
    reqStoerungenMissbrauch.append(reqVerschluesselung)
    
    reqEreignisseErkennen = Requirement(
        u"gefährliche Ereignisse erkennen",
        ikComment = u"innerhalb der Kurzdarstellung")
    reqItSicherheitskonzept.append(reqEreignisseErkennen)
    
    reqEreignisseErkennen.append(reqDokuVerantwortlichkeiten)
    reqEreignisseErkennen.append(reqDokuSysteme)
    reqEreignisseErkennen.append(reqMonitoring)
    reqEreignisseErkennen.append(reqPerformance)
    reqEreignisseErkennen.append(reqProtokollierungen)
    reqEreignisseErkennen.append(reqAuditierungen)
    
    reqBusinessContinuity = Requirement(
        u"Fortführung nach Schaden oder Störung",
        ikComment = u"innerhalb der Kurzdarstellung")
    reqItSicherheitskonzept.append(reqBusinessContinuity)
    
    reqBusinessContinuity.append(reqDokuVerantwortlichkeiten)
    reqBusinessContinuity.append(reqDokuExterne)
    reqBusinessContinuity.append(reqDokuRichtlinien)
    reqBusinessContinuity.append(reqDokuSysteme)
    reqBusinessContinuity.append(reqSystemkonfiguration)
    reqBusinessContinuity.append(reqDokuAenderungen)
    reqBusinessContinuity.append(reqBackup)
    
    # ###############################
    # ####### vorläufiges Ende
    # ###############################

def createUtils(root_folder, connection=None, dummy_db=None):
    madeAdmUtilCompliance = ensureUtility(root_folder, IAdmUtilCompliance,
                                          'AdmUtilCompliance', AdmUtilCompliance,
                                          name='AdmUtilCompliance',
                                          copy_to_zlog=False)

    if isinstance(madeAdmUtilCompliance, AdmUtilCompliance):
        logger.info(u"bootstrap: Ensure named AdmUtilCompliance")
        dcore = IWriteZopeDublinCore(madeAdmUtilCompliance)
        dcore.title = u"Compliance Utiltiy"
        dcore.created = datetime.utcnow()
        madeAdmUtilCompliance.ikName = dcore.title
        madeAdmUtilCompliance.__post_init__()
        sitem = root_folder.getSiteManager()
        utils = [util for util in sitem.registeredUtilities()
                 if util.provided.isOrExtends(IAdmUtilSupervisor)]
        instAdmUtilSupervisor = utils[0].component
        instAdmUtilSupervisor.appendEventHistory(\
            u" bootstrap: made Compliance Utiltiy")
    else:
        if False:
            sitem = root_folder.getSiteManager()
            utils = [ util for util in sitem.registeredUtilities()
                      if util.provided.isOrExtends(IAdmUtilCompliance)]
            instAdmUtilCompliance = utils[0].component
            logger.info(u"replacing all Requirements")
            fillUtilitiyWithReqs(instAdmUtilCompliance)
    transaction.get().commit()
    if connection is not None:
        connection.close()

def bootStrapSubscriberDatabase(event):
    """initialisation of eventcrossbar utility on first database startup
    """
    if appsetup.getConfigContext().hasFeature('devmode'):
        logger.info(u"starting bootStrapSubscriberDatabase (org.ict_ok...)")
    dummy_db, connection, dummy_root, root_folder = \
            getInformationFromEvent(event)
    createUtils(root_folder, connection, dummy_db)
    from org.ict_ok.admin_utils.compliance.lxml_demo import lxmlDemo
    lxmlDemo()
