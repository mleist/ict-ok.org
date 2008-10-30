# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611
#
"""Configuration adapter for email-config files
"""

__version__ = "$Id$"

# python imports
import tempfile
import os
from datetime import datetime
import logging
from pytz import timezone
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Utils, Encoders
import mimetypes
#import email

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.component import getUtility
from zope.sendmail.interfaces import IMailDelivery
from zope.app.security.interfaces import IAuthentication
from zope.app.principalannotation.interfaces import IPrincipalAnnotationUtility

# z3c imports
from z3c.rml import pagetemplate

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import ISuperclass
from org.ict_ok.admin_utils.notifier.notifier import \
     Notifier
from org.ict_ok.admin_utils.notifier.imail.interfaces import \
     INotifierEmail, IEventIfNotifierEmail
from org.ict_ok.admin_utils.usermanagement.usermanagement import \
     getNotifierDict4User
from org.ict_ok.admin_utils.notifier.notifier import notifyLabel
from org.ict_ok.version import getIkVersion

logger = logging.getLogger("NotifierEmail")
berlinTZ = timezone('Europe/Berlin')


class NotifierEmail(Notifier):
    """Implementation of email notifier wrapper
    """

    implements(INotifierEmail, IEventIfNotifierEmail)

    hostname = FieldProperty(INotifierEmail['hostname'])
    portServer = FieldProperty(INotifierEmail['portServer'])
    from_addr = FieldProperty(INotifierEmail['from_addr'])
    # Event interface
    eventInpObjs_notify = FieldProperty(\
        IEventIfNotifierEmail['eventInpObjs_notify'])
    

    def __init__(self):
        Notifier.__init__(self)
        self.ikRevision = __version__
        
    def sendNotify(self, notifyEvent=None, notifyObj=None):
        """
        sending the real notification to the user
        """
        print "NotifierEmail::sendNotify(%s, %s)" % (notifyEvent, notifyObj)
        pau_utility = getUtility(IAuthentication)
        en_utility = getUtility(IMailDelivery, 'ikEmailNotifierQueue')
        toList = []
        toShortList = []
        if pau_utility and pau_utility.has_key('principals'):
            principals = pau_utility['principals']
            for (name, obj) in principals.items():
                #print "v" * 60
                #print "principal_name: %s" % name
                principal_id = principals.prefix + name
                #print "principal_id: %s" % principal_id
                notifDict = getNotifierDict4User(principal_id)
                #returns:
                #{'timezone': None,
                 #'email': None,
                 #'notifierChannels': None,
                 #'notifierLevel': None,
                 #'shortEmail': None,
                 #'shortNotifierChannels': None,
                 #'shortNotifierLevel': None,
                 #'shortEmail': None,
                 #}
                #print "notifDict: %s" % notifDict
                #print "notifyEvent.channels", notifyEvent.channels
                #print "notifyEvent.level", notifyEvent.level
                # long email
                #print "email: %s" % notifDict['email']
                if notifDict['email'] is not None \
                   and len(notifDict['email']) > 0 \
                   and notifyEvent is not None \
                   and notifyEvent.channels is not None \
                   and notifyEvent.level is not None \
                   and notifDict['notifierChannels'] is not None \
                   and (notifyEvent.level >= notifDict['notifierLevel']) \
                   and (len(set(notifDict['notifierChannels'])\
                            .intersection(notifyEvent.channels)) > 0):
                    toList.append(notifDict['email'])
                # short email
                #print "shortEmail: %s" % notifDict['shortEmail']
                if notifDict['shortEmail'] is not None \
                   and len(notifDict['shortEmail']) > 0:
                    toShortList.append(notifDict['shortEmail'])
                if notifDict['shortEmail'] is not None \
                   and len(notifDict['shortEmail']) > 0 \
                   and notifyEvent is not None \
                   and notifyEvent.channels is not None \
                   and notifyEvent.level is not None \
                   and notifDict['shortNotifierChannels'] is not None \
                   and (notifyEvent.level >= notifDict['shortNotifierLevel']) \
                   and (len(set(notifDict['shortNotifierChannels'])\
                            .intersection(notifyEvent.channels)) > 0):
                    toShortList.append(notifDict['shortEmail'])
                #print "^" * 60
                #if en_utility:
                    #en_utility.send("aaa", [email], "ccc_msg")
                #email = pr_anno_utility.getAnnotationsById(principal_id).data['org.ict_ok.admin_utils.usermanagement']['email']
                #print "email: %s" % email
                #dddd2 = AdmUtilUserManagement(obj)
                #print "dddd2: %s" % dddd2
                #print "dddd2.email: %s" % dddd2.email
        print "toList: ", toList
        print "toShortList: ", toShortList
        if en_utility:
            if len(toList) > 0:
                filename = datetime.now().strftime('ictrpt_%Y%m%d%H%M%S.pdf')
                f_handle, f_name = tempfile.mkstemp(filename)
                #authorStr = self.request.principal.title
                authorStr = notifyLabel
                #from zope.i18n.locales import LocaleDates
                #dates = LocaleDates()
                #my_formatter = dates.getFormatter('dateTime', 'full')
                #my_formatter = self.request.locale.dates.getFormatter(
                    #'dateTime', 'medium')
                #userTZ = getUserTimezone()
                #userTZ = getUserTimezone()
                #longTimeString = my_formatter.format(\
                    #userTZ.fromutc(datetime.utcnow()))
                #longTimeString = my_formatter.format(\
                    #datetime.utcnow())
                #versionStr = "%s [%s]" % (longTimeString, getIkVersion())
                versionStr = "[%s]" % (getIkVersion())
                if ISuperclass.providedBy(notifyEvent.object):
                    notifyEvent.object.generatePdf(\
                        f_name, authorStr, versionStr)
                else:
                    self.generatePdf(f_name, authorStr, versionStr)
                for rcpt in set(toList):
                    msg = MIMEMultipart()
                    msg['To'] = rcpt
                    msg['From'] = self.from_addr
                    msg['Subject'] = '[%s] %s' % (str(notifyLabel),
                                                  notifyEvent.subject)
                    msg['Date'] = Utils.formatdate(localtime = 1)
                    msg['Message-ID'] = Utils.make_msgid()
                    if type(notifyEvent.object) == type("") or \
                       type(notifyEvent.object) == type(""):
                        outText = notifyEvent.object
                    else:
                        if ISuperclass.providedBy(notifyEvent.object):
                            outText = u"System: '%s': state changed" % \
                                    (notifyEvent.object.ikName)
                        else:
                            outText = u"unknown object type in ict-ok.org instance"
                    body = MIMEText(outText, _subtype='plain', _charset='latin-1')
                    msg.attach(body)
                    datafile = open(f_name, "r")
                    msg.attach(self.attachment(filename, datafile))
                    datafile.close()
                    en_utility.send(self.from_addr, [rcpt], msg.as_string())
                #print "self.from_addr: ", self.from_addr
                #print "toList: ", toList
                #print "msg.as_string(): ", msg.as_string()
                os.remove(f_name)
            for rcpt in set(toShortList):
                msg = MIMEMultipart()
                msg['To'] = rcpt
                msg['From'] = self.from_addr
                msg['Subject'] = '[%s] %s' % (str(notifyLabel),
                                              notifyEvent.subject)
                msg['Date'] = Utils.formatdate(localtime = 1)
                msg['Message-ID'] = Utils.make_msgid()
                if type(notifyEvent.object) == type("") or \
                   type(notifyEvent.object) == type(""):
                    outText = notifyEvent.object
                else:
                    if ISuperclass.providedBy(notifyEvent.object):
                        outText = u"System: '%s': state changed" % \
                                (notifyEvent.object.ikName)
                    else:
                        outText = u"unknown object type in ict-ok.org instance"
                body = MIMEText(outText, _subtype='plain', _charset='latin-1')
                msg.attach(body)
                en_utility.send(self.from_addr, [rcpt], msg.as_string())

    def send_test(self, messageText):
        """
        will send a test message by the notifier
        """
        print "NotifierEmail.send_test(%s)" % messageText
        from org.ict_ok.admin_utils.notifier.notifier import NotifyUserEvent, infoLevel
        channels = ['ch_misc']
        subject = u"test message"
        testEvent = NotifyUserEvent(subject, channels, infoLevel, "test")
        self.sendNotify(testEvent)
        #pau_utility = getUtility(IAuthentication)
        #en_utility = getUtility(IMailDelivery, 'ikEmailNotifierQueue')
        #if pau_utility and pau_utility.has_key('principals'):
            #principals = pau_utility['principals']
            #toList = []
            #toShortList = []
            #for name in principals.keys():
                #print "v" * 60
                #print "principal_name: %s" % name
                #principal_id = principals.prefix + name
                #print "principal_id: %s" % principal_id
                #notifDict = getNotifierDict4User(principal_id)
                ##returns:
                ##{'email': None,
                 ##'notifierChannels': None,
                 ##'notifierLevel': None,
                 ##'shortEmail': None,
                 ##'shortNotifierChannels': None,
                 ##'shortNotifierLevel': None,
                 ##'shortEmail': None,
                 ##}
                #print "notifDict: %s" % notifDict
                #print "email: %s" % notifDict['email']
                #if notifDict['email'] is not None \
                   #and len(notifDict['email']) > 0:
                    #toList.append(notifDict['email'])
                #print "shortEmail: %s" % notifDict['shortEmail']
                #if notifDict['shortEmail'] is not None \
                   #and len(notifDict['shortEmail']) > 0:
                    #toShortList.append(notifDict['shortEmail'])
                #print "^" * 60
            #print "en_utility: ", en_utility
            #print "toList: ", toList
            #print "toShortList: ", toShortList
            #if en_utility is not None:
                ##en_utility.send(en_utility.from_addr, toList, messageText)
                #print "#" * 60
                ##print self.create_test_message(toList)
                ##print "-" * 60

    #def create_test_message(self, toList):
        #ptFileName = tempfile.mktemp('.pt')
        #pdfFileName = tempfile.mktemp('.pdf')
        #open(ptFileName, 'w').write('''\
        #<?xml version="1.0" encoding="UTF-8" ?>
        #<!DOCTYPE document SYSTEM "rml.dtd">
        #<document filename="template.pdf"
            #xmlns:tal="http://xml.zope.org/namespaces/tal">
        
          #<template pageSize="(21cm, 29cm)">
            #<pageTemplate id="main">
              #<frame id="main" x1="2cm" y1="2cm"
                     #width="17cm" height="25cm" />
            #</pageTemplate>
          #</template>
        
          #<story>
            #<para
                #tal:repeat="name context/names"
                #tal:content="name" />
          #</story>
        
        #</document>
        #''')

        #rmlPageTemplate = pagetemplate.RMLPageTemplateFile(ptFileName)
        #open(pdfFileName, 'w').write(\
            #rmlPageTemplate(names=toList))
            ##rmlPageTemplate(names=(u'Roy', u'Daniel', u'Julian', u'Stephan')))
        #pdfFileName.seek(0)
        #msg = MIMEMultipart()
        #msg['To'] = 'leist@ikom-online.de'
        #msg['Subject'] = '[IKOMtrol] %s %s' % ('Objekt', 'Status')
        #msg['Date'] = Utils.formatdate(localtime = 1)
        #msg['Message-ID'] = Utils.make_msgid()
        #body = MIMEText( "test text", _subtype='plain', _charset='latin-1')
        #msg.attach(body)
        #msg.attach(self.attachment( "data.pdf", pdfFileName))
        #return msg.as_string()
        
    def attachment( self, filename, fd):
        mimetype, mimeencoding = mimetypes.guess_type(filename)
        if mimeencoding or (mimetype is None):
            mimetype = 'application/octet-stream'
        maintype, subtype = mimetype.split('/')  
        if maintype == 'text':
            retval = MIMEText(fd.read(), _subtype=subtype, _charset='latin-1')
        else:
            retval = MIMEBase(maintype, subtype)
            retval.set_payload(fd.read())
            Encoders.encode_base64(retval)
        retval.add_header('Content-Disposition', 'attachment',
                filename = filename)
        fd.close()
        return retval

    #def out( self, outMeta, outList, outText):
        #msg = MIMEMultipart()
        #msg['To'] = 'leist@ikom-online.de'
        ##msg['From'] = 'Test Sender <sender@example.com>'
        #if outMeta.has_key('Location'):
            #msg['Subject'] = '[IKOMtrol][%s] %s %s' % (outMeta['Location'], outMeta['Objekt'], outMeta['Status'])
        #else:
            #msg['Subject'] = '[IKOMtrol] %s %s' % (outMeta['Objekt'], outMeta['Status'])
        #msg['Date'] = Utils.formatdate(localtime = 1)
        #msg['Message-ID'] = Utils.make_msgid()
        ##body = MIMEText(message, _subtype='plain')
        #body = MIMEText( outText, _subtype='plain', _charset='latin-1')
        #msg.attach(body)

        #ikreportmail = IkReportMail( "toooooo", outMeta)
        #tmpFile = os.tmpfile()
        #ikreportmail.gen( tmpFile, outList)
        #tmpFile.seek(0)
        #msg.attach( self.attachment( "IKOMtrol.pdf", tmpFile))
        #return msg.as_string()    
