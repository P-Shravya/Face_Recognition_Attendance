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
from admin_app import admin_bp

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
        15: 'NLP',
        8: 'Testing',
        16: 'Testing',
        17: 'Testing',
        18: 'Testing',
        19: 'Testing',
        20: 'Testing',
        21: 'Testing',
        22: 'Testing',
        23: 'Testing',
    },
    'TUE': {
        9: 'OST',
        10: 'ES',
        11: 'SE',
        12: 'AIML',
        8: 'Testing',
        13: 'Testing',
        14: 'Testing',
        15: 'Testing',
        16: 'Testing',
        17: 'Testing',
        18: 'Testing',
        19: 'Testing',
        20: 'Testing',
        21: 'Testing',
        22: 'Testing',
        23: 'Testing',
    },
    'WED': {
        9: 'SE',
        10: 'OST',
        11: 'ES LAB',
        12: 'ES LAB',
        14: 'CRT',
        15: 'AIML',
        8: 'Testing',
        13: 'Testing',
        16: 'Testing',
        17: 'Testing',
        18: 'Testing',
        19: 'Testing',
        20: 'Testing',
        21: 'Testing',
        22: 'Testing',
        23: 'Testing',
    },
    'THU': {
        9: 'NLP',
        10: 'SE',
        11: 'ES',
        12: 'OST',
        14: 'NLP',
        15: 'AIML',
        8: 'Testing',
        13: 'Testing',
        16: 'Testing',
        17: 'Testing',
        18: 'Testing',
        19: 'Testing',
        20: 'Testing',
        21: 'Testing',
        22: 'Testing',
        23: 'Testing',
    },
    'FRI': {
        9: 'AIML',
        10: 'SE',
        11: 'NLP',
        12: 'OST',
        14: 'SE LAB',
        15: 'AIML LAB',
        8: 'Testing',
        13: 'Testing',
        16: 'Testing',
        17: 'Testing',
        18: 'Testing',
        19: 'Testing',
        20: 'Testing',
        21: 'Testing',
        22: 'Testing',
        23: 'Testing',
    },
    'SAT': {
        9: 'ES',
        10: 'LIBRARY',
        11: 'MINI PROJECTS',
        12: 'MINI PROJECTS',
        14: 'TECHNICAL SEMINARS',
        8: 'Testing',
        13: 'Testing',
        15: 'Testing',
        16: 'Testing',
        17: 'Testing',
        18: 'Testing',
        19: 'Testing',
        20: 'Testing',
        21: 'Testing',
        22: 'Testing',
        23: 'Testing',
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
    
    # Handle both full names and abbreviations
    if department == 'CME' or department == 'COMPUTER ENGINEERING':
        return subject_schedule_CME
    elif department == 'AIML' or department == 'ARTIFICIAL INTELLIGENCE & MACHINE LEARNING':
        return subject_schedule_AI_DS
    elif department == 'IT' or department == 'INFORMATION TECHNOLOGY':
        return subject_schedule_IT
    elif department == 'CSE' or department == 'COMPUTER SCIENCE & ENGINEERING':
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
    print(f"[DEBUG] Registration data received: {data}")
    #python variables storing JSON objects i.e: from input forms of javaScript
    name = data.get("name")
    student_id = data.get("studentId")
    email = data.get("email")
    password = data.get("password")
    department = data.get("department").strip().upper()
    year = data.get("year")
    semester = data.get("semester")
    face_encoding_b64 = data.get("face_encoding")  # list from JS or convert later
    print(f"[DEBUG] name={name}, student_id={student_id}, email={email}, department={department}, year={year}, semester={semester}")
    print(f"[DEBUG] face_encoding_b64 exists: {face_encoding_b64 is not None}")
    # Input validation
    if not re.match(EMAIL_REGEX, email):
        print("[DEBUG] Invalid email format.")
        return jsonify({"error": "Invalid email format"}), 400
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        face_encoding_blob = base64.b64decode(face_encoding_b64)
    except Exception as e:
        print(f"[DEBUG] Error decoding face encoding: {e}")
        return jsonify({"error": "Invalid face encoding"}), 400
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
        print("[DEBUG] Registration successful.")
        return jsonify({"message": "User registered successfully"})
    except mysql.connector.IntegrityError as e:
        print(f"[DEBUG] Integrity error: {e}")
        return jsonify({"error": str(e)}), 409
    except Exception as e:
        print(f"[DEBUG] Registration error: {e}")
        return jsonify({"error": str(e)}), 500

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
    if 8 <= hour < 9:
        return '8:00-9:00'
    elif 9 <= hour < 10:
        return '9:00-10:00'
    elif 10 <= hour < 11:
        return '10:00-11:00'
    elif 11 <= hour < 12:
        return '11:00-12:00'
    elif 12 <= hour < 13:
        return '12:00-13:00'
    elif 14 <= hour < 15:
        return '14:00-15:00'
    elif 15 <= hour < 16:
        return '15:00-16:00'
    elif 16 <= hour < 17:
        return '16:00-17:00'
    else:
        return None

@app.route('/get_subjects', methods=['POST'])
def get_subjects():
    data = request.json
    department = data.get('department').strip().upper()
    semester = data.get('semester')
    print(f"[DEBUG] /get_subjects called with department={department}, semester={semester}")
    time_slot = get_current_time_slot()
    print(f"[DEBUG] Current time slot: {time_slot}")
    if not time_slot:
        print("[DEBUG] No valid time slot found.")
        return jsonify({"subjects": []})
    schedule = get_department_schedule(department)
    print(f"[DEBUG] Department schedule: {schedule}")
    if not schedule:
        print("[DEBUG] Invalid department.")
        return jsonify({"error": "Invalid department"}), 400
    current_hour = int(time_slot.split(':')[0])
    current_subject = get_current_subject(schedule, current_hour)
    print(f"[DEBUG] Current subject: {current_subject}")
    if not current_subject:
        print("[DEBUG] No current subject found.")
        return jsonify({"subjects": []})
    
    current_date = datetime.now().strftime('%Y-%m-%d')
    current_day = datetime.now().strftime('%A')

    # Return the current subject based on schedule, not from database
    return jsonify({
        "subjects": [
            {
                "Subject": current_subject, 
                "Time_slot": time_slot,
                "Date": current_date,
                "Day": current_day
            }
        ]
    })

@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    data = request.json
    image_data = data.get('image')
    department = data.get('department').strip().upper()
    semester = data.get('semester')
    student_id = data.get('student_id')
    print(f"[DEBUG] /mark_attendance called with student_id={student_id}, department={department}, semester={semester}")
    time_slot = get_current_time_slot()
    print(f"[DEBUG] Current time slot: {time_slot}")
    if not time_slot:
        print("[DEBUG] No valid time slot found.")
        return jsonify({"success": False, "message": "Outside of class hours"})
    current_day = datetime.now().strftime('%A')
    print(f"[DEBUG] Current day: {current_day}")
    current_date = datetime.now().date()
    print(f"[DEBUG] Current date: {current_date}")
    
    # Process face image
    image_data = image_data.split(',')[1]
    image_bytes = base64.b64decode(image_data)
    np_img = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    
    # Generate face encoding
    face_locations = face_recognition.face_locations(img)
    print(f"[DEBUG] Face locations found: {face_locations}")
    if len(face_locations) == 0:
        print("[DEBUG] No face detected in image.")
        return jsonify({"success": False, "message": "No face detected"})
    
    current_encoding = face_recognition.face_encodings(img, face_locations)[0]
    
    # Get stored face encoding
    cursor.execute("SELECT Face_encoded FROM students WHERE Student_id = %s", (student_id,))
    result = cursor.fetchone()
    print(f"[DEBUG] Stored face encoding fetched: {result is not None}")
    if not result:
        print("[DEBUG] Student not found in database.")
        return jsonify({"success": False, "message": "Student not found"})
    
    stored_encoding = np.frombuffer(result[0])
    
    # Compare face encodings
    match = face_recognition.compare_faces([stored_encoding], current_encoding, tolerance=0.6)[0]
    print(f"[DEBUG] Face match result: {match}")
    if not match:
        print("[DEBUG] Face verification failed.")
        return jsonify({"success": False, "message": "Face verification failed"})
    
    # Get current subject from schedule
    schedule = get_department_schedule(department)
    current_hour = int(time_slot.split(':')[0])
    current_subject = get_current_subject(schedule, current_hour)
    
    if not current_subject:
        print("[DEBUG] No current subject found.")
        return jsonify({"success": False, "message": "No class scheduled at this time"})
    
    table_name = f"attendance_{get_department_table_name(department)}_{semester}"
    
    try:
        # Check if attendance record exists for this student, date, subject, time slot, and day
        select_query = f"""
        SELECT 1 FROM {table_name} 
        WHERE Student_id = %s AND Subject = %s AND Date = %s AND Time_slot = %s AND Day = %s
        """
        cursor.execute(select_query, (student_id, current_subject, current_date, time_slot, current_day))
        exists = cursor.fetchone()
        
        if not exists:
            # Insert a new attendance record for this student, subject, date, time slot, and day
            insert_query = f"""
            INSERT INTO {table_name} (Date, Student_id, Subject, Time_slot, Day, Status)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (current_date, student_id, current_subject, time_slot, current_day, True))
            print(f"[DEBUG] New attendance record created for student {student_id}")
        else:
            # Update existing attendance record to mark as present
            update_query = f"""
            UPDATE {table_name}
            SET Status = TRUE
            WHERE Student_id = %s AND Subject = %s AND Date = %s AND Time_slot = %s AND Day = %s
            """
            cursor.execute(update_query, (student_id, current_subject, current_date, time_slot, current_day))
            print(f"[DEBUG] Existing attendance record updated for student {student_id}")
        
        db.commit()
        print(f"[DEBUG] Attendance marked successfully for student {student_id}, subject {current_subject}, date {current_date}, time_slot {time_slot}, day {current_day}")
        
        return jsonify({
            "success": True,
            "marked_subjects": [current_subject]
        })
        
    except mysql.connector.Error as e:
        print(f"[DEBUG] Database error: {e}")
        db.rollback()
        return jsonify({"success": False, "message": f"Database error: {str(e)}"}), 500
    except Exception as e:
        print(f"[DEBUG] Unexpected error: {e}")
        db.rollback()
        return jsonify({"success": False, "message": f"Unexpected error: {str(e)}"}), 500

def get_department_table_name(department):
    """Convert department name to table name format"""
    department = department.upper()
    if department == 'INFORMATION TECHNOLOGY':
        return 'IT'
    elif department == 'COMPUTER SCIENCE & ENGINEERING':
        return 'CSE'
    elif department == 'ARTIFICIAL INTELLIGENCE & MACHINE LEARNING':
        return 'AI_DS'
    elif department == 'COMPUTER ENGINEERING':
        return 'CME'
    elif department == 'ELECTRONICS & COMMUNICATION ENGINEERING':
        return 'ECE'
    elif department == 'ELECTRICAL & ELECTRONICS ENGINEERING':
        return 'EEE'
    else:
        return department  # Return as is if it's already an abbreviation

app.register_blueprint(admin_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)