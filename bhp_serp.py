from burp import IBurpExtender
from burp import IContextMenuFactory

from java.net import URL
from java.util import ArrayList
from javax.swing import JMenuItem
from thread import start_new_thread

import json
import socket
import urllib

API_KEY = '3e8bf5712898c90524ae7195002a61458bb2d1b1094c0a973fb26ad095e917d7'
API_HOST = 'serpapi.com'

class BurpExtender(IBurpExtender, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self.context = None
        
        callbacks.setExtensionName('BHP serp')
        callbacks.registerContextMenuFactory(self)
        
        return
    def createMenuItems(self, context_menu):
        self.context = context_menu
        menu_list = ArrayList()
        menu_list.add(JMenuItem('Send to Serp', actionPerformed=self.serp_menu))
        return menu_list
    
    def serp_menu(self, event):
        http_traffic = self.context.getSelectedMessages()
        print('%d requests highlighted' % len(http_traffic))
        
        for traffic in http_traffic:
            http_service = traffic.getHttpService()
            host = http_service.getHost()
            
            print('User selected host : %s' % host)
            self.serp_search(host)
            
        return
    def serp_search(self, host):
        try:
            is_ip = bool(socket.inet_aton(host))
        except socket.error:
            is_ip = False
            
        if is_ip:
            ip_address = host
            domain = False
        else:
            ip_address = socket.gethostbyname(host)
            domain = True
        
        start_new_thread(self.serp_query, ('domain:%s'%ip_address,))
        
        if domain:
            start_new_thread(self.serp_query, ('domain : %s' % host,))
            
    def serp_query(self, serp_query_string):
        print('Performing Bing search: %s' % serp_query_string)
        http_request  = 'GET https://%s/search.json?' % API_HOST
        http_request += 'q=%s&api_key=%s HTTP/1.1\r\n' % (urllib.parse.quote(serp_query_string), API_KEY)  
        http_request += 'Host: %s\r\n' % API_HOST
        http_request += 'Connection: close\r\n'
        http_request += 'User-Agent: Black Hat Python\r\n\r\n'
        
        json_body = self._callbacks.makeHttpRequest(API_HOST, 443, True, http_request).tostring()
        
        json_body = json_body.split('\r\n\r\n',1)[1]
        try:
            response = json.loads(json_body)
        except (TypeError, ValueError) as err:
            print('No results from serp: %s' % err)
        else:
            sites = list()
            if response.get('organic_results'):
                sites = response['organic_results'] # tree / response => webpages => value
            if len(sites):
                for site in sites:
                    print('*' * 100)
                    print('Title: %s' % site.get('title'))
                    print('URL: %s' % site.get('link'))
                    print('Description: %s' % site.get('snippet'))
                    print('*' * 100)

                    java_url = URL(site['link'])
                    if not self._callbacks.isInScope(java_url):
                        print('Adding %s to serp scope' % site['link'])
                        self._callbacks.includeInScope(java_url)
            else:
                print('Empty response from serp: %s' % serp_query_string)
        return