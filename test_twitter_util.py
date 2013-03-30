#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

import twitter_util

class TwitterUtilTests(unittest.TestCase):
  def test_get_statuses(self):
    stats = twitter_util.get_statuses("knaka")
    self.assertNotEqual(stats, None)
  def test_expand_url(self):
    self.assertEqual(
     twitter_util.expand_url("http://t.co/pPEsEJYe"),
     "http://www.amazon.co.jp/gp/product/4797354143?ie=UTF8&tag=ayutaya-22&linkCode=shr&camp=1207&creative=8411&creativeASIN=4797354143" )
  ## ？
  #def test_expand_text(self):
  #  self.assertEqual(
  #   twitter_util.expand_url(u"foo http://t.co/pPEsEJYe bar http://t.co/bPKBXlDa buzz") == {'expanded': u'foo http://www.amazon.co.jp/gp/product/4797354143?ie=UTF8&tag=ayutaya-22&linkCode=shr&camp=1207&creative=8411&creativeASIN=4797354143 bar http://www.amazon.co.jp/gp/product/4839941734?ie=UTF8&tag=ayutaya-22&linkCode=shr&camp=1207&creative=8411&creativeASIN=4839941734&redirect=true&ref_=oh_details_o01_s00_i00 buzz', 'urls': {u'http://t.co/pPEsEJYe': 'http://www.amazon.co.jp/gp/product/4797354143?ie=UTF8&tag=ayutaya-22&linkCode=shr&camp=1207&creative=8411&creativeASIN=4797354143', u'http://t.co/bPKBXlDa': 'http://www.amazon.co.jp/gp/product/4839941734?ie=UTF8&tag=ayutaya-22&linkCode=shr&camp=1207&creative=8411&creativeASIN=4839941734&redirect=true&ref_=oh_details_o01_s00_i00'} }, True )

if __name__ == '__main__':
  unittest.main()
