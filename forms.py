from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, DateField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length

INCOME_CHOICES = [
    ('ถ่ายเอกสาร A4 ขาวดำ', 'ถ่ายเอกสาร A4 ขาวดำ'),
    ('ถ่ายเอกสาร A4 สี', 'ถ่ายเอกสาร A4 สี'),
    ('print A4 ขาวดำ', 'print A4 ขาวดำ'),
    ('print A4 สี', 'print A4 สี'),
    ('เคลือบบัตร ขนาดการ์ดทั่วไป', 'เคลือบบัตร ขนาดการ์ดทั่วไป'),
    ('เคลือบบัตร ขนาด A4', 'เคลือบบัตร ขนาด A4'),
    ('ถ่ายเอกสาร A3 สี', 'ถ่ายเอกสาร A3 สี'),
    ('ถ่ายเอกสาร A3 ขาวดำ', 'ถ่ายเอกสาร A3 ขาวดำ'),
    ('print A3 ขาวดำ', 'print A3 ขาวดำ'),
    ('print A3', 'print A3'),
    ('อื่นๆ', 'อื่นๆ'),
]

EXPENSE_CHOICES = [
    ('ค่าหมึก', 'ค่าหมึก'),
    ('ค่ากระดาษ', 'ค่ากระดาษ'),
    ('ค่าน้ำ', 'ค่าน้ำ'),
    ('ค่าไฟ', 'ค่าไฟ'),
    ('อื่นๆ', 'อื่นๆ'),
]

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class EntryForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    type = SelectField('Type', choices=[('income','รายรับ'), ('expense','รายจ่าย')], validators=[DataRequired()])
    category = SelectField('Category', choices=[], validators=[DataRequired()])
    custom_category = StringField('ถ้าต้องการเพิ่มรายการอื่น')
    description = TextAreaField('รายละเอียด')
    amount = DecimalField('จำนวนเงิน', validators=[DataRequired()])
    submit = SubmitField('บันทึก')

class RegistrationForm(FlaskForm):
    username = StringField('ชื่อผู้ใช้', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('อีเมล', validators=[DataRequired(), Length(min=6, max=120)])
    password = PasswordField('รหัสผ่าน', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('ยืนยันรหัสผ่าน', validators=[DataRequired()])
    submit = SubmitField('สมัครสมาชิก')
