import mysql.connector
from werkzeug.security import generate_password_hash

# Update these values to match your MySQL setup
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Sh@867417',
    'database': 'Student_info'
}

admins = [
    {
        'email': 'pshravya05@gmail.com',
        'password': 'for_admin',
        'admin_name': 'Shravya'
    },
    
]

conn = mysql.connector.connect(**DB_CONFIG)
cur = conn.cursor()

for admin in admins:
    password_hash = generate_password_hash(admin['password'])
    try:
        cur.execute(
            "INSERT INTO admins (email, password_hash, admin_name) VALUES (%s, %s, %s)",
            (admin['email'], password_hash, admin['admin_name'])
        )
        print(f"Added admin: {admin['email']}")
    except Exception as e:
        print(f"Failed to add {admin['email']}: {e}")

conn.commit()
cur.close()
conn.close()
print("Done.")