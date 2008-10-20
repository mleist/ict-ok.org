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
import logging
from pytz import timezone
from email.MIMEText import MIMEText
#from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Utils, Encoders
import mimetypes
import email

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
from org.ict_ok.admin_utils.notifier.notifier import \
     Notifier
from org.ict_ok.admin_utils.notifier.imail.interfaces import \
     INotifierEmail, IEventIfNotifierEmail

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
        en_utility = getUtility(IMailDelivery, 'ikEmailNotifierQueue')
        print "en_utility: %s" % en_utility
        #if en_utility:
            #en_utility.send("aaa", "bbb", "ccc")
        pau_utility = getUtility(IAuthentication)
        pr_anno_utility = getUtility(IPrincipalAnnotationUtility)
        if pau_utility and pau_utility.has_key('principals'):
            principals = pau_utility['principals']
            for (name, obj) in principals.items():
                #print "principal_name: %s" % name
                principal_id = principals.prefix + name
                #print "principal_id: %s" % principal_id
                principal_annos = pr_anno_utility.getAnnotationsById(principal_id)
                if principal_annos:
                    if principal_annos.data.has_key('org.ict_ok.admin_utils.usermanagement'):
                        email = principal_annos.data['org.ict_ok.admin_utils.usermanagement']['email']
                        print "email: %s" % email
                        if en_utility:
                            en_utility.send("aaa", [email], "ccc_msg")
                #email = pr_anno_utility.getAnnotationsById(principal_id).data['org.ict_ok.admin_utils.usermanagement']['email']
                #print "email: %s" % email
                #dddd2 = AdmUtilUserManagement(obj)
                #print "dddd2: %s" % dddd2
                #print "dddd2.email: %s" % dddd2.email

    def send_test(self, messageText):
        """
        will send a test message by the notifier
        """
        print "NotifierEmail.send_test(%s)" % messageText
        pau_utility = getUtility(IAuthentication)
        pr_anno_utility = getUtility(IPrincipalAnnotationUtility)
        en_utility = getUtility(IMailDelivery, 'ikEmailNotifierQueue')
        if pau_utility and pau_utility.has_key('principals'):
            principals = pau_utility['principals']
            toList = []
            toShortList = []
            for name in principals.keys():
                print "principal_name: %s" % name
                principal_id = principals.prefix + name
                print "principal_id: %s" % principal_id
                principal_annos = pr_anno_utility.getAnnotationsById(principal_id)
                if principal_annos:
                    if principal_annos.data.has_key('org.ict_ok.admin_utils.usermanagement'):
                        email = principal_annos.data['org.ict_ok.admin_utils.usermanagement']['email']
                        print "email: %s" % email
                        if email is not None and len(email) > 0:
                            toList.append(email)
                        if hasattr(principal_annos.data[\
                            'org.ict_ok.admin_utils.usermanagement'],
                                   'shortEmail'):
                            shortEmail = principal_annos.data[\
                                'org.ict_ok.admin_utils.usermanagement']\
                                       ['shortEmail']
                        else:
                            shortEmail = None
                        print "shortEmail: %s" % shortEmail
                        if shortEmail is not None and len(shortEmail) > 0:
                            toShortList.append(shortEmail)
            print "en_utility: ", en_utility
            print "toList: ", toList
            print "toShortList: ", toShortList
            if en_utility is not None:
                #en_utility.send(en_utility.from_addr, toList, messageText)
                print "-" * 60
                #print self.create_test_message(toList)
                #print "-" * 60

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
