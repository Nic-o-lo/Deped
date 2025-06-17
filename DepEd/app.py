from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///deped.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# -------------------------------
# Database Models
# -------------------------------

class tblUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, unique=True, nullable=False)
    firstname = db.Column(db.String(100), nullable=False)
    middlename = db.Column(db.String(100))
    lastname = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    admin = db.Column(db.Boolean, default=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    officeName = db.Column(db.String(100), nullable=False)

class Office(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Officename = db.Column(db.String(100))
    Officedetails = db.Column(db.String(255))

class tblProject(db.Model):
    projectID = db.Column(db.Integer, primary_key=True)
    projectDetails = db.Column(db.String(255))
    userID = db.Column(db.Integer)  # No ForeignKey to tblUser
    createdAt = db.Column(db.Date, default=datetime.utcnow)
    editedAt = db.Column(db.Date)
    prNumber = db.Column(db.Integer)

class track(db.Model):
    trackID = db.Column(db.Integer, primary_key=True)
    trackDetails = db.Column(db.String(255))
    userID = db.Column(db.Integer)  # No ForeignKey to tblUser
    remarks = db.Column(db.String(255))
    createdAt = db.Column(db.Date, default=datetime.utcnow)
    updatedAt = db.Column(db.Date)
    projectID = db.Column(db.Integer)  # No ForeignKey to tblProject

# -------------------------------
# Routes
# -------------------------------

@app.route('/')
def home():
    return send_from_directory('.', 'Home.html')

@app.route('/dashboard')
def dashboard():
    return send_from_directory('.', 'Dashboard.html')

@app.route('/create')
def create():
    return send_from_directory('.', 'Create.html')

@app.route('/create-success')
def create_success():
    return send_from_directory('.', 'CreateSuccess.html')

@app.route('/accounts')
def accounts():
    return send_from_directory('.', 'Accounts.html')

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = tblUser.query.filter_by(username=data.get('username'), password=data.get('password')).first()
    if user:
        return jsonify({'status': 'success', 'role': 'admin' if user.admin else 'user'})
    return jsonify({'status': 'fail'}), 401

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    print("Received data:", data)  # Debug print
    try:
        # Check for duplicate userID or username
        if tblUser.query.filter_by(userID=int(data.get('userID'))).first():
            return jsonify({'status': 'fail', 'message': 'User ID already exists.'}), 400
        if tblUser.query.filter_by(username=data.get('username')).first():
            return jsonify({'status': 'fail', 'message': 'Username already exists.'}), 400

        new_user = tblUser(
            userID=int(data.get('userID')),
            firstname=data.get('firstname'),
            middlename=data.get('middlename'),
            lastname=data.get('lastname'),
            position=data.get('position'),
            admin=bool(data.get('admin')) if isinstance(data.get('admin'), bool) else str(data.get('admin')).lower() == 'true',
            username=data.get('username'),
            password=data.get('password'),
            officeName=data.get('officeName')
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        db.session.rollback()
        print("Error creating user:", e)  # Debug print
        return jsonify({'status': 'fail', 'message': str(e)}), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    users = tblUser.query.all()
    result = []
    for user in users:
        result.append({
            'id': user.id,
            'userID': user.userID,
            'firstname': user.firstname,
            'middlename': user.middlename,
            'lastname': user.lastname,
            'position': user.position,
            'admin': user.admin,
            'username': user.username,
            'officeName': user.officeName
        })
    return jsonify(result)

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = tblUser.query.get(user_id)
    if not user:
        return jsonify({'status': 'fail', 'message': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

# -------------------------------
# Run App
# -------------------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
