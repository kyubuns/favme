# -*- coding: utf-8 -*-
from flask import Flask, request
from jinja2 import FileSystemLoader, Environment

app = Flask(__name__)
env = Environment(loader=FileSystemLoader("."))

@app.route("/", methods=['GET', 'POST'])
def helloworld():
  template = env.get_template("test.html")
  userinput = request.values.get("name")
  return template.render(name = userinput)

if __name__ == "__main__":
  app.run(debug=True)
