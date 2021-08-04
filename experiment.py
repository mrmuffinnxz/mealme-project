from datetime import datetime, date

last_login = datetime(2020,9,4,15,30).date()
now = datetime.today().date()

print((now - last_login).days)