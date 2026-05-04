from pydantic import BaseModel, Field


class UserLoginRequest(BaseModel):
    username: str
    password: str


class UserRegisterRequest(BaseModel):
    username: str
    password: str
    role: str
    full_name: str
    email: str = ""
    phone: str = ""


class PatientCreateRequest(BaseModel):
    full_name: str
    age: int
    gender: str
    blood_group: str
    phone: str
    email: str = ""
    address: str = ""
    emergency_contact: str = ""
    allergies: str = ""


class MedicalRecordCreateRequest(BaseModel):
    doctor_id: int
    diagnosis: str
    symptoms: str
    treatment: str
    prescription: str
    notes: str = ""
    follow_up: str = ""


class LabReportCreateRequest(BaseModel):
    test_name: str
    result: str
    normal_range: str
    status: str
    notes: str = ""


class BillingCreateRequest(BaseModel):
    consultation_fee: float = Field(default=0, ge=0)
    medicine_cost: float = Field(default=0, ge=0)
    lab_cost: float = Field(default=0, ge=0)
    payment_method: str


class SymptomAnalysisRequest(BaseModel):
    symptoms: str
    age: int
    gender: str


class PrescriptionRequest(BaseModel):
    diagnosis: str
    allergies: str = ""


class LabAnalysisRequest(BaseModel):
    test_name: str
    result: str
    normal_range: str


class DischargeSummaryRequest(BaseModel):
    patient_name: str
    diagnosis: str
    treatment: str
    prescription: str
    follow_up: str
