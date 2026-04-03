"""
Database Management Module

Handles all JSON-based data storage and retrieval operations.
Manages cases, appointments, users, and doctor profiles in JSON format.
"""

import json
import os
from datetime import datetime, timedelta

# ── File paths ─────────────────────────────────────────────────────────────────
CASES_FILE        = "data/cases.json"
APPOINTMENTS_FILE = "data/appointments.json"
USERS_FILE        = "data/users.json"
DOCTORS_FILE      = "data/doctors.json"


def ensure_data_files():
    """Create data directory and empty JSON files if they don't exist."""
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(CASES_FILE):
        with open(CASES_FILE, "w") as f:
            json.dump([], f, indent=4)

    if not os.path.exists(APPOINTMENTS_FILE):
        with open(APPOINTMENTS_FILE, "w") as f:
            json.dump([], f, indent=4)

    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f, indent=4)

    if not os.path.exists(DOCTORS_FILE):
        _seed_doctors_file()


def _seed_doctors_file():
    """Seed doctors.json with default doctor profiles."""
    default_doctors = {
        "doctor1": {
            "display_name": "Dr. Anjali Sharma",
            "specialization": "Dermatology & Skin Disorders",
            "qualification": "MD Dermatology, MBBS",
            "experience_years": 12,
            "location": {"city": "Mumbai", "area": "Bandra West"},
            "availability": "available",
            "current_load": 0,
            "total_cases_handled": 145,
            "rating": 4.8,
            "bio": "Expert in inflammatory skin conditions, psoriasis, and cosmetic dermatology.",
            "estimated_response_hours": 4,
            "languages": ["English", "Hindi", "Marathi"],
            "hospital": "Lilavati Hospital, Mumbai"
        },
        "doctor2": {
            "display_name": "Dr. Rajesh Patel",
            "specialization": "Clinical & Cosmetic Dermatology",
            "qualification": "DNB Dermatology, MBBS",
            "experience_years": 9,
            "location": {"city": "Mumbai", "area": "Andheri East"},
            "availability": "available",
            "current_load": 0,
            "total_cases_handled": 98,
            "rating": 4.6,
            "bio": "Specialises in acne, fungal infections, and cosmetic skin procedures.",
            "estimated_response_hours": 4,
            "languages": ["English", "Hindi", "Gujarati"],
            "hospital": "Kokilaben Hospital, Mumbai"
        },
        "doctor3": {
            "display_name": "Dr. Priya Gupta",
            "specialization": "Pediatric & Allergic Dermatology",
            "qualification": "MD Dermatology, MBBS, FIAD",
            "experience_years": 14,
            "location": {"city": "Delhi", "area": "South Delhi"},
            "availability": "available",
            "current_load": 0,
            "total_cases_handled": 210,
            "rating": 4.9,
            "bio": "Leading specialist in pediatric skin disorders, eczema, and allergic skin diseases.",
            "estimated_response_hours": 3,
            "languages": ["English", "Hindi"],
            "hospital": "AIIMS Delhi"
        },
        "doctor4": {
            "display_name": "Dr. Arjun Mehta",
            "specialization": "Cosmetic & Laser Dermatology",
            "qualification": "MD Dermatology, MBBS",
            "experience_years": 8,
            "location": {"city": "Bangalore", "area": "Indiranagar"},
            "availability": "available",
            "current_load": 0,
            "total_cases_handled": 87,
            "rating": 4.7,
            "bio": "Pioneer in laser treatments for skin pigmentation, vitiligo, and rosacea.",
            "estimated_response_hours": 4,
            "languages": ["English", "Hindi", "Kannada"],
            "hospital": "Manipal Hospital, Bangalore"
        },
        "doctor5": {
            "display_name": "Dr. Kavitha Nair",
            "specialization": "General & Tropical Dermatology",
            "qualification": "MD Dermatology, MBBS, DTM",
            "experience_years": 16,
            "location": {"city": "Chennai", "area": "T. Nagar"},
            "availability": "available",
            "current_load": 0,
            "total_cases_handled": 312,
            "rating": 4.9,
            "bio": "Renowned expert in tropical skin diseases, fungal infections, and cancer screening.",
            "estimated_response_hours": 3,
            "languages": ["English", "Tamil", "Malayalam"],
            "hospital": "Apollo Hospitals, Chennai"
        },
        "doctor6": {
            "display_name": "Dr. Siddharth Rao",
            "specialization": "Dermatopathology & Skin Cancer",
            "qualification": "MD Dermatology, MBBS",
            "experience_years": 11,
            "location": {"city": "Hyderabad", "area": "Jubilee Hills"},
            "availability": "available",
            "current_load": 0,
            "total_cases_handled": 176,
            "rating": 4.8,
            "bio": "Specialist in skin biopsy interpretation, melanoma detection, and dermatopathology.",
            "estimated_response_hours": 4,
            "languages": ["English", "Hindi", "Telugu"],
            "hospital": "Yashoda Hospital, Hyderabad"
        }
    }
    with open(DOCTORS_FILE, "w") as f:
        json.dump(default_doctors, f, indent=4)


# Initialise on module import
ensure_data_files()


# ══════════════════════════════════════════════════════════════════════════════
# CASES
# ══════════════════════════════════════════════════════════════════════════════

def load_cases():
    ensure_data_files()
    try:
        with open(CASES_FILE, "r") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_cases(cases):
    with open(CASES_FILE, "w") as f:
        json.dump(cases, f, indent=4)


def add_case(case_dict):
    try:
        cases = load_cases()
        cases.append(case_dict)
        save_cases(cases)
        return True
    except Exception:
        return False


def get_user_cases(username):
    cases = load_cases()
    return [c for c in cases if c.get("user") == username]


def get_pending_cases():
    cases = load_cases()
    return [c for c in cases if not c.get("doctor_verified", False)]


def get_pending_cases_for_doctor(doctor_username):
    """Return unverified cases assigned to a specific doctor."""
    cases = load_cases()
    return [
        c for c in cases
        if not c.get("doctor_verified", False)
        and c.get("assigned_doctor") == doctor_username
    ]


def get_approved_cases():
    cases = load_cases()
    return [c for c in cases if c.get("doctor_verified", False)]


def get_approved_cases_for_doctor(doctor_username):
    """Return verified cases reviewed by a specific doctor."""
    cases = load_cases()
    return [
        c for c in cases
        if c.get("doctor_verified", False)
        and c.get("doctor_name") == doctor_username
    ]


def update_case(case_index, updates):
    try:
        cases = load_cases()
        if 0 <= case_index < len(cases):
            cases[case_index].update(updates)
            save_cases(cases)
            return True
        return False
    except Exception:
        return False


def delete_case(case_index):
    try:
        cases = load_cases()
        if 0 <= case_index < len(cases):
            cases.pop(case_index)
            save_cases(cases)
            return True
        return False
    except Exception:
        return False


# ══════════════════════════════════════════════════════════════════════════════
# APPOINTMENTS
# ══════════════════════════════════════════════════════════════════════════════

def load_appointments():
    ensure_data_files()
    try:
        with open(APPOINTMENTS_FILE, "r") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_appointments(appointments):
    with open(APPOINTMENTS_FILE, "w") as f:
        json.dump(appointments, f, indent=4)


def request_appointment(appointment_dict):
    try:
        appointments = load_appointments()
        appointment_dict["status"] = "pending"
        appointment_dict["created_at"] = datetime.now().isoformat()
        appointments.append(appointment_dict)
        save_appointments(appointments)
        return True
    except Exception:
        return False


def get_user_appointments(username):
    appointments = load_appointments()
    return [apt for apt in appointments if apt.get("user") == username]


def get_doctor_appointments(doctor_id):
    appointments = load_appointments()
    return [apt for apt in appointments if apt.get("doctor") == doctor_id]


def update_appointment_status(appointment_index, status, notes=""):
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
    except Exception:
        return False


def get_pending_appointments():
    appointments = load_appointments()
    return [apt for apt in appointments if apt.get("status") == "pending"]


def get_pending_appointments_for_doctor(doctor_username):
    appointments = load_appointments()
    return [
        apt for apt in appointments
        if apt.get("status") == "pending" and apt.get("doctor") == doctor_username
    ]


# ══════════════════════════════════════════════════════════════════════════════
# DOCTORS
# ══════════════════════════════════════════════════════════════════════════════

def load_doctors():
    ensure_data_files()
    try:
        with open(DOCTORS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_doctors(doctors):
    with open(DOCTORS_FILE, "w") as f:
        json.dump(doctors, f, indent=4)


def get_all_cities():
    """Return sorted list of unique cities from the doctor registry."""
    doctors = load_doctors()
    cities = sorted({d["location"]["city"] for d in doctors.values()})
    return cities


def get_doctors_by_city(city=None):
    """
    Return list of (username, profile) tuples filtered by city.
    If city is None or 'All Cities', return all doctors.
    """
    doctors = load_doctors()
    result = []
    for username, profile in doctors.items():
        if city and city != "All Cities":
            if profile["location"]["city"].lower() != city.lower():
                continue
        result.append((username, profile))
    return result


def get_available_doctors(city=None):
    """Return only available doctors, optionally filtered by city."""
    return [
        (u, p) for u, p in get_doctors_by_city(city)
        if p.get("availability") == "available"
    ]


def assign_doctor_round_robin(city=None):
    """
    Assign a doctor using round-robin load balancing.
    Picks the available doctor with the fewest active cases in the given city.

    Returns:
        (doctor_username: str, profile: dict) | (None, None)
    """
    candidates = get_available_doctors(city)
    if not candidates:
        candidates = get_available_doctors()   # fallback: ignore city filter
    if not candidates:
        return None, None

    # Pick the one with lowest current_load
    candidates.sort(key=lambda x: x[1].get("current_load", 0))
    return candidates[0]


def increment_doctor_load(doctor_username):
    """Increment the active case count for a doctor."""
    doctors = load_doctors()
    if doctor_username in doctors:
        doctors[doctor_username]["current_load"] = doctors[doctor_username].get("current_load", 0) + 1
        save_doctors(doctors)


def decrement_doctor_load(doctor_username):
    """Decrement the active case count for a doctor (min 0)."""
    doctors = load_doctors()
    if doctor_username in doctors:
        current = doctors[doctor_username].get("current_load", 0)
        doctors[doctor_username]["current_load"] = max(0, current - 1)
        doctors[doctor_username]["total_cases_handled"] = doctors[doctor_username].get("total_cases_handled", 0) + 1
        save_doctors(doctors)


def set_doctor_availability(doctor_username, status):
    """Set a doctor's availability status ('available' | 'busy')."""
    doctors = load_doctors()
    if doctor_username in doctors:
        doctors[doctor_username]["availability"] = status
        save_doctors(doctors)


def get_doctor_profile(doctor_username):
    """Get a single doctor's profile dict."""
    doctors = load_doctors()
    return doctors.get(doctor_username)


def register_doctor_profile(username, display_name="", specialization="", city="", area="", hospital="", bio=""):
    """Create a doctor entry in doctors.json for a newly registered doctor."""
    doctors = load_doctors()
    if username not in doctors:
        doctors[username] = {
            "display_name": display_name or f"Dr. {username.title()}",
            "specialization": specialization or "General Dermatology",
            "qualification": "MBBS",
            "experience_years": 0,
            "location": {"city": city or "Unknown", "area": area or ""},
            "availability": "available",
            "current_load": 0,
            "total_cases_handled": 0,
            "rating": 4.0,
            "bio": bio or "Dermatologist",
            "estimated_response_hours": 4,
            "languages": ["English"],
            "hospital": hospital or ""
        }
        save_doctors(doctors)


# ══════════════════════════════════════════════════════════════════════════════
# STATISTICS
# ══════════════════════════════════════════════════════════════════════════════

def get_statistics():
    cases = load_cases()
    appointments = load_appointments()
    return {
        "total_cases": len(cases),
        "pending_cases": len(get_pending_cases()),
        "approved_cases": len(get_approved_cases()),
        "total_appointments": len(appointments),
        "pending_appointments": len(get_pending_appointments())
    }


def get_doctor_statistics(doctor_username):
    """Statistics scoped to a single doctor."""
    cases = load_cases()
    appointments = load_appointments()
    assigned   = [c for c in cases if c.get("assigned_doctor") == doctor_username]
    pending    = [c for c in assigned if not c.get("doctor_verified", False)]
    approved   = [c for c in assigned if c.get("doctor_verified", False)]
    my_apts    = [a for a in appointments if a.get("doctor") == doctor_username]
    pend_apts  = [a for a in my_apts if a.get("status") == "pending"]
    return {
        "total_cases": len(assigned),
        "pending_cases": len(pending),
        "approved_cases": len(approved),
        "total_appointments": len(my_apts),
        "pending_appointments": len(pend_apts)
    }
