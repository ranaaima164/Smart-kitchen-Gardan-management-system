"""Smart Kitchen Garden Management System - Main Application"""
import os
from app import create_app, db
from app.models import User, Plant, Schedule, CareTips

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()
        print("Smart Kitchen Garden Management System Running")
        print("Database initialized successfully")
        print("Server running at http://localhost:5000")
    
    # Run the Flask application
    app.run(debug=True, host='0.0.0.0', port=5000)
