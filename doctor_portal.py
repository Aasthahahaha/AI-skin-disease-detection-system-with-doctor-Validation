"""
Doctor Portal Module — Premium UI with Assignment Filtering & Availability Toggle
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime

from database import (
    load_cases,
    save_cases,
    get_pending_cases_for_doctor,
    get_approved_cases_for_doctor,
    load_appointments,
    get_pending_appointments_for_doctor,
    update_appointment_status,
    get_doctor_statistics,
    get_doctor_profile,
    set_doctor_availability,
    decrement_doctor_load,
)
from auth import logout


def doctor_dashboard():
    doctor_username = st.session_state.get("username", "Doctor")
    profile = get_doctor_profile(doctor_username) or {}
    display_name  = profile.get("display_name", f"Dr. {doctor_username.title()}")
    specialization = profile.get("specialization", "Dermatology")
    location      = profile.get("location", {})
    city          = location.get("city", "")
    availability  = profile.get("availability", "available")

    # ── Sidebar ────────────────────────────────────────────────────────────────
    with st.sidebar:
        def toggle_theme(): st.session_state["theme"] = "light" if st.session_state.get("theme", "dark") == "dark" else "dark"
        theme_label = "☀️ Light Mode" if st.session_state.get("theme", "dark") == "dark" else "🌙 Dark Mode"
        st.button(theme_label, on_click=toggle_theme, key="doctor_theme_btn", use_container_width=True)
        st.markdown("---")
        st.markdown(f"""
        <div class="sidebar-profile">
            <div class="sidebar-avatar">🩺</div>
            <div class="sidebar-name">{display_name}</div>
            <div class="sidebar-role-badge doctor-badge">Doctor</div>
            <div class="sidebar-spec">{specialization}</div>
            <div class="sidebar-location">📍 {city}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### 🟢 Availability Status")

        current_status = "available" if availability == "available" else "busy"
        toggle = st.toggle(
            "Available for new cases",
            value=(current_status == "available"),
            help="Turn off to stop receiving new cases"
        )
        new_status = "available" if toggle else "busy"
        if new_status != availability:
            set_doctor_availability(doctor_username, new_status)
            st.rerun()

        avail_color = "#10B981" if new_status == "available" else "#EF4444"
        st.markdown(f"""
        <div style="text-align:center;margin-top:0.5rem;">
            <span style="color:{avail_color};font-weight:600;font-size:0.9rem;">
                {'🟢 Accepting Cases' if new_status == 'available' else '🔴 Not Accepting Cases'}
            </span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        stats = get_doctor_statistics(doctor_username)
        st.markdown(f"""
        <div class="sidebar-stats">
            <div class="sidebar-stat"><span class="sidebar-stat-num">{stats['total_cases']}</span><span class="sidebar-stat-label">My Cases</span></div>
            <div class="sidebar-stat"><span class="sidebar-stat-num pending">{stats['pending_cases']}</span><span class="sidebar-stat-label">Pending</span></div>
            <div class="sidebar-stat"><span class="sidebar-stat-num approved">{stats['approved_cases']}</span><span class="sidebar-stat-label">Reviewed</span></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Doctor profile card in sidebar
        if profile:
            st.markdown(f"""
            <div class="sidebar-doctor-card">
                <p>⭐ Rating: <strong>{profile.get('rating', '—')}</strong></p>
                <p>📋 Total Handled: <strong>{profile.get('total_cases_handled', 0)}</strong></p>
                <p>⏱ Avg Response: <strong>~{profile.get('estimated_response_hours', 4)}h</strong></p>
                <p>🏥 {profile.get('hospital', '')}</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            logout()

    # ── Header ─────────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="dashboard-header">
        <div class="dashboard-header-content">
            <div>
                <h1>👨‍⚕️ Doctor Dashboard</h1>
                <p>Welcome, <strong>{display_name}</strong> — {specialization} · {city}</p>
            </div>
            <div class="header-badge">MediScan AI</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Global stats ───────────────────────────────────────────────────────────
    _show_doctor_stats(doctor_username)

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🔍 My Pending Cases", "✅ Reviewed Cases", "📅 My Appointments"])
    with tab1:
        review_my_cases(doctor_username)
    with tab2:
        view_my_approved_cases(doctor_username)
    with tab3:
        manage_my_appointments(doctor_username)


def _show_doctor_stats(doctor_username):
    stats = get_doctor_statistics(doctor_username)
    col1, col2, col3, col4, col5 = st.columns(5)
    cards = [
        ("stat-card-blue",   "📊", "My Cases",      stats["total_cases"],         "Assigned to me"),
        ("stat-card-yellow", "⏳", "Pending",        stats["pending_cases"],        "Needs review"),
        ("stat-card-green",  "✅", "Reviewed",       stats["approved_cases"],       "Verified"),
        ("stat-card-purple", "📅", "Appointments",   stats["total_appointments"],   "Total"),
        ("stat-card-orange", "⏰", "Pending Apts",   stats["pending_appointments"], "Waiting"),
    ]
    for col, (css, icon, label, val, sub) in zip([col1,col2,col3,col4,col5], cards):
        with col:
            st.markdown(f"""
            <div class="stat-card {css}">
                <div class="stat-card-icon">{icon}</div>
                <div class="stat-card-label">{label}</div>
                <div class="stat-card-value">{val}</div>
                <div class="stat-card-change">{sub}</div>
            </div>""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# TAB 1 — PENDING CASES (scoped to this doctor)
# ──────────────────────────────────────────────────────────────────────────────

def review_my_cases(doctor_username):
    st.markdown("""
    <div class="medical-card">
        <div class="medical-card-header">
            <h2 class="medical-card-title">🔍 Cases Assigned to Me</h2>
        </div>
        <p>Review AI predictions and provide your professional diagnosis.</p>
    </div>
    """, unsafe_allow_html=True)

    cases = get_pending_cases_for_doctor(doctor_username)

    if not cases:
        st.markdown("""
        <div class="medical-card" style="text-align:center;padding:3rem;background:linear-gradient(135deg,var(--success-light) 0%,transparent 100%);">
            <h2 style="color:var(--success-dark);">🎉 All Caught Up!</h2>
            <p style="color:var(--success-dark);">No pending cases at the moment. Great work!</p>
        </div>""", unsafe_allow_html=True)
        return

    col1, _ = st.columns([2, 1])
    with col1:
        search_term = st.text_input("🔎 Search by patient", placeholder="Patient username...", label_visibility="collapsed")

    if search_term:
        cases = [c for c in cases if search_term.lower() in c.get("user", "").lower()]

    st.markdown(f"**{len(cases)} case(s) awaiting your review**")
    st.markdown("<br>", unsafe_allow_html=True)

    for i, case in enumerate(cases):
        _display_case_for_review(case, doctor_username)


def _display_case_for_review(case, doctor_username):
    all_cases = load_cases()
    original_index = None
    for idx, c in enumerate(all_cases):
        if (c.get("user") == case.get("user") and
                c.get("date") == case.get("date") and
                c.get("image") == case.get("image")):
            original_index = idx
            break

    # Image quality info
    iq = case.get("image_quality", {})
    quality_html = ""
    if iq:
        quality_html = f"""
        <div class="val-meta" style="margin-top:0.5rem;">
            <span class="val-chip">📐 {iq.get('width',0)}×{iq.get('height',0)} px</span>
            <span class="val-chip">🔍 Sharpness: {iq.get('blur_score',0):.0f}</span>
            <span class="val-chip">☀️ Brightness: {iq.get('brightness',0):.0f}</span>
        </div>"""

    st.markdown(f"""
    <div class="medical-card" style="border-left:4px solid var(--warning);">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;">
            <h3 style="margin:0;">📋 Case Review — Patient: {case.get('user','N/A')}</h3>
            <span class="badge badge-warning">⏳ PENDING</span>
        </div>
        {quality_html}
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1.5])

    with col1:
        st.markdown("""
        <div class="medical-card">
            <div class="medical-card-header"><h4 class="medical-card-title">📷 Patient Image</h4></div>
        """, unsafe_allow_html=True)
        image_path = case.get("image", "")
        if os.path.exists(image_path):
            st.image(image_path, caption=f"Submitted: {case.get('date','')[:10]}", use_container_width=True)
        else:
            st.error("❌ Image not found")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""<div class="medical-card"><div class="medical-card-header"><h4 class="medical-card-title">📊 Case Information</h4></div>""", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="info-box info-box-primary">
            <p style="margin:0 0 0.25rem 0;font-size:0.875rem;font-weight:600;">PATIENT</p>
            <p style="margin:0;font-size:1.1rem;font-weight:600;">👤 {case.get('user','N/A')}</p>
        </div>
        <div class="info-box info-box-primary" style="margin-top:0.5rem;">
            <p style="margin:0 0 0.25rem 0;font-size:0.875rem;font-weight:600;">SUBMISSION DATE</p>
            <p style="margin:0;font-weight:600;">📅 {case.get('date','N/A')[:19]}</p>
        </div>
        <div class="result-highlight" style="text-align:left;margin-top:0.75rem;">
            <div class="result-title">🤖 AI PREDICTION</div>
            <div class="result-value" style="font-size:1.75rem;">{case.get('ai_result','N/A')}</div>
            <p style="margin-top:0.5rem;color:var(--primary);font-weight:600;">📊 Confidence: <strong>{case.get('confidence','N/A')}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("""<div class="medical-card"><div class="medical-card-header"><h4 class="medical-card-title">🩺 Your Review</h4></div>""", unsafe_allow_html=True)

        doctor_notes = st.text_area(
            "Clinical Notes & Observations",
            placeholder="Enter your clinical observations, diagnosis, and recommendations...",
            key=f"notes_{original_index}",
            height=120
        )
        agree_ai = st.radio(
            "🤖 AI Assessment:",
            ["✅ Agree with AI", "⚠️ Disagree with AI"],
            key=f"agree_{original_index}",
            horizontal=True
        )
        if "Disagree" in agree_ai:
            correct_diagnosis = st.text_input("Correct Diagnosis", placeholder="Your diagnosis...", key=f"diag_{original_index}")
        else:
            correct_diagnosis = case.get("ai_result", "")

        if st.button("✅ Approve & Submit Review", key=f"approve_{original_index}", type="primary", use_container_width=True):
            if not doctor_notes:
                st.error("❌ Please provide clinical notes.")
            elif "Disagree" in agree_ai and not correct_diagnosis:
                st.error("❌ Please provide the correct diagnosis.")
            else:
                if original_index is not None:
                    all_cases[original_index].update({
                        "doctor_verified":  True,
                        "doctor_notes":     doctor_notes,
                        "doctor_name":      doctor_username,
                        "ai_agreed":        "Agree" in agree_ai,
                        "correct_diagnosis": correct_diagnosis,
                        "verified_at":      datetime.now().isoformat(),
                        "status":           "approved"
                    })
                    save_cases(all_cases)
                    decrement_doctor_load(doctor_username)
                    st.success("✅ Case approved! Patient will be notified.")
                    st.balloons()
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# TAB 2 — REVIEWED CASES
# ──────────────────────────────────────────────────────────────────────────────

def view_my_approved_cases(doctor_username):
    st.markdown("""
    <div class="medical-card">
        <div class="medical-card-header">
            <h2 class="medical-card-title">✅ My Reviewed Cases</h2>
        </div>
        <p>Cases you have reviewed and approved.</p>
    </div>
    """, unsafe_allow_html=True)

    cases = get_approved_cases_for_doctor(doctor_username)

    if not cases:
        st.markdown("""<div class="medical-card" style="text-align:center;padding:2rem;"><p style="opacity:0.6;">📭 No reviewed cases yet.</p></div>""", unsafe_allow_html=True)
        return

    search = st.text_input("🔎 Search by patient", placeholder="Patient username...", key="search_approved", label_visibility="collapsed")
    if search:
        cases = [c for c in cases if search.lower() in c.get("user","").lower()]

    st.markdown(f"**{len(cases)} reviewed case(s)**")
    st.markdown("<br>", unsafe_allow_html=True)

    for case in cases:
        st.markdown(f"""
        <div class="case-card" style="border-left:4px solid var(--success);">
            <div class="case-card-header">
                <h4 style="margin:0;">📋 {case.get('user','N/A')}</h4>
                <span class="badge badge-success">✅ APPROVED</span>
            </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns([1, 2, 1])
        with c1:
            if os.path.exists(case.get("image", "")):
                st.image(case["image"], caption="Patient Image", use_container_width=True)
        with c2:
            st.markdown(f"""
            <div style="padding:1rem;">
                <p><strong>👤 Patient:</strong> {case.get('user','N/A')}</p>
                <p><strong>📅 Submitted:</strong> {case.get('date','N/A')[:19]}</p>
                <p><strong>🤖 AI Prediction:</strong> {case.get('ai_result','N/A')} ({case.get('confidence','N/A')})</p>
                <p><strong>✅ Verified:</strong> {case.get('verified_at','N/A')[:19]}</p>
            </div>""", unsafe_allow_html=True)
        with c3:
            agreed_html = '<div class="info-box info-box-success"><p style="margin:0;font-weight:600;">🤖 AI Agreed</p></div>' if case.get("ai_agreed") else '<div class="info-box info-box-warning"><p style="margin:0;font-weight:600;">⚠️ AI Disagreed</p></div>'
            st.markdown(agreed_html, unsafe_allow_html=True)
            if case.get("correct_diagnosis"):
                st.markdown(f"""<div class="info-box info-box-primary" style="margin-top:0.5rem;"><p style="margin:0 0 0.25rem 0;font-size:0.75rem;font-weight:600;">FINAL DIAGNOSIS</p><p style="margin:0;font-weight:600;">{case.get('correct_diagnosis')}</p></div>""", unsafe_allow_html=True)

        if case.get("doctor_notes"):
            with st.expander("📝 Clinical Notes"):
                st.markdown(f'<p style="font-style:italic;">{case["doctor_notes"]}</p>', unsafe_allow_html=True)

        st.markdown("</div><br>", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# TAB 3 — APPOINTMENTS (scoped)
# ──────────────────────────────────────────────────────────────────────────────

def manage_my_appointments(doctor_username):
    st.markdown("""
    <div class="medical-card">
        <div class="medical-card-header">
            <h2 class="medical-card-title">📅 My Appointments</h2>
        </div>
        <p>Manage your patient appointment requests.</p>
    </div>
    """, unsafe_allow_html=True)

    appointments = get_pending_appointments_for_doctor(doctor_username)

    if not appointments:
        st.markdown("""
        <div class="medical-card" style="text-align:center;padding:3rem;">
            <h3 style="color:var(--success-dark);">🎉 No Pending Appointments</h3>
            <p>All requests have been processed!</p>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"**{len(appointments)} pending appointment(s)**")
        st.markdown("<br>", unsafe_allow_html=True)
        all_apts = load_appointments()

        for apt in appointments:
            original_index = None
            for idx, a in enumerate(all_apts):
                if a.get("user") == apt.get("user") and a.get("date") == apt.get("date") and a.get("time") == apt.get("time"):
                    original_index = idx
                    break

            urgency = apt.get("urgency", "Medium")
            urg_colors = {"Low": "var(--success)", "Medium": "var(--warning)", "High": "var(--error)", "Urgent": "#991B1B"}
            bc = urg_colors.get(urgency, "var(--warning)")

            st.markdown(f"""
            <div class="medical-card" style="border-left:4px solid {bc};">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;">
                    <h4 style="margin:0;">📅 Appointment Request</h4>
                    <span class="badge" style="background:{bc};color:white;">⚡ {urgency.upper()}</span>
                </div>
            """, unsafe_allow_html=True)

            c1, c2, c3 = st.columns([2, 2, 1.5])
            with c1:
                st.markdown(f"""
                <div class="info-box info-box-primary">
                    <p style="margin:0 0 0.25rem 0;font-size:0.875rem;font-weight:600;">PATIENT</p>
                    <p style="margin:0;font-size:1.1rem;font-weight:600;">👤 {apt.get('user','N/A')}</p>
                </div>""", unsafe_allow_html=True)
                st.markdown(f"**📅 Date:** {apt.get('date','N/A')}  \n**⏰ Time:** {apt.get('time','N/A')}")
            with c2:
                st.markdown("**📝 Symptoms:**")
                st.markdown(f"""<div style="background:rgba(255,255,255,0.05);padding:0.75rem;border-radius:8px;border-left:3px solid var(--primary);"><p style="margin:0;line-height:1.6;">{apt.get('symptoms','N/A')}</p></div>""", unsafe_allow_html=True)
            with c3:
                if st.button("✅ Approve", key=f"apt_approve_{original_index}", use_container_width=True, type="primary"):
                    if original_index is not None:
                        update_appointment_status(original_index, "approved")
                        st.success("✅ Approved!")
                        st.rerun()
                if st.button("❌ Reject", key=f"apt_reject_{original_index}", use_container_width=True):
                    if original_index is not None:
                        update_appointment_status(original_index, "rejected")
                        st.warning("Appointment rejected.")
                        st.rerun()

            with st.expander("📝 Add Notes for Patient"):
                notes = st.text_area("Notes", placeholder="Instructions for the patient...", key=f"apt_notes_{original_index}", label_visibility="collapsed")
                if st.button("💾 Save Notes", key=f"save_apt_{original_index}"):
                    if original_index is not None and notes:
                        update_appointment_status(original_index, "pending", notes)
                        st.success("✅ Notes saved!")

            st.markdown("</div><br>", unsafe_allow_html=True)

    # All appointments table
    st.markdown("""<div class="medical-card"><div class="medical-card-header"><h3 class="medical-card-title">📋 All My Appointments</h3></div></div>""", unsafe_allow_html=True)
    all_my_apts = [a for a in load_appointments() if a.get("doctor") == doctor_username]
    if all_my_apts:
        apt_data = []
        for apt in all_my_apts:
            si = {"pending": "⏳", "approved": "✅", "rejected": "❌"}.get(apt.get("status",""), "📋")
            apt_data.append({
                "Patient": apt.get("user",""),
                "Date": apt.get("date",""),
                "Time": apt.get("time",""),
                "Urgency": apt.get("urgency",""),
                "Status": f"{si} {apt.get('status','').upper()}"
            })
        st.dataframe(pd.DataFrame(apt_data), use_container_width=True, height=280)
    else:
        st.info("📭 No appointments yet.")