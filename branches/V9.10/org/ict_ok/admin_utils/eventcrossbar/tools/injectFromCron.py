#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007 Ingenieurbuero IKOM,
#               Markus Leist <leist at ikom-online.de>
# See also LICENSE.txt or http://www.ict_ok.org/LICENSE
# This file is part of ict_ok.org.
#
# $Id$
#
"""implementation of a "cron signal injector" in ICT_Ok

$ crontab -l
*   *   *   *   * /home/markus/Projekte/ICT_Ok-hp/injectFromCron.py minute
0   *   *   *   * /home/markus/Projekte/ICT_Ok-hp/injectFromCron.py hour
0   0   *   *   * /home/markus/Projekte/ICT_Ok-hp/injectFromCron.py day
0   0   1   *   * /home/markus/Projekte/ICT_Ok-hp/injectFromCron.py month
0   0   1   1   * /home/markus/Projekte/ICT_Ok-hp/injectFromCron.py year
12  2   *   *   * /home/markus/Projekte/ICT_Ok-hp/injectFromCron.py db_pack

"""

__version__ = "$Id$"

import sys
#sys.path.append("/opt/ikom/Zope3/src")
sys.path.append("/home/markus/Projekte/ICT_Ok-hp/zope_b33/src/")

import httplib
import xmlrpclib
from datetime import datetime
from pytz import timezone
from base64 import encodestring

utcTZ = timezone('UTC')
berlinTZ = timezone('Europe/Berlin')

class BasicAuthTransport(xmlrpclib.Transport):
    def __init__(self, arg_username=None,
                 arg_password=None, arg_verbose=0):
        self.username = arg_username
        self.password = arg_password
        self.verbose = arg_verbose

    def request(self, arg_host, handler,
                request_body, verbose=0):
        # issue XML-RPC request

        self.verbose = verbose

        h = httplib.HTTP(arg_host)
        h.putrequest("POST", handler)

        # required by HTTP/1.1
        h.putheader("Host", arg_host)

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
            raise xmlrpclib.ProtocolError(arg_host + handler,
                                          errcode, errmsg, headers)

        return self.parse_response(h.getfile())


if __name__ == '__main__':
    args = sys.argv
    print "aa: %s" % args
    modeString = ""
    if len(args) > 1:
        modeString = args[1]
    print "modeString: %s" % modeString
    url = 'http://localhost:8080/++etc++site/default/AdmUtilCron'
    username = 'admin'
    password = 'admin'
    host = xmlrpclib.Server(
        url, transport = BasicAuthTransport(username, password)
        )

    fd = open("/home/markus/tmp/xmlrpc_errors.log", "a+")
    dateNow = datetime.now(utcTZ).astimezone(berlinTZ)
    #dateNow = xmlrpclib.DateTime()
    errVal = host.triggerCronEvent(str(dateNow), modeString)
    #errVal = host.triggerCronEvent(dateNow)
    if errVal:
        print >> fd, "Error: %s" % errVal
    fd.close()
