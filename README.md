# IT Business Shop - ระบบจัดการรายรับรายจ่าย

🏪 **ระบบจัดการร้าน IT Business Shop แบบครบครัน** พัฒนาด้วย Flask และ Bootstrap 5

## ✨ Features

### 🔐 **ระบบจัดการสมาชิก**
- สมัครสมาชิกใหม่
- เข้าสู่ระบบ/ออกจากระบบ
- Role-based Access Control (Admin/User)
- จัดการสมาชิก (Admin เท่านั้น)

### 💰 **ระบบจัดการรายรับ-รายจ่าย**
- เพิ่ม/แก้ไข/ลบรายการรายรับ-รายจ่าย
- หมวดหมู่ที่กำหนดเองได้
- ระบบ pagination
- Dashboard แสดงสถิติครบถ้วน

### 📊 **Dashboard และรายงาน**
- สถิติรายวัน, รายเดือน, รายปี
- กราฟแสดงแนวโน้ม (Chart.js)
- แสดงยอดรวมและกำไร
- UI สวยงามด้วย Bootstrap 5

### 📤 **นำเข้า/ส่งออกข้อมูล**
- Export เป็น CSV
- Import จาก CSV
- รองรับ UTF-8 BOM

## 🚀 Quick Start

### Requirements
- Python 3.8+
- Flask 2.3.2
- SQLAlchemy 2.0.19
- Bootstrap 5.3.0

### Installation

1. **Clone repository**
```bash
git clone https://github.com/YOUR_USERNAME/it_business_shop.git
cd it_business_shop
```

2. **ติดตั้ง dependencies**
```bash
pip install -r requirements.txt
```

3. **สร้าง database**
```bash
python init_member_system.py
```

4. **รันระบบ**
```bash
python app_main.py
```

5. **เข้าใช้งาน**
- เปิดเบราว์เซอร์ไปที่: `http://127.0.0.1:8000`
- Login: admin / admin123

## 📁 Project Structure

```
it_business_shop/
├── app_main.py              # Main Flask application
├── models.py                # Database models (User, Entry)
├── forms.py                 # WTForms (Login, Registration, Entry)
├── init_member_system.py    # Database initialization
├── requirements.txt         # Python dependencies
├── static/
│   └── main.js             # Frontend JavaScript
├── templates/
│   ├── base.html           # Base template
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   ├── dashboard.html      # Dashboard with charts
│   ├── entries.html        # Transaction list
│   ├── entry_form.html     # Add/Edit transaction
│   ├── members.html        # Member management (Admin)
│   └── import_export.html  # Import/Export page
└── business.db             # SQLite database (auto-generated)
```

## 🔑 Default Login

**Admin Account:**
- Username: `admin`
- Password: `admin123`
- Role: `admin`
- Email: `admin@itbusinessshop.com`

## 🎨 Features Preview

### 🏠 Dashboard
- สถิติรายรับ-รายจ่าย แบ่งตาม วัน/เดือน/ปี
- กราฟแนวโน้ม 7 วันย้อนหลัง
- เมนูด่วนไปยังฟังก์ชันต่างๆ

### 👥 จัดการสมาชิก (Admin)
- ดูรายชื่อสมาชิกทั้งหมด
- เปิด/ปิดการใช้งาน
- เลื่อน/ลดสิทธิ์ Admin
- ลบสมาชิก

### 💼 จัดการรายการ
- เพิ่มรายรับ: การขาย, บริการ
- เพิ่มรายจ่าย: ค่าหมึก, กระดาษ, ค่าน้ำ-ไฟ
- แก้ไข/ลบรายการ
- ระบบหมวดหมู่ที่ปรับแต่งได้

## 🛠 Technology Stack

- **Backend:** Flask 2.3.2, SQLAlchemy 2.0.19
- **Frontend:** Bootstrap 5.3.0, Chart.js, Font Awesome
- **Database:** SQLite
- **Authentication:** Flask-Login
- **Forms:** WTForms with CSRF protection
- **Styling:** Sarabun Font (Thai), Modern gradient design

## � Railway Deployment

### Deploy to Railway (Recommended)

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Deploy from GitHub**
   ```bash
   # Connect your GitHub repository
   # Railway will automatically detect Python app
   ```

3. **Add PostgreSQL Database**
   - In Railway dashboard, click "New"
   - Select "Database" → "PostgreSQL"
   - Railway will provide DATABASE_URL automatically

4. **Environment Variables**
   Set these in Railway dashboard:
   ```
   FLASK_ENV=production
   SECRET_KEY=your-secret-key-here
   PORT=8000
   ```

5. **Deploy**
   - Push to GitHub (Railway auto-deploys)
   - App will be available at `https://your-app.railway.app`

### Railway Configuration Files
- `Procfile` - Process definition
- `railway.json` - Railway configuration
- `requirements.txt` - Includes PostgreSQL support
- `runtime.txt` - Python version

## 🐛 Troubleshooting

### Local Development Issues
หากเกิดปัญหา "no such column":
```bash
python init_member_system.py
```

### Port Already in Use
หากพอร์ต 8000 ถูกใช้งาน:
```bash
# แก้ไขในไฟล์ app_main.py บรรทัดสุดท้าย
app.run(debug=True, host='127.0.0.1', port=8001)
```

### Railway Deployment Issues
- Check Railway logs for errors
- Ensure DATABASE_URL is set
- Verify all environment variables

## 📝 License

MIT License

## 👨‍💻 Author

สร้างโดย AI Assistant สำหรับการจัดการร้าน IT Business Shop

---

## 📞 Support

หากมีปัญหาการใช้งาน กรุณาสร้าง Issue ใน GitHub repository
