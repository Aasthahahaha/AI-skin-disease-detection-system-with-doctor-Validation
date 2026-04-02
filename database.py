"""
Database Management Module

Handles all JSON-based data storage and retrieval operations.
Manages cases, appointments, and user data in JSON format.
"""

import json
import os
from datetime import datetime

# File paths
CASES_FILE = "data/cases.json"
APPOINTMENTS_FILE = "data/appointments.json"
USERS_FILE = "data/users.json"

def ensure_data_files():
    """
    Create data directory and empty JSON files if they don't exist.
    """
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Create cases.json if it doesn't exist
    if not os.path.exists(CASES_FILE):
        with open(CASES_FILE, "w") as f:
            json.dump([], f, indent=4)
    
    # Create appointments.json if it doesn't exist
    if not os.path.exists(APPOINTMENTS_FILE):
        with open(APPOINTMENTS_FILE, "w") as f:
            json.dump([], f, indent=4)
    
    # Ensure users.json exists (for auth module)
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f, indent=4)

# Initialize data files on module import
ensure_data_files()

# ==================== CASES FUNCTIONS ====================

def load_cases():
    """
    Load all cases from the JSON file.
    
    Returns:
        list: List of case dictionaries
    """
    ensure_data_files()
    try:
        with open(CASES_FILE, "r") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_cases(cases):
    """
    Save all cases to the JSON file.
    
    Args:
        cases (list): List of case dictionaries to save
    """
    with open(CASES_FILE, "w") as f:
        json.dump(cases, f, indent=4)

def add_case(case_dict):
    """
    Add a new case to the database.
    
    Args:
        case_dict (dict): Case data containing user, image, ai_result, etc.
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cases = load_cases()
        cases.append(case_dict)
        save_cases(cases)
        return True
    except Exception as e:
        st.error(f"Error adding case: {e}")
        return False

def get_user_cases(username):
    """
    Get all cases for a specific user.
    
    Args:
        username (str): Username to filter cases
    
    Returns:
        list: List of cases for the user
    """
    cases = load_cases()
    return [case for case in cases if case.get("user") == username]

def get_pending_cases():
    """
    Get all cases waiting for doctor approval.
    
    Returns:
        list: List of unverified cases
    """
    cases = load_cases()
    return [case for case in cases if not case.get("doctor_verified", False)]

def get_approved_cases():
    """
    Get all cases approved by doctors.
    
    Returns:
        list: List of verified cases
    """
    cases = load_cases()
    return [case for case in cases if case.get("doctor_verified", False)]

def update_case(case_index, updates):
    """
    Update a specific case with new data.
    
    Args:
        case_index (int): Index of the case to update
        updates (dict): Dictionary of fields to update
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cases = load_cases()
        if 0 <= case_index < len(cases):
            cases[case_index].update(updates)
            save_cases(cases)
            return True
        return False
    except Exception as e:
        st.error(f"Error updating case: {e}")
        return False

def delete_case(case_index):
    """
    Delete a case from the database.
    
    Args:
        case_index (int): Index of the case to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cases = load_cases()
        if 0 <= case_index < len(cases):
            cases.pop(case_index)
            save_cases(cases)
            return True
        return False
    except Exception as e:
        st.error(f"Error deleting case: {e}")
        return False

# ==================== APPOINTMENTS FUNCTIONS ====================

def load_appointments():
    """
    Load all appointments from the JSON file.
    
    Returns:
        list: List of appointment dictionaries
    """
    ensure_data_files()
    try:
        with open(APPOINTMENTS_FILE, "r") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_appointments(appointments):
    """
    Save all appointments to the JSON file.
    
    Args:
        appointments (list): List of appointment dictionaries to save
    """
    with open(APPOINTMENTS_FILE, "w") as f:
        json.dump(appointments, f, indent=4)

def request_appointment(appointment_dict):
    """
    Request a new appointment.
    
    Args:
        appointment_dict (dict): Appointment data containing user, doctor, date, etc.
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        appointments = load_appointments()
        appointment_dict["status"] = "pending"
        appointment_dict["created_at"] = datetime.now().isoformat()
        appointments.append(appointment_dict)
        save_appointments(appointments)
        return True
    except Exception as e:
        st.error(f"Error requesting appointment: {e}")
        return False

def get_user_appointments(username):
    """
    Get all appointments for a specific user.
    
    Args:
        username (str): Username to filter appointments
    
    Returns:
        list: List of appointments for the user
    """
    appointments = load_appointments()
    return [apt for apt in appointments if apt.get("user") == username]

def get_doctor_appointments(doctor_id):
    """
    Get all appointments for a specific doctor.
    
    Args:
        doctor_id (str): Doctor's username
    
    Returns:
        list: List of appointments for the doctor
    """
    appointments = load_appointments()
    return [apt for apt in appointments if apt.get("doctor") == doctor_id]

def update_appointment_status(appointment_index, status, notes=""):
    """
    Update an appointment's status.
    
    Args:
        appointment_index (int): Index of the appointment
        status (str): New status (pending, approved, rejected, completed)
        notes (str): Optional notes for the appointment
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        appointments = load_appointments()
        if 0 <= appointment_index < len(appointments):
            appointments[appointment_index]["status"] = status
            if notes:
                appointments[appointment_index]["notes"] = notes
            appointments[appointment_index]["updated_at"] = datetime.now().isoformat()
            save_appointments(appointments)
            return True
        return False
    except Exception as e:
        st.error(f"Error updating appointment: {e}")
        return False

def get_pending_appointments():
    """
    Get all pending appointments.
    
    Returns:
        list: List of pending appointments
    """
    appointments = load_appointments()
    return [apt for apt in appointments if apt.get("status") == "pending"]

# ==================== STATISTICS FUNCTIONS ====================

def get_statistics():
    """
    Get system statistics.
    
    Returns:
        dict: Dictionary containing case counts, appointment counts, etc.
    """
    cases = load_cases()
    appointments = load_appointments()
    
    return {
        "total_cases": len(cases),
        "pending_cases": len(get_pending_cases()),
        "approved_cases": len(get_approved_cases()),
        "total_appointments": len(appointments),
        "pending_appointments": len(get_pending_appointments())
    }

