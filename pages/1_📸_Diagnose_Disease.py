# pages/1_📸_Diagnose_Disease.py

import uuid
from pathlib import Path

import numpy as np
import streamlit as st

from config import BASE_DIR
from utils.auth import require_login
from utils.image_utils import load_image, preprocess_image, to_model_tensor
from utils.geo import parse_latlon, district_to_fake_coords
from models.disease_model import get_model, predict, UNKNOWN_LABEL
from services.reporting import create_report
from services.weather import get_weather_and_risk
import services.advisory as advisory_service

# Restrict access
require_login(roles=["farmer", "expert", "admin"])

st.title("📸 Diagnose Disease & Report Case")

# Farmer and field information
col1, col2 = st.columns(2)

with col1:
    farmer_name = st.text_input("Farmer name", value=st.session_state.get("user", ""))
    phone = st.text_input("Phone number", max_chars=15)
    crop = st.selectbox("Crop", ["Wheat", "Rice", "Maize", "Tomato", "Potato", "Other"])
    variety = st.text_input("Variety (optional)")
    district = st.text_input("District / Taluk")

with col2:
    lat = st.text_input("Latitude (optional)")
    lon = st.text_input("Longitude (optional)")

# Image capture / upload
st.subheader("Capture or upload image")
use_camera = st.toggle("Use camera", value=True)

if use_camera:
    image_file = st.camera_input("Take a picture of the affected leaf/plant")
else:
    image_file = st.file_uploader(
        "Upload leaf/plant image", type=["jpg", "jpeg", "png"]
    )

submit = st.button("Run Diagnosis")

# --- Main logic -------------------------------------------------------------

if submit and image_file:
    # 1. Load + show image
    image = load_image(image_file)
    st.image(image, caption="Captured / Uploaded sample", use_column_width=True)

    # 2. Preprocess for model (NHWC, [0,1])
    proc = preprocess_image(image)
    tensor = to_model_tensor(proc)               # shape (1, H, W, 3)

    # 3. Run prediction
    _ = get_model()                              # ensure model is loaded
    result = predict(tensor, crop)

    # 4. Display AI diagnosis with clear HEALTHY / INFECTED / UNKNOWN
    st.subheader("AI Diagnosis")

    if result.disease == UNKNOWN_LABEL:
        st.error(
            "The system could not confidently detect a crop leaf from this image.\n\n"
            "Please try again with a clearer photo of the affected leaf or plant."
        )
        # Show advisory but DO NOT store as a report
        advisory_text = advisory_service.generate_advisory(result.disease, result.severity)
        st.subheader("Advisory")
        st.write(advisory_text)
        st.stop()

    status_text = "INFECTED" if result.infected else "HEALTHY"
    st.write(f"**Plant status:** {status_text}")
    st.write(f"**Predicted disease/class:** {result.disease}")
    st.write(f"**Confidence:** {result.confidence:.2f}")
    st.write(f"**Estimated severity:** {result.severity}")

    st.write("Top candidates:")
    for name, prob in result.top_k:
        st.write(f"- {name}: {prob:.2f}")

    # 5. Risk & weather context
    w = get_weather_and_risk(district or "Unknown", crop)
    st.subheader("Risk & Weather Context")
    st.write(
        f"Recent rain: {w['rain_mm']} mm, humidity: {w['humidity']}%, "
        f"environmental risk score: {w['risk_score']}"
    )

    # 6. Advisory for valid crop images
    advisory_text = advisory_service.generate_advisory(result.disease, result.severity)
    st.subheader("Advisory")
    st.write(advisory_text)

    # 7. Save image
    img_dir = BASE_DIR / "uploaded_images"
    img_dir.mkdir(exist_ok=True)
    fname = f"{uuid.uuid4().hex}.jpg"
    fpath = img_dir / fname
    image.save(fpath)

    # 8. Location handling
    coords = parse_latlon(lat, lon)
    if not coords and district:
        coords = district_to_fake_coords(district)
    lat_val, lon_val = (coords if coords else (None, None))

    # 9. Build payload and store in DB
    payload = {
        "farmer_name": farmer_name,
        "phone": phone,
        "crop": crop,
        "variety": variety,
        "district": district,
        "latitude": lat_val,
        "longitude": lon_val,
        "image_path": str(fpath),
        "predicted_disease": result.disease,
        "confidence": result.confidence,
        "severity": result.severity,
        "risk_score": w["risk_score"],
        "advisory": advisory_text,
        "status": "OPEN",
    }
    report_id = create_report(payload)
    st.success(f"Report created with ID: {report_id}")

elif submit and not image_file:
    st.error("Please capture or upload an image first.")
