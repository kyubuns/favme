# -*- coding: utf-8 -*-
import urllib
import lxml.html

class FavTemplateConverter:
  @staticmethod
  def run(filename):
    s = open(filename).read()
    dom = lxml.html.fromstring(s)
    print dom.body
    print list(dom)
    print dom.body
    print list(dom.body)
    print dom.body[2].text
    print list(dom.body[4])
    print list(dom.body[4].attrib)
    print dom.body[4].attrib['action']
    print dom.body[4].attrib["method"]

FavTemplateConverter.run('./jinja2/test.html')
