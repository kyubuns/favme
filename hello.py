# -*- coding: utf-8 -*-
from flask import Flask, request
from jinja2 import FileSystemLoader, Environment
from favme import FavEnvironment, favreq

app = Flask(__name__)
env = FavEnvironment(loader=FileSystemLoader("."))

@app.route("/", methods=['GET', 'POST'])
def helloworld():
  template = env.get_template("test.html")
  userinput = favreq("name")
  return template.render(name = userinput)

if __name__ == "__main__":
  app.run(debug=True)
