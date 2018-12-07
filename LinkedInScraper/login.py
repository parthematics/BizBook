import cookielib
import os
import urllib
import urllib2
import re
import string
import sys
import config
from bs4 import BeautifulSoup

def linkedIn():
        global opener
        cookie_filename = "cookies.txt"

        cj = cookielib.MozillaCookieJar(cookie_filename)
        if os.access(cookie_filename, os.F_OK):
            cj.load()

        # Load Proxy settings
        if len(config.proxylist) > 0:
            #print "[Status] Setting up proxy (%s)" % config.proxylist[0]
            proxy_handler = urllib2.ProxyHandler({'https':config.proxylist[0]})
            opener = urllib2.build_opener(
                proxy_handler,
                urllib2.HTTPRedirectHandler(),
                urllib2.HTTPHandler(debuglevel=0),
                urllib2.HTTPSHandler(debuglevel=0),
                urllib2.HTTPCookieProcessor(cj)
            )
        else:
            opener = urllib2.build_opener(
                urllib2.HTTPRedirectHandler(),
                urllib2.HTTPHandler(debuglevel=0),
                urllib2.HTTPSHandler(debuglevel=0),
                urllib2.HTTPCookieProcessor(cj)
            )

        # Get CSRF Token
        #print "[Status] Obtaining a CSRF token"
        html = loadPage("https://www.linkedin.com/")
        soup = BeautifulSoup(html, "html.parser")
        csrf = soup.find(id="loginCsrfParam-login")['value']
        #print csrf
        # Authenticate
        login_data = urllib.urlencode({
            'session_key': config.linkedin['username'],
            'session_password': config.linkedin['password'],
            'loginCsrfParam': csrf,
        })
        html = loadPage("https://www.linkedin.com/uas/login-submit", login_data)
        soup = BeautifulSoup(html, "html.parser")
        try:
            print cj._cookies['.www.linkedin.com']['/']['li_at'].value
        except:
            print "error"
        cj.save()
        os.remove(cookie_filename)

def loadPage(url, data=None):
        try:
            response = opener.open(url)
        except:
            print "\n Your IP may have been temporarily blocked"

        try:
            if data is not None:
                response = opener.open(url, data)
            else:
                response = opener.open(url)
            #return response.headers.get('Set-Cookie')
            return ''.join(response.readlines())
        except:
            print "Exception"
            sys.exit(0)

linkedIn()
