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
from urlparse import urlparse

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
from org.ict_ok.components.superclass.interfaces import INavigation

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
            if stateAdapter and \
               hasattr(stateAdapter, 'getStateValue'):
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
#            item_ppath = zapi.canonicalPath(zapi.getParent(item)) + u'/'
            url = urlparse(zapi.absoluteURL(zapi.getParent(item),
                                            self.request))
            item_ppath = url.path + u'/'
            item_ppath = item_ppath.replace('//', '/')
            if item_len > 0:
                if stateOverview:
                    result.append(xmlEscape(
                        u'<collection title=%s name=%s iklen=%s icon_url=%s rem="1.1.1" ' +
                        u'state_url=%s path=%s navparam="children1.xml" expable="" state_val=%s/>',
                        xml_title, name, item_len, iconUrl, stateIconUrl,
                        item_ppath, stateOverview))
                else:
                    result.append(xmlEscape(
                        u'<collection title=%s name=%s iklen=%s icon_url=%s rem="1.1.2" ' +
                        u'state_url=%s navparam="children2.xml" expable="" path=%s/>',
                        xml_title, name, item_len, iconUrl, stateIconUrl,
                        item_ppath))
            else:
                if stateOverview:
                    result.append(xmlEscape(
                        u'<collection title=%s name=%s iklen=%s icon_url=%s rem="1.2.1" ' +
                        u'state_url=%s navparam="children3.xml" path=%s state_val=%s/>',
                        xml_title, name, item_len, iconUrl, stateIconUrl,
                        item_ppath, stateOverview))
                else:
                    result.append(xmlEscape(
                        u'<collection title=%s name=%s iklen=%s icon_url=%s rem="1.2.2" ' +
                        u'state_url=%s navparam="children4.xml" path=%s/>',
                        xml_title, name, item_len, iconUrl, stateIconUrl,
                        item_ppath))

        return u' '.join(result)


    def getViewList(self, container):
        """Return an XML document that contains the children of an object."""
        subItems = []
        try:
            itemNav = INavigation(self.context)
            view_name = self.request.get('view', None)
            if itemNav is not None and view_name is not None:
                objList = itemNav.getViewObjList(view_name)
                #print "ooooooooooooooo: ", objList
            #print "ddd4: ", objList
            for obj in objList:
                (xml_title, name, item_ppath, iklen,
                 stateIconUrl, stateValue,
                 stateOverview, additionalAttributes) = \
                    self.getCollectionAttributes(obj)
                subItems.append(xmlEscapeWithCData(
                    u'<collection title=%s name=%s iklen=%s rem="2.1.1.2" '
                    u'icon_url=%s isopen="" expable="" state_url=%s path=%s '
                    u'state_val=%s>%s</collection>',
                    xml_title, name, iklen, stateIconUrl,
                    stateIconUrl, u'/'+ item_ppath, stateOverview,
                    'result'))
            #for obj in objList:
        except TypeError:
            pass
        return u' '.join(subItems)


    def children(self):
        """ """
        print "children"
        container = self.context
        self.request.response.setHeader('content-type',
                                        'text/xml;charset=utf-8')
        setNoCacheHeaders(self.request.response)
        if self.request.get('view', None):
            res = (u'<?xml version="1.0" ?><children> %s </children>'
                    % self.getViewList(container))
        else:
            res = (u'<?xml version="1.0" ?><children> %s </children>'
                    % self.children_utility(container))
        return res

    def getCollectionAttributes(self, obj_arg):
        additionalAttributes = ''
        if type(obj_arg) is tuple:
            #import pdb
            #pdb.set_trace()
            (attributeName, displayTitle, obj) = obj_arg
            appendUrl = '?getAttr&attrName=%s' % attributeName
        else:
            appendUrl = ''
            obj = obj_arg
        
        parentItem = zapi.getParent(obj)
        obj_url = urlparse(zapi.absoluteURL(obj, self.request))
        parent_url = urlparse(zapi.absoluteURL(parentItem, self.request))
        if type(obj_arg) is tuple:
            xml_title = displayTitle
            additionalAttributes += ' expable="" '
            attrList = getattr(obj, attributeName, None)
            iklen = len(attrList)
        else:
            try:
                xml_title = obj.getDcTitle()
            except ForbiddenAttribute:
                xml_title = _('[top]')
            iklen = len(obj)
        name = obj_url.path.split('/')[-1] + appendUrl
        stateIconUrl = self.getStateIconUrl(obj)
        stateValue = self.getStateValue(obj)
        stateOverview = self.getStateOverview(obj)
        item_ppath = parent_url.path + u'/'
        item_ppath = item_ppath.replace('//', '/')
        if item_ppath[0] == "/":
            item_ppath = item_ppath[1:]
#        try:
#            item_len = len(IContentList(oldItem).getContentList())
#        except TypeError:
#            item_len = self.getLengthOf(oldItem)
        return (xml_title, name, item_ppath,
                iklen, stateIconUrl, stateValue,
                stateOverview, additionalAttributes)
        
        
        
    def singleBranchTree(self, root=''):
        #print "singleBranchTree"
        result = ''
        oldItem = self.context
        # -----------------------------------
        subItems = []
        try:
            oldItemNav = INavigation(oldItem)
            objList = oldItemNav.getContextObjList()
            #print "ddd4: ", objList
            for obj in objList:
                if type(obj) is tuple: # obj is a special view
                    #print "uuuuu: ", obj
                    (navView, viewTitle, contextObj) = obj
                    (xml_title, name, item_ppath, iklen,
                     stateIconUrl, stateValue,
                     stateOverview, additionalAttributes) = \
                        self.getCollectionAttributes(contextObj)
                    subItems.append(xmlEscapeWithCData(
                        u'<collection title=%s name=%s iklen=%s rem="2.1.1.2" '
                        u'icon_url=%s expable="" navparam=%s state_url=%s path=%s '
                        u'>%s</collection>',
                        viewTitle,
                        item_ppath + name , 
                        '1', 'generic',
                        xmlEscapeWithCData('view=%s', navView),
                        'generic', '/', 
                        'result'))
#                    subItems.append(xmlEscapeWithCData(
#                        u'<collection title=%s name=%s iklen=%s rem="2.1.1.2" '
#                        u'icon_url=%s expable="" state_url=%s path=%s '
#                        u'>%s</collection>',
#                        viewTitle, 'Interfaces/15eaa7b86bf9ec0217f9b6d0fe084fd1b', '1', '',
#                        'stateIconUrl', '/', 
#                        'result'))
                else:
                    (xml_title, name, item_ppath, iklen,
                     stateIconUrl, stateValue,
                     stateOverview, additionalAttributes) = \
                        self.getCollectionAttributes(obj)
                    subItems.append(xmlEscapeWithCData(
                        u'<collection title=%s name=%s iklen=%s rem="2.1.1.2" '
                        u'icon_url=%s isopen="" expable="" state_url=%s path=%s '
                        u'state_val=%s>%s</collection>',
                        xml_title, name, iklen, stateIconUrl,
                        stateIconUrl, item_ppath, stateOverview,
                        result))
#            try:
#                subItems.append(xmlEscapeWithCData(
#                    u'<collection title=%s name=%s iklen=%s rem="2.1.1.2" '
#                    u'icon_url=%s expable="" state_url=%s path=%s '
#                    u'>%s</collection>',
#                    'Addresses2', 'Interfaces/15eaa7b86bf9ec0217f9b6d0fe084fd1b', '1', '',
#                    'stateIconUrl', '/', 
#                    'result'))
#            except Exception, errText:
#                print "errText: ", errText
#            subItems.append('<collection title="Addresses" name="Addresses" iklen="1" icon_url="" rem="1.1.2" state_url="generic" expable="" path="/"/>')
        except TypeError, errText:
            print "lange Nase gezogen: ", errText
            return self.singleBranchTree2(root)
        # -----------------------------------
#        try:
#            parentItem = zapi.getParent(oldItem)
#            (xml_title, name, item_ppath, iklen,
#             stateIconUrl, stateValue, stateOverview) = \
#                self.getCollectionAttributes(parentItem)
#            subItems.append(xmlEscapeWithCData(
#                u'<collection title=%s name=%s iklen=%s rem="2.1.1.2" '
#                u'icon_url=%s isopen="" expable="" state_url=%s path=%s '
#                u'state_val=%s>%s</collection>',
#                u'All '+xml_title, name, iklen, stateIconUrl,
#                stateIconUrl, item_ppath, stateOverview,
#                result))
#        except TypeError:
#            pass
        # -----------------------------------

        result = u' '.join(subItems)

        # -----------------------------------
        (xml_title, name, item_ppath, iklen,
         stateIconUrl, stateValue, stateOverview,
         additionalAttributes) = \
            self.getCollectionAttributes(oldItem)
        if len(result) > 0: # collection has content
            result = xmlEscapeWithCData(
                      u'<collection isfocused2="" title=%s name=%s iklen=%s rem="3.1" '
                      u'icon_url=%s state_url=%s navparam="children5.xml" path=%s isopen="" isroot="">%s</collection>',
                      xml_title, name, iklen, stateIconUrl, stateIconUrl,
                      item_ppath, result)
        else:
            result = xmlEscapeWithCData(
                      u'<collection isfocused2="" title=%s name=%s iklen=%s rem="3.2" '
                      u'icon_url=%s state_url=%s navparam="children6.xml" path=%s expable="" '
                      u'isroot="">%s</collection>',
                      xml_title, name, iklen, stateIconUrl, stateIconUrl,
                      item_ppath, result)
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
        
        
    def singleBranchTree3(self, root=''):
        result = ''
        oldItem = self.context
        xml_title = '11111'
        name = '22222'
        subitem_len = 0
        #oldItem = []
        iconUrl = ''
        stateIconUrl = ''
        item_ppath = ''
        stateOverview = ''
        rootName = '8888'
        baseURL = ''
        subItems = []
        #import pdb
        #pdb.set_trace()
#        subItems.append(xmlEscapeWithCData(
#            u'<collection isfocused="" title=%s '
#            u'name=%s iklen=%s rem="2.2.1.1" '
#            u'icon_url=%s state_url=%s path=%s '
#            u'state_val=%s>%s</collection>', 
#            xml_title, name, subitem_len, iconUrl,
#            stateIconUrl, item_ppath, stateOverview,
#            result))
        result = u' '.join(subItems)

#        dcAdapter = IGeneralDublinCore(oldItem)
        xml_title = oldItem.getDcTitle()
#        if dcAdapter:
#            if dcAdapter.title:
#                xml_title = dcAdapter.title
        iconUrl = self.getIconUrl(oldItem)
        url2=urlparse(zapi.absoluteURL(oldItem,self.request))
        name = url2[2].split('/')[-1]
        parentItem = zapi.getParent(oldItem)
        #parentItem.keys()[parentItem.values().index(oldItem)]
        stateIconUrl = self.getStateIconUrl(oldItem)
        #stateValue = self.getStateValue(oldItem)
        stateOverview = self.getStateOverview(oldItem)
        try:
            item_len = len(IContentList(oldItem).getContentList())
        except TypeError:
            item_len = self.getLengthOf(oldItem)
#            item_ppath = zapi.canonicalPath(zapi.getParent(item)) + u'/'
        url = urlparse(zapi.absoluteURL(zapi.getParent(oldItem),
                                        self.request))
        item_ppath = url.path + u'/'
        item_ppath = item_ppath.replace('//', '/')
        
        if len(result) > 0: # collection has content
            result = xmlEscapeWithCData(
                      u'<collection title=%s name=%s iklen=%s rem="3.1" '
                      u'icon_url=%s path=%s isopen="" isroot="">%s</collection>',
                      xml_title, name, len(oldItem), iconUrl,
                      item_ppath, result)
        else:
            result = xmlEscapeWithCData(
                      u'<collection title=%s name=%s iklen=%s rem="3.2" '
                      u'icon_url=%s path=%s expable="" '
                      u'isroot="">%s</collection>',
                      xml_title, name, len(oldItem), iconUrl,
                      item_ppath, result)
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

    def singleBranchTree2(self, root=''):
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
#                    item_ppath = zapi.canonicalPath(zapi.getParent(subItem)) \
#                               + u'/'
                    url = urlparse(zapi.absoluteURL(zapi.getParent(subItem),
                                                    self.request))
                    item_ppath = url.path + u'/'
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

