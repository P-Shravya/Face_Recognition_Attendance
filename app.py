from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import mysql.connector
import base64
import re
import bcrypt
import cv2
import numpy as np
from mysql.connector import Error
import os

app = Flask(__name__, template_folder='.')
CORS(app) 

def get_db_connection():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Sh@867417",
            database="Student_info"
        )
        return db
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

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

    try:
        # Strip base64 prefix
        image_data = image_data.split(',')[1]
        image_bytes = base64.b64decode(image_data)
        np_img = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Load the face cascade classifier
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            return jsonify({'error': 'No face detected'}), 400

        # Get the first face
        x, y, w, h = faces[0]
        face_img = gray[y:y+h, x:x+w]
        
        # Resize to a standard size
        face_img = cv2.resize(face_img, (100, 100))
        
        # Convert to bytes
        face_bytes = face_img.tobytes()

        return jsonify({
            'encoding': base64.b64encode(face_bytes).decode('utf-8')
        })
    except Exception as e:
        return jsonify({'error': f'Error processing image: {str(e)}'}), 500

@app.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    #python variables storing JSON objects i.e: from input forms of javaScript
    name = data.get("name")
    student_id = data.get("studentId")
    email = data.get("email")
    password = data.get("password")
    department = data.get("department")
    year = data.get("year")
    semester = data.get("semester")
    face_encoding_b64 = data.get("face_encoding")

    # Validate required fields
    required_fields = ["name", "studentId", "email", "password", "department", "year", "semester", "face_encoding"]
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Input validation
    if not re.match(EMAIL_REGEX, email):
        return jsonify({"error": "Invalid email format"}), 400

    try:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        face_encoding_blob = base64.b64decode(face_encoding_b64)

        db = get_db_connection()
        if not db:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = db.cursor()
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
        cursor.close()
        db.close()
        return jsonify({"message": "User registered successfully"})
    except mysql.connector.IntegrityError as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 409
    except Exception as e:
        return jsonify({"error": f"Registration failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)