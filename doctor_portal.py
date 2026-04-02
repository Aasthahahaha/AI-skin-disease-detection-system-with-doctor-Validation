"""
Doctor Portal Module - Professional Medical SaaS Design
Extensive HTML/CSS implementation for admin panel
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Import project modules
from database import (
    load_cases,
    save_cases,
    get_pending_cases,
    get_approved_cases,
    load_appointments,
    get_pending_appointments,
    update_appointment_status,
    get_statistics
)
from auth import logout


def doctor_dashboard():
    """
    Display professional doctor dashboard with HTML/CSS admin panel design
    """
    
    doctor_name = st.session_state.get("username", "Doctor")
    
    # Dashboard Header with HTML/CSS
    st.markdown(f"""
    <div class="dashboard-header">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h1>👨‍⚕️ Doctor Dashboard</h1>
                <p>Welcome, <strong>Dr. {doctor_name}</strong></p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Logout button
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    with col4:
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            logout()
    
    # Statistics Section
    st.markdown("""
    <div class="medical-card">
        <div class="medical-card-header">
            <h3 class="medical-card-title">📊 System Overview</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    show_statistics()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs([
        "🔍 Pending Cases",
        "✅ Approved Cases",
        "📅 Appointments"
    ])
    
    with tab1:
        review_cases()
    
    with tab2:
        view_approved_cases()
    
    with tab3:
        manage_appointments()


def show_statistics():
    """
    Display system statistics with HTML/CSS stat cards
    """
    stats = get_statistics()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card stat-card-blue">
            <div class="stat-card-icon">📊</div>
            <div class="stat-card-label">Total Cases</div>
            <div class="stat-card-value">{stats["total_cases"]}</div>
            <div class="stat-card-change">All submissions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card stat-card-yellow">
            <div class="stat-card-icon">⏳</div>
            <div class="stat-card-label">Pending</div>
            <div class="stat-card-value">{stats["pending_cases"]}</div>
            <div class="stat-card-change">Needs review</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card stat-card-green">
            <div class="stat-card-icon">✅</div>
            <div class="stat-card-label">Approved</div>
            <div class="stat-card-value">{stats["approved_cases"]}</div>
            <div class="stat-card-change">Verified</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card stat-card-purple">
            <div class="stat-card-icon">📅</div>
            <div class="stat-card-label">Appointments</div>
            <div class="stat-card-value">{stats["total_appointments"]}</div>
            <div class="stat-card-change">Total</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="stat-card stat-card-orange">
            <div class="stat-card-icon">⏰</div>
            <div class="stat-card-label">Pending Apts</div>
            <div class="stat-card-value">{stats["pending_appointments"]}</div>
            <div class="stat-card-change">Waiting</div>
        </div>
        """, unsafe_allow_html=True)


def review_cases():
    """
    Display and manage pending cases with HTML/CSS design
    """
    
    st.markdown("""
    <div class="medical-card">
        <div class="medical-card-header">
            <h2 class="medical-card-title">🔍 Cases Awaiting Review</h2>
        </div>
        <div class="medical-card-body">
            <p style="color: var(--text-secondary);">
                Review AI predictions and provide professional diagnosis
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Get pending cases
    cases = get_pending_cases()
    
    if not cases:
        st.markdown("""
        <div class="medical-card" style="text-align: center; padding: 3rem; background: linear-gradient(135deg, var(--success-light) 0%, #FFFFFF 100%);">
            <h2 style="color: var(--success-dark); margin-bottom: 1rem;">🎉 All Caught Up!</h2>
            <p style="color: var(--success-dark); font-size: 1.1rem;">
                No pending cases at the moment. Great work!
            </p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Search filter
    col1, col2 = st.columns([2, 1])
    with col1:
        search_term = st.text_input(
            "🔎 Search by patient name",
            placeholder="Enter patient username...",
            label_visibility="collapsed"
        )
    
    if search_term:
        cases = [c for c in cases if search_term.lower() in c.get("user", "").lower()]
        st.caption(f"Found {len(cases)} matching case(s)")
    
    st.markdown(f"**Showing {len(cases)} case(s) awaiting review**")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display cases for review
    for i, case in enumerate(cases):
        display_case_for_review(case, i)


def display_case_for_review(case, case_index):
    """
    Display single case review card with HTML/CSS
    """
    
    # Get original index
    all_cases = load_cases()
    original_index = None
    for idx, c in enumerate(all_cases):
        if (c.get("user") == case.get("user") and 
            c.get("date") == case.get("date") and
            c.get("image") == case.get("image")):
            original_index = idx
            break
    
    # Case review card header
    st.markdown("""
    <div class="medical-card" style="border-left: 4px solid var(--warning); background: var(--warning-light);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <h3 style="margin: 0; color: var(--warning-dark);">📋 Case Review Required</h3>
            <span class="badge badge-warning">⏳ PENDING REVIEW</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1.5])
    
    with col1:
        # Patient image
        st.markdown("""
        <div class="medical-card">
            <div class="medical-card-header">
                <h4 class="medical-card-title">📷 Patient Image</h4>
            </div>
        """, unsafe_allow_html=True)
        
        image_path = case.get("image", "")
        if os.path.exists(image_path):
            st.image(
                image_path,
                caption=f"Submitted: {case.get('date', 'N/A')[:10]}",
                use_container_width=True
            )
        else:
            st.error("❌ Image not found")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        # Case information
        st.markdown("""
        <div class="medical-card">
            <div class="medical-card-header">
                <h4 class="medical-card-title">📊 Case Information</h4>
            </div>
        """, unsafe_allow_html=True)
        
        # Patient info box
        st.markdown(f"""
        <div class="info-box info-box-primary">
            <p style="margin: 0 0 0.25rem 0; font-size: 0.875rem; color: var(--info-dark); font-weight: 600;">
                PATIENT
            </p>
            <p style="margin: 0; font-size: 1.1rem; font-weight: 600; color: var(--info-dark);">
                👤 {case.get('user', 'N/A')}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Date info box
        st.markdown(f"""
        <div class="info-box info-box-primary">
            <p style="margin: 0 0 0.25rem 0; font-size: 0.875rem; color: var(--info-dark); font-weight: 600;">
                SUBMISSION DATE
            </p>
            <p style="margin: 0; font-weight: 600; color: var(--info-dark);">
                📅 {case.get('date', 'N/A')[:19]}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # AI Prediction highlight
        st.markdown(f"""
        <div class="result-highlight" style="text-align: left;">
            <div class="result-title">🤖 AI PREDICTION</div>
            <div class="result-value" style="font-size: 1.75rem;">{case.get('ai_result', 'N/A')}</div>
            <p style="margin-top: 0.75rem; color: var(--primary); font-weight: 600;">
                📊 Confidence: <strong>{case.get('confidence', 'N/A')}</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        # Doctor's review section
        st.markdown("""
        <div class="medical-card">
            <div class="medical-card-header">
                <h4 class="medical-card-title">🩺 Professional Review</h4>
            </div>
        """, unsafe_allow_html=True)
        
        # Notes input
        doctor_notes = st.text_area(
            "Clinical Notes & Observations",
            placeholder="Enter detailed clinical observations, diagnosis, and recommendations...",
            key=f"notes_{original_index}",
            height=120,
            help="Provide your professional assessment"
        )
        
        # AI agreement radio
        agree_ai = st.radio(
            "🤖 AI Prediction Assessment:",
            ["✅ Agree with AI", "⚠️ Disagree with AI"],
            key=f"agree_{original_index}",
            horizontal=True
        )
        
        # Conditional diagnosis input
        if "Disagree" in agree_ai:
            correct_diagnosis = st.text_input(
                "Correct Diagnosis",
                placeholder="Enter your diagnosis...",
                key=f"diagnosis_{original_index}"
            )
        else:
            correct_diagnosis = case.get("ai_result", "")
        
        # Approve button
        approve_btn = st.button(
            "✅ Approve & Submit Review",
            key=f"approve_{original_index}",
            type="primary",
            use_container_width=True
        )
        
        if approve_btn:
            if not doctor_notes:
                st.error("❌ Please provide clinical notes before approving.")
            elif "Disagree" in agree_ai and not correct_diagnosis:
                st.error("❌ Please provide the correct diagnosis.")
            else:
                if original_index is not None:
                    # Update case
                    all_cases[original_index]["doctor_verified"] = True
                    all_cases[original_index]["doctor_notes"] = doctor_notes
                    all_cases[original_index]["doctor_name"] = st.session_state.get("username", "")
                    all_cases[original_index]["ai_agreed"] = "Agree" in agree_ai
                    all_cases[original_index]["correct_diagnosis"] = correct_diagnosis
                    all_cases[original_index]["verified_at"] = datetime.now().isoformat()
                    all_cases[original_index]["status"] = "approved"
                    
                    save_cases(all_cases)
                    st.success("✅ **Case approved successfully!** Patient will be notified.")
                    st.balloons()
                    st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)


def view_approved_cases():
    """
    Display approved cases with HTML/CSS design
    """
    
    st.markdown("""
    <div class="medical-card">
        <div class="medical-card-header">
            <h2 class="medical-card-title">✅ Approved Case Archive</h2>
        </div>
        <div class="medical-card-body">
            <p style="color: var(--text-secondary);">
                View all professionally reviewed and approved cases
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Get approved cases
    cases = get_approved_cases()
    
    if not cases:
        st.markdown("""
        <div class="medical-card" style="text-align: center; padding: 2rem;">
            <p style="color: var(--text-secondary); font-size: 1.1rem;">
                📭 No approved cases yet.
            </p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Search
    col1, col2 = st.columns([2, 1])
    with col1:
        search_term = st.text_input(
            "🔎 Search by patient name",
            placeholder="Enter patient username...",
            key="search_approved"
        )
    
    if search_term:
        cases = [c for c in cases if search_term.lower() in c.get("user", "").lower()]
    
    st.markdown(f"**Showing {len(cases)} approved case(s)**")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display approved cases
    for case in cases:
        st.markdown("""
        <div class="case-card" style="border-left: 4px solid var(--success); background: var(--success-light);">
            <div class="case-card-header">
                <h4 style="margin: 0; color: var(--success-dark);">📋 Approved Case</h4>
                <span class="badge badge-success">✅ APPROVED</span>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            image_path = case.get("image", "")
            if os.path.exists(image_path):
                st.image(
                    image_path,
                    caption="Patient Image",
                    use_container_width=True
                )
        
        with col2:
            # Case details
            st.markdown(f"""
            <div style="padding: 1rem;">
                <p style="margin-bottom: 0.5rem;">
                    <strong style="color: var(--text-primary);">👤 Patient:</strong> 
                    <span style="color: var(--text-secondary);">{case.get('user', 'N/A')}</span>
                </p>
                <p style="margin-bottom: 0.5rem;">
                    <strong style="color: var(--text-primary);">📅 Submitted:</strong> 
                    <span style="color: var(--text-secondary);">{case.get('date', 'N/A')[:19]}</span>
                </p>
                <p style="margin-bottom: 0.5rem;">
                    <strong style="color: var(--text-primary);">🤖 AI Prediction:</strong> 
                    <span style="color: var(--text-secondary);">{case.get('ai_result', 'N/A')} ({case.get('confidence', 'N/A')})</span>
                </p>
                <p style="margin-bottom: 0.5rem;">
                    <strong style="color: var(--text-primary);">👨‍⚕️ Reviewed by:</strong> 
                    <span style="color: var(--text-secondary);">Dr. {case.get('doctor_name', 'N/A')}</span>
                </p>
                <p style="margin-bottom: 0;">
                    <strong style="color: var(--text-primary);">✅ Verified:</strong> 
                    <span style="color: var(--text-secondary);">{case.get('verified_at', 'N/A')[:19]}</span>
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            # AI agreement status
            if case.get("ai_agreed"):
                st.markdown("""
                <div class="info-box info-box-success">
                    <p style="margin: 0; font-weight: 600;">🤖 AI Agreed</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="info-box info-box-warning">
                    <p style="margin: 0; font-weight: 600;">⚠️ AI Disagreed</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Final diagnosis
            if case.get("correct_diagnosis"):
                st.markdown(f"""
                <div class="info-box info-box-primary">
                    <p style="margin: 0 0 0.25rem 0; font-size: 0.75rem; font-weight: 600;">
                        FINAL DIAGNOSIS
                    </p>
                    <p style="margin: 0; font-weight: 600;">
                        {case.get('correct_diagnosis')}
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        # Doctor's notes
        if case.get("doctor_notes"):
            with st.expander("📝 View Clinical Notes"):
                st.markdown(f"""
                <div style="background: var(--card-bg); padding: 1rem; border-radius: 8px;">
                    <p style="font-style: italic; color: var(--text-primary); line-height: 1.6; margin: 0;">
                        {case.get('doctor_notes')}
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div><br>", unsafe_allow_html=True)


def manage_appointments():
    """
    Manage appointments with HTML/CSS design
    """
    
    st.markdown("""
    <div class="medical-card">
        <div class="medical-card-header">
            <h2 class="medical-card-title">📅 Appointment Management</h2>
        </div>
        <div class="medical-card-body">
            <p style="color: var(--text-secondary);">
                Review and manage patient appointment requests
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Get pending appointments
    appointments = get_pending_appointments()
    
    if not appointments:
        st.markdown("""
        <div class="medical-card" style="text-align: center; padding: 3rem; background: linear-gradient(135deg, var(--success-light) 0%, #FFFFFF 100%);">
            <h3 style="color: var(--success-dark); margin-bottom: 1rem;">🎉 No Pending Appointments</h3>
            <p style="color: var(--success-dark);">All appointment requests have been processed!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"**{len(appointments)} appointment request(s) pending**")
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Display appointments
        for i, apt in enumerate(appointments):
            display_appointment_card(apt, i)
    
    # All appointments section
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="medical-card">
        <div class="medical-card-header">
            <h3 class="medical-card-title">📋 All Appointments</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    all_appointments = load_appointments()
    
    if not all_appointments:
        st.info("📭 No appointments in the system.")
    else:
        # Create dataframe
        apt_data = []
        for apt in all_appointments:
            status_emoji = {"pending": "⏳", "approved": "✅", "rejected": "❌"}.get(apt.get("status", ""), "📋")
            apt_data.append({
                "Patient": apt.get("user", ""),
                "Doctor": apt.get("doctor", ""),
                "Date": apt.get("date", ""),
                "Time": apt.get("time", ""),
                "Urgency": apt.get("urgency", ""),
                "Status": f"{status_emoji} {apt.get('status', '').upper()}"
            })
        
        if apt_data:
            df = pd.DataFrame(apt_data)
            st.dataframe(df, use_container_width=True, height=300)


def display_appointment_card(apt, apt_index):
    """
    Display single appointment card with HTML/CSS
    """
    
    # Get original index
    all_apts = load_appointments()
    original_index = None
    for idx, a in enumerate(all_apts):
        if (a.get("user") == apt.get("user") and 
            a.get("date") == apt.get("date") and
            a.get("time") == apt.get("time")):
            original_index = idx
            break
    
    # Urgency styling
    urgency = apt.get("urgency", "Medium")
    urgency_colors = {
        "Low": ("var(--success)", "var(--success-light)"),
        "Medium": ("var(--warning)", "var(--warning-light)"),
        "High": ("var(--error)", "var(--error-light)"),
        "Urgent": ("#991B1B", "#FEE2E2")
    }
    border_color, bg_color = urgency_colors.get(urgency, ("var(--warning)", "var(--warning-light)"))
    
    st.markdown(f"""
    <div class="medical-card" style="border-left: 4px solid {border_color}; background: {bg_color};">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <h4 style="margin: 0;">📅 Appointment Request</h4>
            <span class="badge" style="background: {border_color}; color: white;">
                ⚡ {urgency.upper()} PRIORITY
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 2, 1.5])
    
    with col1:
        st.markdown(f"""
        <div class="info-box info-box-primary">
            <p style="margin: 0 0 0.25rem 0; font-size: 0.875rem; font-weight: 600;">PATIENT</p>
            <p style="margin: 0; font-size: 1.1rem; font-weight: 600;">
                👤 {apt.get('user', 'N/A')}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"**📅 Requested Date:** {apt.get('date', 'N/A')}")
        st.markdown(f"**⏰ Requested Time:** {apt.get('time', 'N/A')}")
    
    with col2:
        st.markdown("**📝 Patient Symptoms:**")
        st.markdown(f"""
        <div style="background: var(--card-bg); padding: 1rem; border-radius: 8px; border-left: 3px solid var(--primary);">
            <p style="margin: 0; color: var(--text-primary); line-height: 1.6;">
                {apt.get('symptoms', 'N/A')}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("**⚡ Actions**")
        
        # Approve button
        if st.button(
            "✅ Approve",
            key=f"apt_approve_{original_index}",
            use_container_width=True,
            type="primary"
        ):
            if original_index is not None:
                update_appointment_status(original_index, "approved")
                st.success("✅ Appointment approved!")
                st.rerun()
        
        # Reject button
        if st.button(
            "❌ Reject",
            key=f"apt_reject_{original_index}",
            use_container_width=True
        ):
            if original_index is not None:
                update_appointment_status(original_index, "rejected")
                st.warning("Appointment rejected.")
                st.rerun()
    
    # Notes section
    with st.expander("📝 Add Notes for Patient"):
        notes = st.text_area(
            "Clinical notes or instructions",
            placeholder="Add any notes or instructions for the patient...",
            key=f"apt_notes_{original_index}",
            label_visibility="collapsed"
        )
        
        if st.button("💾 Save Notes", key=f"save_apt_notes_{original_index}"):
            if original_index is not None and notes:
                update_appointment_status(original_index, "pending", notes)
                st.success("✅ Notes saved successfully!")
    
    st.markdown("<br>", unsafe_allow_html=True)