"""
User Portal Module — Premium Dark UI with Advanced Features
• Image quality validation before AI analysis
• Location-based doctor selection with city filtering  
• Multi-doctor system with estimated response time
"""

import streamlit as st
import os
from datetime import datetime, timedelta

from ml_model import predict_disease
from image_validator import validate_image, quality_score
from database import (
    add_case,
    get_user_cases,
    request_appointment,
    load_appointments,
    get_doctors_by_city,
    get_available_doctors,
    get_all_cities,
    assign_doctor_round_robin,
    increment_doctor_load,
    get_doctor_profile,
)
from auth import logout


# ──────────────────────────────────────────────────────────────────────────────
# DASHBOARD ENTRY POINT
# ──────────────────────────────────────────────────────────────────────────────

def user_dashboard(username):
    # ── Sidebar ────────────────────────────────────────────────────────────────
    with st.sidebar:
        def toggle_theme(): st.session_state["theme"] = "light" if st.session_state.get("theme", "dark") == "dark" else "dark"
        theme_label = "☀️ Light Mode" if st.session_state.get("theme", "dark") == "dark" else "🌙 Dark Mode"
        st.button(theme_label, on_click=toggle_theme, key="user_theme_btn", use_container_width=True)
        st.markdown("---")
        st.markdown(f"""
        <div class="sidebar-profile">
            <div class="sidebar-avatar">👤</div>
            <div class="sidebar-name">{username}</div>
            <div class="sidebar-role-badge">Patient</div>
        </div>
        """, unsafe_allow_html=True)

        cases = get_user_cases(username)
        appointments = load_appointments()
        user_apts = [a for a in appointments if a.get("user") == username]
        pending_cases = len([c for c in cases if not c.get("doctor_verified", False)])
        approved_cases = len([c for c in cases if c.get("doctor_verified", False)])

        st.markdown(f"""
        <div class="sidebar-stats">
            <div class="sidebar-stat"><span class="sidebar-stat-num">{len(cases)}</span><span class="sidebar-stat-label">Total Cases</span></div>
            <div class="sidebar-stat"><span class="sidebar-stat-num pending">{pending_cases}</span><span class="sidebar-stat-label">Pending</span></div>
            <div class="sidebar-stat"><span class="sidebar-stat-num approved">{approved_cases}</span><span class="sidebar-stat-label">Approved</span></div>
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
                <h1>🩺 Patient Portal</h1>
                <p>Welcome back, <strong>{username}</strong> — AI-powered skin analysis at your fingertips</p>
            </div>
            <div class="header-badge">MediScan AI</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Stat Cards ─────────────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    pending_apts = len([a for a in user_apts if a.get("status") == "pending"])

    with col1:
        st.markdown(f"""
        <div class="stat-card stat-card-blue">
            <div class="stat-card-icon">📊</div>
            <div class="stat-card-label">Total Cases</div>
            <div class="stat-card-value">{len(cases)}</div>
            <div class="stat-card-change">All submissions</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card stat-card-yellow">
            <div class="stat-card-icon">⏳</div>
            <div class="stat-card-label">Pending Review</div>
            <div class="stat-card-value">{pending_cases}</div>
            <div class="stat-card-change">Awaiting doctor</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="stat-card stat-card-green">
            <div class="stat-card-icon">✅</div>
            <div class="stat-card-label">Approved</div>
            <div class="stat-card-value">{approved_cases}</div>
            <div class="stat-card-change">Doctor verified</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="stat-card stat-card-purple">
            <div class="stat-card-icon">📅</div>
            <div class="stat-card-label">Appointments</div>
            <div class="stat-card-value">{len(user_apts)}</div>
            <div class="stat-card-change">{pending_apts} pending</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📸 New Analysis", "📋 My Cases", "📅 Appointments"])
    with tab1:
        upload_and_predict(username)
    with tab2:
        view_case_history(username)
    with tab3:
        appointment_section(username)


# ──────────────────────────────────────────────────────────────────────────────
# TAB 1 — UPLOAD & PREDICT
# ──────────────────────────────────────────────────────────────────────────────

def upload_and_predict(username):
    st.markdown("""
    <div class="medical-card">
        <div class="medical-card-header">
            <h2 class="medical-card-title">🔬 AI-Powered Skin Analysis</h2>
        </div>
        <div class="medical-card-body">
            <p>Upload a clear photo of the affected skin area. Our AI analyses it instantly, then a licensed dermatologist validates the result within ~4 hours.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_upload, col_preview = st.columns([1, 1])

    with col_upload:
        st.markdown("""
        <div class="medical-card">
            <div class="medical-card-header">
                <h3 class="medical-card-title">📤 Upload Image</h3>
            </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Choose a skin image...",
            type=["jpg", "jpeg", "png"],
            help="Upload a clear image — min 800×800 px",
            label_visibility="collapsed"
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # Tips
        st.markdown("""
        <div class="medical-card info-card-blue">
            <h4 style="margin-bottom:0.75rem;">💡 Tips for Best Results</h4>
            <ul class="tips-list">
                <li>✅ Use good natural or indoor lighting</li>
                <li>✅ Focus clearly on the affected area</li>
                <li>✅ Minimum 800×800 px resolution</li>
                <li>✅ Keep image sharp and in-focus</li>
                <li>❌ Avoid blurry or over-exposed shots</li>
                <li>❌ Do not apply filters or edit the photo</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_preview:
        if uploaded_file is not None:
            file_bytes = uploaded_file.getvalue()

            # ── Image Quality Validation ───────────────────────────────────────
            st.markdown("""
            <div class="medical-card">
                <div class="medical-card-header">
                    <h3 class="medical-card-title">🛡️ Image Quality Check</h3>
                </div>
            """, unsafe_allow_html=True)

            with st.spinner("Analysing image quality..."):
                is_valid, error_msg, meta = validate_image(file_bytes)

            if not is_valid:
                st.markdown(f"""
                <div class="validation-fail">
                    <div class="val-icon">❌</div>
                    <div class="val-title">Validation Failed</div>
                    <div class="val-msg">{error_msg}</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                return

            # Quality score badge
            q_score = quality_score(meta)
            q_color = "#10B981" if q_score >= 70 else "#F59E0B" if q_score >= 45 else "#EF4444"
            warn_html = ""
            if meta.get("resolution_warning"):
                warn_html = '<p class="val-warn">⚠️ Image resolution is below 1024×1024 — results may be less accurate.</p>'

            st.markdown(f"""
            <div class="validation-pass">
                <div class="val-icon">✅</div>
                <div class="val-title">Image Validated</div>
                <div class="val-meta">
                    <span class="val-chip">📐 {meta['width']}×{meta['height']} px</span>
                    <span class="val-chip">🔍 Sharpness: {meta['blur_score']:.0f}</span>
                    <span class="val-chip">☀️ Brightness: {meta['brightness']:.0f}</span>
                    <span class="val-chip" style="background:rgba({','.join(['16,185,129' if q_color=='#10B981' else '245,158,11' if q_color=='#F59E0B' else '239,68,68'])},0.15);border-color:{q_color};color:{q_color};">
                        ⭐ Quality: {q_score}/100
                    </span>
                </div>
                {warn_html}
            </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # ── Image Preview ──────────────────────────────────────────────────
            st.markdown("""
            <div class="medical-card">
                <div class="medical-card-header">
                    <h3 class="medical-card-title">🖼️ Preview</h3>
                </div>
            """, unsafe_allow_html=True)
            st.image(uploaded_file, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # ── Doctor Selection ───────────────────────────────────────────────
            st.markdown("""
            <div class="medical-card">
                <div class="medical-card-header">
                    <h3 class="medical-card-title">👨‍⚕️ Select a Doctor</h3>
                </div>
                <p style="margin-bottom:1rem;">Choose a dermatologist near you, or let us auto-assign the next available doctor.</p>
            """, unsafe_allow_html=True)

            cities = ["All Cities"] + get_all_cities()
            selected_city = st.selectbox("📍 Filter by City", cities, key="city_filter")

            doctors = get_doctors_by_city(None if selected_city == "All Cities" else selected_city)

            if not doctors:
                st.warning("No doctors available in this city right now. Auto-assignment will be used.")
                chosen_doctor_username = None
            else:
                doctor_options = {}
                for uname, profile in doctors:
                    avail_icon = "🟢" if profile.get("availability") == "available" else "🔴"
                    label = (f"{avail_icon} {profile['display_name']} — "
                             f"{profile['specialization']} "
                             f"({profile['location']['city']}) ⭐{profile['rating']}")
                    doctor_options[label] = uname

                # Render doctor cards
                for uname, profile in doctors:
                    avail_dot = "avail-green" if profile.get("availability") == "available" else "avail-red"
                    avail_text = "Available" if profile.get("availability") == "available" else "Busy"
                    st.markdown(f"""
                    <div class="doctor-card">
                        <div class="doctor-card-top">
                            <div class="doctor-avatar">🩺</div>
                            <div class="doctor-info">
                                <div class="doctor-name">{profile['display_name']}</div>
                                <div class="doctor-spec">{profile['specialization']}</div>
                                <div class="doctor-hospital">🏥 {profile.get('hospital','')}</div>
                            </div>
                            <div class="doctor-meta">
                                <div class="doctor-rating">⭐ {profile['rating']}</div>
                                <div class="avail-dot {avail_dot}">{avail_text}</div>
                                <div class="doctor-response">⏱ ~{profile['estimated_response_hours']}h response</div>
                            </div>
                        </div>
                        <div class="doctor-tags">
                            <span class="dtag">📍 {profile['location']['city']}, {profile['location']['area']}</span>
                            <span class="dtag">🎓 {profile['qualification']}</span>
                            <span class="dtag">📋 {profile['total_cases_handled']} cases</span>
                            <span class="dtag">🗣 {', '.join(profile['languages'][:2])}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                selected_label = st.selectbox(
                    "Select Doctor",
                    ["⚡ Auto-assign best available doctor"] + list(doctor_options.keys()),
                    key="doctor_select"
                )
                if selected_label.startswith("⚡"):
                    chosen_doctor_username = None
                else:
                    chosen_doctor_username = doctor_options.get(selected_label)

            st.markdown("</div>", unsafe_allow_html=True)

            # ── AI Analysis ────────────────────────────────────────────────────
            st.markdown("""
            <div class="medical-card">
                <div class="medical-card-header">
                    <h3 class="medical-card-title">🤖 AI Analysis</h3>
                </div>
            """, unsafe_allow_html=True)

            if st.button("🔍 Analyse & Submit Case", type="primary", use_container_width=True):
                with st.spinner("🧠 AI is analysing your image..."):
                    # Save file
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename  = f"{username}_{timestamp}_{uploaded_file.name}"
                    filepath  = os.path.join("uploads", filename)
                    os.makedirs("uploads", exist_ok=True)
                    with open(filepath, "wb") as f:
                        f.write(file_bytes)

                    # AI prediction
                    disease, confidence = predict_disease(filepath)

                    # Doctor assignment
                    city_for_assign = selected_city if selected_city != "All Cities" else None
                    if chosen_doctor_username:
                        assigned_doc = chosen_doctor_username
                        doc_profile  = get_doctor_profile(assigned_doc)
                    else:
                        assigned_doc, doc_profile = assign_doctor_round_robin(city_for_assign)

                    if assigned_doc:
                        increment_doctor_load(assigned_doc)
                        resp_hours = doc_profile.get("estimated_response_hours", 4) if doc_profile else 4
                        expected_by = (datetime.now() + timedelta(hours=resp_hours)).isoformat()
                        doc_display = doc_profile.get("display_name", assigned_doc) if doc_profile else assigned_doc
                    else:
                        expected_by = (datetime.now() + timedelta(hours=4)).isoformat()
                        doc_display = "Next available doctor"

                # Results
                st.markdown(f"""
                <div class="result-highlight">
                    <div class="result-title">🤖 AI DIAGNOSIS</div>
                    <div class="result-value">{disease}</div>
                    <div class="result-confidence">{confidence}% Confidence</div>
                </div>
                """, unsafe_allow_html=True)

                if assigned_doc and doc_profile:
                    st.markdown(f"""
                    <div class="assign-box">
                        <div class="assign-icon">👨‍⚕️</div>
                        <div>
                            <div class="assign-title">Assigned to {doc_display}</div>
                            <div class="assign-sub">{doc_profile.get('specialization','')} · {doc_profile.get('location',{}).get('city','')}</div>
                            <div class="assign-eta">⏱ Expected review by: {expected_by[:16].replace('T',' ')}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # Save case
                case_data = {
                    "user":             username,
                    "image":            filepath,
                    "ai_result":        disease,
                    "confidence":       f"{confidence}%",
                    "doctor_verified":  False,
                    "doctor_notes":     "",
                    "doctor_name":      "",
                    "assigned_doctor":  assigned_doc or "",
                    "expected_response_by": expected_by,
                    "image_quality":    meta,
                    "date":             datetime.now().isoformat(),
                    "status":           "pending"
                }
                if add_case(case_data):
                    st.success("✅ Case saved successfully! View it in 'My Cases' tab.")
                else:
                    st.error("❌ Error saving case. Please try again.")

            st.markdown("</div>", unsafe_allow_html=True)

        else:
            # Empty state
            st.markdown("""
            <div class="upload-zone">
                <div class="upload-zone-icon">🩻</div>
                <div class="upload-zone-title">Upload a Skin Image</div>
                <div class="upload-zone-subtitle">Select an image using the uploader on the left</div>
            </div>
            """, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# TAB 2 — CASE HISTORY
# ──────────────────────────────────────────────────────────────────────────────

def view_case_history(username):
    st.markdown("""
    <div class="medical-card">
        <div class="medical-card-header">
            <h2 class="medical-card-title">📋 Medical Case History</h2>
        </div>
        <p>All your past skin analyses and doctor reviews.</p>
    </div>
    """, unsafe_allow_html=True)

    cases = get_user_cases(username)

    if not cases:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">📭</div>
            <h3>No Cases Yet</h3>
            <p>Head to the <strong>New Analysis</strong> tab to submit your first skin image.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    filter_opt = st.selectbox(
        "Filter",
        ["All Cases", "Pending Review", "Doctor Approved"],
        label_visibility="collapsed"
    )
    if filter_opt == "Pending Review":
        filtered = [c for c in cases if not c.get("doctor_verified", False)]
    elif filter_opt == "Doctor Approved":
        filtered = [c for c in cases if c.get("doctor_verified", False)]
    else:
        filtered = cases

    st.markdown(f"**Showing {len(filtered)} of {len(cases)} case(s)**")
    st.markdown("<br>", unsafe_allow_html=True)

    for i, case in enumerate(filtered):
        case_number = cases.index(case) + 1
        is_approved = case.get("doctor_verified", False)
        badge_class = "badge-success" if is_approved else "badge-warning"
        badge_text  = "✅ APPROVED"   if is_approved else "⏳ PENDING"

        # Assigned doctor info
        assigned = case.get("assigned_doctor", "")
        assigned_prof = get_doctor_profile(assigned) if assigned else None
        doc_display = assigned_prof.get("display_name", assigned) if assigned_prof else "Pending assignment"
        eta = case.get("expected_response_by", "")[:16].replace("T", " ") if case.get("expected_response_by") else "—"

        st.markdown(f"""
        <div class="case-card">
            <div class="case-card-header">
                <div class="case-card-title">📋 Case #{case_number}</div>
                <span class="badge {badge_class}">{badge_text}</span>
            </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns([1, 2])
        with c1:
            if os.path.exists(case.get("image", "")):
                st.image(case["image"], caption=f"Submitted: {case.get('date','')[:10]}", use_container_width=True)
            else:
                st.error("📷 Image not found")

        with c2:
            st.markdown(f"""
            <div style="padding:0.5rem;">
                <p><strong>📅 Date:</strong> {case.get('date','N/A')[:19]}</p>
                <p><strong>🤖 AI Result:</strong> {case.get('ai_result','N/A')}</p>
                <p><strong>📊 Confidence:</strong> {case.get('confidence','N/A')}</p>
                <p><strong>👨‍⚕️ Assigned Doctor:</strong> {doc_display}</p>
                <p><strong>⏱ Expected Response:</strong> {eta}</p>
            </div>
            """, unsafe_allow_html=True)

            if is_approved:
                st.markdown(f"""
                <div class="info-box info-box-success">
                    <p style="margin:0 0 0.25rem 0;font-weight:600;">✅ Reviewed by Dr. {case.get('doctor_name','N/A')}</p>
                    <p style="margin:0;"><strong>🩺 Verified Diagnosis:</strong> {case.get('correct_diagnosis', case.get('ai_result','N/A'))}</p>
                </div>
                """, unsafe_allow_html=True)
                if case.get("doctor_notes"):
                    with st.expander("📝 View Doctor's Notes"):
                        st.markdown(f"""
                        <div style="background:rgba(255,255,255,0.05);padding:1rem;border-radius:8px;">
                            <p style="font-style:italic;">{case.get('doctor_notes')}</p>
                        </div>""", unsafe_allow_html=True)
                st.caption(f"✓ Verified on: {case.get('verified_at','N/A')[:19]}")
            else:
                st.markdown("""
                <div class="info-box info-box-warning">
                    <p style="margin:0;font-weight:600;">⏳ Awaiting doctor review</p>
                </div>""", unsafe_allow_html=True)

        st.markdown("</div><br>", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# TAB 3 — APPOINTMENTS
# ──────────────────────────────────────────────────────────────────────────────

def appointment_section(username):
    st.markdown("""
    <div class="medical-card">
        <div class="medical-card-header">
            <h2 class="medical-card-title">📅 Schedule an Appointment</h2>
        </div>
        <p>Request an in-person or tele-consultation with a dermatologist near you.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("""
        <div class="medical-card">
            <div class="medical-card-header">
                <h3 class="medical-card-title">📝 Request Form</h3>
            </div>
        """, unsafe_allow_html=True)

        cities = ["All Cities"] + get_all_cities()
        apt_city = st.selectbox("📍 Select City", cities, key="apt_city")
        city_filter = None if apt_city == "All Cities" else apt_city
        doctors = get_doctors_by_city(city_filter)

        if not doctors:
            st.warning("No doctors available in this city.")
            return

        doctor_options = {f"{p['display_name']} ({p['location']['city']})": u for u, p in doctors}

        with st.form("appointment_form", clear_on_submit=True):
            selected_doctor = st.selectbox("👨‍⚕️ Select Doctor", list(doctor_options.keys()))
            appointment_date = st.date_input("📅 Preferred Date", min_value=datetime.now().date())
            appointment_time = st.time_input("⏰ Preferred Time")
            symptoms = st.text_area("📋 Describe Symptoms", placeholder="Describe your skin condition and concerns...", height=120)
            urgency  = st.select_slider("⚡ Urgency Level", options=["Low", "Medium", "High", "Urgent"], value="Medium")

            submit = st.form_submit_button("📤 Submit Request", type="primary", use_container_width=True)

            if submit:
                if not symptoms:
                    st.error("❌ Please describe your symptoms.")
                else:
                    apt_data = {
                        "user":     username,
                        "doctor":   doctor_options[selected_doctor],
                        "date":     str(appointment_date),
                        "time":     str(appointment_time),
                        "symptoms": symptoms,
                        "urgency":  urgency,
                        "status":   "pending"
                    }
                    if request_appointment(apt_data):
                        st.success("✅ Appointment request submitted!")
                        st.info("📧 The doctor will confirm your appointment shortly.")
                    else:
                        st.error("❌ Error submitting appointment. Please try again.")

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="medical-card">
            <div class="medical-card-header">
                <h3 class="medical-card-title">📋 My Appointments</h3>
            </div>
        """, unsafe_allow_html=True)

        appointments = load_appointments()
        user_apts    = [apt for apt in appointments if apt.get("user") == username]

        if not user_apts:
            st.markdown("""
            <div style="text-align:center;padding:2rem;">
                <p style="opacity:0.6;">📭 No appointments yet.</p>
            </div>""", unsafe_allow_html=True)
        else:
            for apt in user_apts:
                status = apt.get("status", "pending")
                colors = {
                    "approved": ("var(--success)", "var(--success-light)"),
                    "rejected": ("var(--error)",   "var(--error-light)"),
                    "pending":  ("var(--warning)", "var(--warning-light)"),
                }
                icons  = {"approved": "✅", "rejected": "❌", "pending": "⏳"}
                sc, bg = colors.get(status, colors["pending"])
                si     = icons.get(status, "📋")

                doc_prof = get_doctor_profile(apt.get("doctor", ""))
                doc_name = doc_prof.get("display_name", apt.get("doctor", "N/A")) if doc_prof else apt.get("doctor", "N/A")

                st.markdown(f"""
                <div style="background:{bg};padding:1rem;border-radius:10px;margin-bottom:1rem;border-left:4px solid {sc};">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">
                        <strong style="color:{sc};">👨‍⚕️ {doc_name}</strong>
                        <span class="badge" style="background:{sc};color:white;">{si} {status.upper()}</span>
                    </div>
                    <p style="margin:0.2rem 0;font-size:0.875rem;">📅 {apt.get('date','N/A')} at {apt.get('time','N/A')}</p>
                    <p style="margin:0.2rem 0;font-size:0.875rem;">⚡ Urgency: <strong>{apt.get('urgency','N/A')}</strong></p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)