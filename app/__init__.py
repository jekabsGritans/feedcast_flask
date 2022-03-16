from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

from app.auth.controllers import auth as auth_mod
from app.podcast.controllers import pod as pod_mod

app.register_blueprint(auth_mod)
app.register_blueprint(pod_mod)

db.create_all()