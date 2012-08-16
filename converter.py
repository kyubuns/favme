# -*- coding: utf-8 -*-
import urllib
import lxml.html
import lxml.etree
import re
import sys

class FavTemplateConverter:
  @staticmethod
  def run(filename):
    s = open(filename).read()
    dom = lxml.html.fromstring(s)
    FavTemplateConverter.sub(dom.head)
    FavTemplateConverter.sub(dom.body)
    return lxml.etree.tostring(dom, pretty_print=True)

  @staticmethod
  def eri(tag, parent_tag, js_flag=False):
    tmp = "html|"
    if parent_tag == "script" or js_flag == True:
      tmp += "js|"
    if parent_tag == "style":
      tmp += "css|"
    return "{{" + tag + "|" + tmp[:-1] + "}}"

  @staticmethod
  def sub(root):
    for element in list(root):
      #text
      if element.text != None:
        c = re.compile('{{.*?}}')
        for m in re.finditer(c, element.text):
          original = m.group()
          tag = m.group()[2:-2].replace(" ", "")
          if tag.find('|') != -1:
            continue
          element.text = element.text.replace(original, FavTemplateConverter.eri(tag, element.tag))

      #attrib
      for attribname in list(element.attrib):
        c = re.compile('{{.*?}}')
        for m in re.finditer(c, element.attrib[attribname]):
          original = m.group()
          tag = m.group()[2:-2].replace(" ", "")
          if tag.find('|') != -1:
            continue
          element.attrib[attribname] = element.attrib[attribname].replace(original, FavTemplateConverter.eri(tag, element.tag, True))

      #child
      FavTemplateConverter.sub(element)

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print "usage: *******************"
  else:
    print FavTemplateConverter.run(sys.argv[1])
