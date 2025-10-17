#!/bin/bash

# Railway Deployment Script for IT Business Shop
echo "🚂 Deploying IT Business Shop to Railway..."

# Install dependencies
pip install -r requirements.txt

# Create database tables
python -c "
from app_main import Base, engine, Session, User
from werkzeug.security import generate_password_hash
import os

print('Creating database tables...')
Base.metadata.create_all(engine)

# Create admin user if not exists
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
    print('✅ Admin user created: admin/admin123')
else:
    print('✅ Admin user already exists')
s.close()
print('🎉 Database setup complete!')
"

echo "✅ Deployment setup complete!"