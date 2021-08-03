from flask import Blueprint

dashboard = Blueprint('dashboard', __name__)

@dashboard.route("/url", methods=['GET'])
def hello():
  return 'hello world'
