# # app.py - Complete Flask API for Homoeopathic Clinic
# from flask import Flask, request, jsonify, send_from_directory, render_template
# from flask_cors import CORS
# import json
# import os
# from datetime import datetime
# from typing import Dict, List, Any
# import uuid

# app = Flask(__name__, static_folder='static', template_folder='templates')
# CORS(app)  # Enable CORS for all routes

# # Data storage file
# DATA_FILE = 'clinic_data.json'

# class ClinicDataManager:
#     """Manages clinic data storage and operations"""
    
#     def __init__(self, data_file: str):
#         self.data_file = data_file
#         self.data = self._load_data()
    
#     def _load_data(self) -> Dict[str, Any]:
#         """Load data from JSON file or create initial data"""
#         if os.path.exists(self.data_file):
#             try:
#                 with open(self.data_file, 'r', encoding='utf-8') as f:
#                     return json.load(f)
#             except (json.JSONDecodeError, IOError) as e:
#                 print(f"Error loading data file: {e}")
#                 return self._create_initial_data()
#         else:
#             return self._create_initial_data()
    
#     def _create_initial_data(self) -> Dict[str, Any]:
#         """Create initial data structure"""
#         return {
#             "patients": [],
#             "messages": [],
#             "settings": {
#                 "clinic_name": "Sai Homoeopathic Treatment",
#                 "phone": "+91 7005602518",
#                 "email": "saihomeopathytreatment@gmail.com",
#                 "address": "Khoo Bazar, Opposite Saraswati Vidya Mandir Paprola, Kasba Paprola, Himachal Pradesh 176115",
#                 "hours": {
#                     "monday": "Closed",
#                     "tuesday": "9:00 AM - 8:00 PM",
#                     "wednesday": "9:00 AM - 8:00 PM",
#                     "thursday": "9:00 AM - 8:00 PM",
#                     "friday": "9:00 AM - 8:00 PM",
#                     "saturday": "9:00 AM - 8:00 PM",
#                     "sunday": "9:00 AM - 8:00 PM"
#                 }
#             },
#             "next_patient_id": 1,
#             "users": [
#                 {
#                     "username": "admin",
#                     "password": "admin123",  # In production, use hashed passwords
#                     "role": "admin"
#                 }
#             ]
#         }
    
#     def save_data(self) -> bool:
#         """Save data to JSON file"""
#         try:
#             with open(self.data_file, 'w', encoding='utf-8') as f:
#                 json.dump(self.data, f, indent=2, default=str)
#             return True
#         except IOError as e:
#             print(f"Error saving data: {e}")
#             return False
    
#     def generate_patient_id(self) -> str:
#         """Generate unique patient ID"""
#         patient_id = self.data["next_patient_id"]
#         self.data["next_patient_id"] += 1
#         return f"SAI-{patient_id:03d}"
    
#     def get_statistics(self) -> Dict[str, Any]:
#         """Calculate dashboard statistics"""
#         patients = self.data["patients"]
#         messages = self.data["messages"]
#         now = datetime.now()
        
#         # This month vs last month
#         current_month = now.month
#         current_year = now.year
        
#         this_month_patients = [
#             p for p in patients 
#             if datetime.strptime(p["registration_date"], "%Y-%m-%d").month == current_month
#             and datetime.strptime(p["registration_date"], "%Y-%m-%d").year == current_year
#         ]
        
#         # Revenue calculation
#         this_month_revenue = sum(float(p.get("total_fee", 0)) for p in this_month_patients)
        
#         # Disease distribution
#         diseases = {}
#         for patient in patients:
#             disease = patient.get("disease", "Unknown")
#             diseases[disease] = diseases.get(disease, 0) + 1
        
#         return {
#             "total_patients": len(patients),
#             "new_patients_this_month": len([p for p in this_month_patients if p.get("type") == "new"]),
#             "monthly_revenue": this_month_revenue,
#             "pending_messages": len([m for m in messages if m.get("status") == "new"]),
#             "disease_distribution": [{"name": k, "count": v} for k, v in diseases.items()]
#         }

# # Initialize data manager
# data_manager = ClinicDataManager(DATA_FILE)

# # ============ HELPER FUNCTIONS ============
# def validate_patient_data(data: Dict[str, Any]) -> tuple[bool, str]:
#     """Validate patient data"""
#     required_fields = ["name", "phone", "disease"]
#     for field in required_fields:
#         if field not in data or not data[field]:
#             return False, f"Missing required field: {field}"
    
#     if "age" in data and not isinstance(data["age"], (int, str)):
#         return False, "Age must be a number"
    
#     return True, ""

# def format_response(data: Any, success: bool = True, message: str = "", status: int = 200):
#     """Standard response format"""
#     return jsonify({
#         "success": success,
#         "message": message,
#         "data": data
#     }), status

# # ============ ROUTES ============

# @app.route('/')
# def index():
#     """Serve main website"""
#     return render_template('index.html')

# @app.route('/admin')
# def admin():
#     """Serve admin dashboard"""
#     return render_template('admin.html')

# # ============ API ROUTES ============

# # 1. Clinic Information
# @app.route('/api/info', methods=['GET'])
# def get_clinic_info():
#     """Get clinic information and statistics"""
#     stats = data_manager.get_statistics()
#     return format_response({
#         "clinic_info": data_manager.data["settings"],
#         "statistics": stats
#     })

# # 2. Patient Management
# @app.route('/api/patients', methods=['GET'])
# def get_patients():
#     """Get all patients with optional filtering"""
#     patients = data_manager.data["patients"]
    
#     # Apply filters
#     name_filter = request.args.get('name', '').lower()
#     type_filter = request.args.get('type', '')
#     status_filter = request.args.get('status', '')
    
#     filtered_patients = patients
    
#     if name_filter:
#         filtered_patients = [
#             p for p in filtered_patients 
#             if name_filter in p.get("name", "").lower() 
#             or name_filter in p.get("disease", "").lower()
#             or name_filter in p.get("patient_id", "").lower()
#         ]
    
#     if type_filter:
#         filtered_patients = [p for p in filtered_patients if p.get("type") == type_filter]
    
#     if status_filter:
#         filtered_patients = [p for p in filtered_patients if p.get("status") == status_filter]
    
#     return format_response(filtered_patients)

# @app.route('/api/patients/<int:patient_id>', methods=['GET'])
# def get_patient(patient_id: int):
#     """Get specific patient by ID"""
#     patient = next((p for p in data_manager.data["patients"] if p.get("id") == patient_id), None)
    
#     if patient:
#         return format_response(patient)
#     else:
#         return format_response(None, False, "Patient not found", 404)

# @app.route('/api/patients', methods=['POST'])
# def create_patient():
#     """Create new patient"""
#     try:
#         data = request.get_json()
        
#         # Validate data
#         is_valid, message = validate_patient_data(data)
#         if not is_valid:
#             return format_response(None, False, message, 400)
        
#         # Generate patient ID
#         patient_id = data_manager.generate_patient_id()
        
#         # Create patient object
#         patient = {
#             "id": data_manager.data["next_patient_id"],
#             "patient_id": patient_id,
#             "name": data["name"],
#             "phone": data["phone"],
#             "disease": data["disease"],
#             "type": data.get("type", "new"),
#             "registration_date": data.get("registration_date", datetime.now().strftime("%Y-%m-%d")),
#             "age": data.get("age"),
#             "gender": data.get("gender"),
#             "email": data.get("email"),
#             "address": data.get("address"),
#             "disease_duration": data.get("disease_duration"),
#             "symptoms": data.get("symptoms"),
#             "previous_treatment": data.get("previous_treatment"),
#             "appointment_type": data.get("appointment_type", "consultation"),
#             "consultation_fee": float(data.get("consultation_fee", 0)),
#             "medicine_fee": float(data.get("medicine_fee", 0)),
#             "total_fee": float(data.get("total_fee", 0)),
#             "doctor_notes": data.get("doctor_notes"),
#             "prescription": data.get("prescription"),
#             "next_visit_date": data.get("next_visit_date"),
#             "status": data.get("status", "active"),
#             "visit_count": 1,
#             "last_visit_date": datetime.now().strftime("%Y-%m-%d"),
#             "created_at": datetime.now().isoformat()
#         }
        
#         # Calculate total fee if not provided
#         if patient["total_fee"] == 0:
#             patient["total_fee"] = patient["consultation_fee"] + patient["medicine_fee"]
        
#         # Add to patients list
#         data_manager.data["patients"].append(patient)
        
#         # Save data
#         if data_manager.save_data():
#             return format_response(patient, message=f"Patient {patient['name']} created successfully")
#         else:
#             return format_response(None, False, "Failed to save patient", 500)
            
#     except Exception as e:
#         return format_response(None, False, f"Error creating patient: {str(e)}", 500)

# @app.route('/api/patients/<int:patient_id>', methods=['PUT'])
# def update_patient(patient_id: int):
#     """Update existing patient"""
#     try:
#         data = request.get_json()
        
#         # Find patient
#         patients = data_manager.data["patients"]
#         patient_index = next((i for i, p in enumerate(patients) if p.get("id") == patient_id), None)
        
#         if patient_index is None:
#             return format_response(None, False, "Patient not found", 404)
        
#         # Update patient data
#         patients[patient_index].update({
#             **data,
#             "last_visit_date": datetime.now().strftime("%Y-%m-%d"),
#             "visit_count": patients[patient_index].get("visit_count", 1) + 1,
#             "updated_at": datetime.now().isoformat()
#         })
        
#         # Save data
#         if data_manager.save_data():
#             return format_response(patients[patient_index], message="Patient updated successfully")
#         else:
#             return format_response(None, False, "Failed to update patient", 500)
            
#     except Exception as e:
#         return format_response(None, False, f"Error updating patient: {str(e)}", 500)

# @app.route('/api/patients/<int:patient_id>', methods=['DELETE'])
# def delete_patient(patient_id: int):
#     """Delete patient"""
#     patients = data_manager.data["patients"]
#     patient_index = next((i for i, p in enumerate(patients) if p.get("id") == patient_id), None)
    
#     if patient_index is None:
#         return format_response(None, False, "Patient not found", 404)
    
#     # Remove patient
#     deleted_patient = patients.pop(patient_index)
    
#     # Save data
#     if data_manager.save_data():
#         return format_response(deleted_patient, message="Patient deleted successfully")
#     else:
#         return format_response(None, False, "Failed to delete patient", 500)

# # 3. Patient Search (for typeahead)
# @app.route('/api/patients/search', methods=['GET'])
# def search_patients():
#     """Search patients by name (for typeahead) - Returns COMPLETE patient data"""
#     query = request.args.get('q', '').lower()
    
#     if len(query) < 3:  # Changed to 3 characters minimum
#         return format_response([])
    
#     patients = data_manager.data["patients"]
#     matches = []
    
#     for patient in patients:
#         if query in patient.get("name", "").lower():
#             # Return the COMPLETE patient object with ALL fields
#             matches.append(patient)  # ← KEY FIX: Returns complete patient, not just selected fields
    
#     return format_response(matches[:10])

# # 4. Dashboard Statistics
# @app.route('/api/dashboard/stats', methods=['GET'])
# def get_dashboard_stats():
#     """Get dashboard statistics"""
#     stats = data_manager.get_statistics()
#     return format_response(stats)

# # 5. Message Management
# @app.route('/api/messages', methods=['GET'])
# def get_messages():
#     """Get all messages"""
#     messages = data_manager.data["messages"]
#     return format_response(messages)

# @app.route('/api/messages', methods=['POST'])
# def create_message():
#     """Create new message (contact form)"""
#     try:
#         data = request.get_json()
        
#         # Validate required fields
#         required_fields = ["name", "phone", "message"]
#         for field in required_fields:
#             if field not in data or not data[field]:
#                 return format_response(None, False, f"Missing required field: {field}", 400)
        
#         # Create message object
#         message = {
#             "id": len(data_manager.data["messages"]) + 1,
#             "name": data["name"],
#             "phone": data["phone"],
#             "email": data.get("email"),
#             "appointment_type": data.get("appointment_type", "consultation"),
#             "message": data["message"],
#             "date": datetime.now().isoformat(),
#             "status": "new"
#         }
        
#         # Add to messages
#         data_manager.data["messages"].append(message)
        
#         # Save data
#         if data_manager.save_data():
#             return format_response(message, message="Message sent successfully")
#         else:
#             return format_response(None, False, "Failed to save message", 500)
            
#     except Exception as e:
#         return format_response(None, False, f"Error creating message: {str(e)}", 500)

# @app.route('/api/messages/<int:message_id>', methods=['PUT'])
# def update_message(message_id: int):
#     """Update message (mark as read)"""
#     messages = data_manager.data["messages"]
#     message_index = next((i for i, m in enumerate(messages) if m.get("id") == message_id), None)
    
#     if message_index is None:
#         return format_response(None, False, "Message not found", 404)
    
#     data = request.get_json()
#     messages[message_index].update(data)
    
#     if data_manager.save_data():
#         return format_response(messages[message_index], message="Message updated")
#     else:
#         return format_response(None, False, "Failed to update message", 500)

# @app.route('/api/messages/<int:message_id>', methods=['DELETE'])
# def delete_message(message_id: int):
#     """Delete message"""
#     messages = data_manager.data["messages"]
#     message_index = next((i for i, m in enumerate(messages) if m.get("id") == message_id), None)
    
#     if message_index is None:
#         return format_response(None, False, "Message not found", 404)
    
#     deleted_message = messages.pop(message_index)
    
#     if data_manager.save_data():
#         return format_response(deleted_message, message="Message deleted")
#     else:
#         return format_response(None, False, "Failed to delete message", 500)

# # 6. Authentication
# @app.route('/api/auth/login', methods=['POST'])
# def login():
#     """Admin login"""
#     try:
#         data = request.get_json()
#         username = data.get("username")
#         password = data.get("password")
        
#         # Find user
#         users = data_manager.data["users"]
#         user = next((u for u in users if u["username"] == username and u["password"] == password), None)
        
#         if user:
#             # In production, generate a proper JWT token
#             token = str(uuid.uuid4())
#             return format_response({
#                 "token": token,
#                 "user": {
#                     "username": user["username"],
#                     "role": user["role"]
#                 }
#             }, message="Login successful")
#         else:
#             return format_response(None, False, "Invalid credentials", 401)
            
#     except Exception as e:
#         return format_response(None, False, f"Login error: {str(e)}", 500)

# @app.route('/api/auth/verify', methods=['POST'])
# def verify_token():
#     """Verify authentication token"""
#     # In production, implement proper JWT verification
#     return format_response({"valid": True})

# # 7. Settings Management
# @app.route('/api/settings', methods=['GET'])
# def get_settings():
#     """Get clinic settings"""
#     return format_response(data_manager.data["settings"])

# @app.route('/api/settings', methods=['PUT'])
# def update_settings():
#     """Update clinic settings"""
#     try:
#         data = request.get_json()
#         data_manager.data["settings"].update(data)
        
#         if data_manager.save_data():
#             return format_response(data_manager.data["settings"], message="Settings updated")
#         else:
#             return format_response(None, False, "Failed to update settings", 500)
            
#     except Exception as e:
#         return format_response(None, False, f"Error updating settings: {str(e)}", 500)

# # ============ ERROR HANDLERS ============
# @app.errorhandler(404)
# def not_found(error):
#     return format_response(None, False, "Resource not found", 404)

# @app.errorhandler(500)
# def server_error(error):
#     return format_response(None, False, "Internal server error", 500)

# # ============ MAIN ENTRY POINT ============
# if __name__ == '__main__':
#     # Create necessary directories
#     os.makedirs('templates', exist_ok=True)
#     os.makedirs('static', exist_ok=True)
    
#     print("\n" + "="*60)
#     print("SAI HOMOEOPATHIC CLINIC MANAGEMENT SYSTEM")
#     print("="*60)
#     print(f"API URL: http://localhost:5000")
#     print(f"Website: http://localhost:5000")
#     print(f"Admin Panel: http://localhost:5000/admin")
#     print("="*60)
#     print("\nAvailable endpoints:")
#     print("  GET  /api/info           - Clinic information")
#     print("  GET  /api/patients       - List patients")
#     print("  POST /api/patients       - Create patient")
#     print("  GET  /api/dashboard/stats - Dashboard statistics")
#     print("  POST /api/messages       - Contact form")
#     print("  POST /api/auth/login     - Admin login")
#     print("="*60)
#     print("\nAdmin credentials:")
#     print("  Username: admin")
#     print("  Password: admin123")
#     print("="*60 + "\n")
    
#     app.run(debug=True, host='0.0.0.0', port=5000)





from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
import uuid

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)  # Enable CORS for all routes

# Data storage file
DATA_FILE = 'clinic_data.json'

class ClinicDataManager:
    """Manages clinic data storage and operations"""
    
    def __init__(self, data_file: str):
        self.data_file = data_file
        self.data = self._load_data()
    
    def _load_data(self) -> Dict[str, Any]:
        """Load data from JSON file or create initial data"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading data file: {e}")
                return self._create_initial_data()
        else:
            return self._create_initial_data()
    
    def _create_initial_data(self) -> Dict[str, Any]:
        """Create initial data structure"""
        return {
            "patients": [],
            "messages": [],
            "settings": {
                "clinic_name": "Sai Homoeopathic Treatment",
                "phone": "+91 7005602518",
                "email": "saihomeopathytreatment@gmail.com",
                "address": "Khoo Bazar, Opposite Saraswati Vidya Mandir Paprola, Kasba Paprola, Himachal Pradesh 176115",
                "hours": {
                    "monday": "Closed",
                    "tuesday": "9:00 AM - 8:00 PM",
                    "wednesday": "9:00 AM - 8:00 PM",
                    "thursday": "9:00 AM - 8:00 PM",
                    "friday": "9:00 AM - 8:00 PM",
                    "saturday": "9:00 AM - 8:00 PM",
                    "sunday": "9:00 AM - 8:00 PM"
                }
            },
            "next_patient_id": 1,
            "users": [
                {
                    "username": "admin",
                    "password": "admin123",  # In production, use hashed passwords
                    "role": "admin"
                }
            ]
        }
    
    def save_data(self) -> bool:
        """Save data to JSON file"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, default=str)
            return True
        except IOError as e:
            print(f"Error saving data: {e}")
            return False
    
    def generate_patient_id(self) -> str:
        """Generate unique patient ID"""
        patient_id = self.data["next_patient_id"]
        self.data["next_patient_id"] += 1
        return f"SAI-{patient_id:03d}"
    
    def get_statistics(self) -> Dict[str, Any]:
        """Calculate dashboard statistics"""
        patients = self.data["patients"]
        messages = self.data["messages"]
        now = datetime.now()
        
        # This month vs last month
        current_month = now.month
        current_year = now.year
        
        this_month_patients = [
            p for p in patients 
            if datetime.strptime(p["registration_date"], "%Y-%m-%d").month == current_month
            and datetime.strptime(p["registration_date"], "%Y-%m-%d").year == current_year
        ]
        
        # Revenue calculation
        this_month_revenue = sum(float(p.get("total_fee", 0)) for p in this_month_patients)
        
        # Disease distribution
        diseases = {}
        for patient in patients:
            disease = patient.get("disease", "Unknown")
            diseases[disease] = diseases.get(disease, 0) + 1
        
        return {
            "total_patients": len(patients),
            "new_patients_this_month": len([p for p in this_month_patients if p.get("type") == "new"]),
            "monthly_revenue": this_month_revenue,
            "pending_messages": len([m for m in messages if m.get("status") == "new"]),
            "disease_distribution": [{"name": k, "count": v} for k, v in diseases.items()]
        }
    
    def get_analytics_data(self, year: int) -> List[Dict[str, Any]]:
        """Get analytics data for a specific year"""
        patients = self.data["patients"]
        
        # Filter patients by year
        year_patients = [
            p for p in patients 
            if datetime.strptime(p["registration_date"], "%Y-%m-%d").year == year
        ]
        
        # Monthly data
        monthly_data = []
        for month_num in range(1, 13):
            month_patients = [
                p for p in year_patients 
                if datetime.strptime(p["registration_date"], "%Y-%m-%d").month == month_num
            ]
            
            # Current month stats
            month_revenue = sum(float(p.get("total_fee", 0)) for p in month_patients)
            month_new_patients = len(month_patients)
            
            # Calculate total patients up to this month
            month_total_patients = len([
                p for p in year_patients 
                if datetime.strptime(p["registration_date"], "%Y-%m-%d").month <= month_num
            ])
            
            # Previous month for comparison
            prev_month_num = month_num - 1 if month_num > 1 else 12
            prev_year = year if month_num > 1 else year - 1
            prev_month_patients = [
                p for p in self.data["patients"]
                if datetime.strptime(p["registration_date"], "%Y-%m-%d").month == prev_month_num
                and datetime.strptime(p["registration_date"], "%Y-%m-%d").year == prev_year
            ]
            
            prev_month_revenue = sum(float(p.get("total_fee", 0)) for p in prev_month_patients)
            prev_month_patients_count = len(prev_month_patients)
            
            # Calculate growth percentages
            revenue_growth = self.calculate_growth(prev_month_revenue, month_revenue)
            patient_growth = self.calculate_growth(prev_month_patients_count, month_new_patients)
            avg_fee = month_revenue / month_new_patients if month_new_patients > 0 else 0
            
            monthly_data.append({
                "month_num": month_num,  # Add month number for sorting/filtering
                "month": datetime(year, month_num, 1).strftime("%b %Y"),
                "revenue": round(month_revenue, 2),
                "newPatients": month_new_patients,
                "totalPatients": month_total_patients,
                "revenueGrowth": revenue_growth,
                "patientGrowth": patient_growth,
                "avgFeePerPatient": round(avg_fee, 2)
            })
        
        return monthly_data
    
    def calculate_growth(self, previous: float, current: float) -> float:
        """Calculate percentage growth"""
        if previous == 0:
            return 100.0 if current > 0 else 0.0
        return round(((current - previous) / previous) * 100, 1)
    
    def get_yearly_comparison(self) -> List[Dict[str, Any]]:
        """Get yearly comparison data"""
        patients = self.data["patients"]
        
        # Get all years with patient data
        available_years = sorted(set(
            datetime.strptime(p["registration_date"], "%Y-%m-%d").year 
            for p in patients
        ))
        
        yearly_data = []
        for year in available_years:
            year_patients = [
                p for p in patients 
                if datetime.strptime(p["registration_date"], "%Y-%m-%d").year == year
            ]
            year_revenue = sum(float(p.get("total_fee", 0)) for p in year_patients)
            
            # Calculate growth from previous year
            prev_year = year - 1
            prev_year_patients = [
                p for p in patients 
                if datetime.strptime(p["registration_date"], "%Y-%m-%d").year == prev_year
            ]
            prev_year_revenue = sum(float(p.get("total_fee", 0)) for p in prev_year_patients)
            growth = self.calculate_growth(prev_year_revenue, year_revenue)
            
            yearly_data.append({
                "year": year,
                "totalRevenue": round(year_revenue, 2),
                "totalPatients": len(year_patients),
                "growth": growth
            })
        
        return yearly_data, available_years

# Initialize data manager
data_manager = ClinicDataManager(DATA_FILE)

# ============ HELPER FUNCTIONS ============
def validate_patient_data(data: Dict[str, Any]) -> tuple[bool, str]:
    """Validate patient data"""
    required_fields = ["name", "phone", "disease"]
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"Missing required field: {field}"
    
    if "age" in data and not isinstance(data["age"], (int, str)):
        return False, "Age must be a number"
    
    return True, ""

def format_response(data: Any, success: bool = True, message: str = "", status: int = 200):
    """Standard response format"""
    return jsonify({
        "success": success,
        "message": message,
        "data": data
    }), status

# ============ ROUTES ============

@app.route('/')
def index():
    """Serve main website"""
    return render_template('index.html')

@app.route('/admin')
def admin():
    """Serve admin dashboard"""
    return render_template('admin.html')

# ============ API ROUTES ============

# 1. Clinic Information
@app.route('/api/info', methods=['GET'])
def get_clinic_info():
    """Get clinic information and statistics"""
    stats = data_manager.get_statistics()
    return format_response({
        "clinic_info": data_manager.data["settings"],
        "statistics": stats
    })

# 2. Patient Management
@app.route('/api/patients', methods=['GET'])
def get_patients():
    """Get all patients with optional filtering"""
    patients = data_manager.data["patients"]
    
    # Apply filters
    name_filter = request.args.get('name', '').lower()
    type_filter = request.args.get('type', '')
    status_filter = request.args.get('status', '')
    
    filtered_patients = patients
    
    if name_filter:
        filtered_patients = [
            p for p in filtered_patients 
            if name_filter in p.get("name", "").lower() 
            or name_filter in p.get("disease", "").lower()
            or name_filter in p.get("patient_id", "").lower()
        ]
    
    if type_filter:
        filtered_patients = [p for p in filtered_patients if p.get("type") == type_filter]
    
    if status_filter:
        filtered_patients = [p for p in filtered_patients if p.get("status") == status_filter]
    
    return format_response(filtered_patients)

@app.route('/api/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id: int):
    """Get specific patient by ID"""
    patient = next((p for p in data_manager.data["patients"] if p.get("id") == patient_id), None)
    
    if patient:
        return format_response(patient)
    else:
        return format_response(None, False, "Patient not found", 404)

@app.route('/api/patients', methods=['POST'])
def create_patient():
    """Create new patient (FIXED VERSION)"""
    try:
        data = request.get_json(force=True)

        # ---------------- Validate ----------------
        is_valid, message = validate_patient_data(data)
        if not is_valid:
            return format_response(None, False, message, 400)

        # ---------------- Generate IDs SAFELY ----------------
        numeric_id = data_manager.data["next_patient_id"]
        patient_id = f"SAI-{numeric_id:03d}"
        data_manager.data["next_patient_id"] += 1

        # ---------------- Fees (safe float conversion) ----------------
        consultation_fee = float(data.get("consultation_fee") or 0)
        medicine_fee = float(data.get("medicine_fee") or 0)
        total_fee = float(data.get("total_fee") or 0)

        if total_fee == 0:
            total_fee = consultation_fee + medicine_fee

        # ---------------- Create Patient ----------------
        patient = {
            "id": numeric_id,
            "patient_id": patient_id,
            "name": data["name"],
            "phone": data["phone"],
            "disease": data["disease"],
            "type": data.get("type", "new"),
            "registration_date": data.get("registration_date", datetime.now().strftime("%Y-%m-%d")),
            "age": data.get("age"),
            "gender": data.get("gender"),
            "email": data.get("email"),
            "address": data.get("address"),
            "disease_duration": data.get("disease_duration"),
            "symptoms": data.get("symptoms"),
            "previous_treatment": data.get("previous_treatment"),
            "appointment_type": data.get("appointment_type", "consultation"),
            "consultation_fee": consultation_fee,
            "medicine_fee": medicine_fee,
            "total_fee": total_fee,
            "doctor_notes": data.get("doctor_notes"),
            "prescription": data.get("prescription"),
            "next_visit_date": data.get("next_visit_date"),
            "status": data.get("status", "active"),
            "visit_count": 1,
            "last_visit_date": datetime.now().strftime("%Y-%m-%d"),
            "created_at": datetime.now().isoformat()
        }

        # ---------------- Save ----------------
        data_manager.data["patients"].append(patient)

        if not data_manager.save_data():
            return format_response(None, False, "Failed to save patient", 500)

        return format_response(patient, True, f"Patient {patient['name']} created successfully")

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return format_response(None, False, f"Error creating patient: {str(e)}", 500)


@app.route('/api/patients/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id: int):
    """Update existing patient"""
    try:
        data = request.get_json()
        
        # Find patient
        patients = data_manager.data["patients"]
        patient_index = next((i for i, p in enumerate(patients) if p.get("id") == patient_id), None)
        
        if patient_index is None:
            return format_response(None, False, "Patient not found", 404)
        
        # Update patient data
        patients[patient_index].update({
            **data,
            "last_visit_date": datetime.now().strftime("%Y-%m-%d"),
            "visit_count": patients[patient_index].get("visit_count", 1) + 1,
            "updated_at": datetime.now().isoformat()
        })
        
        # Save data
        if data_manager.save_data():
            return format_response(patients[patient_index], message="Patient updated successfully")
        else:
            return format_response(None, False, "Failed to update patient", 500)
            
    except Exception as e:
        return format_response(None, False, f"Error updating patient: {str(e)}", 500)

@app.route('/api/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id: int):
    """Delete patient"""
    patients = data_manager.data["patients"]
    patient_index = next((i for i, p in enumerate(patients) if p.get("id") == patient_id), None)
    
    if patient_index is None:
        return format_response(None, False, "Patient not found", 404)
    
    # Remove patient
    deleted_patient = patients.pop(patient_index)
    
    # Save data
    if data_manager.save_data():
        return format_response(deleted_patient, message="Patient deleted successfully")
    else:
        return format_response(None, False, "Failed to delete patient", 500)

# 3. Patient Search (for typeahead)
@app.route('/api/patients/search', methods=['GET'])
def search_patients():
    """Search patients by name (for typeahead) - Returns COMPLETE patient data"""
    query = request.args.get('q', '').lower()
    
    if len(query) < 2:
        return format_response([])
    
    patients = data_manager.data["patients"]
    type_filter = request.args.get('type', '')
    
    matches = []
    for patient in patients:
        if query in patient.get("name", "").lower():
            if type_filter and patient.get("type") != type_filter:
                continue
            matches.append(patient)
    
    return format_response(matches[:10])

# 4. Dashboard Statistics
@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """Get dashboard statistics"""
    stats = data_manager.get_statistics()
    return format_response(stats)

# 5. Analytics Data
# 5. Analytics Data - FIXED VERSION
@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Get analytics data for dashboard"""
    try:
        period = request.args.get('period', 'monthly')
        year = int(request.args.get('year', datetime.now().year))
        
        # Get monthly data for the year
        monthly_data = data_manager.get_analytics_data(year)
        
        # Get yearly comparison data
        yearly_data, available_years = data_manager.get_yearly_comparison()
        
        # Current date for calculations
        now = datetime.now()
        current_month_num = now.month if now.year == year else 12
        
        # Find current month data and previous month data
        current_month_data = None
        prev_month_data = None
        
        for data in monthly_data:
            # Extract month number from the month string (e.g., "Feb 2026" -> month 2)
            month_num = datetime.strptime(data["month"], "%b %Y").month
            if month_num == current_month_num:
                current_month_data = data
            elif month_num == current_month_num - 1:
                prev_month_data = data
        
        # If current month not found, use last available month
        if not current_month_data and monthly_data:
            current_month_data = monthly_data[-1]
        
        # Calculate YTD revenue (sum of revenue for months up to current month)
        ytd_revenue = 0
        for data in monthly_data:
            month_num = datetime.strptime(data["month"], "%b %Y").month
            if month_num <= current_month_num:
                ytd_revenue += data["revenue"]
        
        # Calculate YTD growth compared to previous year
        ytd_growth = 0
        if year > min(available_years, default=year):
            prev_year = year - 1
            prev_year_monthly_data = data_manager.get_analytics_data(prev_year)
            prev_year_ytd_revenue = 0
            for data in prev_year_monthly_data:
                month_num = datetime.strptime(data["month"], "%b %Y").month
                if month_num <= current_month_num:
                    prev_year_ytd_revenue += data["revenue"]
            ytd_growth = data_manager.calculate_growth(prev_year_ytd_revenue, ytd_revenue)
        
        # Calculate average revenue growth
        avg_revenue_growth = 0
        if current_month_data and prev_month_data:
            avg_revenue_growth = data_manager.calculate_growth(
                prev_month_data["avgFeePerPatient"],
                current_month_data["avgFeePerPatient"]
            )
        
        # Prepare summary data
        summary = {
            "currentRevenue": current_month_data["revenue"] if current_month_data else 0,
            "currentPatients": current_month_data["newPatients"] if current_month_data else 0,
            "revenueGrowth": current_month_data["revenueGrowth"] if current_month_data else 0,
            "patientGrowth": current_month_data["patientGrowth"] if current_month_data else 0,
            "avgRevenuePerPatient": current_month_data["avgFeePerPatient"] if current_month_data else 0,
            "avgRevenueGrowth": avg_revenue_growth,
            "ytdRevenue": round(ytd_revenue, 2),
            "ytdGrowth": ytd_growth
        }
        
        # Prepare chart data based on period
        if period == 'quarterly':
            # Group by quarters
            labels = ['Q1', 'Q2', 'Q3', 'Q4']
            revenue = [0, 0, 0, 0]
            patients = [0, 0, 0, 0]
            
            for data in monthly_data:
                # Extract month number to determine quarter
                month_num = datetime.strptime(data["month"], "%b %Y").month
                quarter_index = (month_num - 1) // 3
                if quarter_index < 4:
                    revenue[quarter_index] += data["revenue"]
                    patients[quarter_index] += data["newPatients"]
            
            chart_data = {"labels": labels, "revenue": revenue, "patients": patients}
        elif period == 'yearly':
            # Yearly data (last 3 years)
            recent_years = sorted(available_years, reverse=True)[:3]
            recent_years.reverse()  # Show oldest to newest
            
            labels = [str(year) for year in recent_years]
            revenue = []
            patients = []
            
            for y in recent_years:
                year_data = data_manager.get_analytics_data(y)
                year_revenue = sum(data["revenue"] for data in year_data)
                year_patients = sum(data["newPatients"] for data in year_data)
                revenue.append(year_revenue)
                patients.append(year_patients)
            
            chart_data = {"labels": labels, "revenue": revenue, "patients": patients}
        else:  # monthly (default)
            labels = [data["month"] for data in monthly_data]
            revenue = [data["revenue"] for data in monthly_data]
            patients = [data["newPatients"] for data in monthly_data]
            
            chart_data = {"labels": labels, "revenue": revenue, "patients": patients}
        
        return format_response({
            "summary": summary,
            "monthlyData": monthly_data,
            "yearlyData": yearly_data,
            "chartData": chart_data,
            "availableYears": available_years
        })
        
    except Exception as e:
        import traceback
        print(f"Error in analytics: {str(e)}")
        print(traceback.format_exc())
        return format_response(None, False, f"Error loading analytics: {str(e)}", 500)

# 6. Message Management
@app.route('/api/messages', methods=['GET'])
def get_messages():
    """Get all messages"""
    messages = data_manager.data["messages"]
    return format_response(messages)

@app.route('/api/messages', methods=['POST'])
def create_message():
    """Create new message (contact form)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ["name", "phone", "message"]
        for field in required_fields:
            if field not in data or not data[field]:
                return format_response(None, False, f"Missing required field: {field}", 400)
        
        # Create message object
        message = {
            "id": len(data_manager.data["messages"]) + 1,
            "name": data["name"],
            "phone": data["phone"],
            "email": data.get("email"),
            "appointment_type": data.get("appointment_type", "consultation"),
            "message": data["message"],
            "date": datetime.now().isoformat(),
            "status": "new"
        }
        
        # Add to messages
        data_manager.data["messages"].append(message)
        
        # Save data
        if data_manager.save_data():
            return format_response(message, message="Message sent successfully")
        else:
            return format_response(None, False, "Failed to save message", 500)
            
    except Exception as e:
        return format_response(None, False, f"Error creating message: {str(e)}", 500)

@app.route('/api/messages/<int:message_id>', methods=['PUT'])
def update_message(message_id: int):
    """Update message (mark as read)"""
    messages = data_manager.data["messages"]
    message_index = next((i for i, m in enumerate(messages) if m.get("id") == message_id), None)
    
    if message_index is None:
        return format_response(None, False, "Message not found", 404)
    
    data = request.get_json()
    messages[message_index].update(data)
    
    if data_manager.save_data():
        return format_response(messages[message_index], message="Message updated")
    else:
        return format_response(None, False, "Failed to update message", 500)

@app.route('/api/messages/<int:message_id>', methods=['DELETE'])
def delete_message(message_id: int):
    """Delete message"""
    messages = data_manager.data["messages"]
    message_index = next((i for i, m in enumerate(messages) if m.get("id") == message_id), None)
    
    if message_index is None:
        return format_response(None, False, "Message not found", 404)
    
    deleted_message = messages.pop(message_index)
    
    if data_manager.save_data():
        return format_response(deleted_message, message="Message deleted")
    else:
        return format_response(None, False, "Failed to delete message", 500)

# 7. Authentication
@app.route('/api/auth/login', methods=['POST'])
def login():
    """Admin login"""
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        
        # Find user
        users = data_manager.data["users"]
        user = next((u for u in users if u["username"] == username and u["password"] == password), None)
        
        if user:
            # In production, generate a proper JWT token
            token = str(uuid.uuid4())
            return format_response({
                "token": token,
                "user": {
                    "username": user["username"],
                    "role": user["role"]
                }
            }, message="Login successful")
        else:
            return format_response(None, False, "Invalid credentials", 401)
            
    except Exception as e:
        return format_response(None, False, f"Login error: {str(e)}", 500)

@app.route('/api/auth/verify', methods=['POST'])
def verify_token():
    """Verify authentication token"""
    # In production, implement proper JWT verification
    return format_response({"valid": True})

# 8. Settings Management
@app.route('/api/settings', methods=['GET'])
def get_settings():
    """Get clinic settings"""
    return format_response(data_manager.data["settings"])

@app.route('/api/settings', methods=['PUT'])
def update_settings():
    """Update clinic settings"""
    try:
        data = request.get_json()
        data_manager.data["settings"].update(data)
        
        if data_manager.save_data():
            return format_response(data_manager.data["settings"], message="Settings updated")
        else:
            return format_response(None, False, "Failed to update settings", 500)
            
    except Exception as e:
        return format_response(None, False, f"Error updating settings: {str(e)}", 500)

# ============ ERROR HANDLERS ============
@app.errorhandler(404)
def not_found(error):
    return format_response(None, False, "Resource not found", 404)

@app.errorhandler(500)
def server_error(error):
    return format_response(None, False, "Internal server error", 500)

# ============ MAIN ENTRY POINT ============
if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("\n" + "="*60)
    print("SAI HOMOEOPATHIC CLINIC MANAGEMENT SYSTEM")
    print("="*60)
    print(f"API URL: http://localhost:5000")
    print(f"Website: http://localhost:5000")
    print(f"Admin Panel: http://localhost:5000/admin")
    print("="*60)
    print("\nAvailable endpoints:")
    print("  GET  /api/info           - Clinic information")
    print("  GET  /api/patients       - List patients")
    print("  POST /api/patients       - Create patient")
    print("  GET  /api/dashboard/stats - Dashboard statistics")
    print("  GET  /api/analytics      - Analytics data")
    print("  POST /api/messages       - Contact form")
    print("  POST /api/auth/login     - Admin login")
    print("="*60)
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)