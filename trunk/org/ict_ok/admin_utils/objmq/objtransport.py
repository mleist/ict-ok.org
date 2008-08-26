# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0611
#
"""implementation of a "Object-Message-Queue-Utility" 
"""

__version__ = "$Id$"

# python imports
import logging
from re import  match
from base64 import encodestring
import httplib
import xmlrpclib

# zope imports
from zope.interface import implements
from zope.component import getGlobalSiteManager

# ict_ok.org imports
from org.ict_ok.admin_utils.objmq.interfaces import IAdmUtilObjTransport

logger = logging.getLogger("AdmUtilObjMQ")


class BasicAuthTransport(xmlrpclib.Transport):
    """authtentication class for xml-rpc call
    """
    def __init__(self, username=None, password=None, verbose=0):
        self.username = username
        self.password = password
        self.verbose = verbose

    def request(self, host, handler, request_body, verbose=0):
        """doing while xml-rpc call"""
        # issue XML-RPC request
        self.verbose = verbose
        h = httplib.HTTP(host)
        h.putrequest("POST", handler)
        # required by HTTP/1.1
        h.putheader("Host", host)
        # required by XML-RPC
        h.putheader("User-Agent", self.user_agent)
        h.putheader("Content-Type", "text/xml")
        h.putheader("Content-Length", str(len(request_body)))
        # basic auth
        if self.username is not None and self.password is not None:
            h.putheader("AUTHORIZATION", "Basic %s" %
                        encodestring("%s:%s" % (self.username, self.password)
                                     ).replace("\012", ""))
        h.endheaders()
        if request_body:
            h.send(request_body)
        errcode, errmsg, headers = h.getreply()
        if errcode != 200:
            raise xmlrpclib.ProtocolError(host + handler,
                                          errcode, errmsg, headers)
        return self.parse_response(h.getfile())



class AdmUtilObjTransport(object):
    """A pseudo-mailer that delivers objects by xmlrpc."""

    implements(IAdmUtilObjTransport)

    def __init__(self, hostname='localhost'):
        self.hostname = hostname

    def send(self, fromaddr, toaddrs, message):
        """
        send object data as faked e-mail
        """
        gsm = getGlobalSiteManager()
        #logger.info(u"AdmUtilObjTransport.msg: %s" % (message))
        for toaddr in toaddrs:
            (t_prot, t_uid, t_ip, t_port, t_path) = \
             match(r"(\w*)://(\w*)@([\w.]*):(\d*)(.*)", toaddr).groups()
            url = u"%s://%s:%s%s" % (t_prot, t_ip, t_port, t_path)
            host = xmlrpclib.Server(
                url, transport = BasicAuthTransport('admin', 'admin'))
            retVal = host.objmq_subscribe(message)
            if not retVal:
                logger.warning(u"AdmUtilObjTransport return 'False' (oid not ok?)")
      