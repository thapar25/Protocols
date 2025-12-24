def fetch_basic_info() -> str:
    """Fetches basic health information of the user."""
    return "Name: Pulkit Thapar, Age: 25, Height: 170cm, Weight: 69kg, Blood Type: O+, Allergies: None"  # sample data


def fetch_vitals_summary() -> str:
    """Fetches summary of vital health statistics."""
    return "Avg. blood Pressure: 120/80 mmHg, Avg. Heart Rate: 72 bpm, Respiratory Rate: 16 breaths/min, Temperature: 98.6°F"  # sample data


def fetch_designated_doctor() -> str:
    """Fetches the designated healthcare provider's information."""
    return "Dr. John Smith, General Physician"


def contact_healthcare_provider(message: str) -> str:
    """Sends a message to the designated healthcare provider's assistant."""
    return f"Message sent to healthcare provider: {message}"
