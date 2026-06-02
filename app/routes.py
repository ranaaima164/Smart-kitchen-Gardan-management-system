"""Routes for Kitchen Garden Management System"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from app import db
from app.models import User, Plant, Garden, Schedule, CareTips
from datetime import datetime, timedelta

main_bp = Blueprint('main', __name__)
api_bp = Blueprint('api', __name__)

# ==================== MAIN ROUTES ====================

@main_bp.route('/')
def index():
    """Home page"""
    total_plants = Plant.query.count()
    total_users = User.query.count()
    return render_template('index.html', total_plants=total_plants, total_users=total_users)

@main_bp.route('/plants')
def plants():
    """Display all plants"""
    plants = Plant.query.all()
    return render_template('plants.html', plants=plants)

@main_bp.route('/plant/<int:plant_id>')
def plant_detail(plant_id):
    """Display plant details"""
    plant = Plant.query.get_or_404(plant_id)
    schedules = Schedule.query.filter_by(plant_id=plant_id).all()
    care_tips = CareTips.query.filter_by(plant_id=plant_id).all()
    return render_template('plant_detail.html', plant=plant, schedules=schedules, care_tips=care_tips)

@main_bp.route('/seasons')
def seasons():
    """Display plants by season"""
    season = request.args.get('season', 'Summer')
    plants = Plant.query.filter_by(best_season=season).all()
    return render_template('seasons.html', plants=plants, season=season)

@main_bp.route('/dashboard')
def dashboard():
    """User dashboard"""
    return render_template('dashboard.html')

# ==================== API ROUTES ====================

@api_bp.route('/plants', methods=['GET'])
def get_plants():
    """Get all plants"""
    plants = Plant.query.all()
    return jsonify([{
        'id': plant.id,
        'name': plant.name,
        'description': plant.description,
        'best_season': plant.best_season,
        'watering_frequency': plant.watering_frequency,
        'sunlight_hours': plant.sunlight_hours,
        'soil_type': plant.soil_type,
        'harvest_days': plant.harvest_days
    } for plant in plants])

@api_bp.route('/plants/<int:plant_id>', methods=['GET'])
def get_plant(plant_id):
    """Get plant details"""
    plant = Plant.query.get_or_404(plant_id)
    return jsonify({
        'id': plant.id,
        'name': plant.name,
        'description': plant.description,
        'best_season': plant.best_season,
        'watering_frequency': plant.watering_frequency,
        'sunlight_hours': plant.sunlight_hours,
        'soil_type': plant.soil_type,
        'ph_level': plant.ph_level,
        'spacing': plant.spacing,
        'harvest_days': plant.harvest_days
    })

@api_bp.route('/plants/season/<season>', methods=['GET'])
def get_plants_by_season(season):
    """Get plants for a specific season"""
    plants = Plant.query.filter_by(best_season=season).all()
    return jsonify([{
        'id': plant.id,
        'name': plant.name,
        'best_season': plant.best_season,
        'sunlight_hours': plant.sunlight_hours
    } for plant in plants])

@api_bp.route('/schedule/<int:plant_id>', methods=['GET'])
def get_schedule(plant_id):
    """Get watering schedule for a plant"""
    schedules = Schedule.query.filter_by(plant_id=plant_id).all()
    return jsonify([{
        'id': schedule.id,
        'task': schedule.task,
        'frequency': schedule.frequency,
        'duration': schedule.duration,
        'notes': schedule.notes
    } for schedule in schedules])

@api_bp.route('/care-tips/<int:plant_id>', methods=['GET'])
def get_care_tips(plant_id):
    """Get care tips for a plant"""
    tips = CareTips.query.filter_by(plant_id=plant_id).all()
    return jsonify([{
        'id': tip.id,
        'category': tip.category,
        'tip': tip.tip,
        'priority': tip.priority
    } for tip in tips])

@api_bp.route('/search', methods=['GET'])
def search_plants():
    """Search plants by name"""
    query = request.args.get('q', '')
    plants = Plant.query.filter(Plant.name.ilike(f'%{query}%')).all()
    return jsonify([{
        'id': plant.id,
        'name': plant.name,
        'description': plant.description[:100] + '...' if plant.description else 'N/A'
    } for plant in plants])

@api_bp.route('/plants', methods=['POST'])
def create_plant():
    """Create a new plant (admin only)"""
    data = request.get_json()
    
    plant = Plant(
        name=data.get('name'),
        description=data.get('description'),
        best_season=data.get('best_season'),
        watering_frequency=data.get('watering_frequency'),
        sunlight_hours=data.get('sunlight_hours', 0),
        soil_type=data.get('soil_type'),
        ph_level=data.get('ph_level'),
        spacing=data.get('spacing'),
        harvest_days=data.get('harvest_days', 0)
    )
    
    db.session.add(plant)
    db.session.commit()
    
    return jsonify({'message': 'Plant created successfully', 'plant_id': plant.id}), 201
