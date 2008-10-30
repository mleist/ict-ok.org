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

__version__ = "$Id$"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory
from zope.app.rotterdam.xmlobject import traverse, xmlEscape, getParents, \
     translate, xmlEscapeWithCData, IReadContainer, titleTemplate, \
     loadingMsg, ReadContainerXmlObjectView, setNoCacheHeaders, \
     getParentsFromContextToObject
from zope.component import getAdapter
from zope.component.interfaces import ComponentLookupError
from zope.dublincore.interfaces import IGeneralDublinCore
from zope.app import zapi
from zope.security import checkPermission
from zope.app.catalog.interfaces import ICatalog
from zope.security.interfaces import ForbiddenAttribute

# ict_ok.org imports
from org.ict_ok.components.supernode.interfaces import IState
from org.ict_ok.components.supernode.interfaces import IContentList

_ = MessageFactory('org.ict_ok')

class IkReadContainerXmlObjectView(ReadContainerXmlObjectView):

    def getStateIconUrl(self, item):
        try:
            result = item.getShortname()
        except ForbiddenAttribute:
            result = "Error in IkReadContainerXmlObjectView"
        icon = None
        try:
            stateAdapter = getAdapter(item, IState)
            if stateAdapter:
                icon_name = u"state_%s" % (stateAdapter.getStateOverview())
                #print "icon_name: ", icon_name
                stateNum = stateAdapter.getStateOverview(-1)
                return "%s%d" % (item.getShortname(), stateNum)
                #iconName = stateAdapter.getIconName()
                #if iconName:
                    #return u"/@@/pics/" + iconName
                #icon = zapi.queryMultiAdapter((item, self.request),
                                              #name=icon_name)
        except ComponentLookupError, err:
            pass
        except AttributeError, err:
            pass
        if not icon:
            icon = zapi.queryMultiAdapter((item, self.request),
                                          name='zmi_icon')
        if icon:
            result = icon.url()
        return result

    def getStateValue(self, item):
        result = ''
        try:
            stateAdapter = getAdapter(item, IState)
            if stateAdapter:
                result = str(stateAdapter.getStateValue())
        except ComponentLookupError, err:
            pass
        return result

    def getStateDict(self, item):
        result = None
        try:
            stateAdapter = getAdapter(item, IState)
            if stateAdapter:
                result = stateAdapter.getStateDict()
        except ComponentLookupError, err:
            pass
        return result

    def getStateOverview(self, item):
        result = None
        try:
            stateAdapter = getAdapter(item, IState)
            if stateAdapter:
                result = stateAdapter.getStateOverview()
        except ComponentLookupError, err:
            pass
        except AttributeError, err:
            pass
        return result

    def children_utility(self, container):
        """Return an XML document that contains the children of an object."""
        result = []
        try:
            keys = [obj.objectID for \
                    obj in IContentList(container).getContentList()]
        except TypeError:
            keys = list(container.keys())

        # include the site manager
        keys.append(u'++etc++site')

        for name in keys:

            # Only include items we can traverse to
            item = traverse(container, name, None)
            if item is None:
                my_catalog = zapi.getUtility(ICatalog)
                res = my_catalog.searchResults(oid_index=name)
                if len(res) > 0:
                    item = iter(res).next()
                if item is None:
                    continue
            if name == u'++etc++site' and \
               not checkPermission(\
                   'org.ict_ok.ikadmin_utils.usermanagement.Edit', item):
                continue
            dcAdapter = IGeneralDublinCore(item)
            xml_title = name
            if dcAdapter:
                if dcAdapter.title:
                    xml_title = dcAdapter.title
            iconUrl = self.getIconUrl(item)
            stateIconUrl = self.getStateIconUrl(item)
            #stateValue = self.getStateValue(item)
            stateOverview = self.getStateOverview(item)
            try:
                item_len = len(IContentList(item).getContentList())
            except TypeError:
                item_len = self.getLengthOf(item)
            item_ppath = zapi.canonicalPath(zapi.getParent(item)) + u'/'
            item_ppath = item_ppath.replace('//', '/')
            if item_len > 0:
                if stateOverview:
                    result.append(xmlEscape(
                        u'<collection title=%s name=%s iklen=%s icon_url=%s rem="1.1.1" ' +
                        u'state_url=%s path=%s expable="" state_val=%s/>',
                        xml_title, name, item_len, iconUrl, stateIconUrl,
                        item_ppath, stateOverview))
                else:
                    result.append(xmlEscape(
                        u'<collection title=%s name=%s iklen=%s icon_url=%s rem="1.1.2" ' +
                        u'state_url=%s expable="" path=%s/>',
                        xml_title, name, item_len, iconUrl, stateIconUrl,
                        item_ppath))
            else:
                if stateOverview:
                    result.append(xmlEscape(
                        u'<collection title=%s name=%s iklen=%s icon_url=%s rem="1.2.1" ' +
                        u'state_url=%s path=%s state_val=%s/>',
                        xml_title, name, item_len, iconUrl, stateIconUrl,
                        item_ppath, stateOverview))
                else:
                    result.append(xmlEscape(
                        u'<collection title=%s name=%s iklen=%s icon_url=%s rem="1.2.2" ' +
                        u'state_url=%s path=%s/>',
                        xml_title, name, item_len, iconUrl, stateIconUrl,
                        item_ppath))

        return u' '.join(result)


    def children(self):
        """ """
        container = self.context
        self.request.response.setHeader('content-type',
                                        'text/xml;charset=utf-8')
        setNoCacheHeaders(self.request.response)
        res = (u'<?xml version="1.0" ?><children> %s </children>'
                % self.children_utility(container))
        return res

    def singleBranchTree(self, root=''):
        """Return an XML document with the siblings and parents of an object.

        There is only one branch expanded, in other words, the tree is
        filled with the object, its siblings and its parents with
        their respective siblings.

        """
        result = ''
        oldItem = self.context
        try:
            oldItemOid = self.context.getObjectId()
        except:
            oldItemOid = "+++"

        vh = self.request.getVirtualHostRoot()
        if vh:
            #print "vh: ", vh
            vhrootView = zapi.getMultiAdapter(
                    (vh, self.request), name='absolute_url')
            baseURL = vhrootView() + '/'
            try:
                rootName = '[' + vh.__name__ + ']'
            except:
                # we got the containment root itself as the virtual host
                # and there is no name.
                rootName = _('[top]')
            parents = getParentsFromContextToObject(self.context, vh)
        else:
            rootName = _('[top]')
            baseURL = self.request.getApplicationURL() + '/'
            parents = getParents(self.context)
        rootName = translate(rootName, context=self.request,
                             default=rootName)
        for item in parents:
            # skip skin if present
            if item == oldItem:
                continue
            if item is None:
                continue
            subItems = []
            if IReadContainer.providedBy(item):
                keys = list(item.keys())
            else:
                keys = []
            # include the site manager
            #keys.append(u'++etc++site')
            for name in keys:
                # Only include items we can traverse to
                try:
                    subItem = traverse(item, name, None)
                except ValueError:
                    subItem = None
                if subItem is None:
                    continue
                #if name == u'++etc++site' and \
                   #not checkPermission(\
                       #'org.ict_ok.admin_utils.supervisor.DataDump',
                       #subItem):
                    #continue
                iconUrl = self.getIconUrl(subItem)
                try:
                    subitem_len = len(IContentList(self.context).getContentList())
                except TypeError:
                    try:
                        subitem_len = self.getLengthOf(subItem)
                    except TypeError:
                        subitem_len = 0
                    except AttributeError:
                        subitem_len = 0
                try:
                    dcAdapter = IGeneralDublinCore(subItem)
                except TypeError:
                    dcAdapter = None
                xml_title = name
                if dcAdapter:
                    if dcAdapter.title:
                        xml_title = dcAdapter.title
                stateIconUrl = self.getStateIconUrl(subItem)
                if zapi.getParent(subItem):
                    item_ppath = zapi.canonicalPath(zapi.getParent(subItem)) \
                               + u'/'
                    item_ppath = item_ppath.replace('//', '/')
                else:
                    item_ppath = "/"
                try:
                    subItemOid = subItem.getObjectId()
                except:
                    subItemOid = "---"
                stateOverview = self.getStateOverview(item)
                if subitem_len > 0:
                    # the test below seems to be broken
                    # with the ++etc++site case
                    if subItem == oldItem:
                        if oldItemOid == subItemOid: # focussed
                            subItems.append(xmlEscapeWithCData(
                                u'<collection isfocused="" title=%s name=%s '
                                u'iklen=%s rem="2.1.1.1" '
                                u'icon_url=%s isopen="" expable="" state_url=%s '
                                u'path=%s state_val=%s>%s</collection>', 
                                xml_title, name, subitem_len, iconUrl,
                                stateIconUrl, item_ppath, stateOverview,
                                result))
                        else:
                            subItems.append(xmlEscapeWithCData(
                                u'<collection title=%s name=%s iklen=%s rem="2.1.1.2" '
                                u'icon_url=%s isopen="" expable="" state_url=%s path=%s '
                                u'state_val=%s>%s</collection>', 
                                xml_title, name, subitem_len, iconUrl,
                                stateIconUrl, item_ppath, stateOverview,
                                result))
                    else:
                        subItems.append(xmlEscape(
                            u'<collection title=%s name=%s iklen=%s rem="2.1.2" '
                            u'icon_url=%s expable="" state_url=%s path=%s/>',
                            xml_title, name, subitem_len, iconUrl,
                            stateIconUrl, item_ppath))
                else:
                    if subItem == oldItem:
                        if oldItemOid == subItemOid: # focussed
                            subItems.append(xmlEscapeWithCData(
                                u'<collection isfocused="" title=%s '
                                u'name=%s iklen=%s rem="2.2.1.1" '
                                u'icon_url=%s state_url=%s path=%s '
                                u'state_val=%s>%s</collection>', 
                                xml_title, name, subitem_len, iconUrl,
                                stateIconUrl, item_ppath, stateOverview,
                                result))
                        else:
                            subItems.append(xmlEscapeWithCData(
                                u'<collection title=%s name=%s iklen=%s '
                                u'icon_url=%s state_url=%s path=%s rem="2.2.1.2" '
                                u'state_val=%s>%s</collection>', 
                                xml_title, name, subitem_len, iconUrl,
                                stateIconUrl, item_ppath, stateOverview,
                                result))
                    else:
                        subItems.append(xmlEscape(
                            u'<collection title=%s name=%s iklen=%s rem="2.2.2" '
                            u'icon_url=%s state_url=%s path=%s/>',
                            xml_title, name, subitem_len, iconUrl,
                            stateIconUrl, item_ppath))

            result = u' '.join(subItems)
            oldItem = item

        # do not forget root folder
        iconUrl = self.getIconUrl(oldItem)
        xml_title = "ICT_Ok"
        rootName =  "."
        
        if len(result) > 0: # collection has content
            result = xmlEscapeWithCData(
                      u'<collection title=%s name=%s baseURL=%s iklen=%s rem="3.1" '
                      u'icon_url=%s path=%s isopen="" isroot="">%s</collection>',
                      xml_title, rootName, baseURL, len(oldItem), iconUrl,
                      "/", result)
        else:
            result = xmlEscapeWithCData(
                      u'<collection title=%s name=%s baseURL=%s iklen=%s rem="3.2" '
                      u'icon_url=%s path=%s expable="" '
                      u'isroot="">%s</collection>',
                      xml_title, rootName, baseURL, len(oldItem), iconUrl,
                      "/", result)

        self.request.response.setHeader('Content-Type', 'text/xml')
        setNoCacheHeaders(self.request.response)
        title = translate(titleTemplate,
                          context=self.request, default=titleTemplate)
        loading = translate(loadingMsg,
                          context=self.request, default=loadingMsg)
        return xmlEscapeWithCData(
                u'<?xml version="1.0" encoding="ISO-8859-1"?>'
                u'<children title_tpl=%s title=%s '
                u'loading_msg=%s>%s</children>',
                title, title, loading, result)

