"""
User Portal Module - Professional Medical SaaS Design
Extensive HTML/CSS implementation with minimal Streamlit
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Import project modules
from ml_model import predict_disease
from database import (
    add_case,
    get_user_cases,
    request_appointment,
    load_appointments
)
from auth import logout


def user_dashboard(username):
    """
    Display professional user dashboard with HTML/CSS design
    """
    
    # Dashboard Header with HTML/CSS
    st.markdown(f"""
    <div class="dashboard-header">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h1>👤 Patient Portal</h1>
                <p>Welcome back, <strong>{username}</strong></p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Logout button in top right
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    with col4:
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            logout()
    
    # Quick Stats Section with HTML/CSS
    st.markdown("""
    <div class="medical-card">
        <div class="medical-card-header">
            <h3 class="medical-card-title">📊 Quick Overview</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Get statistics
    cases = get_user_cases(username)
    appointments = load_appointments()
    user_appointments = [apt for apt in appointments if apt.get("user") == username]
    
    pending_cases = len([c for c in cases if not c.get("doctor_verified", False)])
    approved_cases = len([c for c in cases if c.get("doctor_verified", False)])
    pending_apts = len([a for a in user_appointments if a.get("status") == "pending"])
    
    # Display stat cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card stat-card-blue">
            <div class="stat-card-icon">📊</div>
            <div class="stat-card-label">Total Cases</div>
            <div class="stat-card-value">{len(cases)}</div>
            <div class="stat-card-change">All submissions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card stat-card-yellow">
            <div class="stat-card-icon">⏳</div>
            <div class="stat-card-label">Pending Review</div>
            <div class="stat-card-value">{pending_cases}</div>
            <div class="stat-card-change">Awaiting doctor</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card stat-card-green">
            <div class="stat-card-icon">✅</div>
            <div class="stat-card-label">Approved</div>
            <div class="stat-card-value">{approved_cases}</div>
            <div class="stat-card-change">Doctor verified</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card stat-card-purple">
            <div class="stat-card-icon">📅</div>
            <div class="stat-card-label">Appointments</div>
            <div class="stat-card-value">{len(user_appointments)}</div>
            <div class="stat-card-change">{pending_apts} pending</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Create tabs for different features
    tab1, tab2, tab3 = st.tabs([
        "📸 New Analysis",
        "📋 My Cases",
        "📅 Appointments"
    ])
    
    with tab1:
        upload_and_predict(username)
    
    with tab2:
        view_case_history(username)
    
    with tab3:
        appointment_section(username)


def upload_and_predict(username):
    """
    Handle image upload and AI prediction with HTML/CSS design
    """
    
    # Upload Card with HTML/CSS
    st.markdown("""
    <div class="medical-card">
        <div class="medical-card-header">
            <h2 class="medical-card-title">🔬 AI-Powered Skin Analysis</h2>
        </div>
        <div class="medical-card-body">
            <p style="color: var(--text-secondary); margin-bottom: 1.5rem;">
                Upload a clear image of the affected skin area for AI analysis. 
                Our advanced system will provide an initial assessment, which will then be 
                reviewed by a licensed dermatologist.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Two column layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="medical-card">
            <div class="medical-card-header">
                <h3 class="medical-card-title">📤 Upload Image</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # File uploader (Streamlit component - backend)
        uploaded_file = st.file_uploader(
            "Choose a skin image...",
            type=["jpg", "jpeg", "png"],
            help="Upload a clear image of the affected skin area",
            label_visibility="collapsed"
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Tips section with HTML/CSS
        st.markdown("""
        <div class="medical-card" style="background: var(--info-light); border-left: 4px solid var(--info);">
            <h4 style="color: var(--info-dark); margin-bottom: 1rem;">💡 Tips for Best Results</h4>
            <ul style="color: var(--info-dark); line-height: 1.8; margin: 0; padding-left: 1.5rem;">
                <li>✅ Use good natural lighting</li>
                <li>✅ Focus clearly on the affected area</li>
                <li>✅ Avoid blurriness or motion</li>
                <li>✅ Include surrounding healthy skin</li>
                <li>❌ Don't use filters or editing</li>
                <li>❌ Avoid extreme angles</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if uploaded_file is not None:
            # Image preview card
            st.markdown("""
            <div class="medical-card">
                <div class="medical-card-header">
                    <h3 class="medical-card-title">🖼️ Image Preview</h3>
                </div>
            """, unsafe_allow_html=True)
            
            st.image(
                uploaded_file,
                caption="Uploaded Image",
                use_container_width=True
            )
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Analysis card
            st.markdown("""
            <div class="medical-card">
                <div class="medical-card-header">
                    <h3 class="medical-card-title">🤖 AI Analysis</h3>
                </div>
            """, unsafe_allow_html=True)
            
            # Analyze button
            if st.button("🔍 Analyze Image", type="primary", use_container_width=True):
                with st.spinner("🔄 AI is analyzing your image..."):
                    # Save uploaded file
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{username}_{timestamp}_{uploaded_file.name}"
                    filepath = os.path.join("uploads", filename)
                    
                    os.makedirs("uploads", exist_ok=True)
                    
                    with open(filepath, "wb") as f:
                        f.write(uploaded_file.getvalue())
                    
                    # Get AI prediction
                    disease, confidence = predict_disease(filepath)
                    
                    # Display results with HTML/CSS
                    st.markdown(f"""
                    <div class="result-highlight">
                        <div class="result-title">🤖 AI DIAGNOSIS</div>
                        <div class="result-value">{disease}</div>
                        <div class="result-confidence">{confidence}% Confidence</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Status badge
                    st.markdown("""
                    <div class="info-box info-box-warning">
                        <p style="margin: 0; font-weight: 600;">
                            ⏳ <strong>Status:</strong> Pending Doctor Review
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Next steps info
                    st.markdown("""
                    <div class="info-box info-box-primary">
                        <p style="margin: 0;">
                            <strong>ℹ️ Next Steps:</strong> Your case has been submitted and is awaiting 
                            review by a licensed dermatologist. You'll be notified once the review is complete.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Save case
                    case_data = {
                        "user": username,
                        "image": filepath,
                        "ai_result": disease,
                        "confidence": f"{confidence}%",
                        "doctor_verified": False,
                        "doctor_notes": "",
                        "doctor_name": "",
                        "date": datetime.now().isoformat(),
                        "status": "pending"
                    }
                    
                    if add_case(case_data):
                        st.success("✅ **Case saved successfully!** View it in 'My Cases' tab.")
                    else:
                        st.error("❌ Error saving case. Please try again.")
            
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            # Empty state with HTML/CSS
            st.markdown("""
            <div class="upload-zone">
                <div class="upload-zone-icon">📋</div>
                <div class="upload-zone-title">Upload Image</div>
                <div class="upload-zone-subtitle">Select an image from the upload box on the left</div>
            </div>
            """, unsafe_allow_html=True)


def view_case_history(username):
    """
    Display user's case history with HTML/CSS cards
    """
    
    st.markdown("""
    <div class="medical-card">
        <div class="medical-card-header">
            <h2 class="medical-card-title">📋 Medical Case History</h2>
        </div>
        <div class="medical-card-body">
            <p style="color: var(--text-secondary);">
                View all your past skin analyses and doctor reviews
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Get user's cases
    cases = get_user_cases(username)
    
    if not cases:
        st.markdown("""
        <div class="medical-card" style="text-align: center; padding: 3rem; background: linear-gradient(135deg, var(--info-light) 0%, #FFFFFF 100%);">
            <h3 style="color: var(--text-secondary); margin-bottom: 1rem;">📭 No Cases Yet</h3>
            <p style="color: var(--text-secondary); font-size: 1.1rem; margin-bottom: 0;">
                You haven't uploaded any images for analysis yet.
            </p>
            <p style="color: var(--text-secondary); margin-top: 1rem;">
                Go to the <strong>'New Analysis'</strong> tab to get started!
            </p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Filter options
    col1, col2 = st.columns([2, 1])
    with col1:
        filter_option = st.selectbox(
            "📂 Filter cases by status",
            ["All Cases", "Pending Review", "Doctor Approved"],
            label_visibility="collapsed"
        )
    
    # Filter cases
    if filter_option == "Pending Review":
        filtered_cases = [c for c in cases if not c.get("doctor_verified", False)]
    elif filter_option == "Doctor Approved":
        filtered_cases = [c for c in cases if c.get("doctor_verified", False)]
    else:
        filtered_cases = cases
    
    st.markdown(f"**Showing {len(filtered_cases)} of {len(cases)} case(s)**")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display cases
    for i, case in enumerate(filtered_cases):
        case_number = cases.index(case) + 1
        is_approved = case.get("doctor_verified", False)
        
        # Case card with HTML/CSS
        badge_class = "badge-success" if is_approved else "badge-warning"
        badge_text = "✅ APPROVED" if is_approved else "⏳ PENDING"
        
        st.markdown(f"""
        <div class="case-card">
            <div class="case-card-header">
                <div class="case-card-title">📋 Case #{case_number}</div>
                <span class="badge {badge_class}">{badge_text}</span>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Display image
            if os.path.exists(case.get("image", "")):
                st.image(
                    case.get("image", ""),
                    caption=f"Submitted: {case.get('date', 'N/A')[:10]}",
                    use_container_width=True
                )
            else:
                st.error("📷 Image not found")
        
        with col2:
            # Case details with HTML/CSS
            st.markdown(f"""
            <div style="padding: 1rem;">
                <p style="margin-bottom: 0.5rem;">
                    <strong style="color: var(--text-primary);">📅 Submission Date:</strong> 
                    <span style="color: var(--text-secondary);">{case.get('date', 'N/A')[:19]}</span>
                </p>
                <p style="margin-bottom: 0.5rem;">
                    <strong style="color: var(--text-primary);">🤖 AI Analysis:</strong> 
                    <span style="color: var(--text-secondary);">{case.get('ai_result', 'N/A')}</span>
                </p>
                <p style="margin-bottom: 1rem;">
                    <strong style="color: var(--text-primary);">📊 Confidence Level:</strong> 
                    <span style="color: var(--text-secondary);">{case.get('confidence', 'N/A')}</span>
                </p>
            """, unsafe_allow_html=True)
            
            # Doctor review section
            if is_approved:
                st.markdown(f"""
                <div class="info-box info-box-success">
                    <p style="margin: 0 0 0.5rem 0; font-weight: 600; color: var(--success-dark);">
                        ✅ Reviewed by Dr. {case.get('doctor_name', 'N/A')}
                    </p>
                    <p style="margin: 0; color: var(--success-dark);">
                        <strong>🩺 Verified Diagnosis:</strong> {case.get('correct_diagnosis', case.get('ai_result', 'N/A'))}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                if case.get("doctor_notes"):
                    with st.expander("📝 View Doctor's Notes"):
                        st.markdown(f"""
                        <div style="background: var(--card-bg); padding: 1rem; border-radius: 8px;">
                            <p style="font-style: italic; color: var(--text-primary); line-height: 1.6;">
                                {case.get('doctor_notes')}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.caption(f"✓ Verified on: {case.get('verified_at', 'N/A')[:19]}")
            else:
                st.markdown("""
                <div class="info-box info-box-warning">
                    <p style="margin: 0; font-weight: 600;">
                        ⏳ Awaiting doctor review
                    </p>
                </div>
                """, unsafe_allow_html=True)
                st.caption("Your case will be reviewed by a dermatologist shortly")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div><br>", unsafe_allow_html=True)


def appointment_section(username):
    """
    Handle appointment requests with HTML/CSS design
    """
    
    st.markdown("""
    <div class="medical-card">
        <div class="medical-card-header">
            <h2 class="medical-card-title">📅 Schedule an Appointment</h2>
        </div>
        <div class="medical-card-body">
            <p style="color: var(--text-secondary);">
                Request a consultation with our dermatology specialists
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Get available doctors
    from auth import load_users
    users = load_users()
    doctors = [(name, data) for name, data in users.items() if data.get("role") == "Doctor"]
    
    if not doctors:
        st.error("❌ No doctors available at the moment. Please check back later.")
        return
    
    doctor_options = {f"Dr. {name}": name for name, _ in doctors}
    
    # Two column layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Appointment request form
        st.markdown("""
        <div class="medical-card">
            <div class="medical-card-header">
                <h3 class="medical-card-title">📝 Request Form</h3>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("appointment_form", clear_on_submit=True):
            selected_doctor = st.selectbox(
                "👨‍⚕️ Select Doctor",
                options=list(doctor_options.keys()),
                help="Choose your preferred dermatologist"
            )
            
            appointment_date = st.date_input(
                "📅 Preferred Date",
                min_value=datetime.now().date(),
                help="Select your preferred appointment date"
            )
            
            appointment_time = st.time_input(
                "⏰ Preferred Time",
                help="Select your preferred time slot"
            )
            
            symptoms = st.text_area(
                "📋 Describe Your Symptoms",
                placeholder="Please describe your skin condition, symptoms, when they started, and any concerns...",
                help="Provide detailed information about your condition",
                height=120
            )
            
            urgency = st.select_slider(
                "⚡ Urgency Level",
                options=["Low", "Medium", "High", "Urgent"],
                value="Medium",
                help="How urgent is your condition?"
            )
            
            submit = st.form_submit_button(
                "📤 Submit Appointment Request",
                type="primary",
                use_container_width=True
            )
            
            if submit:
                if not selected_doctor or not symptoms:
                    st.error("❌ Please fill in all required fields.")
                else:
                    appointment_data = {
                        "user": username,
                        "doctor": doctor_options[selected_doctor],
                        "date": str(appointment_date),
                        "time": str(appointment_time),
                        "symptoms": symptoms,
                        "urgency": urgency,
                        "status": "pending"
                    }
                    
                    if request_appointment(appointment_data):
                        st.success("✅ **Appointment request submitted successfully!**")
                        st.info("📧 You will receive a notification once the doctor reviews your request.")
                    else:
                        st.error("❌ Error submitting appointment. Please try again.")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        # Appointment history
        st.markdown("""
        <div class="medical-card">
            <div class="medical-card-header">
                <h3 class="medical-card-title">📋 My Appointments</h3>
            </div>
        """, unsafe_allow_html=True)
        
        appointments = load_appointments()
        user_appointments = [apt for apt in appointments if apt.get("user") == username]
        
        if not user_appointments:
            st.markdown("""
            <div style="text-align: center; padding: 2rem;">
                <p style="color: var(--text-secondary); font-size: 1rem;">
                    📭 You haven't requested any appointments yet.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            for apt in user_appointments:
                status = apt.get("status", "pending")
                
                # Status styling
                if status == "approved":
                    status_color = "var(--success)"
                    status_bg = "var(--success-light)"
                    status_icon = "✅"
                elif status == "rejected":
                    status_color = "var(--error)"
                    status_bg = "var(--error-light)"
                    status_icon = "❌"
                else:
                    status_color = "var(--warning)"
                    status_bg = "var(--warning-light)"
                    status_icon = "⏳"
                
                st.markdown(f"""
                <div style="background: {status_bg}; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid {status_color};">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <strong style="color: {status_color};">👨‍⚕️ Dr. {apt.get('doctor', 'N/A')}</strong>
                        <span class="badge" style="background: {status_color}; color: white;">
                            {status_icon} {status.upper()}
                        </span>
                    </div>
                    <p style="margin: 0.25rem 0; font-size: 0.875rem; color: var(--text-secondary);">
                        📅 {apt.get('date', 'N/A')} at {apt.get('time', 'N/A')}
                    </p>
                    <p style="margin: 0.25rem 0; font-size: 0.875rem; color: var(--text-secondary);">
                        ⚡ Urgency: <strong>{apt.get('urgency', 'N/A')}</strong>
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)