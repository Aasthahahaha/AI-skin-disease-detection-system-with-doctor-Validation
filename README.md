# AI-Assisted Skin Disease Detection System

A prototype web application for AI-powered skin disease detection with doctor verification workflow.

## 🏥 Features

### User Portal
- 📸 Upload skin images for AI analysis
- 🤖 Get instant AI predictions with confidence scores
- 📋 View case history and approval status
- 📅 Request appointments with doctors
- 🔍 Track case status (pending/approved)

### Doctor Portal
- 👨‍⚕️ Review and approve patient cases
- 📝 Add clinical notes and diagnosis
- 📊 View statistics and case metrics
- 📅 Manage appointment requests
- 🔍 Search and filter cases

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Streamlit

### Installation

1. Install Streamlit:
```bash
pip install streamlit pandas
```

2. Navigate to the project directory:
```bash
cd /Users/rahul/Downloads/skindemo\ copy.py
```

3. Run the application:
```bash
streamlit run app.py
```

4. Open your browser and go to:
```
http://localhost:8501
```

## 👤 Demo Accounts

| Role | Username | Password |
|------|----------|----------|
| User | user1 | 123 |
| Doctor | doctor1 | 123 |
| User | user2 | 123 |
| Doctor | doctor2 | 123 |

## 📁 Project Structure

```
skin_ai_project/
├── app.py                 # Main application controller
├── auth.py                # Authentication module
├── database.py            # JSON database management
├── user_portal.py         # User dashboard
├── doctor_portal.py       # Doctor dashboard
├── ml_model.py            # AI prediction module
├── aimodel.py             # Legacy model (can be deleted)
├── README.md              # This file
├── TODO.md                # Development notes
├── data/
│   ├── user.json          # User credentials
│   ├── cases.json         # Medical cases
│   └── appointment.json   # Appointments
└── uploads/               # Uploaded images
```

## 🔐 Authentication

- Users can register new accounts
- Login with username/password
- Role-based access (User/Doctor)
- Session management with logout

## 📊 Workflow

1. **User uploads image** → AI analyzes and provides prediction
2. **Case saved** → Status marked as "pending"
3. **Doctor reviews** → Verifies, adds notes, approves
4. **User notified** → Can see approval and doctor's notes

## 🛠️ Technology Stack

- **Frontend/Backend**: Streamlit (Python)
- **Data Storage**: JSON files
- **Authentication**: Session-based
- **AI Model**: Prototype simulation (random predictions)

## ⚠️ Disclaimer

This is a **prototype/demo** for educational purposes only. The AI predictions are simulated and should NOT be used for actual medical diagnosis. Always consult qualified healthcare professionals for medical advice.

## 📝 License

Educational Project - Final Year Engineering Project

