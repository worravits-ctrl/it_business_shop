"""
Simple Emergency Flask App - Stable Version
ไม่มี template dependency, stable routing
"""

import os
import json
from datetime import datetime
from flask import Flask, request, redirect, session

app = Flask(__name__)
app.secret_key = 'emergency-stable-2025'

# Simple Data Store
class SimpleDataStore:
    def __init__(self):
        self.data_dir = "emergency_data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def save_entry(self, entry_data):
        entries_file = os.path.join(self.data_dir, "entries.json")
        entries = self.load_entries()
        entry_data['id'] = len(entries) + 1
        entry_data['created_at'] = datetime.now().isoformat()
        entries.append(entry_data)
        
        with open(entries_file, 'w', encoding='utf-8') as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)
        return entry_data['id']
    
    def load_entries(self):
        entries_file = os.path.join(self.data_dir, "entries.json")
        if not os.path.exists(entries_file):
            return []
        try:
            with open(entries_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def save_member(self, member_data):
        members_file = os.path.join(self.data_dir, "members.json")
        members = self.load_members()
        member_data['id'] = len(members) + 1
        member_data['created_at'] = datetime.now().isoformat()
        members.append(member_data)
        
        with open(members_file, 'w', encoding='utf-8') as f:
            json.dump(members, f, ensure_ascii=False, indent=2)
        return member_data['id']
    
    def load_members(self):
        members_file = os.path.join(self.data_dir, "members.json")
        if not os.path.exists(members_file):
            return []
        try:
            with open(members_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def find_member(self, username):
        members = self.load_members()
        for member in members:
            if member.get('username') == username:
                return member
        return None

# Initialize data store
data_store = SimpleDataStore()

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        # Admin login
        if username == 'admin' and password == 'admin123':
            session['user_id'] = 'admin'
            session['logged_in'] = True
            session['user_role'] = 'admin'
            return redirect('/dashboard')
        
        # Member login
        member = data_store.find_member(username)
        if member and member.get('password') == password:
            session['user_id'] = username
            session['logged_in'] = True
            session['user_role'] = 'member'
            return redirect('/dashboard')
        
        error = 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง'
    else:
        error = ''
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>IT Business Shop - Login</title>
        <meta charset="utf-8">
        <style>
            body {{ 
                font-family: Arial; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh; 
                margin: 0; 
                display: flex; 
                align-items: center; 
                justify-content: center; 
            }}
            .login-box {{ 
                background: white; 
                padding: 40px; 
                border-radius: 15px; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                max-width: 400px; 
                width: 100%; 
            }}
            h1 {{ color: #333; text-align: center; margin-bottom: 30px; }}
            input {{ 
                width: 100%; 
                padding: 12px; 
                margin: 10px 0; 
                border: 1px solid #ddd; 
                border-radius: 8px; 
                box-sizing: border-box; 
            }}
            button {{ 
                width: 100%; 
                padding: 12px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; 
                border: none; 
                border-radius: 8px; 
                cursor: pointer; 
                margin: 10px 0; 
            }}
            .register-btn {{ 
                background: linear-gradient(135deg, #28a745 0%, #20c997 100%); 
                text-decoration: none; 
                display: block; 
                text-align: center; 
            }}
            .error {{ color: red; text-align: center; margin: 10px 0; }}
        </style>
    </head>
    <body>
        <div class="login-box">
            <h1>🏪 IT Business Shop</h1>
            <p style="text-align: center; color: #666;">ระบบจัดการธุรกิจ</p>
            
            {f'<div class="error">{error}</div>' if error else ''}
            
            <form method="post">
                <input type="text" name="username" placeholder="ชื่อผู้ใช้" required>
                <input type="password" name="password" placeholder="รหัสผ่าน" required>
                <button type="submit">เข้าสู่ระบบ</button>
            </form>
            
            <a href="/register" class="register-btn button">สมัครสมาชิกใหม่</a>
        </div>
    </body>
    </html>
    '''

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        
        if not all([username, password, first_name, last_name]):
            error = 'กรุณากรอกข้อมูลให้ครบถ้วน'
        elif data_store.find_member(username):
            error = 'ชื่อผู้ใช้นี้มีอยู่แล้ว'
        elif len(password) < 6:
            error = 'รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร'
        else:
            member_data = {
                'username': username,
                'password': password,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'role': 'member',
                'status': 'active'
            }
            member_id = data_store.save_member(member_data)
            success = f'สมัครสมาชิกสำเร็จ! ID: {member_id}'
            return f'''
            <script>
                alert('{success}');
                window.location.href = '/login';
            </script>
            '''
    else:
        error = ''
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>สมัครสมาชิก - IT Business Shop</title>
        <meta charset="utf-8">
        <style>
            body {{ 
                font-family: Arial; 
                background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
                min-height: 100vh; 
                margin: 0; 
                display: flex; 
                align-items: center; 
                justify-content: center; 
            }}
            .register-box {{ 
                background: white; 
                padding: 40px; 
                border-radius: 15px; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                max-width: 500px; 
                width: 100%; 
            }}
            h1 {{ color: #333; text-align: center; margin-bottom: 30px; }}
            input {{ 
                width: 100%; 
                padding: 12px; 
                margin: 10px 0; 
                border: 1px solid #ddd; 
                border-radius: 8px; 
                box-sizing: border-box; 
            }}
            button {{ 
                width: 100%; 
                padding: 12px; 
                background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
                color: white; 
                border: none; 
                border-radius: 8px; 
                cursor: pointer; 
                margin: 10px 0; 
            }}
            .back-btn {{ 
                background: #6c757d; 
                text-decoration: none; 
                display: block; 
                text-align: center; 
            }}
            .error {{ color: red; text-align: center; margin: 10px 0; }}
        </style>
    </head>
    <body>
        <div class="register-box">
            <h1>👤 สมัครสมาชิกใหม่</h1>
            
            {f'<div class="error">{error}</div>' if error else ''}
            
            <form method="post">
                <input type="text" name="first_name" placeholder="ชื่อจริง" required>
                <input type="text" name="last_name" placeholder="นามสกุล" required>
                <input type="text" name="username" placeholder="ชื่อผู้ใช้" required>
                <input type="email" name="email" placeholder="อีเมล" required>
                <input type="password" name="password" placeholder="รหัสผ่าน (อย่างน้อย 6 ตัวอักษร)" required>
                <button type="submit">สมัครสมาชิก</button>
            </form>
            
            <a href="/login" class="back-btn button">กลับหน้าเข้าสู่ระบบ</a>
        </div>
    </body>
    </html>
    '''

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect('/login')
    
    user_role = session.get('user_role', 'member')
    user_id = session.get('user_id')
    
    entries = data_store.load_entries()
    members = data_store.load_members()
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard - IT Business Shop</title>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial; padding: 20px; background: #f8f9fa; }}
            .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }}
            .btn {{ 
                padding: 12px 20px; 
                margin: 8px; 
                text-decoration: none; 
                border-radius: 8px; 
                display: inline-block; 
                color: white; 
                font-weight: bold; 
            }}
            .btn-primary {{ background: #007bff; }}
            .btn-success {{ background: #28a745; }}
            .btn-info {{ background: #17a2b8; }}
            .btn-warning {{ background: #ffc107; color: black; }}
            .btn-danger {{ background: #dc3545; }}
            .stats {{ background: #e3f2fd; padding: 20px; border-radius: 8px; margin: 20px 0; }}
            h1 {{ color: #333; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏪 IT Business Shop Dashboard</h1>
            <p>ยินดีต้อนรับ: <strong>{user_id}</strong> ({user_role})</p>
            
            <div class="stats">
                <h3>📊 สถิติระบบ</h3>
                <p>📦 รายการทั้งหมด: {len(entries)} รายการ</p>
                <p>👥 สมาชิกทั้งหมด: {len(members)} คน</p>
                <p>🕐 เวลาปัจจุบัน: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <h3>🛠️ เมนูหลัก</h3>
            <a href="/data" class="btn btn-primary">📊 จัดการข้อมูล</a>
            <a href="/members" class="btn btn-info">👥 จัดการสมาชิก</a>
            <a href="/health" class="btn btn-success">💚 Health Check</a>
            <a href="/logout" class="btn btn-danger">🚪 ออกจากระบบ</a>
        </div>
    </body>
    </html>
    '''

@app.route('/data')
def data_page():
    if not session.get('logged_in'):
        return redirect('/login')
    
    entries = data_store.load_entries()
    
    entries_html = ""
    for entry in entries:
        entries_html += f'''
        <tr>
            <td>{entry.get('id', '-')}</td>
            <td>{entry.get('item_name', '-')}</td>
            <td>{entry.get('quantity', '-')}</td>
            <td>{entry.get('price', '-')}</td>
            <td>{entry.get('category', '-')}</td>
            <td>{entry.get('created_at', '-')[:10]}</td>
        </tr>
        '''
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>จัดการข้อมูล - IT Business Shop</title>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial; padding: 20px; background: #f8f9fa; }}
            .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ padding: 10px; border: 1px solid #ddd; text-align: left; }}
            th {{ background: #f8f9fa; }}
            input, select {{ padding: 8px; margin: 5px; border: 1px solid #ddd; border-radius: 4px; }}
            button {{ padding: 8px 16px; background: #007bff; color: white; border: none; border-radius: 4px; }}
            .btn {{ padding: 10px 20px; margin: 5px; text-decoration: none; border-radius: 5px; display: inline-block; }}
            .btn-primary {{ background: #007bff; color: white; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 จัดการข้อมูล</h1>
            
            <h3>➕ เพิ่มรายการใหม่</h3>
            <form method="post" action="/add-entry">
                <input type="text" name="item_name" placeholder="ชื่อสินค้า" required>
                <input type="number" name="quantity" placeholder="จำนวน" required>
                <input type="number" step="0.01" name="price" placeholder="ราคา" required>
                <select name="category">
                    <option value="อิเล็กทรอนิกส์">อิเล็กทรอนิกส์</option>
                    <option value="เครื่องใช้ไฟฟ้า">เครื่องใช้ไฟฟ้า</option>
                    <option value="อื่นๆ">อื่นๆ</option>
                </select>
                <button type="submit">เพิ่มรายการ</button>
            </form>
            
            <h3>📋 รายการทั้งหมด ({len(entries)} รายการ)</h3>
            <table>
                <tr>
                    <th>ID</th>
                    <th>ชื่อสินค้า</th>
                    <th>จำนวน</th>
                    <th>ราคา</th>
                    <th>หมวดหมู่</th>
                    <th>วันที่สร้าง</th>
                </tr>
                {entries_html}
            </table>
            
            <div style="margin-top: 20px;">
                <a href="/dashboard" class="btn btn-primary">← กลับ Dashboard</a>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/add-entry', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        return redirect('/login')
    
    entry_data = {
        'item_name': request.form.get('item_name'),
        'quantity': int(request.form.get('quantity', 0)),
        'price': float(request.form.get('price', 0)),
        'category': request.form.get('category')
    }
    
    data_store.save_entry(entry_data)
    return redirect('/data')

@app.route('/members')
def members_page():
    if not session.get('logged_in'):
        return redirect('/login')
    
    members = data_store.load_members()
    
    members_html = ""
    for member in members:
        members_html += f'''
        <tr>
            <td>{member.get('id', '-')}</td>
            <td>{member.get('username', '-')}</td>
            <td>{member.get('first_name', '')} {member.get('last_name', '')}</td>
            <td>{member.get('email', '-')}</td>
            <td>{member.get('created_at', '-')[:10]}</td>
        </tr>
        '''
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>จัดการสมาชิก - IT Business Shop</title>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial; padding: 20px; background: #f8f9fa; }}
            .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ padding: 10px; border: 1px solid #ddd; text-align: left; }}
            th {{ background: #f8f9fa; }}
            .btn {{ padding: 10px 20px; margin: 5px; text-decoration: none; border-radius: 5px; display: inline-block; }}
            .btn-primary {{ background: #007bff; color: white; }}
            .btn-success {{ background: #28a745; color: white; }}
            .stats {{ background: #e3f2fd; padding: 15px; border-radius: 8px; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>👥 จัดการสมาชิก</h1>
            
            <div class="stats">
                <h3>📊 สถิติสมาชิก</h3>
                <p>จำนวนสมาชิกทั้งหมด: {len(members)} คน</p>
            </div>
            
            <div>
                <a href="/register" class="btn btn-success">➕ เพิ่มสมาชิกใหม่</a>
            </div>
            
            <h3>📋 รายชื่อสมาชิก</h3>
            <table>
                <tr>
                    <th>ID</th>
                    <th>ชื่อผู้ใช้</th>
                    <th>ชื่อ-นามสกุล</th>
                    <th>อีเมล</th>
                    <th>วันที่สมัคร</th>
                </tr>
                {members_html}
            </table>
            
            <div style="margin-top: 20px;">
                <a href="/dashboard" class="btn btn-primary">← กลับ Dashboard</a>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    return {
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'message': 'Emergency app running stable'
    }

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    print(f"🚀 Starting Stable Emergency Server on port {port}")
    print(f"🌐 URL: http://localhost:{port}")
    print(f"🔑 Admin Login: admin / admin123")
    print(f"📱 Register new members at /register")
    
    try:
        app.run(host='0.0.0.0', port=port, debug=False)  # Disable debug to prevent crashes
    except Exception as e:
        print(f"❌ Server Error: {e}")
        print("💡 Try a different port")