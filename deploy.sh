#!/bin/bash

# 🚂 Railway Deployment Script for IT Business Shop
# This script helps deploy the application to Railway

echo "🚂 Railway Deployment Helper"
echo "================================"

# Check if railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found!"
    echo "💡 Install it: npm install -g @railway/cli"
    echo "📖 More info: https://docs.railway.app/develop/cli"
    exit 1
fi

echo "✅ Railway CLI found"

# Login check
echo "🔐 Checking Railway login status..."
if ! railway whoami &> /dev/null; then
    echo "❌ Not logged in to Railway"
    echo "💡 Run: railway login"
    exit 1
fi

echo "✅ Logged in to Railway"

# Project setup
echo "🏗️  Setting up Railway project..."
echo "Choose an option:"
echo "1) Create new Railway project"
echo "2) Link to existing project"
echo "3) Deploy to current project"
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo "🆕 Creating new Railway project..."
        railway create it-business-shop
        ;;
    2)
        echo "🔗 Link to existing project..."
        railway link
        ;;
    3)
        echo "🚀 Using current project..."
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

# Add PostgreSQL if needed
echo "🗄️  Checking for database..."
read -p "Add PostgreSQL database? (y/n): " add_db
if [[ $add_db =~ ^[Yy]$ ]]; then
    echo "📦 Adding PostgreSQL..."
    railway add postgresql
fi

# Set environment variables
echo "⚙️  Setting environment variables..."
read -p "Set SECRET_KEY? (y/n): " set_secret
if [[ $set_secret =~ ^[Yy]$ ]]; then
    read -p "Enter SECRET_KEY: " secret_key
    railway variables set SECRET_KEY="$secret_key"
fi

railway variables set RAILWAY_ENVIRONMENT=production

# Deploy
echo "🚀 Deploying to Railway..."
railway deploy

echo ""
echo "✅ Deployment complete!"
echo "🌐 Your app should be available at your Railway URL"
echo "🔑 Default login: admin / admin123"
echo ""
echo "📊 Next steps:"
echo "1. Check Railway dashboard for your app URL"
echo "2. Login with admin credentials"
echo "3. Create additional users via registration"
echo "4. Start managing your IT business!"

echo ""
echo "🛠️  Useful commands:"
echo "railway logs        - View application logs"
echo "railway open        - Open app in browser"
echo "railway status      - Check deployment status"
