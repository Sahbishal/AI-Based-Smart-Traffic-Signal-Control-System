🚦 AI-Based Smart Traffic Signal Control System

A smart traffic management system using YOLOv11, Flask, and OpenCV to optimize traffic flow with real-time vehicle detection, adaptive signal timing, and emergency vehicle prioritization. Includes a full REST API and an interactive dashboard.

✨ Features

🤖 Real-time vehicle detection (YOLOv11)

🎯 Adaptive traffic signal control based on vehicle density

🚨 Emergency vehicle priority

📊 Real-time dashboard with live statistics

🔌 RESTful API for easy integration

📍 Vehicle tracking and traffic pattern analysis

📈 Traffic analytics & insights

🚀 Quick Start
INSTALL_DEPENDENCIES.bat
START_SYSTEM.bat

macOS / Linux
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python Backend/app.py


Dashboard → http://localhost:8000

API → http://localhost:5000

🔌 API Overview
GET  /health
GET  /api/intersections
GET  /api/intersection/{id}/signal/state
POST /api/detection/image
POST /api/intersection/{id}/emergency/{direction}
GET  /api/stats/overview

📁 Project Structure
Backend/     → Flask API, YOLOv11 detection, signal logic
Frontend/    → Dashboard (HTML/CSS/JS)
run_system.py
requirements.txt

🔧 Configuration

Edit .env to set:

Environment mode

API ports

Logging level

Optional database

🧠 Model Details

YOLOv11 Nano (yolo11n.pt)

Lightweight, high-speed detection


