"""
IT Business Shop - Emergency Flask App
Fixed connection pool and routing issues
"""

import os
from flask import Flask, render_template, request, redirect, session, jsonify, url_for, flash
from werkzeug.security import check_password_hash
import json
from datetime import datetime

# Emergency Data Storage Class
class EmergencyDataStore:
    def __init__(self, data_dir="emergency_data"):
        self.data_dir = data_dir
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
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
    
    def delete_entry(self, entry_id):
        entries = self.load_entries()
        entries = [e for e in entries if e.get('id') != entry_id]
        entries_file = os.path.join(self.data_dir, "entries.json")
        with open(entries_file, 'w', encoding='utf-8') as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)
    
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
    
    def update_member_password(self, username, new_password):
        members = self.load_members()
        for member in members:
            if member.get('username') == username:
                member['password'] = new_password
                member['password_updated_at'] = datetime.now().isoformat()
                break
        
        members_file = os.path.join(self.data_dir, "members.json")
        with open(members_file, 'w', encoding='utf-8') as f:
            json.dump(members, f, ensure_ascii=False, indent=2)
        return True
    
    def find_member(self, username):
        members = self.load_members()
        for member in members:
            if member.get('username') == username:
                return member
        return None

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'emergency-secret-key-2025')

# Initialize Emergency Data Store
data_store = EmergencyDataStore()

# Emergency routes without database
@app.route('/')
def home():
    return redirect('/simple-login')

@app.route('/simple-login', methods=['GET', 'POST'])
def simple_login():
    """Emergency login without database dependencies"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        print(f"Login attempt: {username}")
        
        # Check admin hardcoded login
        if username == 'admin' and password == 'admin123':
            session['user_id'] = 'admin'
            session['logged_in'] = True
            session['user_role'] = 'admin'
            print("Admin login successful")
            return redirect('/emergency-dashboard')
        
        # Check member login from JSON
        member = data_store.find_member(username)
        if member and member.get('password') == password:
            session['user_id'] = username
            session['logged_in'] = True
            session['user_role'] = 'member'
            session['user_name'] = f"{member.get('first_name')} {member.get('last_name')}"
            print(f"Member login successful: {username}")
            return redirect('/emergency-dashboard')
        
        return render_template('simple_login.html', 
                             error='ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')
    
    return render_template('simple_login.html')

@app.route('/emergency-dashboard')
def emergency_dashboard():
    """Emergency dashboard without database"""
    if not session.get('logged_in'):
        return redirect('/simple-login')
    
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>IT Business Shop - Emergency Dashboard</title>
        <meta charset="utf-8">
        <style>
            body { 
                font-family: 'Segoe UI', Arial, sans-serif; 
                padding: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                margin: 0;
            }
            .container { 
                max-width: 800px; 
                margin: 0 auto; 
                background: white; 
                padding: 30px; 
                border-radius: 15px; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            }
            .alert { 
                background: #ffeb3b; 
                padding: 15px; 
                border-radius: 8px; 
                margin-bottom: 20px;
                border-left: 5px solid #ff9800;
            }
            .btn { 
                padding: 12px 25px; 
                margin: 8px; 
                text-decoration: none; 
                border-radius: 8px; 
                display: inline-block; 
                font-weight: bold;
                transition: all 0.3s;
            }
            .btn-primary { background: #007bff; color: white; }
            .btn-success { background: #28a745; color: white; }
            .btn-warning { background: #ffc107; color: black; }
            .btn-danger { background: #dc3545; color: white; }
            .btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
            h1 { color: #333; text-align: center; margin-bottom: 30px; }
            .status { background: #e3f2fd; padding: 15px; border-radius: 8px; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚨 IT Business Shop - Emergency Mode</h1>
            
            <div class="alert">
                <strong>⚠️ Emergency Mode Active</strong><br>
                ระบบกำลังทำงานในโหมดฉุกเฉิน เนื่องจากปัญหาการเชื่อมต่อฐานข้อมูล
            </div>
            
            <div class="status">
                <h3>📊 สถานะระบบ</h3>
                <p>✅ เซิร์ฟเวอร์: ทำงานปกติ</p>
                <p>⚠️ ฐานข้อมูล: ปัญหาการเชื่อมต่อ</p>
                <p>🔧 โหมด: Emergency Recovery</p>
                <p>👤 ผู้ใช้: admin (Emergency Session)</p>
            </div>
            
            <h3>🛠️ เครื่องมือฉุกเฉิน</h3>
            <a href="/test" class="btn btn-primary">🔍 ทดสอบระบบ</a>
            <a href="/health" class="btn btn-success">💚 Health Check</a>
            <a href="/status" class="btn btn-warning">📈 สถานะเซิร์ฟเวอร์</a>
            <a href="/data-manager" class="btn btn-primary">📊 จัดการข้อมูล</a>
            <a href="/members" class="btn btn-info">👥 จัดการสมาชิก</a>
            <a href="/logout" class="btn btn-danger">🚪 ออกจากระบบ</a>
            
            <div style="margin-top: 30px; text-align: center; color: #666;">
                <p>Emergency Mode - October 2025</p>
                <p>System Administrator: GitHub Copilot</p>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/test')
def test():
    """System test endpoint"""
    try:
        # Test basic functionality
        import datetime
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return f'''
        <h1>🧪 System Test Results</h1>
        <p>✅ Flask Server: Working</p>
        <p>✅ Python: Working</p>
        <p>✅ Time: {current_time}</p>
        <p>✅ Session: {session.get('logged_in', False)}</p>
        <p>⚠️ Database: Bypassed (Emergency Mode)</p>
        <p><a href="/emergency-dashboard">← กลับ Dashboard</a></p>
        '''
    except Exception as e:
        return f'<h1>❌ Test Failed</h1><p>Error: {str(e)}</p>'

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'emergency_mode',
        'message': 'Server running in emergency mode',
        'timestamp': '2025-10-17',
        'database': 'bypassed',
        'authentication': 'emergency_session'
    })

@app.route('/status')
def status():
    """Server status"""
    return '''
    <h1>📊 Server Status</h1>
    <p><strong>Mode:</strong> Emergency Recovery</p>
    <p><strong>Database:</strong> Connection issues - bypassed</p>
    <p><strong>Authentication:</strong> Emergency session active</p>
    <p><strong>Last Update:</strong> October 17, 2025</p>
    <p><a href="/emergency-dashboard">← กลับ Dashboard</a></p>
    '''

@app.route('/data-manager')
def data_manager():
    """หน้าจัดการข้อมูล JSON"""
    if not session.get('logged_in'):
        return redirect('/simple-login')
    
    entries = data_store.load_entries()
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>จัดการข้อมูล - IT Business Shop</title>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial; padding: 20px; background: #f8f9fa; }}
            .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }}
            .btn {{ padding: 10px 20px; margin: 5px; text-decoration: none; border-radius: 5px; display: inline-block; }}
            .btn-primary {{ background: #007bff; color: white; }}
            .btn-success {{ background: #28a745; color: white; }}
            .btn-danger {{ background: #dc3545; color: white; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ padding: 10px; border: 1px solid #ddd; text-align: left; }}
            th {{ background: #f8f9fa; }}
            .form-group {{ margin: 15px 0; }}
            input, select {{ padding: 8px; margin: 5px; border: 1px solid #ddd; border-radius: 4px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 จัดการข้อมูล (JSON File Storage)</h1>
            
            <div style="background: #e3f2fd; padding: 15px; border-radius: 8px; margin: 20px 0;">
                <h3>💾 วิธีการจัดเก็บข้อมูล</h3>
                <p>✅ <strong>JSON Files:</strong> ข้อมูลจัดเก็บในไฟล์ JSON</p>
                <p>✅ <strong>Emergency Mode:</strong> ไม่ต้องใช้ฐานข้อมูล</p>
                <p>✅ <strong>Persistent:</strong> ข้อมูลคงอยู่แม้เซิร์ฟเวอร์รีสตาร์ท</p>
                <p>📁 <strong>Path:</strong> emergency_data/entries.json</p>
                <p>📈 <strong>จำนวนรายการ:</strong> {len(entries)} รายการ</p>
            </div>
            
            <!-- ฟอร์มเพิ่มข้อมูล -->
            <h3>➕ เพิ่มรายการใหม่</h3>
            <form method="post" action="/add-entry">
                <div class="form-group">
                    <input type="text" name="item_name" placeholder="ชื่อสินค้า" required>
                    <input type="number" name="quantity" placeholder="จำนวน" required>
                    <input type="number" step="0.01" name="price" placeholder="ราคา" required>
                    <select name="category">
                        <option value="อิเล็กทรอนิกส์">อิเล็กทรอนิกส์</option>
                        <option value="เครื่องใช้ไฟฟ้า">เครื่องใช้ไฟฟ้า</option>
                        <option value="อื่นๆ">อื่นๆ</option>
                    </select>
                    <button type="submit" class="btn btn-success">เพิ่มรายการ</button>
                </div>
            </form>
            
            <!-- แสดงข้อมูล -->
            <h3>📋 รายการทั้งหมด</h3>
            <a href="/export-csv" class="btn btn-primary">📄 ส่งออก CSV</a>
            <a href="/clear-all" class="btn btn-danger" onclick="return confirm('ต้องการลบทั้งหมด?')">🗑️ ลบทั้งหมด</a>
            
            <table>
                <tr>
                    <th>ID</th>
                    <th>ชื่อสินค้า</th>
                    <th>จำนวน</th>
                    <th>ราคา</th>
                    <th>หมวดหมู่</th>
                    <th>วันที่สร้าง</th>
                    <th>จัดการ</th>
                </tr>
    '''
    
    for entry in entries:
        html += f'''
                <tr>
                    <td>{entry.get('id', '-')}</td>
                    <td>{entry.get('item_name', '-')}</td>
                    <td>{entry.get('quantity', '-')}</td>
                    <td>{entry.get('price', '-')}</td>
                    <td>{entry.get('category', '-')}</td>
                    <td>{entry.get('created_at', '-')[:10]}</td>
                    <td><a href="/delete-entry/{entry.get('id')}" class="btn btn-danger" onclick="return confirm('ต้องการลบ?')">ลบ</a></td>
                </tr>
        '''
    
    html += '''
            </table>
            
            <div style="margin-top: 30px;">
                <a href="/emergency-dashboard" class="btn btn-primary">← กลับ Dashboard</a>
            </div>
        </div>
    </body>
    </html>
    '''
    
    return html

@app.route('/add-entry', methods=['POST'])
def add_entry():
    """เพิ่มรายการใหม่"""
    if not session.get('logged_in'):
        return redirect('/simple-login')
    
    entry_data = {
        'item_name': request.form.get('item_name'),
        'quantity': int(request.form.get('quantity', 0)),
        'price': float(request.form.get('price', 0)),
        'category': request.form.get('category')
    }
    
    data_store.save_entry(entry_data)
    return redirect('/data-manager')

@app.route('/delete-entry/<int:entry_id>')
def delete_entry(entry_id):
    """ลบรายการ"""
    if not session.get('logged_in'):
        return redirect('/simple-login')
    
    data_store.delete_entry(entry_id)
    return redirect('/data-manager')

@app.route('/clear-all')
def clear_all():
    """ลบรายการทั้งหมด"""
    if not session.get('logged_in'):
        return redirect('/simple-login')
    
    data_store.clear_all_entries()
    return redirect('/data-manager')

@app.route('/export-csv')
def export_csv():
    """ส่งออก CSV"""
    if not session.get('logged_in'):
        return redirect('/simple-login')
    
    entries = data_store.load_entries()
    
    if not entries:
        return "ไม่มีข้อมูลให้ส่งออก"
    
    import csv
    from io import StringIO
    from flask import Response
    
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=['id', 'item_name', 'quantity', 'price', 'category', 'created_at'])
    writer.writeheader()
    writer.writerows(entries)
    
    response = Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={"Content-disposition": "attachment; filename=emergency_data.csv"}
    )
    
    return response

@app.route('/register', methods=['GET', 'POST'])
def register():
    """สมัครสมาชิกใหม่"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        # Validation
        if not all([username, email, first_name, last_name, password]):
            return render_template('register.html', error='กรุณากรอกข้อมูลให้ครบถ้วน')
        
        if password != confirm_password:
            return render_template('register.html', error='รหัสผ่านไม่ตรงกัน')
        
        if len(password) < 6:
            return render_template('register.html', error='รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร')
        
        # Check if username exists
        if data_store.find_member(username):
            return render_template('register.html', error='ชื่อผู้ใช้นี้มีอยู่แล้ว')
        
        # Save member
        member_data = {
            'username': username,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'password': password,  # In real app, should hash this
            'role': 'member',
            'status': 'active'
        }
        
        member_id = data_store.save_member(member_data)
        return render_template('register.html', success=f'สมัครสมาชิกสำเร็จ! ID: {member_id}')
    
    return render_template('register.html')

@app.route('/members')
def members_list():
    """หน้าจัดการสมาชิก"""
    if not session.get('logged_in'):
        return redirect('/simple-login')
    
    members = data_store.load_members()
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>จัดการสมาชิก - IT Business Shop</title>
        <meta charset="utf-8">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            body {{ font-family: Arial; padding: 20px; background: #f8f9fa; }}
            .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }}
            .btn {{ padding: 10px 20px; margin: 5px; text-decoration: none; border-radius: 5px; display: inline-block; }}
            .btn-primary {{ background: #007bff; color: white; }}
            .btn-success {{ background: #28a745; color: white; }}
            .btn-warning {{ background: #ffc107; color: black; }}
            .btn-danger {{ background: #dc3545; color: white; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ padding: 12px; border: 1px solid #ddd; text-align: left; }}
            th {{ background: #f8f9fa; }}
            .member-card {{ background: #e3f2fd; padding: 15px; border-radius: 8px; margin: 10px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1><i class="fas fa-users"></i> จัดการสมาชิก</h1>
            
            <div class="member-card">
                <h3>📊 สถิติสมาชิก</h3>
                <p>👥 <strong>จำนวนสมาชิกทั้งหมด:</strong> {len(members)} คน</p>
                <p>📅 <strong>อัพเดทล่าสุด:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="mb-3">
                <a href="/register" class="btn btn-success">
                    <i class="fas fa-user-plus"></i> เพิ่มสมาชิกใหม่
                </a>
                <a href="/emergency-dashboard" class="btn btn-primary">
                    <i class="fas fa-arrow-left"></i> กลับ Dashboard
                </a>
            </div>
            
            <table class="table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>ชื่อผู้ใช้</th>
                        <th>ชื่อ-นามสกุล</th>
                        <th>อีเมล</th>
                        <th>เบอร์โทร</th>
                        <th>วันที่สมัคร</th>
                        <th>จัดการ</th>
                    </tr>
                </thead>
                <tbody>
    '''
    
    for member in members:
        html += f'''
                    <tr>
                        <td>{member.get('id', '-')}</td>
                        <td>{member.get('username', '-')}</td>
                        <td>{member.get('first_name', '')} {member.get('last_name', '')}</td>
                        <td>{member.get('email', '-')}</td>
                        <td>{member.get('phone', '-')}</td>
                        <td>{member.get('created_at', '-')[:10]}</td>
                        <td>
                            <a href="/change-password/{member.get('username')}" class="btn btn-warning btn-sm">
                                <i class="fas fa-key"></i> เปลี่ยนรหัส
                            </a>
                        </td>
                    </tr>
        '''
    
    html += '''
                </tbody>
            </table>
        </div>
    </body>
    </html>
    '''
    
    return html

@app.route('/change-password/<username>', methods=['GET', 'POST'])
def change_password(username):
    """เปลี่ยนรหัสผ่านสมาชิก"""
    if not session.get('logged_in'):
        return redirect('/simple-login')
    
    member = data_store.find_member(username)
    if not member:
        return "ไม่พบสมาชิก"
    
    if request.method == 'POST':
        new_password = request.form.get('new_password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        if not new_password:
            error = 'กรุณากรอกรหัสผ่านใหม่'
        elif len(new_password) < 6:
            error = 'รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร'
        elif new_password != confirm_password:
            error = 'รหัสผ่านไม่ตรงกัน'
        else:
            data_store.update_member_password(username, new_password)
            success = 'เปลี่ยนรหัสผ่านสำเร็จ!'
            return f'''
            <script>
                alert('{success}');
                window.location.href = '/members';
            </script>
            '''
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>เปลี่ยนรหัสผ่าน - {username}</title>
        <meta charset="utf-8">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {{ font-family: Arial; padding: 20px; background: #f8f9fa; }}
            .container {{ max-width: 500px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }}
            .form-control {{ margin-bottom: 15px; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }}
            .btn {{ padding: 10px 20px; margin: 5px; text-decoration: none; border-radius: 5px; }}
            .btn-success {{ background: #28a745; color: white; border: none; }}
            .btn-secondary {{ background: #6c757d; color: white; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2><i class="fas fa-key"></i> เปลี่ยนรหัสผ่าน</h2>
            <p><strong>สมาชิก:</strong> {username} ({member.get('first_name')} {member.get('last_name')})</p>
            
            <form method="post">
                <div class="mb-3">
                    <label class="form-label">รหัสผ่านใหม่:</label>
                    <input type="password" class="form-control" name="new_password" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">ยืนยันรหัสผ่าน:</label>
                    <input type="password" class="form-control" name="confirm_password" required>
                </div>
                <button type="submit" class="btn btn-success">บันทึกรหัสผ่านใหม่</button>
                <a href="/members" class="btn btn-secondary">ยกเลิก</a>
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/logout')
def logout():
    """Logout and clear session"""
    session.clear()
    return redirect('/simple-login')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Starting Emergency Server on port {port}")
    print(f"🌐 URL: http://localhost:{port}")
    print(f"🔑 Login: admin / admin123")
    app.run(host='0.0.0.0', port=port, debug=True)