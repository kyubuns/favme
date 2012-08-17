# -*- coding: utf-8 -*-
from flask import request
from jinja2 import Environment, Template
from xml.sax.saxutils import *
from converter import FavTemplateConverter
import jinja2
import copy

class UserInputString:
  def __init__(self, message):
    self._message = message
    self.escapeHTML = False
    self.escapeJS = False
    self.escapeCSS = False
    self.rawHTML = False

  def __eq__(self, i):
    return self._message == i

  def __ne__(self, i):
    return self._message != i

  def __len__(self):
    return len(self._message)

  def getRawString(self):
    return self._message

  def __str__(self):
    if self.rawHTML == False and self.escapeHTML == False and self.escapeJS == False:
      raise TypeError, 'hoge'

    tmp = self._message
    if self.escapeJS == True:
      tmp = js_escape(tmp)
    if self.escapeHTML == True:
      tmp = escape(tmp)
    if self.escapeCSS == True:
      check = tmp.lower()
      if check.find("expression") != -1:
        return "\"\""
    return tmp

def js_escape(src):
  if len(src) == 0:
    return src
  return src.translate({
    ord(u"'"): u"\\\'",
    ord(u'"'): u"\\\"",
    ord(u"\\"):u"\\\\",
    ord(u'/'): u"\\/",
    ord(u'>'): u"\\x3e",
    ord(u':'): u"\\:"
  })

class FavEnvironment(Environment):
  def get_template(self, filename):
    template_text = FavTemplateConverter.run(filename)
    return super(FavEnvironment, self).from_string(template_text)


def favreq(name, default=""):
  return UserInputString(request.values.get(name, default))

##########################################################

def raw_filter(m):
  s = copy.deepcopy(m)
  if s.__class__.__name__ == "UserInputString":
    s.rawHTML = True
  return s
jinja2.filters.FILTERS['raw'] = raw_filter

def html_filter(m):
  s = copy.deepcopy(m)
  if s.__class__.__name__ == "UserInputString":
    s.escapeHTML = True
  return s
jinja2.filters.FILTERS['html'] = html_filter

def js_filter(m):
  s = copy.deepcopy(m)
  if s.__class__.__name__ == "UserInputString":
    s.escapeJS = True
  return s
jinja2.filters.FILTERS['js'] = js_filter

def css_filter(m):
  s = copy.deepcopy(m)
  if s.__class__.__name__ == "UserInputString":
    s.escapeCSS = True
  return s
jinja2.filters.FILTERS['css'] = css_filter

