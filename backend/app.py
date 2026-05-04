from pathlib import Path
import sys

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from ai_helper import (  # noqa: E402
    analyze_lab_report,
    analyze_symptoms,
    generate_discharge_summary,
    suggest_prescription,
)
from analytics import (  # noqa: E402
    get_appointment_stats,
    get_monthly_patients,
    get_patient_gender_data,
    get_total_stats,
)
from auth import get_all_doctors, login_user, register_user  # noqa: E402
from billing import (  # noqa: E402
    create_bill,
    get_daily_revenue,
    get_monthly_revenue,
    get_patient_bills,
)
from database import create_all_tables  # noqa: E402
from patient import (  # noqa: E402
    add_lab_report,
    add_medical_record,
    get_all_patients,
    get_lab_reports,
    get_medical_history,
    get_patient,
    register_patient,
    search_patients,
)

from backend.schemas import (  # noqa: E402
    BillingCreateRequest,
    DischargeSummaryRequest,
    LabAnalysisRequest,
    LabReportCreateRequest,
    MedicalRecordCreateRequest,
    PatientCreateRequest,
    PrescriptionRequest,
    SymptomAnalysisRequest,
    UserLoginRequest,
    UserRegisterRequest,
)

create_all_tables()

app = FastAPI(
    title="AI Health Assistant API",
    description="Split frontend/backend API for the hospital management project.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_dir = BASE_DIR / "frontend"
if frontend_dir.exists():
    app.mount(
        "/frontend",
        StaticFiles(directory=str(frontend_dir), html=True),
        name="frontend",
    )


def _ensure_patient(patient_id: str):
    patient = get_patient(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found.")
    return patient


@app.get("/")
def root():
    if frontend_dir.exists():
        return RedirectResponse(url="/frontend/")
    return {"message": "API is running. Frontend files were not found."}


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/auth/login")
def api_login(payload: UserLoginRequest):
    success, result = login_user(payload.username, payload.password)
    if not success:
        raise HTTPException(status_code=401, detail=result)
    return {"message": "Login successful.", "user": result}


@app.post("/api/auth/register")
def api_register(payload: UserRegisterRequest):
    success, result = register_user(
        payload.username,
        payload.password,
        payload.role,
        payload.full_name,
        payload.email,
        payload.phone,
    )
    if not success:
        raise HTTPException(status_code=400, detail=result)
    return {"message": result}


@app.get("/api/doctors")
def api_doctors():
    return {"doctors": get_all_doctors()}


@app.get("/api/dashboard/stats")
def api_dashboard_stats():
    stats = get_total_stats()
    stats["daily_revenue"] = get_daily_revenue()
    stats["monthly_revenue"] = get_monthly_revenue()
    return stats


@app.get("/api/patients")
def api_patients(search: str = ""):
    patients = search_patients(search) if search else get_all_patients()
    return {"patients": patients}


@app.post("/api/patients")
def api_create_patient(payload: PatientCreateRequest):
    success, result = register_patient(
        payload.full_name,
        payload.age,
        payload.gender,
        payload.blood_group,
        payload.phone,
        payload.email,
        payload.address,
        payload.emergency_contact,
        payload.allergies,
    )
    if not success:
        raise HTTPException(status_code=400, detail=result)

    patient = get_patient(result)
    return {
        "message": "Patient registered successfully.",
        "patient_id": result,
        "patient": patient,
    }


@app.get("/api/patients/{patient_id}")
def api_get_patient(patient_id: str):
    patient = _ensure_patient(patient_id)
    return {"patient": patient}


@app.get("/api/patients/{patient_id}/medical-records")
def api_medical_records(patient_id: str):
    _ensure_patient(patient_id)
    return {"records": get_medical_history(patient_id)}


@app.post("/api/patients/{patient_id}/medical-records")
def api_add_medical_record(
    patient_id: str,
    payload: MedicalRecordCreateRequest,
):
    _ensure_patient(patient_id)
    add_medical_record(
        patient_id,
        payload.doctor_id,
        payload.diagnosis,
        payload.symptoms,
        payload.treatment,
        payload.prescription,
        payload.notes,
        payload.follow_up,
    )
    return {"message": "Medical record added successfully."}


@app.get("/api/patients/{patient_id}/lab-reports")
def api_lab_reports(patient_id: str):
    _ensure_patient(patient_id)
    return {"reports": get_lab_reports(patient_id)}


@app.post("/api/patients/{patient_id}/lab-reports")
def api_add_lab_report(
    patient_id: str,
    payload: LabReportCreateRequest,
):
    _ensure_patient(patient_id)
    add_lab_report(
        patient_id,
        payload.test_name,
        payload.result,
        payload.normal_range,
        payload.status,
        payload.notes,
    )
    return {"message": "Lab report added successfully."}


@app.get("/api/patients/{patient_id}/billing")
def api_patient_billing(patient_id: str):
    _ensure_patient(patient_id)
    return {"bills": get_patient_bills(patient_id)}


@app.post("/api/patients/{patient_id}/billing")
def api_add_bill(
    patient_id: str,
    payload: BillingCreateRequest,
):
    _ensure_patient(patient_id)
    bill_id, total = create_bill(
        patient_id,
        payload.consultation_fee,
        payload.medicine_cost,
        payload.lab_cost,
        payload.payment_method,
    )
    return {
        "message": "Bill created successfully.",
        "bill_id": bill_id,
        "total_amount": total,
    }


@app.get("/api/analytics/overview")
def api_analytics():
    monthly_patients = [
        {"month": row[0], "count": row[1]}
        for row in get_monthly_patients()
    ]
    return {
        "stats": get_total_stats(),
        "gender_distribution": get_patient_gender_data(),
        "monthly_patients": monthly_patients,
        "appointments": get_appointment_stats(),
    }


@app.post("/api/ai/symptom-analysis")
def api_symptom_analysis(payload: SymptomAnalysisRequest):
    return {
        "analysis": analyze_symptoms(
            payload.symptoms,
            payload.age,
            payload.gender,
        )
    }


@app.post("/api/ai/prescription")
def api_prescription(payload: PrescriptionRequest):
    return {
        "suggestion": suggest_prescription(
            payload.diagnosis,
            payload.allergies,
        )
    }


@app.post("/api/ai/lab-analysis")
def api_lab_analysis(payload: LabAnalysisRequest):
    return {
        "analysis": analyze_lab_report(
            payload.test_name,
            payload.result,
            payload.normal_range,
        )
    }


@app.post("/api/ai/discharge-summary")
def api_discharge_summary(payload: DischargeSummaryRequest):
    return {
        "summary": generate_discharge_summary(
            payload.patient_name,
            payload.diagnosis,
            payload.treatment,
            payload.prescription,
            payload.follow_up,
        )
    }
