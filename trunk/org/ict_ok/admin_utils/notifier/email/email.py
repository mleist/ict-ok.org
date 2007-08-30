# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
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

# phython imports
import logging
from pytz import timezone

# zope imports
from zope.interface import implements
from zope.component import getUtility
from zope.sendmail.interfaces import IMailDelivery

# ict_ok.org imports
from org.ict_ok.admin_utils.notifier.notifier import \
     Notifier
from org.ict_ok.admin_utils.notifier.email.interfaces import \
     INotifierEmail

logger = logging.getLogger("NotifierEmail")
berlinTZ = timezone('Europe/Berlin')


class NotifierEmail(Notifier):
    """Implementation of email notifier wrapper
    """

    implements(INotifierEmail)

    def __init__(self):
        super(NotifierEmail, self).__init__()
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
        from zope.app.security.interfaces import IAuthentication
        pau_utility = getUtility(IAuthentication)
        from zope.app.principalannotation.interfaces import IPrincipalAnnotationUtility
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
