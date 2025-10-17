import os
from flask import Flask, render_template, redirect, url_for, flash, request, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime, date
import io, csv
import pandas as pd

from models import Base, User, Entry
from forms import LoginForm, EntryForm, INCOME_CHOICES, EXPENSE_CHOICES

DB_PATH = os.path.join(os.path.dirname(__file__), 'data.db')
engine = create_engine(f'sqlite:///{DB_PATH}', connect_args={"check_same_thread": False})
Session = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    s = Session()
    return s.query(User).get(int(user_id))

# simple user object wrapper that Flask-Login expects
class FlaskUser:
    def __init__(self, user):
        self._u = user
    def get_id(self):
        return str(self._u.id)
    @property
    def is_authenticated(self):
        return True

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        s = Session()
        user = s.query(User).filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(FlaskUser(user))
            return redirect(url_for('dashboard'))
        flash('ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    s = Session()
    # quick sums: today, this month, this year
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

    # chart data: last 7 days aggregated
    dates = [(today.replace(day=today.day - i)) for i in range(6, -1, -1)]
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

@app.route('/entries')
@login_required
def entries():
    page = int(request.args.get('page', 1))
    per_page = 10
    s = Session()
    total = s.query(Entry).count()
    items = s.query(Entry).order_by(Entry.date.desc()).offset((page-1)*per_page).limit(per_page).all()
    return render_template('entries.html', items=items, page=page, per_page=per_page, total=total)

@app.route('/entry/new', methods=['GET','POST'])
@login_required
def entry_new():
    form = EntryForm()
    # populate category choices depending on type
    form.category.choices = INCOME_CHOICES if form.type.data == 'income' else EXPENSE_CHOICES
    if request.method == 'POST':
        # allow custom category
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
    # default choices show income categories
    form.category.choices = INCOME_CHOICES
    return render_template('entry_form.html', form=form)

@app.route('/entry/<int:id>/edit', methods=['GET','POST'])
@login_required
def entry_edit(id):
    s = Session()
    e = s.query(Entry).get(id)
    if not e:
        flash('ไม่พบรายการ')
        return redirect(url_for('entries'))
    form = EntryForm(obj=e)
    # populate choices
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

@app.route('/entry/<int:id>/delete', methods=['POST'])
@login_required
def entry_delete(id):
    s = Session()
    e = s.query(Entry).get(id)
    if e:
        s.delete(e)
        s.commit()
        flash('ลบรายการแล้ว')
    return redirect(url_for('entries'))

@app.route('/export/csv')
@login_required
def export_csv():
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

@app.route('/import/csv', methods=['GET','POST'])
@login_required
def import_csv():
    if request.method=='POST':
        file = request.files.get('file')
        if not file:
            flash('กรุณาเลือกไฟล์')
            return redirect(url_for('import_csv'))
        df = pd.read_csv(file)
        s = Session()
        for _, row in df.iterrows():
            try:
                d = date.fromisoformat(str(row['date']))
            except Exception:
                continue
            e = Entry(date=d, type=row['type'], category=row.get('category','อื่นๆ'),
                      description=row.get('description',''), amount=float(row['amount']), created_by=int(current_user.get_id()))
            s.add(e)
        s.commit()
        flash('นำเข้าข้อมูลสำเร็จ')
        return redirect(url_for('entries'))
    return render_template('import_export.html')

if __name__ == '__main__':
    app.run(debug=True)
