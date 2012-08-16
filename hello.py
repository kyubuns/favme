# -*- coding: utf-8 -*-
from flask import Flask
from jinja2 import FileSystemLoader
from favme import FavTemplate, FavEnvironment, favreq

app = Flask(__name__)
env = FavEnvironment(loader=FileSystemLoader("."))

@app.route("/", methods=['GET','POST'])
def add_user():
  template = env.get_template("test.html")
  inputname = favreq("name")
  if inputname:
    return template.render(name=inputname)
  else:
    return template.render()

if __name__ == "__main__":
  app.run(debug=True)

