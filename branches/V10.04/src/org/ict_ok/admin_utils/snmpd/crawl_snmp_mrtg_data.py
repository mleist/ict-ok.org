# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=
#

import urllib2
import re
import pickle
from BeautifulSoup import BeautifulSoup
from gzip import GzipFile
import time

def begin_marker(textvar):
    return textvar == "<--- BEGIN COPY AND PASTE --->"

def end_marker(textvar):
    return textvar == "<--- FINISH COPY AND PASTE --->"

def parse_vendors(soup, outp_dict):
    vendor_tds = soup.findAll("td", { "class" : "focustext" })
    for vendor_td in vendor_tds:
        # for testing don't crawl all
        #for vendor_a in vendor_td.findAll("a")[:1]:
        for vendor_a in vendor_td.findAll("a"):
            if len(vendor_a.contents) > 0:
                print "vendor: '%s'" % vendor_a.contents[0]
                vendor_dict = outp_dict[unicode(vendor_a.contents[0]).replace(u'\xa0', ' ')] = {}
                products_href = u"http://www.plixer.com/support/" + \
                              vendor_a['href']
                products_page = urllib2.urlopen(products_href)
                soup = BeautifulSoup(products_page,
                                     convertEntities=BeautifulSoup.HTML_ENTITIES)
                parse_products(soup, vendor_dict)

def parse_products(soup, outp_dict):
    products_tds = soup.findAll("td", { "class" : "focustext" })
    for products_td in products_tds:
        for products_a in products_td.findAll("a"):
            print "\tproduct: '%s'" % products_a.contents[0]
            products_dict = outp_dict[unicode(products_a.contents[0]).replace(u'\xa0', ' ')] = {}
            product_href = u"http://www.plixer.com/support/" + \
                         products_a['href']
            product_page = urllib2.urlopen(product_href)
            soup = BeautifulSoup(product_page,
                                 convertEntities=BeautifulSoup.HTML_ENTITIES)
            parse_product(soup, products_dict)

def parse_product(soup, outp_dict):
    product_tds = soup.findAll("td", { "class" : "focustext" })
    for product_td in product_tds:
        for product_a in product_td.findAll("a"):
            if product_a.has_key('onclick'):
                templ_dict = outp_dict[unicode(product_a.contents[0]).replace(u'\xa0', ' ')] = {}
                templ_href = "http://www.plixer.com/support/" +\
                           re.match("^window.open\('([^']*)",
                                    product_a['onclick']).groups()[0]
                templ_page = urllib2.urlopen(templ_href)
                soup = BeautifulSoup(templ_page,
                                     convertEntities = \
                                     BeautifulSoup.HTML_ENTITIES)
                parse_template(soup, templ_dict)

def parse_template(soup, outp_dict):
    start_elem = soup.find(text=lambda text:begin_marker(text))
    end_elem = soup.find(text=lambda text:end_marker(text))
    my_templ = start_elem.parent.parent
    start_elem.parent.extract()
    end_elem.parent.extract()
    rawStringList = my_templ.contents
    rawString = u"".join(rawStringList).strip()
    templStringList = rawString.splitlines()
    oidParser = 'Target\[\$CFGNAME\]\:\ ([^\&]*)\&' + \
              '([^\&:]*)\:\$COMMUNITY\@\$IPADDRESS'
    for templString in templStringList:
        if "Target[" in templString:
            oidMatch = re.match(oidParser, templString)
            if oidMatch:
                outp_dict['oid1'] = oidMatch.groups()[0]
                outp_dict['oid2'] = oidMatch.groups()[1]
        else:
            miscParser = '^(.*)\[\$CFGNAME\]\:\ (.*)$'
            miscMatch = re.match(miscParser, templString)
            if miscMatch:
                outp_dict[unicode(miscMatch.groups()[0]).replace(u'\xa0', ' ')] = miscMatch.groups()[1]


if __name__ == "__main__":
    # open files
    page = urllib2.urlopen("http://www.plixer.com/support/mrtg_repository.php")
    dataFile = GzipFile("snmp_mrtg_data.gz", "wb")
    
    dataFile.write("## mrtg data file for ict_ok.org\n")
    dataFile.write("%f\n" % (time.mktime(time.gmtime())))
    all_templ_data = {}
    
    # parse input data and form out dict
    soup_p = BeautifulSoup(page,
                           convertEntities=BeautifulSoup.HTML_ENTITIES)
    parse_vendors(soup_p, all_templ_data)
    
    # write in a gzipped pickle
    pickle.dump(all_templ_data, dataFile, 0)
    dataFile.close()
