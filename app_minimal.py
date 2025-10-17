"""
Ultra Minimal Flask App - จุดประสงค์: ทำงานได้ไม่หยุด
"""

from flask import Flask, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = 'minimal-2025'

# In-memory storage (simple and reliable)
users = {
    'admin': 'admin123'
}
entries = []
members = []

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>IT Business Shop</title><meta charset="utf-8"></head>
    <body style="font-family: Arial; padding: 50px; background: #f0f0f0;">
        <div style="max-width: 400px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px;">
            <h1 style="text-align: center; color: #333;">🏪 IT Business Shop</h1>
            <p style="text-align: center; color: #666;">ระบบจัดการธุรกิจ - Minimal Version</p>
            <div style="text-align: center; margin: 20px 0;">
                <a href="/login" style="display: inline-block; padding: 12px 24px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; margin: 5px;">เข้าสู่ระบบ</a>
                <a href="/register" style="display: inline-block; padding: 12px 24px; background: #28a745; color: white; text-decoration: none; border-radius: 5px; margin: 5px;">สมัครสมาชิก</a>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        if username in users and users[username] == password:
            session['user'] = username
            return redirect('/dashboard')
        else:
            error_msg = '<div style="color: red; text-align: center; margin: 10px;">ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง</div>'
    else:
        error_msg = ''
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head><title>เข้าสู่ระบบ</title><meta charset="utf-8"></head>
    <body style="font-family: Arial; padding: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; margin: 0;">
        <div style="max-width: 400px; margin: 100px auto; background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
            <h1 style="text-align: center; color: #333; margin-bottom: 30px;">🔐 เข้าสู่ระบบ</h1>
            {error_msg}
            <form method="post">
                <div style="margin: 15px 0;">
                    <input type="text" name="username" placeholder="ชื่อผู้ใช้" required 
                           style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box;">
                </div>
                <div style="margin: 15px 0;">
                    <input type="password" name="password" placeholder="รหัสผ่าน" required 
                           style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box;">
                </div>
                <button type="submit" style="width: 100%; padding: 12px; background: #667eea; color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 16px;">เข้าสู่ระบบ</button>
            </form>
            <div style="text-align: center; margin-top: 20px;">
                <a href="/register" style="color: #667eea; text-decoration: none;">สมัครสมาชิกใหม่</a> | 
                <a href="/" style="color: #667eea; text-decoration: none;">กลับหน้าหลัก</a>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/register', methods=['GET', 'POST'])
def register():
    global users, members
    
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        name = request.form.get('name', '')
        
        if username and password and name:
            if username in users:
                msg = '<div style="color: red; text-align: center; margin: 10px;">ชื่อผู้ใช้นี้มีอยู่แล้ว</div>'
            else:
                users[username] = password
                members.append({'username': username, 'name': name, 'id': len(members) + 1})
                msg = '<div style="color: green; text-align: center; margin: 10px;">สมัครสมาชิกสำเร็จ! <a href="/login">เข้าสู่ระบบ</a></div>'
        else:
            msg = '<div style="color: red; text-align: center; margin: 10px;">กรุณากรอกข้อมูลให้ครบถ้วน</div>'
    else:
        msg = ''
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head><title>สมัครสมาชิก</title><meta charset="utf-8"></head>
    <body style="font-family: Arial; padding: 50px; background: linear-gradient(135deg, #28a745 0%, #20c997 100%); min-height: 100vh; margin: 0;">
        <div style="max-width: 400px; margin: 100px auto; background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
            <h1 style="text-align: center; color: #333; margin-bottom: 30px;">👤 สมัครสมาชิก</h1>
            {msg}
            <form method="post">
                <div style="margin: 15px 0;">
                    <input type="text" name="name" placeholder="ชื่อ-นามสกุล" required 
                           style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box;">
                </div>
                <div style="margin: 15px 0;">
                    <input type="text" name="username" placeholder="ชื่อผู้ใช้" required 
                           style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box;">
                </div>
                <div style="margin: 15px 0;">
                    <input type="password" name="password" placeholder="รหัสผ่าน" required 
                           style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box;">
                </div>
                <button type="submit" style="width: 100%; padding: 12px; background: #28a745; color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 16px;">สมัครสมาชิก</button>
            </form>
            <div style="text-align: center; margin-top: 20px;">
                <a href="/login" style="color: #28a745; text-decoration: none;">มีบัญชีแล้ว? เข้าสู่ระบบ</a>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    
    user = session['user']
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head><title>Dashboard</title><meta charset="utf-8"></head>
    <body style="font-family: Arial; padding: 20px; background: #f8f9fa;">
        <div style="max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px;">
            <h1 style="color: #333;">🏪 Dashboard - IT Business Shop</h1>
            <p>ยินดีต้อนรับ: <strong>{user}</strong></p>
            
            <div style="background: #e3f2fd; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3>📊 สถิติ</h3>
                <p>👥 จำนวนสมาชิก: {len(members)} คน</p>
                <p>📦 จำนวนรายการ: {len(entries)} รายการ</p>
                <p>✅ ระบบทำงานปกติ</p>
            </div>
            
            <h3>🛠️ เมนู</h3>
            <div style="margin: 20px 0;">
                <a href="/data" style="display: inline-block; padding: 12px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; margin: 5px;">📊 จัดการข้อมูล</a>
                <a href="/members" style="display: inline-block; padding: 12px 20px; background: #17a2b8; color: white; text-decoration: none; border-radius: 5px; margin: 5px;">👥 จัดการสมาชิก</a>
                <a href="/test" style="display: inline-block; padding: 12px 20px; background: #28a745; color: white; text-decoration: none; border-radius: 5px; margin: 5px;">🧪 ทดสอบ</a>
                <a href="/logout" style="display: inline-block; padding: 12px 20px; background: #dc3545; color: white; text-decoration: none; border-radius: 5px; margin: 5px;">🚪 ออกจากระบบ</a>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/data', methods=['GET', 'POST'])
def data():
    if 'user' not in session:
        return redirect('/login')
    
    global entries
    
    if request.method == 'POST':
        item = request.form.get('item', '')
        quantity = request.form.get('quantity', '')
        price = request.form.get('price', '')
        
        if item and quantity and price:
            entries.append({
                'id': len(entries) + 1,
                'item': item,
                'quantity': int(quantity),
                'price': float(price)
            })
    
    entries_html = ""
    for entry in entries:
        entries_html += f'''
        <tr>
            <td>{entry['id']}</td>
            <td>{entry['item']}</td>
            <td>{entry['quantity']}</td>
            <td>{entry['price']}</td>
        </tr>
        '''
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head><title>จัดการข้อมูล</title><meta charset="utf-8"></head>
    <body style="font-family: Arial; padding: 20px; background: #f8f9fa;">
        <div style="max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px;">
            <h1 style="color: #333;">📊 จัดการข้อมูล</h1>
            
            <h3>➕ เพิ่มรายการใหม่</h3>
            <form method="post" style="margin: 20px 0;">
                <input type="text" name="item" placeholder="ชื่อสินค้า" required style="padding: 8px; margin: 5px; border: 1px solid #ddd; border-radius: 4px;">
                <input type="number" name="quantity" placeholder="จำนวน" required style="padding: 8px; margin: 5px; border: 1px solid #ddd; border-radius: 4px;">
                <input type="number" step="0.01" name="price" placeholder="ราคา" required style="padding: 8px; margin: 5px; border: 1px solid #ddd; border-radius: 4px;">
                <button type="submit" style="padding: 8px 16px; background: #007bff; color: white; border: none; border-radius: 4px;">เพิ่ม</button>
            </form>
            
            <h3>📋 รายการทั้งหมด ({len(entries)} รายการ)</h3>
            <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                <tr style="background: #f8f9fa;">
                    <th style="padding: 10px; border: 1px solid #ddd;">ID</th>
                    <th style="padding: 10px; border: 1px solid #ddd;">ชื่อสินค้า</th>
                    <th style="padding: 10px; border: 1px solid #ddd;">จำนวน</th>
                    <th style="padding: 10px; border: 1px solid #ddd;">ราคา</th>
                </tr>
                {entries_html}
            </table>
            
            <div style="margin-top: 20px;">
                <a href="/dashboard" style="padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px;">← กลับ Dashboard</a>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/members')
def members_list():
    if 'user' not in session:
        return redirect('/login')
    
    members_html = ""
    for member in members:
        members_html += f'''
        <tr>
            <td>{member['id']}</td>
            <td>{member['username']}</td>
            <td>{member['name']}</td>
        </tr>
        '''
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head><title>จัดการสมาชิก</title><meta charset="utf-8"></head>
    <body style="font-family: Arial; padding: 20px; background: #f8f9fa;">
        <div style="max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px;">
            <h1 style="color: #333;">👥 จัดการสมาชิก</h1>
            
            <div style="background: #e3f2fd; padding: 15px; border-radius: 8px; margin: 20px 0;">
                <h3>📊 สถิติ</h3>
                <p>จำนวนสมาชิกทั้งหมด: {len(members)} คน</p>
            </div>
            
            <h3>📋 รายชื่อสมาชิก</h3>
            <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                <tr style="background: #f8f9fa;">
                    <th style="padding: 10px; border: 1px solid #ddd;">ID</th>
                    <th style="padding: 10px; border: 1px solid #ddd;">ชื่อผู้ใช้</th>
                    <th style="padding: 10px; border: 1px solid #ddd;">ชื่อ-นามสกุล</th>
                </tr>
                {members_html}
            </table>
            
            <div style="margin-top: 20px;">
                <a href="/register" style="padding: 10px 20px; background: #28a745; color: white; text-decoration: none; border-radius: 5px;">➕ เพิ่มสมาชิก</a>
                <a href="/dashboard" style="padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px;">← กลับ Dashboard</a>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/test')
def test():
    if 'user' not in session:
        return redirect('/login')
    
    import datetime
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head><title>ทดสอบระบบ</title><meta charset="utf-8"></head>
    <body style="font-family: Arial; padding: 20px; background: #f8f9fa;">
        <div style="max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px;">
            <h1 style="color: #333;">🧪 ทดสอบระบบ</h1>
            
            <div style="background: #d4edda; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3>✅ ผลการทดสอบ</h3>
                <p>🚀 Flask Server: ทำงานปกติ</p>
                <p>🐍 Python: ทำงานปกติ</p>
                <p>🕐 เวลาปัจจุบัน: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p>👤 ผู้ใช้งาน: {session.get('user')}</p>
                <p>💾 จำนวนข้อมูล: {len(entries)} รายการ</p>
                <p>👥 จำนวนสมาชิก: {len(members)} คน</p>
                <p>🔑 Session: Active</p>
            </div>
            
            <div style="margin-top: 20px;">
                <a href="/dashboard" style="padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px;">← กลับ Dashboard</a>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    return {
        'status': 'ok',
        'users': len(users),
        'entries': len(entries),
        'members': len(members),
        'timestamp': str(__import__('datetime').datetime.now())
    }

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5003))
    print(f"🚀 Minimal Flask Server Starting on port {port}")
    print(f"🌐 URL: http://localhost:{port}")
    print(f"🔐 Default Login: admin / admin123")
    print(f"💡 Ultra stable - no templates, no external deps")
    
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
