from flask import Flask
import os

app = Flask(__name__)
app.secret_key = 'emergency-key-2025'

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>IT Business Shop - Emergency</title>
        <style>
            body { font-family: Arial; padding: 20px; background: #f8f9fa; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
            .btn { padding: 10px 20px; margin: 5px; text-decoration: none; border-radius: 5px; display: inline-block; }
            .btn-success { background: #28a745; color: white; }
            .btn-primary { background: #007bff; color: white; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏪 IT Business Shop</h1>
            <h2>🚨 Emergency Mode Active</h2>
            
            <div style="background: #d4edda; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <h3>✅ System Status:</h3>
                <ul>
                    <li>Emergency server: Online</li>
                    <li>Basic functions: Available</li>
                    <li>Database: Bypassed</li>
                </ul>
            </div>
            
            <div style="background: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <h3>⚠️ Issues Detected:</h3>
                <ul>
                    <li>Database connection pool timeout</li>
                    <li>Main application not responding</li>
                    <li>Connection limit exceeded</li>
                </ul>
            </div>
            
            <div>
                <a href="/health" class="btn btn-success">Health Check</a>
                <a href="/simple" class="btn btn-primary">Simple Dashboard</a>
            </div>
            
            <div style="margin-top: 30px; padding: 15px; background: #e9ecef; border-radius: 5px;">
                <h4>🔧 Recovery Actions Taken:</h4>
                <ol>
                    <li>Reduced database pool size to 2</li>
                    <li>Added connection timeout limits</li>
                    <li>Enabled emergency mode</li>
                    <li>Created simplified entry points</li>
                </ol>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    return {
        'status': 'emergency_mode',
        'timestamp': '2025-10-17',
        'mode': 'simplified',
        'database': 'bypassed'
    }

@app.route('/simple')
def simple():
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>Simple Dashboard</title></head>
    <body style="font-family: Arial; padding: 20px;">
        <h1>🏪 Simple Dashboard</h1>
        <p>Emergency mode - basic functions only</p>
        
        <div style="margin: 20px 0;">
            <button onclick="alert('Feature temporarily disabled')" style="padding: 10px; margin: 5px;">Add Entry</button>
            <button onclick="alert('Feature temporarily disabled')" style="padding: 10px; margin: 5px;">View Entries</button>
            <button onclick="alert('Feature temporarily disabled')" style="padding: 10px; margin: 5px;">Export Data</button>
        </div>
        
        <div style="background: #f8f9fa; padding: 15px; border-radius: 5px;">
            <h3>System Status:</h3>
            <p>✅ Emergency server running</p>
            <p>🔄 Main system recovery in progress</p>
            <p>📞 Contact admin for full functionality</p>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)