# 🌱 CropGuard AI

[![Python](https://img.shields.io/badge/Python-3.10-blue)](https://www.python.org/) 
[![Streamlit](https://img.shields.io/badge/Streamlit-1.24-orange)](https://streamlit.io/) 
[![License](https://img.shields.io/badge/License-Unlicensed-red)](https://github.com/M-Nivetha7/CropGuard-AI)

**CropGuard AI** is a full-stack AI-powered web application for farmers to detect crop diseases using leaf images. Farmers can report cases, view analytics, and track crop health over time.

---

## 🚀 Features

- 📸 Capture or upload leaf images  
- 🤖 AI model predicts whether the crop is healthy or infected  
- 📝 Report disease cases to admins and experts  
- 📊 Farmer dashboard for tracking crop health  
- 🔐 Secure login and user sessions  

---

## 🗂️ Project Structure

```
bash
CropGuard-AI/ 🌱
├── app.py                   # 🖥️ Main Streamlit application
├── assets/                  # 🎨 UI assets like images and logos
│   └── logo.png             # 🌟 Project logo
├── model/                   # 🤖 Machine Learning model files
│   └── plant_disease_model.h5  # 📊 Pre-trained crop disease model
├── pages/                   # 🗂️ Streamlit page modules
│   ├── login.py             # 🔐 Login page
│   ├── dashboard.py         # 📊 Farmer dashboard
│   ├── predict.py           # 🩺 Crop disease prediction page
├── uploaded_images/         # 📷 User-uploaded leaf images (ignored in git)
├── requirements.txt         # 📦 Python dependencies
└── README.md                # 📝 Project README
```

Note: uploaded_images/ contains user-uploaded images and should be added to .gitignore to avoid pushing heavy files.

🛠️ Tech Stack
Layer	Technology
Frontend	Streamlit, HTML, CSS
Backend	Python (Streamlit backend)
Machine Learning	TensorFlow / Keras
Database	SQLite / Local Storage
Deployment	Local / GitHub

💻 Setup Instructions
1. Clone the Repository
bash
Copy code
```
git clone https://github.com/M-Nivetha7/CropGuard-AI.git
```
cd CropGuard-AI
3. Install Dependencies
bash
Copy code
```
pip install -r requirements.txt
```
4. Run the Application
bash
Copy code
```
streamlit run app.py
```
```
Open your browser at http://localhost:8501 to access the portal.
```

📸 How It Works
Farmer logs in via the login page

Captures or uploads a leaf image

AI model predicts crop health status

Dashboard shows reports and historical data

Farmers can track disease cases and take action

🎯 Future Enhancements
Multi-language support for farmers

Real-time notifications to agricultural experts

Geolocation-based disease outbreak alerts

Voice-based UI for easier accessibility

🧑‍💻 Team
M Nivetha – Project Lead, ML & Backend

Ramya – Frontend & UI Design

⭐ Support
If you like this project, give it a ⭐ on GitHub! Contributions and suggestions are welcome.

🔒 License
This project is currently unlicensed. Use for educational purposes only.

📸 Screenshots / Demo
You can add images or GIFs here to showcase your app:

markdown
Copy code
![Dashboard Screenshot](assets/dashboard.png)
![Prediction Demo GIF](assets/demo.gif)
