from flask import request
from jinja2 import Environment, Template
from xml.sax.saxutils import *
import jinja2

class UserInputString:
  def __init__(self, message):
    self._message = message
    self.escapeHTML = False
    self.escapeJS = False
    self.rawHTML = False

  def __eq__(self, i):
    return self._message == i

  def __ne__(self, i):
    return self._message != i

  def getRawString(self):
    return self._message

  def __str__(self):
    if self.rawHTML == False and self.escapeHTML == False and self.escapeJS == False:
      raise TypeError, ''

    tmp = self._message
    if self.escapeHTML == True:
      tmp = escape(tmp)
    if self.escapeJS == True:
      tmp = js_escape(tmp)
    return tmp

  def js_escape(src):
    return src.translate({
      ord(u"'"): u"\'",
      ord(u'"'): u'\"',
      ord(u"\\"): u"\\\\",
      ord(u'/'): u'\/',
      ord(u'>'): u'\x3e'
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

##########################################################

def raw_filter(s):
  if s.__class__.__name__ == "UserInputString":
    s.rawHTML = True
  return s
jinja2.filters.FILTERS['raw'] = raw_filter

def html_filter(s):
  if s.__class__.__name__ == "UserInputString":
    s.escapeHTML = True
  return s
jinja2.filters.FILTERS['html'] = html_filter

def js_filter(s):
  if s.__class__.__name__ == "UserInputString":
    s.escapeJS = True
  return s
jinja2.filters.FILTERS['js'] = js_filter
