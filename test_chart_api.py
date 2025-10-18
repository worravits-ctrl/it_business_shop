#!/usr/bin/env python3
"""
ทดสอบ API สำหรับ Chart ข้อมูลรายเดือน
"""
import requests
import json

# ตั้งค่า session
session = requests.Session()
base_url = "http://127.0.0.1:8000"

def test_chart_apis():
    print("🔐 Testing Chart APIs...")
    
    # 1. ล็อกอินก่อน
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    login_response = session.post(f"{base_url}/login", data=login_data)
    if login_response.status_code == 200 and "Dashboard" in login_response.text:
        print("✅ Login successful")
    else:
        print("❌ Login failed")
        return
    
    # 2. ทดสอบ /api/available-months
    print("\n📅 Testing /api/available-months...")
    months_response = session.get(f"{base_url}/api/available-months")
    
    if months_response.status_code == 200:
        months_data = months_response.json()
        print(f"✅ Available months API works!")
        print(f"   Found {len(months_data.get('available', []))} months with data")
        
        # แสดง 5 เดือนแรก
        if months_data.get('available'):
            print("   Latest months:")
            for item in months_data['available'][:5]:
                print(f"     - {item['month']}/{item['year']}")
    else:
        print(f"❌ Available months API failed: {months_response.status_code}")
        print(f"   Response: {months_response.text}")
        return
    
    # 3. ทดสอบ /api/chart-data 
    print("\n📊 Testing /api/chart-data...")
    
    # ใช้เดือนแรกที่มีข้อมูล
    if months_data.get('available'):
        first_month = months_data['available'][0]
        month = first_month['month']
        year = first_month['year']
        
        chart_response = session.get(f"{base_url}/api/chart-data?month={month}&year={year}")
        
        if chart_response.status_code == 200:
            chart_data = chart_response.json()
            print(f"✅ Chart data API works!")
            print(f"   Month/Year: {month}/{year}")
            print(f"   Days in month: {len(chart_data.get('labels', []))}")
            print(f"   Total income: {sum(chart_data.get('incomes', []))}")
            print(f"   Total expenses: {sum(chart_data.get('expenses', []))}")
            
            # แสดงตัวอย่างข้อมูล 3 วันแรก
            labels = chart_data.get('labels', [])
            incomes = chart_data.get('incomes', [])
            expenses = chart_data.get('expenses', [])
            
            print("   Sample data (first 3 days):")
            for i in range(min(3, len(labels))):
                print(f"     {labels[i]}: รายรับ {incomes[i]}, รายจ่าย {expenses[i]}")
                
        else:
            print(f"❌ Chart data API failed: {chart_response.status_code}")
            print(f"   Response: {chart_response.text}")
    
    print("\n🎉 API testing completed!")

if __name__ == "__main__":
    test_chart_apis()