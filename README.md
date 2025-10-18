# 🏪 IT Business Shop - Complete Management System

A comprehensive Flask web application for managing IT business operations with member management, financial tracking, and modern responsive UI.

## ✨ Features

### 👥 **Member Management System**
- **User Registration & Authentication** - Secure signup and login
- **Role-Based Access Control** - Admin and User roles with different permissions
- **Member Administration** - Admins can manage users, activate/deactivate accounts
- **Profile Management** - User profiles with email and status tracking

### 💰 **Financial Management**
- **Income & Expense Tracking** - Record and categorize transactions
- **Dashboard Analytics** - Real-time statistics and visualizations
- **CSV Import/Export** - Bulk data management capabilities
- **Advanced Reporting** - Daily, monthly, and yearly financial summaries

### 🎨 **Modern UI/UX**
- **Responsive Design** - Bootstrap 5 with mobile-first approach
- **Thai Language Support** - Full Thai interface and content
- **Interactive Charts** - Chart.js integration for data visualization
- **Professional Styling** - Modern gradients and animations

## 🚀 Quick Start

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database and create admin user
python init_member_system.py

# Run the application
python app_main.py
```

**Default Credentials:**
- Username: `admin`
- Password: `admin123`
- Email: `admin@itbusinessshop.com`

### 🚂 Railway Deployment

Deploy to Railway cloud platform with automatic PostgreSQL database:

#### Option 1: One-Click Deploy
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https%3A%2F%2Fgithub.com%2Fworravits-ctrl%2Fit_business_shop)

#### Option 2: Manual Deployment
1. **Connect Repository**
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli
   
   # Login to Railway
   railway login
   
   # Create new project
   railway create it-business-shop
   ```

2. **Add Database**
   ```bash
   # Add PostgreSQL database
   railway add postgresql
   ```

3. **Set Environment Variables**
   ```bash
   # Set production secret key
   railway variables set SECRET_KEY="your-super-secret-key"
   railway variables set RAILWAY_ENVIRONMENT="production"
   ```

4. **Deploy**
   ```bash
   # Deploy the application
   railway deploy
   ```

📖 **Detailed Railway Setup**: See [RAILWAY_SETUP.md](RAILWAY_SETUP.md)

## 📁 Project Structure

```
it_business_shop_flask_app/
├── app_main.py              # Main Flask application
├── models.py                # Database models (User, Entry)
├── forms.py                 # WTForms for user input
├── init_member_system.py    # Database initialization
├── templates/               # HTML templates
│   ├── base.html           # Base template with navigation
│   ├── login.html          # Login page
│   ├── register.html       # User registration
│   ├── dashboard.html      # Analytics dashboard
│   ├── members.html        # Member management (admin)
│   └── ...
├── static/                  # CSS, JS, and assets
├── requirements.txt         # Python dependencies
├── Procfile                # Railway deployment config
└── README.md               # This file
```

## 🔧 Technology Stack

- **Backend**: Flask 2.3.2, SQLAlchemy 2.0.19
- **Authentication**: Flask-Login, Werkzeug password hashing
- **Forms**: Flask-WTF with CSRF protection
- **Database**: SQLite (local) / PostgreSQL (production)
- **Frontend**: Bootstrap 5, Chart.js, Font Awesome
- **Deployment**: Railway, Gunicorn WSGI server

## 🎯 User Roles

### 👑 **Admin Features**
- Full member management capabilities
- User account activation/deactivation
- Role promotion/demotion
- Access to all financial data
- System administration

### 👤 **User Features**
- Personal dashboard access
- Income/expense entry management
- Data export capabilities
- Profile management

## 🛡️ Security Features

- **Password Hashing**: Werkzeug secure password storage
- **Session Management**: Flask-Login secure sessions
- **CSRF Protection**: Flask-WTF CSRF tokens
- **Role Validation**: Server-side permission checks
- **Input Sanitization**: Form validation and sanitization

## 🌐 API Endpoints

### Authentication
- `GET/POST /login` - User login
- `GET/POST /register` - User registration
- `GET /logout` - User logout

### Dashboard & Analytics
- `GET /dashboard` - Main analytics dashboard
- `GET /entries` - Transaction listing
- `GET/POST /entry/new` - Add new transaction

### Member Management (Admin Only)
- `GET /members` - Member management panel
- `POST /admin/toggle_user_status` - Activate/deactivate user
- `POST /admin/toggle_user_role` - Change user role
- `POST /admin/delete_user` - Delete user account

### Data Management
- `GET /export/csv` - Export data to CSV
- `GET/POST /import/csv` - Import data from CSV

## 🔄 Database Schema

### Users Table
```sql
users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
```

### Entries Table
```sql
entries (
    id INTEGER PRIMARY KEY,
    date DATE NOT NULL,
    type VARCHAR(10) NOT NULL,  -- 'income' or 'expense'
    category VARCHAR(120) NOT NULL,
    description TEXT,
    amount FLOAT NOT NULL,
    created_by INTEGER REFERENCES users(id),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Bootstrap team for the amazing CSS framework
- Chart.js for beautiful data visualizations
- Flask community for the excellent web framework
- Railway for simple cloud deployment

---

**Made with ❤️ for IT Business Management**
