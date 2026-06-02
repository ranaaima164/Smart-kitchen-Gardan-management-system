"""Database Models for Kitchen Garden Management System"""
from app import db
from datetime import datetime

class User(db.Model):
    """User model for storing user information"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(120), default='Unknown')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    gardens = db.relationship('Garden', backref='owner', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'

class Plant(db.Model):
    """Plant model for storing plant information"""
    __tablename__ = 'plants'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    best_season = db.Column(db.String(50), nullable=False)  # Summer, Winter, Year-round
    watering_frequency = db.Column(db.String(100), nullable=False)  # Daily, Alternate days, etc.
    sunlight_hours = db.Column(db.Integer, nullable=False)  # Hours per day
    soil_type = db.Column(db.String(100), nullable=False)  # Loamy, Sandy, etc.
    ph_level = db.Column(db.String(50), nullable=False)  # e.g., 6.0-7.0
    spacing = db.Column(db.String(100), nullable=False)  # Distance between plants
    harvest_days = db.Column(db.Integer, nullable=False)  # Days to harvest
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    schedules = db.relationship('Schedule', backref='plant', lazy=True, cascade='all, delete-orphan')
    care_tips = db.relationship('CareTips', backref='plant', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Plant {self.name}>'

class Garden(db.Model):
    """Garden model for storing user's garden"""
    __tablename__ = 'gardens'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.id'), nullable=False)
    planting_date = db.Column(db.DateTime, nullable=False)
    expected_harvest_date = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='Growing')  # Growing, Harvested, Failed
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    plant = db.relationship('Plant', backref='gardens')
    
    def __repr__(self):
        return f'<Garden {self.id}>'

class Schedule(db.Model):
    """Schedule model for plant care schedules"""
    __tablename__ = 'schedules'
    
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.id'), nullable=False)
    task = db.Column(db.String(100), nullable=False)  # Watering, Fertilizing, Pruning
    frequency = db.Column(db.String(100), nullable=False)  # Daily, Weekly, etc.
    duration = db.Column(db.String(100))  # How long to do the task
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Schedule {self.task} for Plant {self.plant_id}>'

class CareTips(db.Model):
    """CareTips model for plant care instructions"""
    __tablename__ = 'care_tips'
    
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Soil, Sunlight, Watering, Fertilizer, Pest Control
    tip = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), default='Normal')  # Critical, High, Normal, Low
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<CareTips {self.category} for Plant {self.plant_id}>'
