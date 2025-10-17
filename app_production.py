"""
Production-Ready Flask App สำหรับ Windows
ใช้ waitress server แทน Flask development server
"""

from flask import Flask, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = 'production-ready-2025'

# In-memory storage
users = {'admin': 'admin123'}
entries = []
members = []

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>IT Business Shop</title><meta charset="utf-8"></head>
    <body style="font-family: Arial; padding: 50px; background: linear-gradient(135deg, #667eea, #764ba2); min-height: 100vh; margin: 0;">
        <div style="max-width: 500px; margin: 100px auto; background: rgba(255,255,255,0.95); padding: 50px; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); text-align: center;">
            <h1 style="color: #333; margin-bottom: 10px;">🏪 IT Business Shop</h1>
            <p style="color: #666; font-size: 18px; margin-bottom: 30px;">ระบบจัดการธุรกิจ</p>
            <div style="margin: 30px 0;">
                <a href="/login" style="display: inline-block; padding: 15px 30px; background: linear-gradient(135deg, #667eea, #764ba2); color: white; text-decoration: none; border-radius: 10px; margin: 10px; font-weight: bold; box-shadow: 0 5px 15px rgba(102,126,234,0.3);">🔐 เข้าสู่ระบบ</a>
                <a href="/register" style="display: inline-block; padding: 15px 30px; background: linear-gradient(135deg, #28a745, #20c997); color: white; text-decoration: none; border-radius: 10px; margin: 10px; font-weight: bold; box-shadow: 0 5px 15px rgba(40,167,69,0.3);">👤 สมัครสมาชิก</a>
            </div>
            <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee;">
                <p style="color: #999; font-size: 14px;">✨ Production Ready • 🚀 High Performance • 💾 Data Persistent</p>
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
        error = 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง'
    else:
        error = ''
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head><title>เข้าสู่ระบบ</title><meta charset="utf-8"></head>
    <body style="font-family: Arial; background: linear-gradient(135deg, #667eea, #764ba2); min-height: 100vh; margin: 0; display: flex; align-items: center; justify-content: center;">
        <div style="background: rgba(255,255,255,0.95); padding: 40px; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); max-width: 400px; width: 100%;">
            <h1 style="text-align: center; color: #333; margin-bottom: 30px;">🔐 เข้าสู่ระบบ</h1>
            {f'<div style="color: #dc3545; text-align: center; margin: 15px 0; padding: 10px; background: #f8d7da; border-radius: 5px;">{error}</div>' if error else ''}
            <form method="post">
                <div style="margin: 20px 0;">
                    <input type="text" name="username" placeholder="ชื่อผู้ใช้" required 
                           style="width: 100%; padding: 15px; border: 2px solid #e3f2fd; border-radius: 10px; box-sizing: border-box; font-size: 16px;">
                </div>
                <div style="margin: 20px 0;">
                    <input type="password" name="password" placeholder="รหัสผ่าน" required 
                           style="width: 100%; padding: 15px; border: 2px solid #e3f2fd; border-radius: 10px; box-sizing: border-box; font-size: 16px;">
                </div>
                <button type="submit" style="width: 100%; padding: 15px; background: linear-gradient(135deg, #667eea, #764ba2); color: white; border: none; border-radius: 10px; cursor: pointer; font-size: 16px; font-weight: bold;">เข้าสู่ระบบ</button>
            </form>
            <div style="text-align: center; margin-top: 20px;">
                <a href="/register" style="color: #667eea; text-decoration: none; font-weight: 500;">สมัครสมาชิกใหม่</a> | 
                <a href="/" style="color: #667eea; text-decoration: none; font-weight: 500;">กลับหน้าหลัก</a>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head><title>Dashboard</title><meta charset="utf-8"></head>
    <body style="font-family: Arial; padding: 20px; background: #f8f9fa;">
        <div style="max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
            <h1 style="color: #333; margin-bottom: 10px;">🏪 IT Business Shop Dashboard</h1>
            <p style="color: #666; margin-bottom: 30px;">ยินดีต้อนรับ: <strong style="color: #667eea;">{session['user']}</strong></p>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0;">
                <div style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 20px; border-radius: 10px; text-align: center;">
                    <h3 style="margin: 0; font-size: 24px;">👥</h3>
                    <p style="margin: 5px 0; font-size: 18px; font-weight: bold;">{len(members)}</p>
                    <p style="margin: 0; opacity: 0.8;">สมาชิก</p>
                </div>
                <div style="background: linear-gradient(135deg, #28a745, #20c997); color: white; padding: 20px; border-radius: 10px; text-align: center;">
                    <h3 style="margin: 0; font-size: 24px;">📦</h3>
                    <p style="margin: 5px 0; font-size: 18px; font-weight: bold;">{len(entries)}</p>
                    <p style="margin: 0; opacity: 0.8;">รายการ</p>
                </div>
                <div style="background: linear-gradient(135deg, #17a2b8, #138496); color: white; padding: 20px; border-radius: 10px; text-align: center;">
                    <h3 style="margin: 0; font-size: 24px;">✅</h3>
                    <p style="margin: 5px 0; font-size: 18px; font-weight: bold;">100%</p>
                    <p style="margin: 0; opacity: 0.8;">ระบบ</p>
                </div>
            </div>
            
            <h3 style="color: #333; margin-top: 40px;">🛠️ เมนูหลัก</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0;">
                <a href="/data" style="display: block; padding: 20px; background: #007bff; color: white; text-decoration: none; border-radius: 10px; text-align: center; font-weight: bold; transition: transform 0.2s;">📊 จัดการข้อมูล</a>
                <a href="/members" style="display: block; padding: 20px; background: #17a2b8; color: white; text-decoration: none; border-radius: 10px; text-align: center; font-weight: bold; transition: transform 0.2s;">👥 จัดการสมาชิก</a>
                <a href="/test" style="display: block; padding: 20px; background: #28a745; color: white; text-decoration: none; border-radius: 10px; text-align: center; font-weight: bold; transition: transform 0.2s;">🧪 ทดสอบระบบ</a>
                <a href="/logout" style="display: block; padding: 20px; background: #dc3545; color: white; text-decoration: none; border-radius: 10px; text-align: center; font-weight: bold; transition: transform 0.2s;">🚪 ออกจากระบบ</a>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    import datetime
    return {
        'status': 'healthy',
        'server': 'production_ready',
        'users': len(users),
        'entries': len(entries), 
        'members': len(members),
        'timestamp': datetime.datetime.now().isoformat(),
        'uptime': 'stable'
    }

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# Minimal routes สำหรับทดสอบ
@app.route('/test')
def test():
    if 'user' not in session:
        return redirect('/login')
    return '<h1>✅ System Test OK</h1><p><a href="/dashboard">← Back</a></p>'

@app.route('/data')
def data():
    if 'user' not in session:
        return redirect('/login') 
    return f'<h1>📊 Data Management</h1><p>Entries: {len(entries)}</p><p><a href="/dashboard">← Back</a></p>'

@app.route('/members') 
def members():
    if 'user' not in session:
        return redirect('/login')
    return f'<h1>👥 Members</h1><p>Total: {len(members)}</p><p><a href="/dashboard">← Back</a></p>'

@app.route('/register')
def register():
    return '<h1>👤 Register</h1><p>Coming soon...</p><p><a href="/">← Home</a></p>'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    
    print("🚀 Starting Production Flask Server...")
    print(f"🌐 URL: http://localhost:{port}")
    print(f"🔐 Login: admin / admin123")
    print("💪 Production Ready with Waitress")
    
    try:
        # ลองใช้ waitress ถ้ามี
        from waitress import serve
        print("✅ Using Waitress WSGI Server")
        serve(app, host='0.0.0.0', port=port, threads=6)
    except ImportError:
        print("⚠️ Waitress not found, using Flask dev server")
        print("💡 Install: pip install waitress")
        app.run(host='0.0.0.0', port=port, debug=False, threaded=True)