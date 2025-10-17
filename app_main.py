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
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    # Production: PostgreSQL on Railway
    engine = create_engine(DATABASE_URL)
else:
    # Development: SQLite
    DB_PATH = os.path.join(os.path.dirname(__file__), 'business.db')
    engine = create_engine(f'sqlite:///{DB_PATH}', connect_args={"check_same_thread": False})

Session = scoped_session(sessionmaker(bind=engine))

# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-it-business-shop-2025')
app.config['WTF_CSRF_ENABLED'] = False  # ปิด CSRF ชั่วคราวเพื่อทดสอบ

# Production configuration
if os.environ.get('FLASK_ENV') == 'production':
    app.config['DEBUG'] = False
    app.config['TESTING'] = False
else:
    app.config['DEBUG'] = True

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

@app.route('/health')
def health_check():
    """Health check endpoint for Railway"""
    try:
        # Test database connection
        s = Session()
        user_count = s.query(User).count()
        s.close()
        
        return {
            'status': 'healthy',
            'database': 'connected',
            'users': user_count,
            'environment': os.environ.get('FLASK_ENV', 'development'),
            'timestamp': datetime.utcnow().isoformat()
        }, 200
    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }, 500

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

@app.route('/entries')
@login_required
def entries():
    try:
        page = int(request.args.get('page', 1))
        per_page = 10
        s = Session()
        total = s.query(Entry).count()
        items = s.query(Entry).order_by(Entry.date.desc()).offset((page-1)*per_page).limit(per_page).all()
        return render_template('entries.html', items=items, page=page, per_page=per_page, total=total)
    except Exception as e:
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
    s = Session()
    try:
        e = s.query(Entry).get(id)
        if e:
            s.delete(e)
            s.commit()
            flash('ลบรายการเรียบร้อยแล้ว', 'success')
        else:
            flash('ไม่พบรายการที่ต้องการลบ', 'error')
        s.close()
        return redirect(url_for('entries'))
    except Exception as ex:
        s.rollback()
        s.close()
        flash(f'เกิดข้อผิดพลาดในการลบ: {str(ex)}', 'error')
        return redirect(url_for('entries'))

@app.route('/export/csv')
@login_required
def export_csv():
    try:
        s = Session()
        items = s.query(Entry).order_by(Entry.date.desc()).all()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['id','date','type','category','description','amount','created_at'])
        for it in items:
            writer.writerow([it.id, it.date.isoformat(), it.type, it.category, it.description, it.amount, it.created_at.isoformat()])
        output.seek(0)
        return send_file(io.BytesIO(output.getvalue().encode('utf-8-sig')),
                         mimetype='text/csv', as_attachment=True, download_name='entries.csv')
    except Exception as e:
        return f'<h1>Export Error</h1><p>{str(e)}</p>'

@app.route('/import/csv', methods=['GET','POST'])
@login_required
def import_csv():
    if request.method == 'GET':
        return render_template('import_export.html')
    
    s = Session()
    try:
        file = request.files.get('file')
        if not file or file.filename == '':
            flash('กรุณาเลือกไฟล์ CSV', 'error')
            return redirect(url_for('import_csv'))
        
        if not file.filename.lower().endswith('.csv'):
            flash('กรุณาเลือกไฟล์ .csv เท่านั้น', 'error')
            return redirect(url_for('import_csv'))
        
        # อ่าน CSV file
        df = pd.read_csv(file, encoding='utf-8-sig')
        
        # ตรวจสอบ columns ที่จำเป็น
        required_columns = ['date', 'type', 'amount']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            flash(f'ไฟล์ CSV ขาดคอลัมน์: {", ".join(missing_columns)}', 'error')
            return redirect(url_for('import_csv'))
        
        imported_count = 0
        error_count = 0
        
        for index, row in df.iterrows():
            try:
                # ตรวจสอบวันที่
                try:
                    if pd.isna(row['date']):
                        continue
                    d = pd.to_datetime(row['date']).date()
                except Exception:
                    error_count += 1
                    continue
                
                # ตรวจสอบจำนวนเงิน
                try:
                    amount = float(row['amount'])
                except Exception:
                    error_count += 1
                    continue
                
                # สร้าง Entry
                e = Entry(
                    date=d, 
                    type=str(row['type']).strip(),
                    category=str(row.get('category', 'อื่นๆ')).strip(),
                    description=str(row.get('description', '')).strip(),
                    amount=amount,
                    created_by=int(current_user.get_id())
                )
                s.add(e)
                imported_count += 1
                
            except Exception as ex:
                error_count += 1
                print(f"Error processing row {index}: {ex}")
                continue
        
        s.commit()
        s.close()
        
        if imported_count > 0:
            flash(f'นำเข้าข้อมูลสำเร็จ {imported_count} รายการ', 'success')
            if error_count > 0:
                flash(f'มีข้อผิดพลาด {error_count} รายการ', 'warning')
        else:
            flash('ไม่สามารถนำเข้าข้อมูลได้ กรุณาตรวจสอบรูปแบบไฟล์', 'error')
        
        return redirect(url_for('entries'))
        
    except Exception as e:
        s.rollback()
        s.close()
        flash(f'เกิดข้อผิดพลาดในการนำเข้าข้อมูล: {str(e)}', 'error')
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

if __name__ == '__main__':
    # Create tables if they don't exist
    Base.metadata.create_all(engine)
    
    # Create admin user if it doesn't exist
    s = Session()
    admin_user = s.query(User).filter_by(username='admin').first()
    if not admin_user:
        from werkzeug.security import generate_password_hash
        admin_user = User(
            username='admin',
            email='admin@itbusinessshop.com',
            password_hash=generate_password_hash('admin123'),
            role='admin',
            is_active=True
        )
        s.add(admin_user)
        s.commit()
        print("Created admin user: admin/admin123")
    s.close()
    
    # Get port from environment (Railway sets PORT)
    port = int(os.environ.get('PORT', 8000))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    print("=" * 50)
    print("Starting IT Business Shop Flask Application")
    print("=" * 50)
    print(f"Access the application at: http://{host}:{port}")
    print("Login credentials:")
    print("  Username: admin")
    print("  Password: admin123")
    print("=" * 50)
    
    try:
        app.run(debug=debug, host=host, port=port)
    except Exception as e:
        print(f"Error starting server: {e}")