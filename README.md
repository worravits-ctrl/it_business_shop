# IT Business Shop - Flask app

This is a minimal Flask app for recording income and expenses for an IT business shop.
- Login (admin created by init_db.py: admin / admin123)
- Add/Edit/Delete entries
- CSV import/export
- Dashboard with quick sums and 7-day chart (Chart.js)
- SQLite database (data.db)

Run:
```
pip install -r requirements.txt
python init_db.py  # creates data.db and admin user
flask run --app app.py --debug
```
