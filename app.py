# from flask import Flask, request, jsonify, send_from_directory, render_template
# from flask_cors import CORS
# import json
# import os
# from datetime import datetime, timedelta
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
    
#     def get_analytics_data(self, year: int) -> List[Dict[str, Any]]:
#         """Get analytics data for a specific year"""
#         patients = self.data["patients"]
        
#         # Filter patients by year
#         year_patients = [
#             p for p in patients 
#             if datetime.strptime(p["registration_date"], "%Y-%m-%d").year == year
#         ]
        
#         # Monthly data
#         monthly_data = []
#         for month_num in range(1, 13):
#             month_patients = [
#                 p for p in year_patients 
#                 if datetime.strptime(p["registration_date"], "%Y-%m-%d").month == month_num
#             ]
            
#             # Current month stats
#             month_revenue = sum(float(p.get("total_fee", 0)) for p in month_patients)
#             month_new_patients = len(month_patients)
            
#             # Calculate total patients up to this month
#             month_total_patients = len([
#                 p for p in year_patients 
#                 if datetime.strptime(p["registration_date"], "%Y-%m-%d").month <= month_num
#             ])
            
#             # Previous month for comparison
#             prev_month_num = month_num - 1 if month_num > 1 else 12
#             prev_year = year if month_num > 1 else year - 1
#             prev_month_patients = [
#                 p for p in self.data["patients"]
#                 if datetime.strptime(p["registration_date"], "%Y-%m-%d").month == prev_month_num
#                 and datetime.strptime(p["registration_date"], "%Y-%m-%d").year == prev_year
#             ]
            
#             prev_month_revenue = sum(float(p.get("total_fee", 0)) for p in prev_month_patients)
#             prev_month_patients_count = len(prev_month_patients)
            
#             # Calculate growth percentages
#             revenue_growth = self.calculate_growth(prev_month_revenue, month_revenue)
#             patient_growth = self.calculate_growth(prev_month_patients_count, month_new_patients)
#             avg_fee = month_revenue / month_new_patients if month_new_patients > 0 else 0
            
#             monthly_data.append({
#                 "month_num": month_num,  # Add month number for sorting/filtering
#                 "month": datetime(year, month_num, 1).strftime("%b %Y"),
#                 "revenue": round(month_revenue, 2),
#                 "newPatients": month_new_patients,
#                 "totalPatients": month_total_patients,
#                 "revenueGrowth": revenue_growth,
#                 "patientGrowth": patient_growth,
#                 "avgFeePerPatient": round(avg_fee, 2)
#             })
        
#         return monthly_data
    
#     def calculate_growth(self, previous: float, current: float) -> float:
#         """Calculate percentage growth"""
#         if previous == 0:
#             return 100.0 if current > 0 else 0.0
#         return round(((current - previous) / previous) * 100, 1)
    
#     def get_yearly_comparison(self) -> List[Dict[str, Any]]:
#         """Get yearly comparison data"""
#         patients = self.data["patients"]
        
#         # Get all years with patient data
#         available_years = sorted(set(
#             datetime.strptime(p["registration_date"], "%Y-%m-%d").year 
#             for p in patients
#         ))
        
#         yearly_data = []
#         for year in available_years:
#             year_patients = [
#                 p for p in patients 
#                 if datetime.strptime(p["registration_date"], "%Y-%m-%d").year == year
#             ]
#             year_revenue = sum(float(p.get("total_fee", 0)) for p in year_patients)
            
#             # Calculate growth from previous year
#             prev_year = year - 1
#             prev_year_patients = [
#                 p for p in patients 
#                 if datetime.strptime(p["registration_date"], "%Y-%m-%d").year == prev_year
#             ]
#             prev_year_revenue = sum(float(p.get("total_fee", 0)) for p in prev_year_patients)
#             growth = self.calculate_growth(prev_year_revenue, year_revenue)
            
#             yearly_data.append({
#                 "year": year,
#                 "totalRevenue": round(year_revenue, 2),
#                 "totalPatients": len(year_patients),
#                 "growth": growth
#             })
        
#         return yearly_data, available_years

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
#     """Create new patient (FIXED VERSION)"""
#     try:
#         data = request.get_json(force=True)

#         # ---------------- Validate ----------------
#         is_valid, message = validate_patient_data(data)
#         if not is_valid:
#             return format_response(None, False, message, 400)

#         # ---------------- Generate IDs SAFELY ----------------
#         numeric_id = data_manager.data["next_patient_id"]
#         patient_id = f"SAI-{numeric_id:03d}"
#         data_manager.data["next_patient_id"] += 1

#         # ---------------- Fees (safe float conversion) ----------------
#         consultation_fee = float(data.get("consultation_fee") or 0)
#         medicine_fee = float(data.get("medicine_fee") or 0)
#         total_fee = float(data.get("total_fee") or 0)

#         if total_fee == 0:
#             total_fee = consultation_fee + medicine_fee

#         # ---------------- Create Patient ----------------
#         patient = {
#             "id": numeric_id,
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
#             "consultation_fee": consultation_fee,
#             "medicine_fee": medicine_fee,
#             "total_fee": total_fee,
#             "doctor_notes": data.get("doctor_notes"),
#             "prescription": data.get("prescription"),
#             "next_visit_date": data.get("next_visit_date"),
#             "status": data.get("status", "active"),
#             "visit_count": 1,
#             "last_visit_date": datetime.now().strftime("%Y-%m-%d"),
#             "created_at": datetime.now().isoformat()
#         }

#         # ---------------- Save ----------------
#         data_manager.data["patients"].append(patient)

#         if not data_manager.save_data():
#             return format_response(None, False, "Failed to save patient", 500)

#         return format_response(patient, True, f"Patient {patient['name']} created successfully")

#     except Exception as e:
#         import traceback
#         print(traceback.format_exc())
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
    
#     if len(query) < 2:
#         return format_response([])
    
#     patients = data_manager.data["patients"]
#     type_filter = request.args.get('type', '')
    
#     matches = []
#     for patient in patients:
#         if query in patient.get("name", "").lower():
#             if type_filter and patient.get("type") != type_filter:
#                 continue
#             matches.append(patient)
    
#     return format_response(matches[:10])

# # 4. Dashboard Statistics
# @app.route('/api/dashboard/stats', methods=['GET'])
# def get_dashboard_stats():
#     """Get dashboard statistics"""
#     stats = data_manager.get_statistics()
#     return format_response(stats)

# # 5. Analytics Data
# # 5. Analytics Data - FIXED VERSION
# @app.route('/api/analytics', methods=['GET'])
# def get_analytics():
#     """Get analytics data for dashboard"""
#     try:
#         period = request.args.get('period', 'monthly')
#         year = int(request.args.get('year', datetime.now().year))
        
#         # Get monthly data for the year
#         monthly_data = data_manager.get_analytics_data(year)
        
#         # Get yearly comparison data
#         yearly_data, available_years = data_manager.get_yearly_comparison()
        
#         # Current date for calculations
#         now = datetime.now()
#         current_month_num = now.month if now.year == year else 12
        
#         # Find current month data and previous month data
#         current_month_data = None
#         prev_month_data = None
        
#         for data in monthly_data:
#             # Extract month number from the month string (e.g., "Feb 2026" -> month 2)
#             month_num = datetime.strptime(data["month"], "%b %Y").month
#             if month_num == current_month_num:
#                 current_month_data = data
#             elif month_num == current_month_num - 1:
#                 prev_month_data = data
        
#         # If current month not found, use last available month
#         if not current_month_data and monthly_data:
#             current_month_data = monthly_data[-1]
        
#         # Calculate YTD revenue (sum of revenue for months up to current month)
#         ytd_revenue = 0
#         for data in monthly_data:
#             month_num = datetime.strptime(data["month"], "%b %Y").month
#             if month_num <= current_month_num:
#                 ytd_revenue += data["revenue"]
        
#         # Calculate YTD growth compared to previous year
#         ytd_growth = 0
#         if year > min(available_years, default=year):
#             prev_year = year - 1
#             prev_year_monthly_data = data_manager.get_analytics_data(prev_year)
#             prev_year_ytd_revenue = 0
#             for data in prev_year_monthly_data:
#                 month_num = datetime.strptime(data["month"], "%b %Y").month
#                 if month_num <= current_month_num:
#                     prev_year_ytd_revenue += data["revenue"]
#             ytd_growth = data_manager.calculate_growth(prev_year_ytd_revenue, ytd_revenue)
        
#         # Calculate average revenue growth
#         avg_revenue_growth = 0
#         if current_month_data and prev_month_data:
#             avg_revenue_growth = data_manager.calculate_growth(
#                 prev_month_data["avgFeePerPatient"],
#                 current_month_data["avgFeePerPatient"]
#             )
        
#         # Prepare summary data
#         summary = {
#             "currentRevenue": current_month_data["revenue"] if current_month_data else 0,
#             "currentPatients": current_month_data["newPatients"] if current_month_data else 0,
#             "revenueGrowth": current_month_data["revenueGrowth"] if current_month_data else 0,
#             "patientGrowth": current_month_data["patientGrowth"] if current_month_data else 0,
#             "avgRevenuePerPatient": current_month_data["avgFeePerPatient"] if current_month_data else 0,
#             "avgRevenueGrowth": avg_revenue_growth,
#             "ytdRevenue": round(ytd_revenue, 2),
#             "ytdGrowth": ytd_growth
#         }
        
#         # Prepare chart data based on period
#         if period == 'quarterly':
#             # Group by quarters
#             labels = ['Q1', 'Q2', 'Q3', 'Q4']
#             revenue = [0, 0, 0, 0]
#             patients = [0, 0, 0, 0]
            
#             for data in monthly_data:
#                 # Extract month number to determine quarter
#                 month_num = datetime.strptime(data["month"], "%b %Y").month
#                 quarter_index = (month_num - 1) // 3
#                 if quarter_index < 4:
#                     revenue[quarter_index] += data["revenue"]
#                     patients[quarter_index] += data["newPatients"]
            
#             chart_data = {"labels": labels, "revenue": revenue, "patients": patients}
#         elif period == 'yearly':
#             # Yearly data (last 3 years)
#             recent_years = sorted(available_years, reverse=True)[:3]
#             recent_years.reverse()  # Show oldest to newest
            
#             labels = [str(year) for year in recent_years]
#             revenue = []
#             patients = []
            
#             for y in recent_years:
#                 year_data = data_manager.get_analytics_data(y)
#                 year_revenue = sum(data["revenue"] for data in year_data)
#                 year_patients = sum(data["newPatients"] for data in year_data)
#                 revenue.append(year_revenue)
#                 patients.append(year_patients)
            
#             chart_data = {"labels": labels, "revenue": revenue, "patients": patients}
#         else:  # monthly (default)
#             labels = [data["month"] for data in monthly_data]
#             revenue = [data["revenue"] for data in monthly_data]
#             patients = [data["newPatients"] for data in monthly_data]
            
#             chart_data = {"labels": labels, "revenue": revenue, "patients": patients}
        
#         return format_response({
#             "summary": summary,
#             "monthlyData": monthly_data,
#             "yearlyData": yearly_data,
#             "chartData": chart_data,
#             "availableYears": available_years
#         })
        
#     except Exception as e:
#         import traceback
#         print(f"Error in analytics: {str(e)}")
#         print(traceback.format_exc())
#         return format_response(None, False, f"Error loading analytics: {str(e)}", 500)

# # 6. Message Management
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

# # 7. Authentication
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

# # 8. Settings Management
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
#     print("  GET  /api/analytics      - Analytics data")
#     print("  POST /api/messages       - Contact form")
#     print("  POST /api/auth/login     - Admin login")
#     print("="*60)
#     print("="*60 + "\n")
    
#     app.run(debug=True, host='0.0.0.0', port=5000)


import os
import traceback
from datetime import datetime
from functools import wraps
from typing import Any, Dict, List

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from supabase import create_client
from werkzeug.exceptions import HTTPException
from werkzeug.security import check_password_hash, generate_password_hash

# ============ CONFIG (read from environment variables / .env file) ============
try:
    from dotenv import load_dotenv
    load_dotenv(override=True)   # .env wins over any old value set in the terminal/system
except ImportError:
    pass


def require_env(name: str) -> str:
    value = os.environ.get(name, "").strip().strip('"').strip("'")   # tolerate quotes/spaces in .env
    if not value:
        raise RuntimeError(f"Missing environment variable: {name}. "
                           f"Set it in your .env file or system environment.")
    return value


SUPABASE_URL = require_env("SUPABASE_URL")
SUPABASE_SERVICE_KEY = require_env("SUPABASE_SERVICE_KEY")
SECRET_KEY = require_env("SECRET_KEY")
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")   # only used if the users table is empty
DEBUG = os.environ.get("FLASK_DEBUG") == "1"
# =============================================================================

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config["SECRET_KEY"] = SECRET_KEY
CORS(app)

sb = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
TOKEN_MAX_AGE = 60 * 60 * 12  # 12 hours


# ============ HELPERS ============
def format_response(data: Any, success: bool = True, message: str = "", status: int = 200):
    return jsonify({"success": success, "message": message, "data": data}), status


def fetch_all(table: str, columns: str = "*", modify=None, page: int = 1000) -> List[Dict]:
    """Supabase returns max ~1000 rows per request, so page through everything."""
    rows, start = [], 0
    while True:
        q = sb.table(table).select(columns).order("id")
        if modify:
            q = modify(q)
        batch = q.range(start, start + page - 1).execute().data
        rows += batch
        if len(batch) < page:
            return rows
        start += page


def clean(value):
    return None if value == "" else value


def to_int(value):
    try:
        return int(value) if value not in (None, "") else None
    except (TypeError, ValueError):
        return None


def to_float(value) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def today() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def digits(value) -> str:
    return "".join(ch for ch in str(value or "") if ch.isdigit())


def token_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        header = request.headers.get("Authorization", "")
        token = header.removeprefix("Bearer ").strip()
        if not token:
            return format_response(None, False, "Authentication required", 401)
        try:
            request.user = serializer.loads(token, max_age=TOKEN_MAX_AGE)
        except (BadSignature, SignatureExpired):
            return format_response(None, False, "Invalid or expired token", 401)
        return fn(*args, **kwargs)
    return wrapper


def ensure_admin():
    if sb.table("users").select("id").limit(1).execute().data:
        return
    if not ADMIN_PASSWORD or ADMIN_PASSWORD == "CHANGE_THIS_PASSWORD":
        print("WARNING: no users exist and ADMIN_PASSWORD not set - nobody can log in.")
        return
    sb.table("users").insert({
        "username": ADMIN_USERNAME,
        "password_hash": generate_password_hash(ADMIN_PASSWORD),
        "role": "admin",
    }).execute()
    print("Created initial admin user.")


# ============ PATIENT / VISIT LOGIC ============
# One row per PERSON in `patients` (one SAI- ID). Every visit + its fees is a row in `visits`.
PROFILE_TEXT = ["name", "phone", "gender", "email", "address", "disease", "disease_duration",
                "symptoms", "previous_treatment", "status", "type"]
VISIT_TEXT = ["appointment_type", "disease", "disease_duration", "symptoms", "doctor_notes", "prescription"]


def clean_profile(data: Dict) -> Dict:
    out = {}
    for f in PROFILE_TEXT:
        if f in data:
            v = data[f]
            out[f] = clean(v.strip() if isinstance(v, str) else v)
    if "age" in data:
        out["age"] = to_int(data["age"])
    return out


def only_filled(d: Dict) -> Dict:
    return {k: v for k, v in d.items() if v not in (None, "")}


def clean_visit(data: Dict) -> Dict:
    consultation = to_float(data.get("consultation_fee"))
    medicine = to_float(data.get("medicine_fee"))
    total = to_float(data.get("total_fee")) or (consultation + medicine)
    visit = {
        "visit_date": clean(data.get("visit_date")) or clean(data.get("registration_date")) or today(),
        "visit_type": clean(data.get("visit_type")) or clean(data.get("type")) or "new",
        "consultation_fee": consultation,
        "medicine_fee": medicine,
        "total_fee": total,
        "next_visit_date": clean(data.get("next_visit_date")),
    }
    for f in VISIT_TEXT:
        v = data.get(f)
        visit[f] = clean(v.strip() if isinstance(v, str) else v)
    visit["appointment_type"] = visit["appointment_type"] or "consultation"
    return visit


def recompute_patient(pid: int):
    """Refresh visit_count / total_paid / dates on the patient from its visits."""
    vs = sb.table("visits").select("visit_date,total_fee").eq("patient_id", pid).execute().data
    upd: Dict[str, Any] = {
        "visit_count": len(vs),
        "total_paid": round(sum(to_float(v["total_fee"]) for v in vs), 2),
        "updated_at": datetime.now().isoformat(),
    }
    if vs:
        dates = [v["visit_date"] for v in vs]
        upd["last_visit_date"] = max(dates)
        upd["registration_date"] = min(dates)
        if len(vs) > 1:
            upd["type"] = "regular"
    sb.table("patients").update(upd).eq("id", pid).execute()


def add_visit(pid: int, data: Dict) -> Dict:
    visit = clean_visit(data)
    visit["patient_id"] = pid
    created = sb.table("visits").insert(visit).execute().data[0]

    # keep the patient's profile current (only overwrite with non-empty values)
    profile = clean_profile(data)
    changes = only_filled({k: v for k, v in profile.items()
                           if k in ("phone", "gender", "email", "address", "age")})
    changes.update(only_filled({k: visit.get(k) for k in ("disease", "disease_duration", "symptoms")}))
    if changes:
        sb.table("patients").update(changes).eq("id", pid).execute()

    recompute_patient(pid)
    return created


def find_existing(name: str, phone: str):
    """Same person = same name (case-insensitive) + same phone digits."""
    n = name.strip().lower()
    rows = sb.table("patients").select("*").ilike("name", f"%{n.replace('%', '')}%").execute().data
    for r in rows:
        if (r.get("name") or "").strip().lower() == n and digits(r.get("phone")) == digits(phone):
            return r
    return None


def get_patient_row(pid: int):
    rows = sb.table("patients").select("*").eq("id", pid).execute().data
    return rows[0] if rows else None


# ============ ANALYTICS ============
def prep_patients(rows):
    return [(int(r["registration_date"][:4]), int(r["registration_date"][5:7]))
            for r in rows if r.get("registration_date")]


def prep_visits(rows):
    return [(int(r["visit_date"][:4]), int(r["visit_date"][5:7]),
             to_float(r.get("total_fee")), r["patient_id"])
            for r in rows if r.get("visit_date")]


def growth(previous: float, current: float) -> float:
    if previous == 0:
        return 100.0 if current > 0 else 0.0
    return round(((current - previous) / previous) * 100, 1)


def month_totals(pp, pv, y, m):
    new_patients = len([1 for yy, mm in pp if yy == y and mm == m])
    fees = [f for yy, mm, f, _ in pv if yy == y and mm == m]
    return new_patients, sum(fees), len(fees)   # new = 1st-time visits, last = ALL visits


def analytics_for_year(pp, pv, year: int):
    data = []
    for m in range(1, 13):
        new_patients, revenue, visits_n = month_totals(pp, pv, year, m)
        py, pm = (year, m - 1) if m > 1 else (year - 1, 12)
        prev_new, prev_rev, prev_visits = month_totals(pp, pv, py, pm)
        data.append({
            "month_num": m,
            "month": datetime(year, m, 1).strftime("%b %Y"),
            "revenue": round(revenue, 2),
            "newPatients": new_patients,          # first-time visits only
            "totalPatients": visits_n,            # every visit (new + returning)
            "revenueGrowth": growth(prev_rev, revenue),
            "newPatientGrowth": growth(prev_new, new_patients),
            "patientGrowth": growth(prev_visits, visits_n),
            "avgFeePerPatient": round(revenue / visits_n, 2) if visits_n else 0,
        })
    return data


def get_statistics() -> Dict[str, Any]:
    patients = fetch_all("patients", "id,registration_date,disease")
    visits = fetch_all("visits", "id,patient_id,visit_date,total_fee")
    now = datetime.now()
    pp, pv = prep_patients(patients), prep_visits(visits)
    new_this_month, revenue, _ = month_totals(pp, pv, now.year, now.month)
    diseases: Dict[str, int] = {}
    for p in patients:
        d = p.get("disease") or "Unknown"
        diseases[d] = diseases.get(d, 0) + 1
    pending = sb.table("messages").select("id", count="exact").eq("status", "new").execute().count
    return {
        "total_patients": len(visits),          # every visit counts
        "unique_patients": len(patients),       # distinct people (SAI IDs)
        "new_patients_this_month": new_this_month,
        "monthly_revenue": revenue,
        "visits_this_month": len([1 for y, m, _, _ in pv if y == now.year and m == now.month]),
        "pending_messages": pending or 0,
        "disease_distribution": [{"name": k, "count": v} for k, v in diseases.items()],
    }


# ============ PAGES ============
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')


# ============ AUTH ============
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    rows = sb.table("users").select("*").eq("username", data.get("username", "")).limit(1).execute().data
    user = rows[0] if rows else None
    if not user or not check_password_hash(user["password_hash"], data.get("password", "")):
        return format_response(None, False, "Invalid credentials", 401)
    token = serializer.dumps({"u": user["username"], "r": user["role"]})
    return format_response({"token": token,
                            "user": {"username": user["username"], "role": user["role"]}},
                           message="Login successful")


@app.route('/api/auth/verify', methods=['POST'])
@token_required
def verify_token():
    return format_response({"valid": True})


# ============ CLINIC INFO / SETTINGS ============
def read_settings() -> Dict:
    rows = sb.table("settings").select("data").eq("id", 1).execute().data
    return rows[0]["data"] if rows else {}


@app.route('/api/info', methods=['GET'])
def get_clinic_info():
    return format_response({"clinic_info": read_settings()})


@app.route('/api/settings', methods=['GET'])
def get_settings():
    return format_response(read_settings())


@app.route('/api/settings', methods=['PUT'])
@token_required
def update_settings():
    new = {**read_settings(), **(request.get_json(silent=True) or {})}
    sb.table("settings").upsert({"id": 1, "data": new}).execute()
    return format_response(new, message="Settings updated")


# ============ PATIENTS ============
@app.route('/api/patients', methods=['GET'])
@token_required
def get_patients():
    name = request.args.get('name', '').strip()
    type_filter = request.args.get('type', '')
    status_filter = request.args.get('status', '')
    limit = to_int(request.args.get('limit'))

    q = sb.table("patients").select("*").order("id", desc=True)
    if name:
        safe = name.replace(",", " ").replace("(", " ").replace(")", " ").replace("%", "")
        q = q.or_(f"name.ilike.%{safe}%,disease.ilike.%{safe}%,patient_id.ilike.%{safe}%,phone.ilike.%{safe}%")
    if type_filter:
        q = q.eq("type", type_filter)
    if status_filter:
        q = q.eq("status", status_filter)

    if limit:
        return format_response(q.limit(limit).execute().data)
    rows, start = [], 0
    while True:
        batch = q.range(start, start + 999).execute().data
        rows += batch
        if len(batch) < 1000:
            break
        start += 1000
    return format_response(rows)


@app.route('/api/patients/search', methods=['GET'])
@token_required
def search_patients():
    query = request.args.get('q', '').strip().replace("%", "").replace(",", " ").replace("(", " ").replace(")", " ")
    if len(query) < 2:
        return format_response([])
    q = sb.table("patients").select("*").or_(f"name.ilike.%{query}%,phone.ilike.%{query}%")
    return format_response(q.order("id", desc=True).limit(10).execute().data)


@app.route('/api/patients/<int:patient_id>', methods=['GET'])
@token_required
def get_patient(patient_id: int):
    patient = get_patient_row(patient_id)
    if not patient:
        return format_response(None, False, "Patient not found", 404)
    visits = (sb.table("visits").select("*").eq("patient_id", patient_id)
              .order("visit_date", desc=True).order("id", desc=True).execute().data)
    return format_response({**patient, "visits": visits})


@app.route('/api/patients', methods=['POST'])
@token_required
def create_patient():
    """Creates a patient + first visit. If the same person (name + phone) already
    exists, the visit is added to the EXISTING patient - no duplicate ID."""
    data = request.get_json(force=True) or {}
    for field in ("name", "phone", "disease"):
        if not data.get(field):
            return format_response(None, False, f"Missing required field: {field}", 400)

    existing = find_existing(data["name"], data["phone"])
    if existing:
        pid = existing["id"]
    else:
        profile = clean_profile(data)
        profile["type"] = "new"
        profile["status"] = profile.get("status") or "active"
        profile["registration_date"] = (clean(data.get("visit_date")) or clean(data.get("registration_date")) or today())
        profile["visit_count"] = 0
        pid = sb.table("patients").insert(profile).execute().data[0]["id"]

    add_visit(pid, data)
    patient = get_patient_row(pid)
    if existing:
        msg = f"Visit added to existing patient {patient['patient_id']} ({patient['name']})"
    else:
        msg = f"Patient {patient['name']} created as {patient['patient_id']}"
    return format_response({**patient, "existing": bool(existing)}, True, msg)


@app.route('/api/patients/<int:patient_id>/visits', methods=['POST'])
@token_required
def create_visit(patient_id: int):
    patient = get_patient_row(patient_id)
    if not patient:
        return format_response(None, False, "Patient not found", 404)
    add_visit(patient_id, request.get_json(force=True) or {})
    patient = get_patient_row(patient_id)
    return format_response(patient, True, f"Visit added to {patient['patient_id']} ({patient['name']})")


@app.route('/api/patients/<int:patient_id>', methods=['PUT'])
@token_required
def update_patient(patient_id: int):
    if not get_patient_row(patient_id):
        return format_response(None, False, "Patient not found", 404)
    changes = clean_profile(request.get_json(silent=True) or {})
    changes["updated_at"] = datetime.now().isoformat()
    res = sb.table("patients").update(changes).eq("id", patient_id).execute()
    return format_response(res.data[0], message="Patient updated successfully")


@app.route('/api/patients/<int:patient_id>', methods=['DELETE'])
@token_required
def delete_patient(patient_id: int):
    res = sb.table("patients").delete().eq("id", patient_id).execute()  # visits cascade
    if not res.data:
        return format_response(None, False, "Patient not found", 404)
    return format_response(res.data[0], message="Patient deleted successfully")


@app.route('/api/visits/<int:visit_id>', methods=['DELETE'])
@token_required
def delete_visit(visit_id: int):
    res = sb.table("visits").delete().eq("id", visit_id).execute()
    if not res.data:
        return format_response(None, False, "Visit not found", 404)
    recompute_patient(res.data[0]["patient_id"])
    return format_response(res.data[0], message="Visit deleted")


# ============ DASHBOARD & ANALYTICS ============
@app.route('/api/dashboard/stats', methods=['GET'])
@token_required
def get_dashboard_stats():
    return format_response(get_statistics())


@app.route('/api/analytics', methods=['GET'])
@token_required
def get_analytics():
    period = request.args.get('period', 'monthly')
    now = datetime.now()
    year = to_int(request.args.get('year')) or now.year

    pp = prep_patients(fetch_all("patients", "id,registration_date"))
    pv = prep_visits(fetch_all("visits", "id,patient_id,visit_date,total_fee"))
    available_years = sorted({y for y, _ in pp} | {y for y, _, _, _ in pv} | {now.year})

    monthly = analytics_for_year(pp, pv, year)

    yearly = []
    for y in available_years:
        rev = sum(f for yy, _, f, _ in pv if yy == y)
        prev_rev = sum(f for yy, _, f, _ in pv if yy == y - 1)
        yearly.append({"year": y, "totalRevenue": round(rev, 2),
                       "totalPatients": len([1 for yy, _, _, _ in pv if yy == y]),
                       "newPatients": len([1 for yy, _ in pp if yy == y]),
                       "growth": growth(prev_rev, rev)})

    cur_num = now.month if now.year == year else 12
    cur = next((m for m in monthly if m["month_num"] == cur_num), monthly[-1])
    prev = next((m for m in monthly if m["month_num"] == cur_num - 1), None)

    ytd = sum(m["revenue"] for m in monthly if m["month_num"] <= cur_num)
    prev_ytd = sum(m["revenue"] for m in analytics_for_year(pp, pv, year - 1) if m["month_num"] <= cur_num)
    ytd_growth = growth(prev_ytd, ytd) if year > min(available_years) else 0

    summary = {
        "currentRevenue": cur["revenue"],
        "currentPatients": cur["totalPatients"],
        "currentNewPatients": cur["newPatients"],
        "newPatientGrowth": cur["newPatientGrowth"],
        "revenueGrowth": cur["revenueGrowth"],
        "patientGrowth": cur["patientGrowth"],
        "avgRevenuePerPatient": cur["avgFeePerPatient"],
        "avgRevenueGrowth": growth(prev["avgFeePerPatient"], cur["avgFeePerPatient"]) if prev else 0,
        "ytdRevenue": round(ytd, 2),
        "ytdGrowth": ytd_growth,
    }

    if period == 'quarterly':
        revenue, patients, visits_q = [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]
        for m in monthly:
            qi = (m["month_num"] - 1) // 3
            revenue[qi] += m["revenue"]
            patients[qi] += m["newPatients"]
            visits_q[qi] += m["totalPatients"]
        chart = {"labels": ['Q1', 'Q2', 'Q3', 'Q4'], "revenue": revenue,
                 "patients": patients, "visits": visits_q}
    elif period == 'yearly':
        recent = available_years[-3:]
        chart = {"labels": [str(y) for y in recent],
                 "revenue": [round(sum(f for yy, _, f, _ in pv if yy == y), 2) for y in recent],
                 "patients": [len([1 for yy, _ in pp if yy == y]) for y in recent],
                 "visits": [len([1 for yy, _, _, _ in pv if yy == y]) for y in recent]}
    else:
        chart = {"labels": [m["month"] for m in monthly],
                 "revenue": [m["revenue"] for m in monthly],
                 "patients": [m["newPatients"] for m in monthly],
                 "visits": [m["totalPatients"] for m in monthly]}

    return format_response({"summary": summary, "monthlyData": monthly, "yearlyData": yearly,
                            "chartData": chart, "availableYears": available_years})


# ============ MESSAGES ============
@app.route('/api/messages', methods=['GET'])
@token_required
def get_messages():
    return format_response(sb.table("messages").select("*").order("date", desc=True).execute().data)


@app.route('/api/messages', methods=['POST'])  # public contact form
def create_message():
    data = request.get_json(silent=True) or {}
    for field in ("name", "phone", "message"):
        if not data.get(field):
            return format_response(None, False, f"Missing required field: {field}", 400)
    row = {
        "name": data["name"][:200],
        "phone": data["phone"][:50],
        "email": clean(data.get("email")),
        "appointment_type": data.get("appointment_type") or "consultation",
        "message": data["message"][:5000],
    }
    res = sb.table("messages").insert(row).execute()
    return format_response(res.data[0], message="Message sent successfully")


@app.route('/api/messages/<int:message_id>', methods=['PUT'])
@token_required
def update_message(message_id: int):
    data = request.get_json(silent=True) or {}
    changes = {k: data[k] for k in ("status",) if k in data}
    res = sb.table("messages").update(changes).eq("id", message_id).execute()
    if not res.data:
        return format_response(None, False, "Message not found", 404)
    return format_response(res.data[0], message="Message updated")


@app.route('/api/messages/<int:message_id>', methods=['DELETE'])
@token_required
def delete_message(message_id: int):
    res = sb.table("messages").delete().eq("id", message_id).execute()
    if not res.data:
        return format_response(None, False, "Message not found", 404)
    return format_response(res.data[0], message="Message deleted")


# ============ ERROR HANDLERS ============
@app.errorhandler(HTTPException)
def http_error(e):
    return format_response(None, False, e.description or e.name, e.code)


@app.errorhandler(Exception)
def server_error(e):
    print(traceback.format_exc())
    return format_response(None, False, "Internal server error", 500)


if __name__ == '__main__':
    ensure_admin()
    app.run(debug=DEBUG, host='0.0.0.0', port=5000)