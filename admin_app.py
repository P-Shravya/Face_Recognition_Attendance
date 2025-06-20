from flask import Blueprint, request, jsonify, session, render_template
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from flask_cors import CORS
from collections import defaultdict
import datetime

admin_bp = Blueprint('admin_bp', __name__, template_folder='templates')

# Update these values to match your MySQL setup
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Sh@867417',
    'database': 'Student_info'
}

def get_db():
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn

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

@admin_bp.route('/admin_login', methods=['POST'])
def admin_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'status': 'fail', 'message': 'Missing credentials'}), 400

    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute('SELECT * FROM admins WHERE email = %s', (email,))
    admin = cur.fetchone()

    if not admin:
        cur.close()
        conn.close()
        return jsonify({'status': 'fail', 'message': 'Wrong admin email entered.'}), 401
    
    if not check_password_hash(admin['password_hash'], password):
        cur.close()
        conn.close()
        return jsonify({'status': 'fail', 'message': 'Wrong password entered.'}), 401

    session['admin_id'] = admin['id']
    cur.close()
    conn.close()
    return jsonify({'status': 'success', 'admin': {'id': admin['id'], 'email': admin['email'], 'admin_name': admin['admin_name']}})

@admin_bp.route('/admin_dashboard')
def admin_dashboard():
    # Render the admin dashboard HTML
    return render_template('admin_dashboard.html')

@admin_bp.route('/api/admin/attendance_logs', methods=['GET'])
def get_attendance_logs():
    department = request.args.get('department', '').strip().upper()
    semester = request.args.get('semester', '').strip()
    period = request.args.get('period', 'date')  # 'date', 'week', 'month'
    start = request.args.get('start', '')
    end = request.args.get('end', '')

    if not department or not semester:
        return jsonify({'logs': [], 'error': 'Department and semester are required.'}), 400

    table_name = f"attendance_{get_department_table_name(department)}_{semester}"
    conn = get_db()
    cur = conn.cursor(dictionary=True)

    # Build date filter
    date_filter = ""
    params = []
    if start and end:
        date_filter = "AND Date BETWEEN %s AND %s"
        params.extend([start, end])
    elif start:
        date_filter = "AND Date >= %s"
        params.append(start)
    elif end:
        date_filter = "AND Date <= %s"
        params.append(end)

    # Query attendance logs
    query = f'''
        SELECT a.Student_id, s.Student_name, s.Department, s.Semester, a.Date, a.Subject, a.Time_slot, a.Day, a.Status
        FROM {table_name} a
        JOIN students s ON a.Student_id = s.Student_id
        WHERE 1=1 {date_filter}
        ORDER BY a.Date, a.Time_slot
    '''
    cur.execute(query, params)
    rows = cur.fetchall()

    # Grouping helpers
    def get_week_key(date):
        # Returns (year, week number)
        if isinstance(date, str):
            date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        return date.isocalendar()[:2]  # (year, week)
    def get_month_key(date):
        if isinstance(date, str):
            date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        return (date.year, date.month)

    # Calculate attendance percentage per student, and build logs
    student_attendance = defaultdict(lambda: {'attended': 0, 'total': 0, 'info': {}})
    logs = []
    week_group = defaultdict(list)
    month_group = defaultdict(list)
    for row in rows:
        sid = row['Student_id']
        student_attendance[sid]['total'] += 1
        if row['Status']:
            student_attendance[sid]['attended'] += 1
        student_attendance[sid]['info'] = {
            'student_name': row['Student_name'],
            'department': row['Department'],
            'semester': row['Semester']
        }
        log_entry = {
            'student_name': row['Student_name'],
            'department': row['Department'],
            'semester': row['Semester'],
            'date': row['Date'].strftime('%Y-%m-%d') if hasattr(row['Date'], 'strftime') else str(row['Date']),
            'subject': row['Subject'],
            'period': row['Time_slot'],
            'status': 'Present' if row['Status'] else 'Absent'
        }
        logs.append(log_entry)
        # Group for week/month
        week_group[get_week_key(row['Date'])].append(log_entry)
        month_group[get_month_key(row['Date'])].append(log_entry)

    # Add attendance percentage to each log
    for log in logs:
        sid = None
        for k, v in student_attendance.items():
            if v['info']['student_name'] == log['student_name']:
                sid = k
                break
        if sid:
            total = student_attendance[sid]['total']
            attended = student_attendance[sid]['attended']
            percent = round((attended / total) * 100, 2) if total > 0 else 0.0
            log['attendance_percent'] = percent
        else:
            log['attendance_percent'] = 0.0

    # Filter/group logs by period
    if period == 'week':
        logs = []
        for week, week_logs in week_group.items():
            # Calculate summary for each student in this week
            week_stats = defaultdict(lambda: {'attended': 0, 'total': 0, 'info': {}})
            for log in week_logs:
                sid = None
                for k, v in student_attendance.items():
                    if v['info']['student_name'] == log['student_name']:
                        sid = k
                        break
                if sid:
                    week_stats[sid]['total'] += 1
                    if log['status'] == 'Present':
                        week_stats[sid]['attended'] += 1
                    week_stats[sid]['info'] = student_attendance[sid]['info']
            for sid, stat in week_stats.items():
                percent = round((stat['attended'] / stat['total']) * 100, 2) if stat['total'] > 0 else 0.0
                logs.append({
                    'student_name': stat['info']['student_name'],
                    'department': stat['info']['department'],
                    'semester': stat['info']['semester'],
                    'week': f"{week[0]}-W{week[1]}",
                    'attendance_percent': percent,
                    'attended': stat['attended'],
                    'total': stat['total']
                })
    elif period == 'month':
        logs = []
        for month, month_logs in month_group.items():
            month_stats = defaultdict(lambda: {'attended': 0, 'total': 0, 'info': {}})
            for log in month_logs:
                sid = None
                for k, v in student_attendance.items():
                    if v['info']['student_name'] == log['student_name']:
                        sid = k
                        break
                if sid:
                    month_stats[sid]['total'] += 1
                    if log['status'] == 'Present':
                        month_stats[sid]['attended'] += 1
                    month_stats[sid]['info'] = student_attendance[sid]['info']
            for sid, stat in month_stats.items():
                percent = round((stat['attended'] / stat['total']) * 100, 2) if stat['total'] > 0 else 0.0
                logs.append({
                    'student_name': stat['info']['student_name'],
                    'department': stat['info']['department'],
                    'semester': stat['info']['semester'],
                    'month': f"{month[0]}-{month[1]:02d}",
                    'attendance_percent': percent,
                    'attended': stat['attended'],
                    'total': stat['total']
                })

    # Summary statistics per department and per subject
    summary = {
        'department': defaultdict(lambda: {'attended': 0, 'total': 0}),
        'subject': defaultdict(lambda: {'attended': 0, 'total': 0})
    }
    for row in rows:
        dept = row['Department']
        subj = row['Subject']
        summary['department'][dept]['total'] += 1
        summary['subject'][subj]['total'] += 1
        if row['Status']:
            summary['department'][dept]['attended'] += 1
            summary['subject'][subj]['attended'] += 1
    # Calculate average attendance percent
    summary_out = {
        'department': [
            {
                'department': dept,
                'attendance_percent': round((v['attended']/v['total'])*100, 2) if v['total'] > 0 else 0.0,
                'attended': v['attended'],
                'total': v['total']
            } for dept, v in summary['department'].items()
        ],
        'subject': [
            {
                'subject': subj,
                'attendance_percent': round((v['attended']/v['total'])*100, 2) if v['total'] > 0 else 0.0,
                'attended': v['attended'],
                'total': v['total']
            } for subj, v in summary['subject'].items()
        ]
    }

    cur.close()
    conn.close()
    return jsonify({'logs': logs, 'summary': summary_out}) 