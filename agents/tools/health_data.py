import random
from datetime import datetime


async def fetch_basic_info() -> str:
    """
    Fetch user's medical profile.
    """
    name = "Pulkit Thapar"
    age = 25
    height_cm = 170
    weight_kg = 69
    blood_type = "O+"
    allergies = "None"
    return (
        f"Name: {name}, Age: {age}, Height: {height_cm} cm, "
        f"Weight: {weight_kg} kg, Blood Type: {blood_type}, Allergies: {allergies}"
    )


async def fetch_vitals_summary() -> str:
    """
    Fetch user's recent vital-sign measurements.
    """
    # Simulate a small range of realistic values.
    systolic = random.randint(110, 130)
    diastolic = random.randint(70, 85)
    heart_rate = random.randint(60, 80)
    respiratory_rate = random.randint(12, 20)
    temperature_c = round(random.uniform(36.5, 37.2), 1)  # Celsius
    temperature_f = round(temperature_c * 9 / 5 + 32, 1)

    return (
        f"Avg. Blood Pressure: {systolic}/{diastolic} mmHg, "
        f"Avg. Heart Rate: {heart_rate} bpm, "
        f"Respiratory Rate: {respiratory_rate} breaths/min, "
        f"Temperature: {temperature_c}°C ({temperature_f}°F)"
        f"At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )


async def fetch_designated_doctor() -> str:
    """
    Fetch information about the user's primary care provider.
    """
    doctor_name = "Dr. John Smith"
    specialty = "General Physician"
    clinic = "Wellness Health Center"
    contact = "(555) 123-4567"
    return f"{doctor_name}, {specialty} - {clinic} (Phone: {contact})"


async def contact_healthcare_provider(message: str) -> str:
    """
    Send a message to the designated provider's assistant. Try to keep the message as informative as possible.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return (
        f'[{timestamp}] Message sent to healthcare provider\'s assistant: "{message}"'
    )
