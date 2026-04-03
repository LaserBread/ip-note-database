from flask import Flask, jsonify, Response, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import LargeBinary
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.exceptions import BadRequest, NotFound
import re

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
    ipv6: Mapped[bytes] = mapped_column(LargeBinary(16), nullable=True)

@app.route('/')
def index():
    return Response("piss off",404)

@app.route('/getall',methods=["GET"])
def getall():
    result = Entry.query.all()
    out = [{key: value.hex() if isinstance(value, bytes) and key not in ['sa_instance_state'] else value for key, value in entry.__dict__.items() if key not in ['_sa_instance_state']} for entry in result]

    return jsonify(out)

@app.route('/add',methods=["POST"])
def add():
    try:
        data = request.get_json()

        ipv6_data = None
        if 'ipv6' in data and data['ipv6'] is not None:
            ipv6_data = bytes.fromhex(data['ipv6'])

        new_entry = Entry(
            name=data['name'],
            hostname=data.get('hostname'),
            ipv4=data.get('ipv4'),
            cidrmask=data.get('cidrmask'),
            mac=data.get('mac'),
            notes=data.get('notes'),
            ipv6=ipv6_data
        )

        db.session.add(new_entry)
        db.session.commit()
        
        return jsonify({
            'message': 'Entry added successfully',
            'id': new_entry.id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), e.response if hasattr(e,"response") else 500
    
@app.route('/update/<int:entry_id>',methods=["PUT"])
def update(entry_id):
    try:
        data = request.get_json()
        
        if entry_id == None:
            raise BadRequest("400 Bad Request: Missing ID", 400)
        
        entry = db.session.get(Entry, entry_id)
        
        if entry == None:
            raise NotFound(f"404 Not Found: Entry with ID {entry_id} doesn't exist.", 404)

        if 'name' in data:
            entry.name = data['name']
        if 'hostname' in data:
            entry.hostname = data['hostname']
        if 'ipv4' in data:
            entry.ipv4 = data['ipv4']
        if 'cidrmask' in data:
            entry.cidrmask = data['cidrmask']
        if 'ipv6' in data:
            if data['ipv6'] is not None:
                try:
                    entry.ipv6 = bytes.fromhex(data['ipv6'])
                except ValueError as e:
                    raise BadRequest(f"Invalid IPv6 '{data['ipv6']}'.")
            else:
                entry.ipv6 = None
        if 'mac' in data:
            entry.mac = data['mac']
        if 'notes' in data:
            entry.notes = data['notes']

        db.session.commit()
        return jsonify({
            'message': 'Entry updated successfully',
            'id': entry.id
        }), 200
    
    except KeyError:
        return jsonify({"error": "400 Bad Request: ID is probably missing"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), e.response if hasattr(e,"response") else 500
    
@app.route('/delete/<int:entry_id>',methods=["DELETE"])
def delete(entry_id):
    try:
        
        if entry_id == None:
            raise BadRequest("400 Bad Request: Missing ID", 400)
        
        entry = db.session.get(Entry, entry_id)
        
        if entry == None:
            raise NotFound(f"404 Not Found: Entry with ID {entry_id} doesn't exist.", 404)

        db.session.delete(entry)
        db.session.commit()
        
        return jsonify({'message': 'Entry deleted successfully', 'id': entry_id}), 200
    
    except KeyError:
        return jsonify({"error": "400 Bad Request: ID is probably missing"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), e.response if hasattr(e,"response") else 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
