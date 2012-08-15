from flask import Flask
from jinja2 import FileSystemLoader
from favme import FavTemplate, FavEnvironment, favreq

app = Flask(__name__)
env = FavEnvironment(loader=FileSystemLoader("."))

@app.route("/", methods=['GET','POST'])
def add_user():
  template = env.get_template("test.html")
  return template.render(name=favreq("name"))

if __name__ == "__main__":
  app.run(debug=True)

