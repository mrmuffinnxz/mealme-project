from flask_login import UserMixin
from datetime import datetime
from mealme_pg import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    last_login = db.Column(db.DateTime, nullable=False, default=datetime.today())
    cal_consume = db.Column(db.Float, nullable=False, default=0)
    cal_needed = db.Column(db.Float, nullable=False, default=2000)
    protein_consume = db.Column(db.Float, nullable=False, default=0)
    protein_needed = db.Column(db.Float, nullable=False, default=50)
    fat_consume = db.Column(db.Float, nullable=False, default=0)
    fat_needed = db.Column(db.Float, nullable=False, default=70)
    carb_consume = db.Column(db.Float, nullable=False, default=0)
    carb_needed = db.Column(db.Float, nullable=False, default=310)
    sugar_consume = db.Column(db.Float, nullable=False, default=0)
    sugar_needed = db.Column(db.Float, nullable=False, default=90)
    sodium_consume = db.Column(db.Float, nullable=False, default=0)
    sodium_needed = db.Column(db.Float, nullable=False, default=3.4)
    prefer_salty = db.Column(db.Float, nullable=False, default=0)
    prefer_sweet = db.Column(db.Float, nullable=False, default=0)
    prefer_sour = db.Column(db.Float, nullable=False, default=0)
    prefer_bitter = db.Column(db.Float, nullable=False, default=0)
    prefer_spicy = db.Column(db.Float, nullable=False, default=0)
    health_score = db.Column(db.String(1000), nullable=False, default="0;0;0;0;0;0;0")
    consume_history = db.Column(db.String(1000), nullable=False, default="-1")
    restrict = db.Column(db.String(1000), nullable=False, default="none")

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    img_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    calories = db.Column(db.Integer, nullable=False)
    protein = db.Column(db.Float, nullable=False, default=0)
    fat = db.Column(db.Float, nullable=False, default=0)
    carb = db.Column(db.Float, nullable=False, default=0)
    sugar = db.Column(db.Float, nullable=False, default=0)
    sodium = db.Column(db.Float, nullable=False, default=0)
    salty = db.Column(db.Float, nullable=False, default=0)
    sweet = db.Column(db.Float, nullable=False, default=0)
    sour = db.Column(db.Float, nullable=False, default=0)
    bitter = db.Column(db.Float, nullable=False, default=0)
    spicy = db.Column(db.Float, nullable=False, default=0)
    restrict = db.Column(db.String(1000), nullable=False, default='none')
    note = db.Column(db.String(1000), nullable=False, default='none')

    def __repr__(self):
        return f"Item('{self.name}', '{self.img_file}', '{self.calories}')"