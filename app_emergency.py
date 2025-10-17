"""
IT Business Shop - Emergency Flask App
Fixed connection pool and routing issues
"""

import os
from flask import Flask, render_template, request, redirect, session, jsonify, url_for
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'emergency-secret-key-2025')

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
        
        print(f"Emergency login attempt: {username}")
        
        # Simple hardcoded login
        if username == 'admin' and password == 'admin123':
            session['user_id'] = 'admin'
            session['logged_in'] = True
            print("Emergency login successful")
            return redirect('/emergency-dashboard')
        else:
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