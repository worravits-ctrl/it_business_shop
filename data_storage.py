"""
Emergency Data Storage - JSON File Based
เก็บข้อมูลในไฟล์ JSON แทนฐานข้อมูล
"""

import json
import os
from datetime import datetime

class EmergencyDataStore:
    def __init__(self, data_dir="emergency_data"):
        self.data_dir = data_dir
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def save_entry(self, entry_data):
        """บันทึกรายการใหม่"""
        entries_file = os.path.join(self.data_dir, "entries.json")
        
        # โหลดข้อมูลเก่า
        entries = self.load_entries()
        
        # เพิ่มข้อมูลใหม่
        entry_data['id'] = len(entries) + 1
        entry_data['created_at'] = datetime.now().isoformat()
        entries.append(entry_data)
        
        # บันทึกกลับไปยังไฟล์
        with open(entries_file, 'w', encoding='utf-8') as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)
        
        return entry_data['id']
    
    def load_entries(self):
        """โหลดรายการทั้งหมด"""
        entries_file = os.path.join(self.data_dir, "entries.json")
        
        if not os.path.exists(entries_file):
            return []
        
        try:
            with open(entries_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def delete_entry(self, entry_id):
        """ลบรายการ"""
        entries = self.load_entries()
        entries = [e for e in entries if e.get('id') != entry_id]
        
        entries_file = os.path.join(self.data_dir, "entries.json")
        with open(entries_file, 'w', encoding='utf-8') as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)
    
    def clear_all_entries(self):
        """ลบรายการทั้งหมด"""
        entries_file = os.path.join(self.data_dir, "entries.json")
        with open(entries_file, 'w', encoding='utf-8') as f:
            json.dump([], f)
    
    def save_member(self, member_data):
        """บันทึกสมาชิก"""
        members_file = os.path.join(self.data_dir, "members.json")
        
        members = self.load_members()
        member_data['id'] = len(members) + 1
        member_data['created_at'] = datetime.now().isoformat()
        members.append(member_data)
        
        with open(members_file, 'w', encoding='utf-8') as f:
            json.dump(members, f, ensure_ascii=False, indent=2)
        
        return member_data['id']
    
    def load_members(self):
        """โหลดสมาชิกทั้งหมด"""
        members_file = os.path.join(self.data_dir, "members.json")
        
        if not os.path.exists(members_file):
            return []
        
        try:
            with open(members_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def export_to_csv(self, data_type="entries"):
        """ส่งออกเป็น CSV"""
        import csv
        from io import StringIO
        
        if data_type == "entries":
            data = self.load_entries()
        else:
            data = self.load_members()
        
        if not data:
            return ""
        
        output = StringIO()
        if data:
            writer = csv.DictWriter(output, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        
        return output.getvalue()

# ตัวอย่างการใช้งาน
if __name__ == "__main__":
    store = EmergencyDataStore()
    
    # ทดสอบบันทึกรายการ
    entry = {
        "item_name": "ทดสอบสินค้า",
        "quantity": 10,
        "price": 100.50,
        "category": "อิเล็กทรอนิกส์"
    }
    
    entry_id = store.save_entry(entry)
    print(f"บันทึกรายการ ID: {entry_id}")
    
    # โหลดรายการ
    all_entries = store.load_entries()
    print(f"รายการทั้งหมด: {len(all_entries)} รายการ")
    
    # ส่งออก CSV
    csv_data = store.export_to_csv()
    print(f"CSV Export:\n{csv_data}")