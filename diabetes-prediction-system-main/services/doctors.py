import json
import os
import random

import streamlit as st

DOCTORS_FILE = "doctors.json"

DEFAULT_DOCTORS = [
    {
        "name": "Dr. Rolisha Sthapit",
        "specialty": "Senior Diabetologist & Endocrinologist",
        "phone": "+977-9800000000",
        "email": "dr.rolisha@healthcare.com",
        "grade": "higher"
    },
    {
        "name": "Dr. Rayan Dangol",
        "specialty": "General Physician (Diabetes Care)",
        "phone": "+977-9841000001",
        "email": "dr.rayan@healthcare.com",
        "grade": "lower"
    },
    {
        "name": "Dr. Aayam Maharjan",
        "specialty": "General Physician (Diabetes Care)",
        "phone": "+977-9841000002",
        "email": "dr.aayam@healthcare.com",
        "grade": "lower"
    }
]


def initialize_doctors():
    if not os.path.exists(DOCTORS_FILE):
        with open(DOCTORS_FILE, 'w') as f:
            json.dump(DEFAULT_DOCTORS, f, indent=4)


@st.cache_resource
def load_doctors():
    if os.path.exists(DOCTORS_FILE):
        try:
            with open(DOCTORS_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            return DEFAULT_DOCTORS
    return DEFAULT_DOCTORS


def save_doctors(doctors):
    with open(DOCTORS_FILE, 'w') as f:
        json.dump(doctors, f, indent=4)


def recommend_doctor(risk_percentage):
    doctors = load_doctors()

    if risk_percentage > 70:
        target_name = "Rolisha Sthapit"
        if doctors:
            for doc in doctors:
                if target_name.lower() in doc.get("name", "").lower():
                    return doc
        return DEFAULT_DOCTORS[0]

    if risk_percentage > 50:
        if not doctors:
            return None
        available = [d for d in doctors if d.get("grade") == "lower"]
        if available:
            return random.choice(available)

    return None
