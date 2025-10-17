"""
สคริปต์สำหรับอัปเดต database schema เพื่อรองรับระบบจัดการสมาชิก
"""

import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash
from models import Base, User, Entry

# ลบไฟล์ database เดิม
if os.path.exists('business.db'):
    os.remove('business.db')
    print("ลบไฟล์ database เดิมเรียบร้อย")

# สร้าง database ใหม่
engine = create_engine('sqlite:///business.db')
Base.metadata.create_all(engine)

print("สร้าง database schema ใหม่เรียบร้อย")

# สร้าง session
Session = sessionmaker(bind=engine)
session = Session()

# สร้างผู้ใช้ admin
admin_user = User(
    username='admin',
    email='admin@itbusinessshop.com',
    password_hash=generate_password_hash('admin123'),
    role='admin',
    is_active=True
)

session.add(admin_user)
session.commit()

print(f"สร้างผู้ใช้ admin เรียบร้อย:")
print(f"  Username: admin")
print(f"  Password: admin123")
print(f"  Role: admin")
print(f"  Email: admin@itbusinessshop.com")

session.close()
print("\nDatabase พร้อมใช้งานสำหรับระบบจัดการสมาชิก!")