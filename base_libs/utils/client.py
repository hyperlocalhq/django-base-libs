# -*- coding: UTF-8 -*-
import base64
import re
import socket
import urllib
import urllib2
try:
    unicode
except NameError:
    unicode = str
"""
Client classes for cross-server communication

= Examples =

== SEARCH GOOGLE BY GET METHOD ==

google = Connection("www.google.com/search?q=funny+jokes")
response = google.send_request(headers={
    'User-Agent': "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
    })
print response.read()

== VALIDATE HTML BY POST METHOD ==
validator = Connection("validator.w3.org/check")
response = validator.send_request(
    headers={'User-Agent': "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"},
    values={'fragment': "<html></html>"}
    )
print response.read()

== RSS OF ACTIVE TICKETS IN JETSON BY GET METHOD ==

username = raw_input("Username: ")
password = raw_input("Password: ")
jetsonproject = AuthSSLConnection(
    "code.jetsonproject.com/report/3?format=rss",
    username=username,
    password=password,
    )
response = jetsonproject.send_request()
print response.read()
# unfortunatelly, this returns the HTML of login screen, because the authentication method on the server is Digest but not Basic

"""


class HttpErrorResponse(object):
    """
    An error response which will be returned instead of raising an error when HttpError occurs. HttpErrorResponse mimicks the object returned on success
    """

    def __init__(self, url, code, msg):
        self.url = url
        self.code = code
        self.msg = msg

    def read(self):
        return ""

    def readline(self):
        return ""

    def readlines(self):
        return []

    def geturl(self):
        return self.url

    def headers(self):
        return []

    def info(self):
        return ""

    def __iter__(self):
        return None

    def next(self):
        return None

    def close(self):
        pass


class Connection(object):
    """Creates a connection to a server"""

    protocol = "http://"
    protocol_pattern = re.compile(r"^\S+://")

    def __init__(self, url, timeout=30, encoding="utf-8"):
        m = self.protocol_pattern.search(url)
        if m:
            self.protocol = m.group(0)
            self.url = self.protocol_pattern.sub("", url)
        else:
            self.url = url
        self.timeout = timeout
        self.encoding = encoding

    def __del__(self):
        if hasattr(self, "response") and self.response:
            self.response.close()

    def send_request(self, headers=None, values=None):
        if not values:
            values = {}
        if not headers:
            headers = {}
        socket.setdefaulttimeout(self.timeout)
        data = None
        encoded_values = {}
        for key, val in values.items():
            if isinstance(val, unicode):
                encoded_values[key] = val.encode(self.encoding)
            else:
                if hasattr(val, "__iter__"):
                    new_val = []
                    for el in val:
                        if isinstance(el, unicode):
                            new_val.append(el.encode(self.encoding))
                        else:
                            new_val.append(el)
                    encoded_values[key] = new_val
                else:
                    encoded_values[key] = val
        if encoded_values:
            data = urllib.urlencode(encoded_values, True)
        request = urllib2.Request(self.protocol + self.url, data, headers)
        try:
            self.response = urllib2.urlopen(request)
        except urllib2.HTTPError as e:
            self.response = HttpErrorResponse(url=self.url, code=e.code, msg=e.msg,)
        return self.response


class SSLConnection(Connection):
    """Creates a connection to a server via SSL"""

    protocol = "https://"


class AuthSSLConnection(SSLConnection):
    """Creates a connection to authenticated server via SSL (Only Basic authentication)"""

    def __init__(self, url, username="", password="", timeout=30):
        super(AuthSSLConnection, self).__init__(url, timeout)
        self.username = username
        self.password = password
        self.base64string = base64.encodestring(
            "%s:%s" % (self.username, self.password)
        )[:-1]

    def send_request(self, headers=None, values=None):
        if not headers:
            headers = {}
        socket.setdefaulttimeout(self.timeout)
        data = None
        if values:
            data = urllib.urlencode(values)
        request = urllib2.Request(self.protocol + self.url, data, headers)
        if self.username:
            request.add_header("Authorization", "Basic %s" % self.base64string)
        self.response = urllib2.urlopen(request)
        return self.response
