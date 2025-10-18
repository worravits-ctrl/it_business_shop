import os
from flask import Flask, render_template, redirect, url_for, flash, request, send_file, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime, date
import io, csv
import pandas as pd

from models import Base, User, Entry
from forms import LoginForm, EntryForm, INCOME_CHOICES, EXPENSE_CHOICES

# Database setup  
# For Railway deployment, use persistent volume or PostgreSQL
DB_URL = os.environ.get('DATABASE_URL')
if DB_URL:
    # Production: Use PostgreSQL on Railway
    engine = create_engine(DB_URL, connect_args={})
else:
    # Development: Use SQLite
    DB_PATH = os.path.join(os.path.dirname(__file__), 'business.db')
    engine = create_engine(f'sqlite:///{DB_PATH}', connect_args={"check_same_thread": False})

Session = scoped_session(sessionmaker(bind=engine))

# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['WTF_CSRF_ENABLED'] = False  # ปิด CSRF ชั่วคราวเพื่อทดสอบ

# Flask-Login setup
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# User wrapper class for Flask-Login
class FlaskUser:
    def __init__(self, user):
        self._u = user
    def get_id(self):
        return str(self._u.id)
    @property
    def is_authenticated(self):
        return True
    @property
    def is_active(self):
        return self._u.is_active
    @property
    def is_anonymous(self):
        return False
    @property
    def username(self):
        return self._u.username
    @property
    def email(self):
        return self._u.email
    @property
    def role(self):
        return self._u.role

@login_manager.user_loader
def load_user(user_id):
    try:
        s = Session()
        user = s.query(User).get(int(user_id))
        if user:
            return FlaskUser(user)
        return None
    except Exception as e:
        print(f"Error loading user: {e}")
        return None

@app.route('/test')
def test():
    try:
        s = Session()
        user_count = s.query(User).count()
        users = s.query(User).all()
        
        html = f'''
        <h1>Test Successful!</h1>
        <p>Flask app is running properly.</p>
        <p>Database connection: OK</p>
        <p>Total users: {user_count}</p>
        '''
        
        for user in users:
            html += f'''
            <p>User: {user.username}, Email: {user.email}, Role: {user.role}, Active: {user.is_active}</p>
            '''
            
        html += '''
        <p><a href="/simple-login">เข้าสู่ระบบ</a></p>
        <p><a href="/dashboard">Dashboard</a></p>
        '''
        return html
    except Exception as e:
        return f'''
        <h1>Test Failed!</h1>
        <p>Error: {str(e)}</p>
        <p><a href="/simple-login">เข้าสู่ระบบ</a></p>
        '''

@app.route('/simple-login', methods=['GET', 'POST'])
def simple_login():
    if request.method == 'POST':
        username = request.form.get('username', 'admin')
        password = request.form.get('password', 'admin123')
        print(f"SIMPLE LOGIN DEBUG: {username}, {password}")
        
        s = Session()
        user = s.query(User).filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(FlaskUser(user))
            print("SIMPLE LOGIN: Success")
            return redirect(url_for('dashboard'))
        else:
            print("SIMPLE LOGIN: Failed")
            return '''<h1>Login Failed</h1><p><a href="/simple-login">Try again</a></p>'''
    
    return '''
    <h1>IT Business Shop - เข้าสู่ระบบ (Simple)</h1>
    <form method="post">
        <p>
            <label>ชื่อผู้ใช้:</label><br>
            <input type="text" name="username" value="admin" required>
        </p>
        <p>
            <label>รหัสผ่าน:</label><br>
            <input type="password" name="password" value="admin123" required>
        </p>
        <p>
            <input type="submit" value="เข้าสู่ระบบ">
        </p>
    </form>
    <p><a href="/test">กลับหน้าทดสอบ</a></p>
    '''

@app.route('/login', methods=['GET','POST'])
def login():
    try:
        if request.method == 'POST':
            # รองรับทั้ง WTForm และ simple form
            username = request.form.get('username')
            password = request.form.get('password')
            
            print(f"DEBUG: Login attempt - username: {username}, password: {password}")
            
            if username and password:
                s = Session()
                user = s.query(User).filter_by(username=username).first()
                print(f"DEBUG: Found user: {user}")
                if user:
                    print(f"DEBUG: Stored hash: {user.password_hash}")
                    print(f"DEBUG: Password check: {check_password_hash(user.password_hash, password)}")
                if user and check_password_hash(user.password_hash, password):
                    login_user(FlaskUser(user))
                    flash('เข้าสู่ระบบสำเร็จ')
                    print("DEBUG: Login successful, redirecting to dashboard")
                    return redirect(url_for('dashboard'))
                flash('ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')
                print("DEBUG: Login failed")
                return redirect(url_for('login'))
        
        # สำหรับ GET request หรือใช้ WTForm
        form = LoginForm()
        if form.validate_on_submit():
            s = Session()
            user = s.query(User).filter_by(username=form.username.data).first()
            if user and check_password_hash(user.password_hash, form.password.data):
                login_user(FlaskUser(user))
                flash('เข้าสู่ระบบสำเร็จ')
                return redirect(url_for('dashboard'))
            flash('ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')
        
        return render_template('login.html', form=form)
    except Exception as e:
        return f'''
        <h1>Login Error</h1>
        <p>Error: {str(e)}</p>
        <p><a href="/simple-login">ใช้หน้า login แบบง่าย</a></p>
        <p><a href="/test">ทดสอบเซิร์ฟเวอร์</a></p>
        '''

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    try:
        s = Session()
        # Quick sums: today, this month, this year
        today = date.today()
        month_start = date(today.year, today.month, 1)
        year_start = date(today.year, 1, 1)

        def sums_between(start, end):
            incomes = s.query(Entry).filter(Entry.date >= start, Entry.date <= end, Entry.type=='income').all()
            expenses = s.query(Entry).filter(Entry.date >= start, Entry.date <= end, Entry.type=='expense').all()
            inc_sum = sum(e.amount for e in incomes)
            exp_sum = sum(e.amount for e in expenses)
            return inc_sum, exp_sum, inc_sum - exp_sum

        t_inc, t_exp, t_net = sums_between(today, today)
        m_inc, m_exp, m_net = sums_between(month_start, today)
        y_inc, y_exp, y_net = sums_between(year_start, today)

        # Chart data: last 7 days aggregated
        dates = []
        for i in range(6, -1, -1):
            try:
                d = today.replace(day=today.day - i)
                dates.append(d)
            except ValueError:
                # Handle month boundary
                import calendar
                prev_month = today.month - 1 if today.month > 1 else 12
                prev_year = today.year if today.month > 1 else today.year - 1
                last_day = calendar.monthrange(prev_year, prev_month)[1]
                d = date(prev_year, prev_month, last_day - (i - today.day))
                dates.append(d)
        
        dates = sorted(dates)
        labels = [d.strftime('%Y-%m-%d') for d in dates]
        chart_incomes = []
        chart_expenses = []
        for d in labels:
            inc, exp, _ = sums_between(date.fromisoformat(d), date.fromisoformat(d))
            chart_incomes.append(inc)
            chart_expenses.append(exp)

        return render_template('dashboard.html',
                               t_inc=t_inc, t_exp=t_exp, t_net=t_net,
                               m_inc=m_inc, m_exp=m_exp, m_net=m_net,
                               y_inc=y_inc, y_exp=y_exp, y_net=y_net,
                               labels=labels, chart_incomes=chart_incomes, chart_expenses=chart_expenses)
    except Exception as e:
        return f'<h1>Dashboard Error</h1><p>{str(e)}</p><p><a href="/test">ทดสอบเซิร์ฟเวอร์</a></p>'

@app.route('/api/chart-data')
@login_required
def chart_data():
    try:
        selected_month = request.args.get('month', date.today().month, type=int)
        selected_year = request.args.get('year', date.today().year, type=int)
        
        s = Session()
        
        # คำนวณจำนวนวันในเดือนที่เลือก
        import calendar
        days_in_month = calendar.monthrange(selected_year, selected_month)[1]
        
        # สร้างรายการวันทั้งเดือน
        dates = []
        labels = []
        chart_incomes = []
        chart_expenses = []
        
        for day in range(1, days_in_month + 1):
            target_date = date(selected_year, selected_month, day)
            dates.append(target_date)
            labels.append(f"{day}/{selected_month}")
            
            # ดึงข้อมูลรายวัน
            daily_incomes = s.query(Entry).filter(
                Entry.date == target_date,
                Entry.type == 'income'
            ).all()
            
            daily_expenses = s.query(Entry).filter(
                Entry.date == target_date, 
                Entry.type == 'expense'
            ).all()
            
            inc_sum = sum(e.amount for e in daily_incomes)
            exp_sum = sum(e.amount for e in daily_expenses)
            
            chart_incomes.append(inc_sum)
            chart_expenses.append(exp_sum)
        
        s.close()
        
        return jsonify({
            'labels': labels,
            'incomes': chart_incomes,
            'expenses': chart_expenses,
            'month': selected_month,
            'year': selected_year
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/available-months')
@login_required 
def available_months():
    try:
        s = Session()
        # ดึงข้อมูลเดือน/ปีที่มีข้อมูลในฐานข้อมูล
        entries = s.query(Entry).all()
        months_years = set()
        
        for entry in entries:
            months_years.add((entry.date.year, entry.date.month))
        
        s.close()
        
        # จัดเรียงและแปลงเป็น list
        available = sorted(list(months_years), reverse=True)
        
        return jsonify({
            'available': [{'year': year, 'month': month} for year, month in available]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/entries')
@login_required
def entries():
    try:
        page = int(request.args.get('page', 1))
        per_page = 20  # เพิ่มจำนวนรายการต่อหน้า
        s = Session()
        total = s.query(Entry).count()
        
        # Debug logging
        print(f"📊 ENTRIES ROUTE DEBUG:")
        print(f"   Total entries in DB: {total}")
        print(f"   Page: {page}, Per page: {per_page}")
        
        # เปลี่ยนเป็นเรียงตาม created_at ล่าสุดก่อน แล้วค่อย date
        items = s.query(Entry).order_by(Entry.created_at.desc(), Entry.date.desc()).offset((page-1)*per_page).limit(per_page).all()
        
        print(f"   Items retrieved: {len(items)}")
        if items:
            print(f"   Latest item: ID:{items[0].id} | {items[0].date} | {items[0].category}")
        
        # Flash message แสดงจำนวนรายการทั้งหมด
        if request.args.get('imported'):
            flash(f'✅ แสดงรายการทั้งหมด {total} รายการ (รายการใหม่อยู่ด้านบนสุด)', 'info')
        
        s.close()
        return render_template('entries.html', items=items, page=page, per_page=per_page, total=total)
    except Exception as e:
        print(f"❌ ENTRIES ROUTE ERROR: {str(e)}")
        return f'<h1>Entries Error</h1><p>{str(e)}</p>'

@app.route('/entry/new', methods=['GET','POST'])
@login_required
def entry_new():
    try:
        form = EntryForm()
        # Populate category choices depending on type
        form.category.choices = INCOME_CHOICES if form.type.data == 'income' else EXPENSE_CHOICES
        if request.method == 'POST':
            # Allow custom category
            if form.custom_category.data:
                category = form.custom_category.data
            else:
                category = form.category.data
            if form.validate_on_submit():
                s = Session()
                e = Entry(date=form.date.data, type=form.type.data, category=category,
                          description=form.description.data, amount=float(form.amount.data), created_by=int(current_user.get_id()))
                s.add(e)
                s.commit()
                flash('บันทึกเรียบร้อย')
                return redirect(url_for('entries'))
        # Default choices show income categories
        form.category.choices = INCOME_CHOICES
        return render_template('entry_form.html', form=form)
    except Exception as e:
        return f'<h1>New Entry Error</h1><p>{str(e)}</p>'

@app.route('/entry/<int:id>/edit', methods=['GET','POST'])
@login_required
def entry_edit(id):
    try:
        s = Session()
        e = s.query(Entry).get(id)
        if not e:
            flash('ไม่พบรายการ')
            return redirect(url_for('entries'))
        form = EntryForm(obj=e)
        # Populate choices
        form.category.choices = INCOME_CHOICES if e.type=='income' else EXPENSE_CHOICES
        if form.validate_on_submit():
            e.date = form.date.data
            e.type = form.type.data
            e.category = form.custom_category.data if form.custom_category.data else form.category.data
            e.description = form.description.data
            e.amount = float(form.amount.data)
            s.commit()
            flash('แก้ไขเรียบร้อย')
            return redirect(url_for('entries'))
        return render_template('entry_form.html', form=form, entry=e)
    except Exception as e:
        return f'<h1>Edit Entry Error</h1><p>{str(e)}</p>'

@app.route('/entry/<int:id>/delete', methods=['POST'])
@login_required
def entry_delete(id):
    try:
        s = Session()
        e = s.query(Entry).get(id)
        if e:
            s.delete(e)
            s.commit()
            flash('✅ ลบรายการแล้ว', 'success')
        else:
            flash('❌ ไม่พบรายการที่ต้องการลบ', 'error')
        return redirect(url_for('entries'))
    except Exception as e:
        flash(f'❌ เกิดข้อผิดพลาดในการลบ: {str(e)}', 'error')
        return redirect(url_for('entries'))

@app.route('/delete_all_entries', methods=['POST'])
@login_required
def delete_all_entries():
    try:
        s = Session()
        # นับจำนวนรายการก่อนลบ
        count = s.query(Entry).count()
        
        if count == 0:
            flash('❌ ไม่มีรายการให้ลบ', 'warning')
        else:
            # ลบรายการทั้งหมด
            s.query(Entry).delete()
            s.commit()
            flash(f'✅ ลบรายการทั้งหมดแล้ว ({count:,} รายการ)', 'success')
        
        return redirect(url_for('entries'))
    except Exception as e:
        flash(f'❌ เกิดข้อผิดพลาดในการลบข้อมูลทั้งหมด: {str(e)}', 'error')
        return redirect(url_for('entries'))

@app.route('/export/csv')
@login_required
def export_csv():
    try:
        s = Session()
        items = s.query(Entry).order_by(Entry.date.desc()).all()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['date','type','category','description','amount'])
        for it in items:
            writer.writerow([it.date.isoformat(), it.type, it.category, it.description, it.amount])
        output.seek(0)
        return send_file(io.BytesIO(output.getvalue().encode('utf-8-sig')),
                         mimetype='text/csv', as_attachment=True, download_name='รายการธุรกิจ.csv')
    except Exception as e:
        flash(f'❌ เกิดข้อผิดพลาดในการส่งออก: {str(e)}', 'error')
        return redirect(url_for('import_csv'))

@app.route('/download/sample-csv')
def download_sample_csv():
    """ดาวน์โหลดไฟล์ตัวอย่าง CSV"""
    try:
        output = io.StringIO()
        writer = csv.writer(output)
        
        # เขียน header
        writer.writerow(['date','type','category','description','amount'])
        
        # เขียนข้อมูลตัวอย่าง
        sample_data = [
            ['2025-10-18', 'income', 'ถ่ายเอกสาร', 'ถ่ายเอกสาร A4 ขาวดำ 50 แผ่น', '50'],
            ['2025-10-18', 'income', 'พิมพ์เอกสาร', 'พิมพ์เอกสาร A4 สี 10 แผ่น', '120'],
            ['2025-10-17', 'expense', 'ค่าวัสดุ', 'ซื้อกระดาษ A4', '300'],
            ['2025-10-17', 'income', 'บริการอื่นๆ', 'สแกนเอกสาร', '30'],
            ['2025-10-16', 'expense', 'ค่าหมึก', 'ซื้อหมึกเครื่องพิมพ์', '450']
        ]
        
        for row in sample_data:
            writer.writerow(row)
        
        output.seek(0)
        return send_file(io.BytesIO(output.getvalue().encode('utf-8-sig')),
                         mimetype='text/csv', 
                         as_attachment=True, 
                         download_name='ตัวอย่างข้อมูล.csv')
    except Exception as e:
        flash(f'❌ ไม่สามารถสร้างไฟล์ตัวอย่างได้: {str(e)}', 'error')
        return redirect(url_for('import_csv'))

@app.route('/simple-import')
def simple_import():
    """หน้า CSV import แบบง่าย (ไม่ต้อง login)"""
    print("📄 Simple Import page accessed")
    with open('simple_import.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/import/csv', methods=['GET', 'POST'])
@login_required  
def import_csv():
    if request.method == 'GET':
        return render_template('import_export.html')
    
    # POST method - นำเข้าข้อมูล CSV
    print("🔄 CSV IMPORT STARTED")
    print(f"📊 Request method: {request.method}")
    print(f"📁 Files in request: {list(request.files.keys())}")
    print(f"📋 Form data keys: {list(request.form.keys())}")
    print(f"📦 Content type: {request.content_type}")
    print(f"📏 Content length: {request.content_length}")
    
    try:
        # 1. ตรวจสอบว่ามีไฟล์หรือไม่
        if 'file' not in request.files:
            print("❌ ERROR: No 'file' key in request.files")
            print(f"❓ Available keys: {list(request.files.keys())}")
            flash('❌ ไม่พบไฟล์ในคำขอ - โปรดลองอีกครั้ง', 'error')
            return redirect(url_for('import_csv'))
        
        uploaded_file = request.files['file']
        print(f"📄 Uploaded file: {uploaded_file.filename}")
        print(f"📊 File object: {type(uploaded_file)}")
        
        if not uploaded_file or uploaded_file.filename == '':
            print("❌ ERROR: No file selected or empty filename")
            flash('❌ กรุณาเลือกไฟล์ CSV', 'error')
            return redirect(url_for('import_csv'))
        
        # 2. อ่านไฟล์ (รองรับ UTF-8 และ UTF-8-BOM)
        try:
            file_content = uploaded_file.read().decode('utf-8-sig')
        except:
            file_content = uploaded_file.read().decode('utf-8')
        
        # 3. แยกบรรทัด
        lines = [line.strip() for line in file_content.strip().split('\n') if line.strip()]
        
        if len(lines) < 2:
            flash('❌ ไฟล์ต้องมีอย่างน้อย 2 บรรทัด (header + ข้อมูล)', 'error')
            return redirect(url_for('import_csv'))
        
        # 4. อ่าน header
        headers = [h.strip().lower() for h in lines[0].split(',')]
        
        if 'date' not in headers or 'amount' not in headers:
            flash('❌ ไฟล์ต้องมีคอลัมน์ "date" และ "amount"', 'error')
            return redirect(url_for('import_csv'))
        
        date_idx = headers.index('date')
        amount_idx = headers.index('amount')
        category_idx = headers.index('category') if 'category' in headers else None
        description_idx = headers.index('description') if 'description' in headers else None
        
        # 5. ประมวลผลข้อมูล
        session = Session()
        success_count = 0
        error_count = 0
        
        for i, line in enumerate(lines[1:], start=2):
            try:
                # แยกคอลัมน์
                values = [v.strip() for v in line.split(',')]
                
                if len(values) <= max(date_idx, amount_idx):
                    error_count += 1
                    print(f"บรรทัด {i}: จำนวนคอลัมน์ไม่ถูกต้อง")
                    continue
                
                # วันที่
                date_str = values[date_idx]
                entry_date = None
                
                # ลองหลายรูปแบบ
                for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d']:
                    try:
                        entry_date = datetime.strptime(date_str, fmt).date()
                        break
                    except:
                        continue
                
                if not entry_date:
                    error_count += 1
                    print(f"บรรทัด {i}: รูปแบบวันที่ไม่ถูกต้อง: {date_str}")
                    continue
                
                # จำนวนเงิน
                amount_str = values[amount_idx].replace(',', '')  # ลบคอมม่า
                amount = float(amount_str)
                
                # ประเภท
                entry_type = 'income' if amount >= 0 else 'expense'
                amount = abs(amount)
                
                # หมวดหมู่และรายละเอียด
                category = values[category_idx] if category_idx and len(values) > category_idx else 'อื่นๆ'
                description = values[description_idx] if description_idx and len(values) > description_idx else ''
                
                # บันทึกข้อมูล
                new_entry = Entry(
                    date=entry_date,
                    type=entry_type,
                    category=category,
                    description=description,
                    amount=amount,
                    created_by=int(current_user.get_id())
                )
                
                session.add(new_entry)
                success_count += 1
                
            except Exception as e:
                error_count += 1
                print(f"บรรทัด {i}: Error - {str(e)}")
                continue
        
        # 6. บันทึกการเปลี่ยนแปลง
        if success_count > 0:
            session.commit()
            flash(f'✅ นำเข้า CSV สำเร็จ {success_count} รายการ' + (f' (ข้าม {error_count} รายการ)' if error_count > 0 else ''), 'success')
            session.close()
            # Redirect พร้อม parameter เพื่อแสดงข้อความแจ้งเตือน
            return redirect(url_for('entries', imported=1))
        else:
            flash(f'❌ ไม่สามารถนำเข้าข้อมูลได้ (ข้าม {error_count} รายการ)', 'error')
            session.close()
            return redirect(url_for('import_csv'))
        
    except Exception as e:
        print(f"Import CSV Error: {str(e)}")
        flash(f'❌ เกิดข้อผิดพลาด: {str(e)}', 'error')
        return redirect(url_for('import_csv'))

# Routes สำหรับระบบจัดการสมาชิก
@app.route('/register', methods=['GET', 'POST'])
def register():
    from forms import RegistrationForm
    from werkzeug.security import generate_password_hash
    
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            # ตรวจสอบรหัสผ่าน
            if form.password.data != form.confirm_password.data:
                flash('รหัสผ่านไม่ตรงกัน', 'error')
                return render_template('register.html', form=form)
            
            s = Session()
            
            # ตรวจสอบ username ซ้ำ
            existing_user = s.query(User).filter_by(username=form.username.data).first()
            if existing_user:
                flash('ชื่อผู้ใช้นี้มีคนใช้แล้ว', 'error')
                return render_template('register.html', form=form)
            
            # ตรวจสอบ email ซ้ำ
            existing_email = s.query(User).filter_by(email=form.email.data).first()
            if existing_email:
                flash('อีเมลนี้มีคนใช้แล้ว', 'error')
                return render_template('register.html', form=form)
            
            # สร้างผู้ใช้ใหม่
            new_user = User(
                username=form.username.data,
                email=form.email.data,
                password_hash=generate_password_hash(form.password.data),
                role='user',
                is_active=True
            )
            
            s.add(new_user)
            s.commit()
            
            flash('สมัครสมาชิกสำเร็จ! กรุณาเข้าสู่ระบบ', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            flash(f'เกิดข้อผิดพลาด: {str(e)}', 'error')
    
    return render_template('register.html', form=form)

@app.route('/members')
@login_required
def members():
    # ตรวจสอบสิทธิ์ admin
    if not hasattr(current_user, 'role') or current_user.role != 'admin':
        flash('คุณไม่มีสิทธิ์เข้าถึงหน้านี้', 'error')
        return redirect(url_for('dashboard'))
    
    try:
        s = Session()
        users = s.query(User).order_by(User.created_at.desc()).all()
        
        # สถิติ
        total_members = len(users)
        active_members = len([u for u in users if u.is_active])
        inactive_members = total_members - active_members
        admin_count = len([u for u in users if u.role == 'admin'])
        
        return render_template('members.html', 
                             users=users,
                             total_members=total_members,
                             active_members=active_members,
                             inactive_members=inactive_members,
                             admin_count=admin_count)
    except Exception as e:
        return f'<h1>Members Error</h1><p>{str(e)}</p>'

@app.route('/admin/toggle_user_status', methods=['POST'])
@login_required
def toggle_user_status():
    if not hasattr(current_user, 'role') or current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'ไม่มีสิทธิ์'})
    
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        is_active = data.get('is_active')
        
        s = Session()
        user = s.query(User).get(user_id)
        if user:
            user.is_active = is_active
            s.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'ไม่พบผู้ใช้'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/toggle_user_role', methods=['POST'])
@login_required
def toggle_user_role():
    if not hasattr(current_user, 'role') or current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'ไม่มีสิทธิ์'})
    
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        role = data.get('role')
        
        s = Session()
        user = s.query(User).get(user_id)
        if user:
            user.role = role
            s.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'ไม่พบผู้ใช้'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/delete_user', methods=['POST'])
@login_required
def delete_user():
    if not hasattr(current_user, 'role') or current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'ไม่มีสิทธิ์'})
    
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        s = Session()
        user = s.query(User).get(user_id)
        if user:
            s.delete(user)
            s.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'ไม่พบผู้ใช้'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# CSV Import Route ใหม่
@app.route('/csv-import', methods=['GET'])
@login_required
def csv_import_page():
    """แสดงหน้า CSV Import"""
    return render_template('csv_import.html')

@app.route('/csv-import', methods=['POST'])
@login_required
def csv_import():
    """ประมวลผลการนำเข้า CSV"""
    try:
        # ตรวจสอบไฟล์
        if 'csvfile' not in request.files:
            return jsonify({'success': False, 'message': 'ไม่พบไฟล์'})
        
        file = request.files['csvfile']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'กรุณาเลือกไฟล์'})
        
        if not file.filename.lower().endswith('.csv'):
            return jsonify({'success': False, 'message': 'กรุณาเลือกไฟล์ .csv'})
        
        # อ่านไฟล์
        file_content = file.read()
        
        # ลอง decode หลาย encoding
        text_content = None
        for encoding in ['utf-8-sig', 'utf-8', 'cp874', 'windows-1252', 'iso-8859-1']:
            try:
                text_content = file_content.decode(encoding)
                break
            except UnicodeDecodeError:
                continue
        
        if not text_content:
            return jsonify({'success': False, 'message': 'ไม่สามารถอ่านไฟล์ได้'})
        
        # แยกบรรทัด
        lines = [line.strip() for line in text_content.strip().split('\n') if line.strip()]
        if len(lines) < 2:
            return jsonify({'success': False, 'message': 'ไฟล์ต้องมีข้อมูลอย่างน้อย 2 บรรทัด'})
        
        # อ่าน header
        headers = [h.strip().lower() for h in lines[0].split(',')]
        
        # ตรวจสอบคอลัมน์ที่จำเป็น
        if 'date' not in headers or 'amount' not in headers:
            return jsonify({'success': False, 'message': 'ไฟล์ต้องมีคอลัมน์ date และ amount'})
        
        # หา index ของแต่ละคอลัมน์
        date_idx = headers.index('date')
        amount_idx = headers.index('amount')
        type_idx = headers.index('type') if 'type' in headers else None
        category_idx = headers.index('category') if 'category' in headers else None
        desc_idx = headers.index('description') if 'description' in headers else None
        
        # ประมวลผลข้อมูล
        s = Session()
        success_count = 0
        error_count = 0
        
        for line_no, line in enumerate(lines[1:], 2):
            try:
                # แยกค่า CSV (รองรับ quotes)
                values = []
                current = ''
                in_quotes = False
                
                for char in line:
                    if char == '"':
                        in_quotes = not in_quotes
                    elif char == ',' and not in_quotes:
                        values.append(current.strip().strip('"'))
                        current = ''
                    else:
                        current += char
                values.append(current.strip().strip('"'))
                
                if len(values) < max(date_idx, amount_idx) + 1:
                    error_count += 1
                    continue
                
                # ดึงข้อมูล
                date_str = values[date_idx].strip()
                amount_str = values[amount_idx].strip()
                
                if not date_str or not amount_str:
                    error_count += 1
                    continue
                
                # แปลงวันที่
                entry_date = None
                for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%Y/%m/%d']:
                    try:
                        entry_date = datetime.strptime(date_str, fmt).date()
                        break
                    except ValueError:
                        continue
                
                if not entry_date:
                    error_count += 1
                    continue
                
                # แปลงจำนวนเงิน
                try:
                    amount = float(amount_str.replace(',', ''))
                    original_amount = amount
                    amount = abs(amount)
                except:
                    error_count += 1
                    continue
                
                # กำหนดประเภท
                if type_idx is not None and type_idx < len(values):
                    entry_type = values[type_idx].strip().lower()
                    if entry_type not in ['income', 'expense']:
                        entry_type = 'expense' if original_amount < 0 else 'income'
                else:
                    entry_type = 'expense' if original_amount < 0 else 'income'
                
                # กำหนดหมวดหมู่
                category = 'อื่นๆ'
                if category_idx is not None and category_idx < len(values):
                    cat = values[category_idx].strip()
                    if cat:
                        category = cat
                
                # กำหนดรายละเอียด
                description = ''
                if desc_idx is not None and desc_idx < len(values):
                    description = values[desc_idx].strip()
                
                # บันทึกข้อมูล
                entry = Entry(
                    date=entry_date,
                    type=entry_type,
                    category=category,
                    description=description,
                    amount=amount,
                    created_by=int(current_user.get_id())
                )
                s.add(entry)
                success_count += 1
                
            except Exception as e:
                error_count += 1
                continue
        
        # บันทึกการเปลี่ยนแปลง
        if success_count > 0:
            s.commit()
        
        s.close()
        
        return jsonify({
            'success': True,
            'message': f'นำเข้าข้อมูลสำเร็จ {success_count} รายการ',
            'success_count': success_count,
            'error_count': error_count
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'})

if __name__ == '__main__':
    # Initialize database tables
    Base.metadata.create_all(engine)
    
    # Create default admin user if not exists
    try:
        from werkzeug.security import generate_password_hash
        s = Session()
        admin_user = s.query(User).filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email='admin@itbusinessshop.com',
                password_hash=generate_password_hash('admin123'),
                role='admin',
                is_active=True
            )
            s.add(admin_user)
            s.commit()
            print("Created default admin user: admin/admin123")
        s.close()
    except Exception as e:
        print(f"Database setup error: {e}")
    
    # Get port from environment (Railway) or use default
    port = int(os.environ.get('PORT', 8000))
    host = '0.0.0.0' if os.environ.get('RAILWAY_ENVIRONMENT') else '127.0.0.1'
    debug = not bool(os.environ.get('RAILWAY_ENVIRONMENT'))
    
    print("=" * 50)
    print("Starting IT Business Shop Flask Application")
    print("=" * 50)
    if os.environ.get('RAILWAY_ENVIRONMENT'):
        print(f"🚂 Running on Railway (Production Mode)")
        print(f"🌐 Host: {host}:{port}")
    else:
        print(f"🖥️  Running Locally (Development Mode)")
        print(f"🌐 Access: http://{host}:{port}")
    print("Login credentials:")
    print("  Username: admin")
    print("  Password: admin123")
    print("=" * 50)
    
    try:
        app.run(debug=debug, host=host, port=port)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")