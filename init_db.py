from sqlalchemy import create_engine
from models import Base, User
from werkzeug.security import generate_password_hash
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'data.db')
engine = create_engine(f'sqlite:///{DB_PATH}')
Base.metadata.create_all(engine)

# create admin user
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
s = Session()
if not s.query(User).filter_by(username='admin').first():
    u = User(username='admin', password_hash=generate_password_hash('admin123'))
    s.add(u)
    s.commit()
    print('Created admin/admin123')
else:
    print('Admin exists')
