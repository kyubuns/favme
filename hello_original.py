# -*- coding: utf-8 -*-
from flask import Flask, request
from jinja2 import FileSystemLoader, Environment, Template

app = Flask(__name__)
env = Environment(loader=FileSystemLoader("."))

@app.route("/", methods=['GET','POST'])
def add_user():
  template = env.get_template("test.html")
  name1 = request.values.get("name1")
  name2 = request.values.get("name2")
  return template.render(name1=name1, name2=name2)

if __name__ == "__main__":
  app.run(debug=True)

