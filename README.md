# 🚦 AI-Powered Smart Traffic Management System

A real-time traffic violation detection and analytics platform. This project utilizes Computer Vision to monitor traffic flow, detect violations, and provide a web-based dashboard for administrative oversight.



## 🚀 Core Features
* **Real-time Detection:** Uses **YOLOv11** for high-accuracy vehicle detection and classification.
* **Automatic License Plate Recognition (ALPR):** Powered by **EasyOCR** to extract vehicle registration numbers.
* **Automated Violation Logging:** Detects stop-line and traffic signal violations, saving data directly to a **Django** backend.
* **Live Analytics Dashboard:** A comprehensive web UI to track total violations, fines, and vehicle types.
* **PDF Report Generation:** Generate professional, legally formatted violation reports using **xhtml2pdf**.

## 🛠️ Tech Stack
* **AI Engine:** Python, YOLOv11, OpenCV, EasyOCR
* **Web Framework:** Django (Python)
* **Database:** SQLite3
* **Frontend:** HTML5, CSS3, Tailwind CSS
* **Reporting:** xhtml2pdf

## 📂 Project Structure
```text
SmartTrafficSystem/
├── traffic_core/           # Django Web Application
│   ├── monitor/            # Dashboard logic and templates
│   ├── traffic_core/       # Project configuration
│   └── db.sqlite3          # Local Database
├── engine.py               # AI Detection Engine (YOLO + OCR)
├── traffic_video.mp4       # Test source video
├── yolo11n.pt              # Trained YOLO weights
└── requirements.txt        # Project dependencies
