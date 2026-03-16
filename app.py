from flask import Flask, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://LaserBread:Foof@localhost/iplist'
db = SQLAlchemy(app)

class Entry(db.Model):
    __tablename__ = "Entries"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    hostname: Mapped[str]
    ipv4: Mapped[int]
    cidrmask: Mapped[int]
    mac: Mapped[str]
    notes: Mapped[str]


@app.route('/')
def index():
    return Response("piss off",404)

@app.route('/getall',methods=["GET"])
def getall():
    result = Entry.query.all()
    out = [{key: value for key, value in entry.__dict__.items() if key not in ['_sa_instance_state']} for entry in result]

    return jsonify(out)

@app.route('/add',methods=["POST"])
def add():
    try:
        pass

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')