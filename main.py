# main.py
import streamlit as st
import pandas as pd
from datetime import datetime, date
import streamlit.components.v1 as components

from database import create_all_tables
from auth import login_user, register_user, get_all_doctors
from patient import (
    register_patient, get_patient,
    search_patients, get_all_patients,
    add_medical_record, get_medical_history,
    add_lab_report, get_lab_reports
)
from billing import (
    create_bill, get_patient_bills,
    get_daily_revenue, get_monthly_revenue
)
from ai_helper import (
    analyze_symptoms, suggest_prescription,
    analyze_lab_report,
    generate_discharge_summary
)
from analytics import (
    get_total_stats, get_patient_gender_data,
    get_monthly_patients, get_appointment_stats
)

# Initialize database
create_all_tables()

# Page config
st.set_page_config(
    page_title="Hospital Management System",
    page_icon="🏥",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stButton > button {
        background-color: #0066cc;
        color: white;
        border-radius: 8px;
        width: 100%;
    }
    h1 {color: #0066cc;}
    h2 {color: #004499;}
</style>
""", unsafe_allow_html=True)

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None

# ============ LOGIN PAGE ============
if not st.session_state.logged_in:
    st.title("🏥 Hospital Management System")
    st.subheader("Please login to continue")

    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])

    with tab1:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.subheader("🔐 Login")
            login_username = st.text_input(
                "Username:",
                key="login_user_field"
            )
            login_password = st.text_input(
                "Password:",
                type="password",
                key="login_pass_field"
            )
            if st.button("🔐 Login", key="login_btn"):
                if login_username and login_password:
                    success, result = login_user(
                        login_username,
                        login_password
                    )
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user = result
                        st.success("Login successful! ✅")
                        st.rerun()
                    else:
                        st.error(result)
                else:
                    st.error("Please fill all fields!")

    with tab2:
        st.subheader("📝 Register New User")
        col1, col2 = st.columns(2)
        with col1:
            new_name = st.text_input(
                "Full Name:",
                key="reg_name_field"
            )
            new_username = st.text_input(
                "Username:",
                key="reg_user_field"
            )
            new_role = st.selectbox(
                "Role:",
                ["doctor", "admin", "nurse"],
                key="reg_role_field"
            )
        with col2:
            new_email = st.text_input(
                "Email:",
                key="reg_email_field"
            )
            new_phone = st.text_input(
                "Phone:",
                key="reg_phone_field"
            )
            new_password = st.text_input(
                "Password:",
                type="password",
                key="reg_pass_field"
            )
        if st.button("📝 Register", key="reg_btn"):
            if new_name and new_username and new_password:
                success, msg = register_user(
                    new_username, new_password,
                    new_role, new_name,
                    new_email, new_phone
                )
                if success:
                    st.success(f"✅ {msg} Please login!")
                else:
                    st.error(msg)
            else:
                st.error("Please fill required fields!")

# ============ MAIN APP ============
else:
    user = st.session_state.user

    with st.sidebar:
        st.title("🏥 HMS")
        st.write(f"👤 {user['full_name']}")
        st.write(f"🔰 {user['role'].title()}")
        st.divider()

        menu = st.selectbox(
            "Navigate:",
            [
                "🏠 Dashboard",
                "👥 Patients",
                "📋 Medical Records",
                "🧪 Lab Reports",
                "💰 Billing",
                "🤖 AI Assistant",
                "📊 Analytics"
            ]
        )
        st.divider()
        if st.button("🚪 Logout", key="logout_btn"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()

    # ======= DASHBOARD =======
    if menu == "🏠 Dashboard":
        st.title("🏥 Hospital Dashboard")
        st.write(f"Welcome, {user['full_name']}! 👋")
        st.divider()

        stats = get_total_stats()
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "👥 Total Patients",
                stats["total_patients"]
            )
        with col2:
            st.metric(
                "📅 Appointments Today",
                stats["today_appointments"]
            )
        with col3:
            st.metric(
                "👨‍⚕️ Total Doctors",
                stats["total_doctors"]
            )
        with col4:
            st.metric(
                "💰 Today Revenue",
                f"₹{stats['today_revenue']:,.0f}"
            )

    # ======= PATIENTS =======
    elif menu == "👥 Patients":
        st.title("👥 Patient Management")

        tab1, tab2, tab3 = st.tabs([
            "🔍 Search",
            "➕ Register",
            "📋 All Patients"
        ])

        with tab1:
            search = st.text_input(
                "Search by name, phone or ID:",
                key="search_patient"
            )
            if st.button("🔍 Search", key="search_btn"):
                if search:
                    patients = search_patients(search)
                    if patients:
                        for p in patients:
                            with st.expander(
                                f"🏥 {p['patient_id']}"
                                f" - {p['full_name']}"
                            ):
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.write(f"**Age:** {p['age']}")
                                    st.write(f"**Gender:** {p['gender']}")
                                    st.write(f"**Blood:** {p['blood_group']}")
                                with col2:
                                    st.write(f"**Phone:** {p['phone']}")
                                    st.write(f"**Allergies:** {p['allergies']}")
                    else:
                        st.warning("No patients found!")

        with tab2:
            st.subheader("➕ Register New Patient")
            col1, col2 = st.columns(2)
            with col1:
                p_name = st.text_input("Full Name:*", key="p_name")
                p_age = st.number_input("Age:*", 1, 120, 25, key="p_age")
                p_gender = st.selectbox(
                    "Gender:*",
                    ["Male", "Female", "Other"],
                    key="p_gender"
                )
                p_blood = st.selectbox(
                    "Blood Group:*",
                    ["A+","A-","B+","B-","O+","O-","AB+","AB-"],
                    key="p_blood"
                )
                p_phone = st.text_input("Phone:*", key="p_phone")
            with col2:
                p_email = st.text_input("Email:", key="p_email")
                p_address = st.text_area("Address:", key="p_address")
                p_emergency = st.text_input("Emergency Contact:*", key="p_emergency")
                p_allergies = st.text_input(
                    "Known Allergies:",
                    placeholder="None",
                    key="p_allergies"
                )
            if st.button("✅ Register Patient", key="reg_patient_btn"):
                if p_name and p_phone and p_emergency:
                    success, patient_id = register_patient(
                        p_name, p_age, p_gender, p_blood,
                        p_phone, p_email, p_address,
                        p_emergency, p_allergies
                    )
                    if success:
                        st.success(f"✅ Registered! ID: {patient_id}")
                        st.balloons()
                    else:
                        st.error(patient_id)
                else:
                    st.error("Fill required fields!")

        with tab3:
            patients = get_all_patients()
            if patients:
                df = pd.DataFrame(patients)
                st.dataframe(
                    df[["patient_id","full_name","age","gender","phone"]],
                    use_container_width=True
                )
                st.info(f"Total: {len(patients)} patients")
            else:
                st.info("No patients registered yet!")

    # ======= MEDICAL RECORDS =======
    elif menu == "📋 Medical Records":
        st.title("📋 Medical Records")

        tab1, tab2 = st.tabs(["➕ Add Record", "📋 View History"])

        with tab1:
            patient_id = st.text_input(
                "Patient ID:",
                key="med_patient_id"
            )
            if patient_id:
                patient = get_patient(patient_id)
                if patient:
                    st.success(f"Patient: {patient['full_name']}")
                    col1, col2 = st.columns(2)
                    with col1:
                        diagnosis = st.text_input("Diagnosis:", key="med_diagnosis")
                        symptoms = st.text_area("Symptoms:", key="med_symptoms")
                        treatment = st.text_area("Treatment:", key="med_treatment")
                    with col2:
                        prescription = st.text_area("Prescription:", key="med_prescription")
                        notes = st.text_area("Notes:", key="med_notes")
                        follow_up = st.date_input("Follow-up:", key="med_followup")

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("💾 Save Record", key="save_record_btn"):
                            if diagnosis:
                                add_medical_record(
                                    patient_id, user["id"],
                                    diagnosis, symptoms,
                                    treatment, prescription,
                                    notes, str(follow_up)
                                )
                                st.success("Record saved! ✅")
                    with col2:
                        if st.button("🤖 AI Suggest", key="ai_suggest_btn"):
                            with st.spinner("AI analyzing..."):
                                suggestion = suggest_prescription(
                                    diagnosis,
                                    patient.get("allergies", "None")
                                )
                            st.info(suggestion)
                else:
                    st.error("Patient not found!")

        with tab2:
            pid = st.text_input("Enter Patient ID:", key="view_history_pid")
            if st.button("📋 Get History", key="get_history_btn"):
                if pid:
                    records = get_medical_history(pid)
                    if records:
                        for r in records:
                            with st.expander(f"📅 {r['date']} - {r['diagnosis']}"):
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.write("**Symptoms:**", r["symptoms"])
                                    st.write("**Diagnosis:**", r["diagnosis"])
                                with col2:
                                    st.write("**Treatment:**", r["treatment"])
                                    st.write("**Prescription:**", r["prescription"])
                    else:
                        st.info("No records found!")

    # ======= LAB REPORTS =======
    elif menu == "🧪 Lab Reports":
        st.title("🧪 Lab Reports")

        tab1, tab2 = st.tabs(["➕ Add Report", "📋 View Reports"])

        with tab1:
            lab_pid = st.text_input("Patient ID:", key="lab_pid")
            if lab_pid:
                col1, col2 = st.columns(2)
                with col1:
                    test_name = st.text_input("Test Name:", key="lab_test")
                    result = st.text_input("Result:", key="lab_result")
                    normal_range = st.text_input("Normal Range:", key="lab_normal")
                with col2:
                    status = st.selectbox(
                        "Status:",
                        ["Normal", "Abnormal", "Critical"],
                        key="lab_status"
                    )
                    notes = st.text_area("Notes:", key="lab_notes")

                if st.button("💾 Save Report", key="save_lab_btn"):
                    if test_name and result:
                        add_lab_report(
                            lab_pid, test_name, result,
                            normal_range, status, notes
                        )
                        st.success("Report saved! ✅")

                if st.button("🤖 AI Analyze", key="ai_lab_btn"):
                    with st.spinner("Analyzing..."):
                        analysis = analyze_lab_report(
                            test_name, result, normal_range
                        )
                    st.write(analysis)

        with tab2:
            view_pid = st.text_input("Patient ID:", key="view_lab_pid")
            if st.button("📋 Get Reports", key="get_lab_btn"):
                reports = get_lab_reports(view_pid)
                if reports:
                    for r in reports:
                        status_color = (
                            "🟢" if r["status"] == "Normal"
                            else "🔴" if r["status"] == "Critical"
                            else "🟡"
                        )
                        with st.expander(
                            f"{status_color} {r['test_name']} - {r['date']}"
                        ):
                            st.write(f"**Result:** {r['result']}")
                            st.write(f"**Normal Range:** {r['normal_range']}")
                            st.write(f"**Status:** {r['status']}")
                            st.write(f"**Notes:** {r['notes']}")
                else:
                    st.info("No reports found!")

    # ======= BILLING =======
    elif menu == "💰 Billing":
        st.title("💰 Billing System")

    tab1, tab2, tab3 = st.tabs([
        "➕ New Bill",
        "📋 View Bills",
        "🖨️ Print Invoice"
    ])

    # ======= NEW BILL =======
    with tab1:
        bill_pid = st.text_input(
            "Patient ID:",
            key="bill_pid"
        )
        if bill_pid:
            patient = get_patient(bill_pid)
            if patient:
                st.success(
                    f"Patient: {patient['full_name']}"
                )

                col1, col2, col3 = st.columns(3)
                with col1:
                    consult = st.number_input(
                        "Consultation ₹:",
                        0.0, 10000.0, 500.0,
                        key="bill_consult"
                    )
                with col2:
                    medicine = st.number_input(
                        "Medicine ₹:",
                        0.0, 10000.0, 0.0,
                        key="bill_medicine"
                    )
                with col3:
                    lab = st.number_input(
                        "Lab Tests ₹:",
                        0.0, 10000.0, 0.0,
                        key="bill_lab"
                    )

                # Show live total
                total = consult + medicine + lab
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(
                        "Subtotal",
                        f"₹{consult+medicine+lab:,.2f}"
                    )
                with col2:
                    tax = total * 0.05
                    st.metric(
                        "GST (5%)",
                        f"₹{tax:,.2f}"
                    )
                with col3:
                    grand_total = total + tax
                    st.metric(
                        "Grand Total",
                        f"₹{grand_total:,.2f}"
                    )

                payment = st.selectbox(
                    "Payment Method:",
                    ["Cash", "Card",
                     "UPI", "Insurance"],
                    key="bill_payment"
                )

                if st.button(
                    "💰 Generate Bill",
                    key="gen_bill_btn"
                ):
                    bill_id, total = create_bill(
                        bill_pid, consult,
                        medicine, lab, payment
                    )
                    st.session_state.last_bill = {
                        "bill_id": bill_id,
                        "patient": patient,
                        "consult": consult,
                        "medicine": medicine,
                        "lab": lab,
                        "total": total,
                        "tax": total * 0.05,
                        "grand_total": total + (total * 0.05),
                        "payment": payment,
                        "date": datetime.now().strftime(
                            "%d-%m-%Y %H:%M"
                        )
                    }
                    st.success(
                        f"✅ Bill #{bill_id} Generated!"
                    )
                    st.balloons()
            else:
                st.error("Patient not found!")

    # ======= VIEW BILLS =======
    with tab2:
        view_bill_pid = st.text_input(
            "Patient ID:",
            key="view_bill_pid"
        )
        if st.button(
            "📋 Get Bills",
            key="get_bills_btn"
        ):
            bills = get_patient_bills(view_bill_pid)
            if bills:
                for b in bills:
                    with st.expander(
                        f"🧾 Bill #{b['id']}"
                        f" - {b['date']}"
                    ):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(
                                f"**Consultation:**"
                                f" ₹{b['consultation_fee']}"
                            )
                            st.write(
                                f"**Medicine:**"
                                f" ₹{b['medicine_cost']}"
                            )
                            st.write(
                                f"**Lab:**"
                                f" ₹{b['lab_cost']}"
                            )
                        with col2:
                            st.write(
                                f"**Total:**"
                                f" ₹{b['total_amount']}"
                            )
                            st.write(
                                f"**Payment:**"
                                f" {b['payment_method']}"
                            )
                            st.write(
                                f"**Status:**"
                                f" {b['payment_status']}"
                            )
            else:
                st.info("No bills found!")

    # ======= PRINT INVOICE =======
    with tab3:
        st.subheader("🖨️ Print Invoice")

        # Check if bill was just generated
        if "last_bill" in st.session_state:
            bill = st.session_state.last_bill
            patient = bill["patient"]
        else:
            st.info(
                "Generate a bill first "
                "OR enter bill details below"
            )
            bill = None
            patient = None

        # Manual invoice entry
        if not bill:
            col1, col2 = st.columns(2)
            with col1:
                inv_pid = st.text_input(
                    "Patient ID:",
                    key="inv_pid"
                )
            with col2:
                inv_bid = st.text_input(
                    "Bill ID:",
                    key="inv_bid"
                )

        # Generate Invoice HTML
        if st.button(
            "🖨️ Generate Invoice",
            key="gen_invoice_btn"
        ):
            if bill and patient:
                b = bill
                p = patient
            else:
                st.error(
                    "Please generate a bill first!"
                )
                st.stop()

            # Beautiful HTML Invoice
            invoice_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}
    body {{
        font-family: Arial, sans-serif;
        padding: 20px;
        color: #333;
    }}
    .invoice-box {{
        max-width: 800px;
        margin: auto;
        padding: 30px;
        border: 1px solid #eee;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }}
    .header {{
        text-align: center;
        background: #0066cc;
        color: white;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
    }}
    .header h1 {{
        font-size: 28px;
        margin-bottom: 5px;
    }}
    .header p {{
        font-size: 14px;
        opacity: 0.9;
    }}
    .invoice-info {{
        display: flex;
        justify-content: space-between;
        margin-bottom: 20px;
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
    }}
    .patient-info {{
        margin-bottom: 20px;
        padding: 15px;
        border: 1px solid #dee2e6;
        border-radius: 8px;
    }}
    .patient-info h3 {{
        color: #0066cc;
        margin-bottom: 10px;
        border-bottom: 2px solid #0066cc;
        padding-bottom: 5px;
    }}
    .info-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 20px;
    }}
    table th {{
        background: #0066cc;
        color: white;
        padding: 12px;
        text-align: left;
    }}
    table td {{
        padding: 12px;
        border-bottom: 1px solid #dee2e6;
    }}
    table tr:hover {{
        background: #f8f9fa;
    }}
    .total-section {{
        background: #f8f9fa;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
    }}
    .total-row {{
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px solid #dee2e6;
    }}
    .grand-total {{
        display: flex;
        justify-content: space-between;
        padding: 15px 0;
        font-size: 20px;
        font-weight: bold;
        color: #0066cc;
        border-top: 2px solid #0066cc;
        margin-top: 10px;
    }}
    .payment-badge {{
        display: inline-block;
        background: #28a745;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 14px;
    }}
    .footer {{
        text-align: center;
        margin-top: 30px;
        padding: 20px;
        background: #f8f9fa;
        border-radius: 8px;
        color: #666;
    }}
    .watermark {{
        text-align: center;
        color: #28a745;
        font-size: 18px;
        font-weight: bold;
        margin: 15px 0;
        padding: 10px;
        border: 2px solid #28a745;
        border-radius: 8px;
    }}
    @media print {{
        body {{ padding: 0; }}
        .no-print {{ display: none; }}
        .invoice-box {{
            box-shadow: none;
            border: none;
        }}
    }}
</style>
</head>
<body>
<div class="invoice-box">

    <!-- HEADER -->
    <div class="header">
        <h1>🏥 City Hospital</h1>
        <p>123 Medical Street, Healthcare City</p>
        <p>📞 +91 98765 43210 |
           📧 info@cityhospital.com</p>
        <p>🌐 www.cityhospital.com</p>
    </div>

    <!-- INVOICE INFO -->
    <div class="invoice-info">
        <div>
            <strong>📄 Invoice Number:</strong>
            #INV-{b['bill_id']:04d}<br>
            <strong>📅 Date:</strong>
            {b['date']}<br>
            <strong>💳 Payment:</strong>
            <span class="payment-badge">
                {b['payment']} ✓
            </span>
        </div>
        <div style="text-align:right">
            <strong>🏥 Hospital ID:</strong>
            HOSP-2026<br>
            <strong>🔰 GST No:</strong>
            27XXXXX1234X1Z5<br>
            <strong>📋 Bill Type:</strong>
            OPD Consultation
        </div>
    </div>

    <!-- PATIENT INFO -->
    <div class="patient-info">
        <h3>👤 Patient Information</h3>
        <div class="info-grid">
            <div>
                <strong>Patient Name:</strong>
                {p['full_name']}<br>
                <strong>Patient ID:</strong>
                {p['patient_id']}<br>
                <strong>Age/Gender:</strong>
                {p['age']} / {p['gender']}
            </div>
            <div>
                <strong>Blood Group:</strong>
                {p['blood_group']}<br>
                <strong>Phone:</strong>
                {p['phone']}<br>
                <strong>Address:</strong>
                {p.get('address', 'N/A')}
            </div>
        </div>
    </div>

    <!-- BILL ITEMS TABLE -->
    <table>
        <thead>
            <tr>
                <th>#</th>
                <th>Description</th>
                <th>Category</th>
                <th style="text-align:right">Amount</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>1</td>
                <td>Doctor Consultation Charges</td>
                <td>🩺 Consultation</td>
                <td style="text-align:right">
                    ₹{b['consult']:,.2f}
                </td>
            </tr>
            <tr>
                <td>2</td>
                <td>Medicine & Pharmacy Charges</td>
                <td>💊 Medicine</td>
                <td style="text-align:right">
                    ₹{b['medicine']:,.2f}
                </td>
            </tr>
            <tr>
                <td>3</td>
                <td>Laboratory Test Charges</td>
                <td>🧪 Lab Tests</td>
                <td style="text-align:right">
                    ₹{b['lab']:,.2f}
                </td>
            </tr>
        </tbody>
    </table>

    <!-- TOTAL SECTION -->
    <div class="total-section">
        <div class="total-row">
            <span>Subtotal:</span>
            <span>₹{b['total']:,.2f}</span>
        </div>
        <div class="total-row">
            <span>GST (5%):</span>
            <span>₹{b['total'] * 0.05:,.2f}</span>
        </div>
        <div class="total-row">
            <span>Discount:</span>
            <span>₹0.00</span>
        </div>
        <div class="grand-total">
            <span>💰 Grand Total:</span>
            <span>₹{b['total'] + (b['total'] * 0.05):,.2f}</span>
        </div>
    </div>

    <!-- PAID WATERMARK -->
    <div class="watermark">
        ✅ PAYMENT RECEIVED - {b['payment'].upper()}
    </div>

    <!-- FOOTER -->
    <div class="footer">
        <p><strong>Thank you for choosing
        City Hospital! 🏥</strong></p>
        <p>Get well soon! 💊</p>
        <br>
        <p style="font-size:12px">
        * This is a computer generated invoice.
        No signature required.<br>
        * For any queries contact:
        billing@cityhospital.com<br>
        * Valid subject to realization of cheque.
        </p>
    </div>

</div>

<!-- PRINT BUTTON -->
<div class="no-print"
     style="text-align:center; margin:20px">
    <button onclick="window.print()"
            style="background:#0066cc;
                   color:white;
                   padding:15px 40px;
                   font-size:18px;
                   border:none;
                   border-radius:8px;
                   cursor:pointer">
        🖨️ Print Invoice
    </button>
</div>

</body>
</html>
"""
            # Show invoice preview
            st.subheader("📄 Invoice Preview:")
            st.components.v1.html(
                invoice_html,
                height=900,
                scrolling=True
            )

            # Download button
            st.download_button(
                label="⬇️ Download Invoice HTML",
                data=invoice_html,
                file_name=f"invoice_{b['bill_id']}.html",
                mime="text/html",
                key="download_invoice"
            )

            st.success("""
            ✅ Invoice Generated!

            **To Print:**
            1. Click 🖨️ Print Invoice button
               in the preview above
            2. OR Download and open in browser
            3. Press Ctrl+P to print
            4. Select your printer
            5. Click Print!
            """)

    # ======= AI ASSISTANT =======
        elif menu == "🤖 AI Assistant":
            st.title("🤖 AI Medical Assistant")
            st.info("AI suggestions are for reference only!")

        ai_option = st.selectbox(
            "Choose AI Feature:",
            [
                "🔍 Symptom Analysis",
                "💊 Prescription Suggestion",
                "🧪 Lab Report Analysis",
                "📄 Discharge Summary"
            ],
            key="ai_option"
        )

        if ai_option == "🔍 Symptom Analysis":
            col1, col2 = st.columns(2)
            with col1:
                ai_age = st.number_input("Patient Age:", 1, 120, 30, key="ai_age")
            with col2:
                ai_gender = st.selectbox("Gender:", ["Male", "Female"], key="ai_gender")
            ai_symptoms = st.text_area("Enter symptoms:", key="ai_symptoms")
            if st.button("🤖 Analyze", key="ai_analyze_btn"):
                if ai_symptoms:
                    with st.spinner("AI analyzing..."):
                        result = analyze_symptoms(ai_symptoms, ai_age, ai_gender)
                    st.subheader("AI Analysis:")
                    st.write(result)

        elif ai_option == "💊 Prescription Suggestion":
            ai_diagnosis = st.text_input("Diagnosis:", key="ai_diagnosis")
            ai_allergies = st.text_input("Patient Allergies:", "None", key="ai_allergies")
            if st.button("💊 Get Suggestion", key="ai_prescription_btn"):
                if ai_diagnosis:
                    with st.spinner("AI suggesting..."):
                        result = suggest_prescription(ai_diagnosis, ai_allergies)
                    st.write(result)

        elif ai_option == "🧪 Lab Report Analysis":
            col1, col2, col3 = st.columns(3)
            with col1:
                ai_test = st.text_input("Test Name:", key="ai_test")
            with col2:
                ai_result = st.text_input("Result:", key="ai_result")
            with col3:
                ai_normal = st.text_input("Normal Range:", key="ai_normal")
            if st.button("🧪 Analyze", key="ai_lab_analyze_btn"):
                if ai_test and ai_result:
                    with st.spinner("Analyzing..."):
                        analysis = analyze_lab_report(ai_test, ai_result, ai_normal)
                    st.write(analysis)

        elif ai_option == "📄 Discharge Summary":
            col1, col2 = st.columns(2)
            with col1:
                dis_name = st.text_input("Patient Name:", key="dis_name")
                dis_diagnosis = st.text_input("Diagnosis:", key="dis_diagnosis")
                dis_treatment = st.text_area("Treatment Given:", key="dis_treatment")
            with col2:
                dis_prescription = st.text_area("Prescription:", key="dis_prescription")
                dis_followup = st.text_input("Follow-up Instructions:", key="dis_followup")
            if st.button("📄 Generate Summary", key="dis_summary_btn"):
                if dis_name and dis_diagnosis:
                    with st.spinner("Generating..."):
                        summary = generate_discharge_summary(
                            dis_name, dis_diagnosis,
                            dis_treatment, dis_prescription,
                            dis_followup
                        )
                    st.write(summary)

    # ======= ANALYTICS =======
        elif menu == "📊 Analytics":
            st.title("📊 Hospital Analytics")

        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "📅 Daily Revenue",
                f"₹{get_daily_revenue():,.0f}"
            )
        with col2:
            st.metric(
                "📅 Monthly Revenue",
                f"₹{get_monthly_revenue():,.0f}"
            )

        st.divider()
        stats = get_total_stats()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Patients", stats["total_patients"])
        with col2:
            st.metric("Total Doctors", stats["total_doctors"])
        with col3:
            st.metric("Today's Appointments", stats["today_appointments"])