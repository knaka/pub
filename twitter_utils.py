#!/usr/bin/python
# -*- coding: utf-8 -*-

### http://dev.twitter.com/doc

uname = 'knaka'

class Conf:
  FailCountThre = 20
  def __init__(self, conf_path):
    self.conf_path = conf_path
    import ConfigParser
    self.parser = ConfigParser.SafeConfigParser({
      'uid': 'knaka',
      'last_sid': '-1', # Last status ID already read
      'archpath_template': '/tmp/%%Y%%m00tweets.txt',
      'toffset': '+9', # Fetched data uses GMT
      'fail_count': '0',
    })
    self.parser.read(self.conf_path)
  def read(self):
    uid = self.parser.get('DEFAULT', 'uid')
    last_sid = self.parser.getint('DEFAULT', 'last_sid')
    archpath_template = self.parser.get('DEFAULT', 'archpath_template')
    toffset = self.parser.getint('DEFAULT', 'toffset')
    self.fail_count = self.parser.getint('DEFAULT', 'fail_count')
    return (uid, last_sid, archpath_template, toffset,)
  def update_last_sid(self, last_sid):
    self.parser.set("DEFAULT", 'last_sid', '%d' % (last_sid,))
    self.fail_count = 0
    self.parser.set("DEFAULT", 'fail_count', '%d' % (self.fail_count,))
    with open(self.conf_path, 'wb') as output:
      self.parser.write(output)
  def increment_failure(self):
    self.fail_count += 1
    if self.fail_count > self.FailCountThre:
      self.fail_count = 0
      parser.set("DEFAULT", 'fail_count', '%d' % (self.fail_count,))
      ## What's New in Python 2.5 ? Python v2.7.2 documentation 
      ## http://docs.python.org/whatsnew/2.5.html
      with open(self.conf_path, 'wb') as output:
        parser.write(output)
      raise
    self.parser.set("DEFAULT", 'fail_count', '%d' % (self.fail_count,))
    with open(self.conf_path, 'wb') as output:
      self.parser.write(output)

## Python Twitter Tools http://mike.verdone.ca/twitter/
## https://github.com/sixohsix/twitter/
## UTF-8 fix: https://github.com/knaka/twitter/
import twitter
import tauthinfo
conskey = tauthinfo.conskey
reqtok = tauthinfo.reqtoks[uname]
oauth = twitter.oauth.OAuth(reqtok['id'], reqtok['secret'],
 conskey['id'], conskey['secret'] )

def get_statuses(uid):
  t = twitter.Twitter(domain = 'api.twitter.com', api_version = '1.1',
   auth = oauth )
  stats = t.statuses.user_timeline(include_rts = True)
  stats.reverse() # Destructive
  return stats

def expand_url(url):
  ## http://docs.python.org/library/urlparse
  import urlparse
  parse_result = urlparse.urlparse(url)
  ## http://docs.python.org/library/httplib
  import httplib
  conn = httplib.HTTPConnection(parse_result.netloc)
  conn.request("GET", parse_result.path)
  resp = conn.getresponse()
  loc = resp.getheader("Location")
  if loc:
    return loc
  else:
    return url

def expand_urls_in_text(text):
  expanded_urls = {}
  def expand_murl(murl):
    url = murl.group(0)
    expanded_url = expand_url(murl.group(0))
    expanded_urls[url] = expanded_url
    return expanded_url
  import re
  text = re.sub(r'https?://t.co/[a-zA-Z0-9_]+', expand_murl, text)
  return (text, expanded_urls,)

import HTMLParser
h = HTMLParser.HTMLParser()

def format_fields(stat):
  ## It is a RT
  if stat.has_key('retweeted_status'):
    url = u'http://twitter.com/%s/status/%s' % (
     stat['retweeted_status']['user']['screen_name'], 
     stat['retweeted_status']['id'], )
    text = u'RT @%s: %s' % (
     stat['retweeted_status']['user']['screen_name'],
     stat['retweeted_status']['text'], )
  ## The others
  else:
    url = u'http://twitter.com/%s/status/%s' % (
     stat['user']['screen_name'],
     stat['id'], )
    text = stat['text']
  ## All stats can have reply_to info
  if stat['in_reply_to_status_id']:
    repurl = u'http://twitter.com/%s/status/%s' % (
     stat['in_reply_to_screen_name'],
     stat['in_reply_to_status_id'], )
  else:
    repurl = u''
  text = h.unescape(text) # "text" is in escaped HTML (XML?)
  text = text.replace("\n", "<br/>")
  return (url, repurl, text,)

if __name__ == '__main__':
  print expand_urls_in_text(u"うー http://t.co/pPEsEJYe にゃー http://t.co/bPKXlDa ぎゃー")
