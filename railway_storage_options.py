"""
Railway Deployment Options สำหรับ IT Business Shop

Option 1: Emergency Mode (ปัจจุบัน)
- app_emergency.py
- JSON file storage
- ไม่ใช้ database
- ข้อมูลหายเมื่อ restart

Option 2: Database Mode
- app_main.py  
- PostgreSQL database
- เสียค่าใช้จ่าย $5/เดือน
- ข้อมูลถาวร

Option 3: Volume Storage (แนะนำ)
- app_emergency.py + Railway Volume
- JSON files ใน persistent volume
- ฟรี + ข้อมูลไม่หาย
"""

# การตั้งค่า Railway Volume
# 1. ใน Railway Dashboard:
#    - เข้า Settings > Volumes
#    - สร้าง Volume ใหม่
#    - Mount Point: /app/data
#    - Size: 1GB (ฟรี)

# 2. แก้ไข app_emergency.py:
import os

class EmergencyDataStore:
    def __init__(self):
        # ใช้ Railway Volume หรือ local directory
        if os.environ.get('RAILWAY_ENVIRONMENT'):
            self.data_dir = "/app/data"  # Railway Volume
        else:
            self.data_dir = "emergency_data"  # Local development
        
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

# 3. Environment Variables ใน Railway:
# RAILWAY_ENVIRONMENT=production
# STORAGE_TYPE=volume

print("Railway Storage Configuration:")
print("1. Emergency Mode: JSON files (current)")
print("2. Database Mode: PostgreSQL ($5/month)")  
print("3. Volume Mode: JSON + persistent (recommended)")