const API_BASE = window.location.protocol === "file:" ? "http://127.0.0.1:8000" : window.location.origin;

const state = {
    currentUser: null,
    selectedPatientId: null,
};

const elements = {
    statusBanner: document.getElementById("status-banner"),
    userBadge: document.getElementById("user-badge"),
    metricPatients: document.getElementById("metric-patients"),
    metricAppointments: document.getElementById("metric-appointments"),
    metricDoctors: document.getElementById("metric-doctors"),
    metricRevenue: document.getElementById("metric-revenue"),
    patientResults: document.getElementById("patient-results"),
    selectedPatientChip: document.getElementById("selected-patient-chip"),
    patientSummary: document.getElementById("patient-summary"),
    medicalHistory: document.getElementById("medical-history"),
    labHistory: document.getElementById("lab-history"),
    billingHistory: document.getElementById("billing-history"),
};

async function fetchJson(path, options = {}) {
    const response = await fetch(`${API_BASE}${path}`, {
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {}),
        },
        ...options,
    });

    let data = {};
    try {
        data = await response.json();
    } catch (error) {
        data = {};
    }

    if (!response.ok) {
        throw new Error(data.detail || "Something went wrong.");
    }

    return data;
}

function showStatus(message, type = "success") {
    elements.statusBanner.textContent = message;
    elements.statusBanner.className = `status-banner ${type}`;
}

function clearStatus() {
    elements.statusBanner.textContent = "";
    elements.statusBanner.className = "status-banner hidden";
}

function formToObject(form) {
    const values = Object.fromEntries(new FormData(form).entries());
    return Object.fromEntries(
        Object.entries(values).map(([key, value]) => [key, typeof value === "string" ? value.trim() : value]),
    );
}

function renderCards(stats) {
    elements.metricPatients.textContent = stats.total_patients ?? 0;
    elements.metricAppointments.textContent = stats.today_appointments ?? 0;
    elements.metricDoctors.textContent = stats.total_doctors ?? 0;
    elements.metricRevenue.textContent = `Rs ${Number(stats.today_revenue ?? 0).toLocaleString("en-IN")}`;
}

function renderHistory(target, items, formatter) {
    if (!items.length) {
        target.innerHTML = `<div class="list-item"><p>No records yet.</p></div>`;
        return;
    }

    target.innerHTML = items.map(formatter).join("");
}

function renderPatientSummary(patient) {
    elements.selectedPatientChip.textContent = patient.patient_id;
    elements.patientSummary.className = "patient-summary";
    elements.patientSummary.innerHTML = `
        <strong>${patient.full_name}</strong><br>
        ${patient.gender}, ${patient.age} years old, blood group ${patient.blood_group || "N/A"}<br>
        Phone: ${patient.phone || "N/A"} | Emergency: ${patient.emergency_contact || "N/A"}<br>
        Allergies: ${patient.allergies || "None recorded"}<br>
        Address: ${patient.address || "Not provided"}
    `;
}

function renderPatientResults(patients) {
    if (!patients.length) {
        elements.patientResults.innerHTML = `<div class="list-item"><p>No matching patients found.</p></div>`;
        return;
    }

    elements.patientResults.innerHTML = patients
        .map(
            (patient) => `
                <div class="list-item">
                    <h4>${patient.full_name}</h4>
                    <p>${patient.patient_id} | ${patient.phone || "No phone"}</p>
                    <button type="button" data-patient-id="${patient.patient_id}">Open chart</button>
                </div>
            `,
        )
        .join("");

    elements.patientResults.querySelectorAll("button[data-patient-id]").forEach((button) => {
        button.addEventListener("click", () => loadPatientWorkspace(button.dataset.patientId));
    });
}

async function loadStats() {
    const stats = await fetchJson("/api/dashboard/stats");
    renderCards(stats);
}

async function loadPatients(search = "") {
    const path = search ? `/api/patients?search=${encodeURIComponent(search)}` : "/api/patients";
    const data = await fetchJson(path);
    renderPatientResults(data.patients || []);
}

async function loadPatientWorkspace(patientId) {
    state.selectedPatientId = patientId;

    const [patientData, recordsData, labsData, billsData] = await Promise.all([
        fetchJson(`/api/patients/${encodeURIComponent(patientId)}`),
        fetchJson(`/api/patients/${encodeURIComponent(patientId)}/medical-records`),
        fetchJson(`/api/patients/${encodeURIComponent(patientId)}/lab-reports`),
        fetchJson(`/api/patients/${encodeURIComponent(patientId)}/billing`),
    ]);

    renderPatientSummary(patientData.patient);
    renderHistory(
        elements.medicalHistory,
        recordsData.records || [],
        (record) => `
            <div class="list-item">
                <h4>${record.diagnosis}</h4>
                <p>${record.date || "No date"} | Follow-up: ${record.follow_up || "Not set"}</p>
                <p>${record.treatment || "No treatment details"}</p>
            </div>
        `,
    );
    renderHistory(
        elements.labHistory,
        labsData.reports || [],
        (report) => `
            <div class="list-item">
                <h4>${report.test_name}</h4>
                <p>${report.result} (${report.status})</p>
                <p>Normal range: ${report.normal_range}</p>
            </div>
        `,
    );
    renderHistory(
        elements.billingHistory,
        billsData.bills || [],
        (bill) => `
            <div class="list-item">
                <h4>Rs ${Number(bill.total_amount || 0).toLocaleString("en-IN")}</h4>
                <p>${bill.date || "No date"} | ${bill.payment_method || "Unknown method"}</p>
                <p>Status: ${bill.payment_status || "Unknown"}</p>
            </div>
        `,
    );
}

function requireSelectedPatient() {
    if (!state.selectedPatientId) {
        throw new Error("Select a patient first.");
    }
}

function requireLoggedUser() {
    if (!state.currentUser) {
        throw new Error("Login as a staff member first.");
    }
}

document.getElementById("login-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    clearStatus();

    try {
        const payload = formToObject(event.currentTarget);
        const data = await fetchJson("/api/auth/login", {
            method: "POST",
            body: JSON.stringify(payload),
        });

        state.currentUser = data.user;
        elements.userBadge.textContent = `${data.user.full_name} (${data.user.role})`;
        elements.userBadge.classList.remove("hidden");
        showStatus("Logged in successfully.");
        event.currentTarget.reset();
    } catch (error) {
        showStatus(error.message, "error");
    }
});

document.getElementById("register-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    clearStatus();

    try {
        const payload = formToObject(event.currentTarget);
        await fetchJson("/api/auth/register", {
            method: "POST",
            body: JSON.stringify(payload),
        });
        showStatus("Staff account created.");
        event.currentTarget.reset();
    } catch (error) {
        showStatus(error.message, "error");
    }
});

document.getElementById("patient-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    clearStatus();

    try {
        const payload = formToObject(event.currentTarget);
        payload.age = Number(payload.age || 0);

        const data = await fetchJson("/api/patients", {
            method: "POST",
            body: JSON.stringify(payload),
        });

        showStatus(`Patient registered with ID ${data.patient_id}.`);
        event.currentTarget.reset();
        await loadStats();
        await loadPatients();
        await loadPatientWorkspace(data.patient_id);
    } catch (error) {
        showStatus(error.message, "error");
    }
});

document.getElementById("search-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    clearStatus();

    try {
        const searchTerm = document.getElementById("search-input").value.trim();
        await loadPatients(searchTerm);
    } catch (error) {
        showStatus(error.message, "error");
    }
});

document.getElementById("medical-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    clearStatus();

    try {
        requireSelectedPatient();
        requireLoggedUser();

        const payload = formToObject(event.currentTarget);
        payload.doctor_id = Number(state.currentUser.id);

        await fetchJson(`/api/patients/${encodeURIComponent(state.selectedPatientId)}/medical-records`, {
            method: "POST",
            body: JSON.stringify(payload),
        });

        showStatus("Medical record saved.");
        event.currentTarget.reset();
        await loadPatientWorkspace(state.selectedPatientId);
    } catch (error) {
        showStatus(error.message, "error");
    }
});

document.getElementById("lab-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    clearStatus();

    try {
        requireSelectedPatient();
        const payload = formToObject(event.currentTarget);

        await fetchJson(`/api/patients/${encodeURIComponent(state.selectedPatientId)}/lab-reports`, {
            method: "POST",
            body: JSON.stringify(payload),
        });

        showStatus("Lab report saved.");
        event.currentTarget.reset();
        await loadPatientWorkspace(state.selectedPatientId);
    } catch (error) {
        showStatus(error.message, "error");
    }
});

document.getElementById("billing-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    clearStatus();

    try {
        requireSelectedPatient();
        const payload = formToObject(event.currentTarget);
        payload.consultation_fee = Number(payload.consultation_fee || 0);
        payload.medicine_cost = Number(payload.medicine_cost || 0);
        payload.lab_cost = Number(payload.lab_cost || 0);

        const data = await fetchJson(`/api/patients/${encodeURIComponent(state.selectedPatientId)}/billing`, {
            method: "POST",
            body: JSON.stringify(payload),
        });

        showStatus(`Bill created for Rs ${Number(data.total_amount || 0).toLocaleString("en-IN")}.`);
        event.currentTarget.reset();
        await loadStats();
        await loadPatientWorkspace(state.selectedPatientId);
    } catch (error) {
        showStatus(error.message, "error");
    }
});

async function initialize() {
    try {
        await loadStats();
        await loadPatients();
    } catch (error) {
        showStatus(`${error.message} Make sure the backend is running on ${API_BASE}.`, "error");
    }
}

initialize();
