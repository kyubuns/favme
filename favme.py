# -*- coding: utf-8 -*-
from flask import request
from jinja2 import Environment, Template
from xml.sax.saxutils import *
import jinja2
import copy

class UserInputString:
  def __init__(self, message):
    self._message = message
    self.escapeHTML = False
    self.escapeJS = False
    self.escapeCSS = False
    self.rawHTML = False
    print "create"

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
    if self.escapeHTML == True:
      tmp = escape(tmp)
    if self.escapeJS == True:
      tmp = js_escape(tmp)
    if self.escapeCSS == True:
      tmp = tmp.lower()
      tmp = tmp.replace("expression", "")
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
    return FavTemplate(super(FavEnvironment, self).get_template(filename))


class FavTemplate:
  def __init__(self, template):
    self.template = template

  def render(self, **elements):
    safe_elements = {}
    for key in elements:
      safe_elements[key] = elements[key]
    return self.template.render(safe_elements)


def favreq(name, default=""):
  return UserInputString(request.values.get(name, default))

def tounicode(data):
  codecs = ['shift_jis','utf-8','euc_jp','cp932',
            'euc_jis_2004','euc_jisx0213','iso2022_jp','iso2022_jp_1',
            'iso2022_jp_2','iso2022_jp_2004','iso2022_jp_3','iso2022_jp_ext',
            'shift_jis_2004','shift_jisx0213','utf_16','utf_16_be',
            'utf_16_le','utf_7','utf_8_sig'];
  for codec in codecs:
    try: return data.decode(codec);
    except: continue;
  return u"";

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
