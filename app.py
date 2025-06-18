from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
from werkzeug.security import check_password_hash
import mysql.connector
import base64
import re
import bcrypt
import cv2
import face_recognition
import pickle
import numpy as np

app = Flask(__name__, template_folder='templates')
app.secret_key = 'your-secret-key-here'  # Required for session

# Configure CORS with more specific settings
CORS(app, 
     resources={r"/*": {
         "origins": ["http://localhost:5000", "http://127.0.0.1:5000"],
         "methods": ["GET", "POST", "OPTIONS"],
         "allow_headers": ["Content-Type", "Authorization"],
         "supports_credentials": True
     }})

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sh@867417",
    database="Student_info"
)
cursor = db.cursor()

# Email validation regex
EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('newregister.html')

@app.route('/generate_encoding', methods=['POST'])
def generate_encoding():
    data = request.json
    image_data = data.get('image')
    if not image_data:
        return jsonify({'error': 'No image data provided'}), 400

    # Strip base64 prefix
    image_data = image_data.split(',')[1]
    image_bytes = base64.b64decode(image_data)
    np_img = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    # Generate encoding
    face_locations = face_recognition.face_locations(img)
    if len(face_locations) == 0:
        return jsonify({'error': 'No face detected'}), 400

    encodings = face_recognition.face_encodings(img, face_locations)
    if len(encodings) == 0:
        return jsonify({'error': 'Encoding failed'}), 400

    encoding = encodings[0]
    encoding_blob = np.array(encoding).tobytes()

    # Send encoding back as base64 for frontend use (or send array if needed)
    return jsonify({
        'encoding': base64.b64encode(encoding_blob).decode('utf-8')
    })

@app.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()

    #python variables storing JSON objects i.e: from input forms of javaScript
    name = data.get("name")
    student_id = data.get("studentId")
    email = data.get("email")
    password = data.get("password")
    department = data.get("department")
    year = data.get("year")
    semester = data.get("semester")
    face_encoding_b64 = data.get("face_encoding")  # list from JS or convert later

    # Input validation
    if not re.match(EMAIL_REGEX, email):
        return jsonify({"error": "Invalid email format"}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Simulate numpy array for face_encoding
    face_encoding_blob = base64.b64decode(face_encoding_b64)

    try:
        query = """
        INSERT INTO students (
            Student_name, Student_id, Department,
            Study_year, Semester, Email, Hashed_pass, Face_encoded
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            name, student_id, department, year, semester,
            email, hashed_password.decode('utf-8'), face_encoding_blob
        ))
        db.commit()
        return jsonify({"message": "User registered successfully"})
    except mysql.connector.IntegrityError as e:
        return jsonify({"error": str(e)}), 409

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
        
    data = request.json
    email = data.get('email')
    password = data.get('password')

    cursor.execute("SELECT Student_name, Student_id, Department, Semester, Hashed_pass FROM students WHERE Email=%s", (email,))
    user = cursor.fetchone()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[4].encode('utf-8')):
        student_data = {
            "Student_name": user[0],
            "Student_id": user[1],
            "Department": user[2],
            "Semester": user[3]
        }
        session['student'] = student_data
        return jsonify({"status": "success", "student": student_data})
    else:
        return jsonify({"status": "fail", "message": "Invalid credentials"}), 401

@app.route('/dashboard')
def dashboard():
    if 'student' in session:
        return render_template("dashboard.html", student=session['student'])
    return redirect(url_for('login'))  

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)