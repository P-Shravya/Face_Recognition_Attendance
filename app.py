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
from datetime import datetime

app = Flask(__name__, template_folder='templates')
app.secret_key = 'your-secret-key-here'  # Required for session

# Subject schedules for different departments
subject_schedule_CME = {
    'MON': {
        9: 'DS LAB',
        10: 'DS LAB',
        11: 'IOT',
        12: 'SE',
        13: 'MEFA',
        14: 'CS'
    },
    'TUE': {
        9: 'WT',
        10: 'TALENTIO',
        11: 'TALENTIO',
        12: 'DS',
        13: 'CS',
        14: 'WT LAB'
    },
    'WED': {
        9: 'IOT',
        10: 'DS',
        11: 'IOT',
        12: 'CS',
        13: 'SE LAB',
        14: 'TALENTIO'
    },
    'THU': {
        9: 'MEFA',
        10: 'SE',
        11: 'MEFA',
        12: 'SE',
        13: 'DS LAB',
        14: 'DS LAB'
    },
    'FRI': {
        9: 'SE LAB',
        10: 'SE LAB',
        11: 'MEFA',
        12: 'WT',
        14: 'Technical Seminar-1'
    },
    'SAT': {
        9: 'CS',
        10: 'DS'
    }
}

subject_schedule_AI_DS = {
    'MON': {
        9: 'SE',
        10: 'Python',
        11: 'MLT LAB',
        12: 'MLT LAB',
        13: 'Talentio',
        14: 'BDA',
        15: 'MLT'
    },
    'TUE': {
        9: 'MLT',
        10: 'Talentio',
        11: 'MLT',
        12: 'WT',
        13: 'SE',
        14: 'MEFA'
    },
    'WED': {
        9: 'BDA',
        10: 'MEFA',
        11: 'MLT',
        12: 'WT',
        13: 'SE',
        14: 'MEFA'
    },
    'THU': {
        9: 'SE+MP LAB',
        10: 'SE+MP LAB',
        11: 'WT LAB',
        12: 'WT LAB',
    },
    'FRI': {
        9: 'MEFA',
        10: 'BDA',
        11: 'BDA',
        12: 'SE',
    },
    'SAT': {
        9: 'WT',
        10: 'MEFA',
        11: 'BDA',
        12: 'SE',
        14: 'Technical Seminar-1'
    }
}

subject_schedule_IT = {
    'MON': {
        9: 'ES',
        10: 'CRT',
        11: 'CRT',
        12: 'SE',
        13: 'AIML',
        14: 'AIML',
        15: 'NLP'
    },
    'TUE': {
        9: 'OST',
        10: 'ES',
        11: 'SE',
        12: 'AIML',
    },
    'WED': {
        9: 'SE',
        10: 'OST',
        11: 'ES LAB',
        12: 'ES LAB',
        14: 'CRT',
        15: 'AIML'
    },
    'THU': {
        9: 'NLP',
        10: 'SE',
        11: 'ES',
        12: 'OST',
        14: 'NLP',
        15: 'AIML'
    },
    'FRI': {
        9: 'AIML',
        10: 'SE',
        11: 'NLP',
        12: 'OST',
        14: 'SE LAB',
        15: 'AIML LAB'
    },
    'SAT': {
        9: 'ES',
        10: 'LIBRARY',
        11: 'MINI PROJECTS',
        12: 'MINI PROJECTS',
        14: 'TECHNICAL SEMINARS'
    }
}

subject_schedule_CSE = {
    'MON': {
        9: 'SE',
        10: 'DIS',
        11: 'BREAK',
        12: 'TS',
        13: 'DM',
        14: 'MEFA',
        15: 'PE'
    },
    'TUE': {
        9: 'MEFA',
        10: 'SE',
        11: 'BREAK',
        12: 'DIS LAB (A1&A2) / DM-B2 LAB (3&4)',
        13: 'DIS LAB (A1&A2) / DM-B2 LAB (3&4)',
        14: 'MENT',
        15: 'TS'
    },
    'WED': {
        9: 'DIS',
        10: 'PE',
        11: 'BREAK',
        12: 'SE-B2 LAB / DM-B1 LAB (3&4)',
        13: 'SE-B2 LAB / DM-B1 LAB (3&4)',
        14: 'DIS (2-05)',
        15: 'TS (1-06)'
    },
    'THU': {
        9: 'DIS-B1 LAB (1&2) / SE-B1 LAB (3&4)',
        10: 'DIS-B1 LAB (1&2) / SE-B1 LAB (3&4)',
        11: 'BREAK',
        12: 'SE (1-206) / DM (1-06) / SE (1-206)',
        13: 'DM',
        14: 'TS',
        15: 'DIS'
    },
    'FRI': {
        9: 'DM',
        10: 'TALENTIO',
        11: 'BREAK',
        12: 'TALENTIO',
        13: 'TALENTIO',
        14: 'SE',
        15: 'TS'
    },
    'SAT': {
        9: 'PE',
        10: 'MEFA',
        11: 'BREAK',
        12: ' ',
        13: ' ',
        14: 'DIS',
        15: 'PE'
    }
}

# Configure CORS with more specific settings
CORS(app, 
     resources={r"/*": {
         "origins": [
             "http://localhost:5000",
             "http://127.0.0.1:5000",
             "http://192.168.29.60:5000"
         ],
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

def get_department_schedule(department):
    department = department.upper()
    if department == 'CME':
        return subject_schedule_CME
    elif department == 'AIML':
        return subject_schedule_AI_DS
    elif department == 'IT':
        return subject_schedule_IT
    elif department == 'CSE':
        return subject_schedule_CSE
    return None

def get_current_subject(schedule, current_hour):
    if not schedule:
        return None
    
    current_day = datetime.now().strftime('%A')[:3].upper()
    day_schedule = schedule.get(current_day, {})
    
    # Find the current subject based on hour
    for hour, subject in sorted(day_schedule.items()):
        if hour <= current_hour < hour + 1:
            return subject
    return None

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/newregister.html')
def newregister():
    return render_template('newregister.html')

@app.route('/register')
def register_page():
    return redirect(url_for('newregister'))

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

# Helper to get current time slot string
def get_current_time_slot():
    now = datetime.now()
    hour = now.hour
    slot_map = {
        8: '8:00-9:00',
        9: '9:00-10:00',
        10: '10:00-11:00',
        11: '11:00-12:00',
        12: '12:00-13:00',
        14: '14:00-15:00',
        15: '15:00-16:00',
        16: '16:00-17:00'
    }
    return slot_map.get(hour, None)

@app.route('/get_subjects', methods=['POST'])
def get_subjects():
    data = request.json
    department = data.get('department')
    semester = data.get('semester')
    
    # Get current time slot
    time_slot = get_current_time_slot()
    if not time_slot:
        return jsonify({"subjects": []})
    
    # Get department schedule
    schedule = get_department_schedule(department)
    if not schedule:
        return jsonify({"error": "Invalid department"}), 400
    
    # Get current subject
    current_hour = int(time_slot.split(':')[0])
    current_subject = get_current_subject(schedule, current_hour)
    if not current_subject:
        return jsonify({"subjects": []})
    
    # Query the appropriate attendance table
    table_name = f"attendance_{department}_{semester}"
    query = f"""
    SELECT DISTINCT Subject, Time_slot 
    FROM {table_name} 
    WHERE Subject = %s AND Time_slot = %s
    """
    try:
        cursor.execute(query, (current_subject, time_slot))
        subjects = cursor.fetchall()
        return jsonify({
            "subjects": [
                {"Subject": subject[0], "Time_slot": subject[1]}
                for subject in subjects
            ]
        })
    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500

@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    data = request.json
    image_data = data.get('image')
    department = data.get('department')
    semester = data.get('semester')
    student_id = data.get('student_id')
    
    # Get current time slot
    time_slot = get_current_time_slot()
    if not time_slot:
        return jsonify({"success": False, "message": "Outside of class hours"})
    
    current_day = datetime.now().strftime('%A')
    
    # Process face image
    image_data = image_data.split(',')[1]
    image_bytes = base64.b64decode(image_data)
    np_img = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    
    # Generate face encoding
    face_locations = face_recognition.face_locations(img)
    if len(face_locations) == 0:
        return jsonify({"success": False, "message": "No face detected"})
    
    current_encoding = face_recognition.face_encodings(img, face_locations)[0]
    
    # Get stored face encoding
    cursor.execute("SELECT Face_encoded FROM students WHERE Student_id = %s", (student_id,))
    result = cursor.fetchone()
    if not result:
        return jsonify({"success": False, "message": "Student not found"})
    
    stored_encoding = np.frombuffer(result[0])
    
    # Compare face encodings
    match = face_recognition.compare_faces([stored_encoding], current_encoding, tolerance=0.6)[0]
    if not match:
        return jsonify({"success": False, "message": "Face verification failed"})
    
    # Get subjects for current time slot
    table_name = f"attendance_{department}_{semester}"
    query = f"""
    SELECT Subject 
    FROM {table_name} 
    WHERE Day = %s AND Time_slot = %s
    """
    cursor.execute(query, (current_day, time_slot))
    subjects = cursor.fetchall()
    
    marked_subjects = []
    for subject in subjects:
        # Update attendance
        update_query = f"""
        UPDATE {table_name} 
        SET Status = TRUE 
        WHERE Student_id = %s AND Subject = %s AND Date = CURRENT_DATE AND Time_slot = %s
        """
        cursor.execute(update_query, (student_id, subject[0], time_slot))
        marked_subjects.append(subject[0])
    
    db.commit()
    
    return jsonify({
        "success": True,
        "marked_subjects": marked_subjects
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)