# 🚂 Railway Deployment Guide - IT Business Shop

## 📋 Pre-deployment Setup

### 1. Database Configuration
Railway will automatically provide PostgreSQL database. The app will detect `DATABASE_URL` environment variable and switch from SQLite to PostgreSQL.

### 2. Environment Variables
Set these in Railway dashboard:
- `SECRET_KEY`: A strong random secret key for Flask sessions
- `DATABASE_URL`: Automatically provided by Railway PostgreSQL service

### 3. Port Configuration
Railway automatically sets the `PORT` environment variable. The app will use Railway's port in production.

## 🚀 Deployment Steps

### Step 1: Connect Repository
1. Go to [Railway](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose this repository: `worravits-ctrl/it_business_shop`

### Step 2: Add PostgreSQL Database
1. In your Railway project dashboard
2. Click "New" → "Database" → "Add PostgreSQL"
3. Railway will automatically set the `DATABASE_URL` environment variable

### Step 3: Configure Environment Variables
1. Go to your service settings
2. Add environment variables:
   ```
   SECRET_KEY=your-super-secret-key-here
   RAILWAY_ENVIRONMENT=production
   ```

### Step 4: Deploy
Railway will automatically:
- Install dependencies from `requirements.txt`
- Run the app using `Procfile` configuration
- Create database tables on first run
- Create default admin user (admin/admin123)

## 🔧 Technical Details

### Files for Railway:
- `Procfile`: Defines how to run the app
- `requirements.txt`: Python dependencies
- `railway.json`: Railway-specific configuration
- `runtime.txt`: Python version specification

### Database Migration:
- **Local**: Uses SQLite (`business.db`)
- **Railway**: Uses PostgreSQL (via `DATABASE_URL`)
- **Auto-migration**: App detects environment and switches automatically

### Default Credentials:
- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@itbusinessshop.com`
- **Role**: `admin`

## 🎯 Features Available on Railway:

✅ **Member Management System**
- User registration and authentication
- Role-based access control (admin/user)
- Member management panel for admins

✅ **Business Analytics**
- Income and expense tracking
- Dashboard with statistics and charts
- CSV import/export functionality

✅ **Modern UI**
- Responsive Bootstrap 5 design
- Mobile-friendly interface
- Professional Thai language support

## 🔒 Security Features:
- Password hashing with Werkzeug
- Session management with Flask-Login
- CSRF protection via Flask-WTF
- Role-based access control

## 📊 Post-Deployment:
1. Access your Railway URL
2. Login with admin credentials
3. Create additional users via registration
4. Start managing your IT business data!

## 🛠️ Troubleshooting:
- Check Railway logs for any deployment errors
- Ensure PostgreSQL service is running
- Verify environment variables are set correctly
- Database tables are created automatically on first run
