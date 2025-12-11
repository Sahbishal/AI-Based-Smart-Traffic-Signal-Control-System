import os
import sys
import subprocess
import webbrowser
import time
import platform
from pathlib import Path

def print_banner():
    banner = """
    ╔═══════════════════════════════════════════════════════════════════╗
    ║          AI-Based Smart Traffic Signal Control System             ║
    ║                     Ready to Launch!                              ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_requirements():
    """Check if required packages are installed"""
    required_packages = ['flask', 'opencv', 'ultralytics', 'torch']
    print("\n📋 Checking requirements...")
    
    try:
        import flask
        import cv2
        import ultralytics
        import torch
        print("✅ All required packages found!")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("\n💡 Run: pip install -r requirements.txt")
        return False

def install_dependencies():
    """Install dependencies from requirements.txt"""
    print("\n📦 Installing dependencies...")
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ requirements.txt not found!")
        return False
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def start_backend_server():
    """Start the Flask backend server"""
    print("\n🚀 Starting Backend Server...")
    backend_path = Path(__file__).parent / "Backend"
    
    if not (backend_path / "app.py").exists():
        print("❌ Backend app.py not found!")
        return None
    
    try:
        if platform.system() == "Windows":
            process = subprocess.Popen(
                [sys.executable, str(backend_path / "app.py")],
                cwd=str(backend_path),
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            process = subprocess.Popen(
                [sys.executable, str(backend_path / "app.py")],
                cwd=str(backend_path)
            )
        print("✅ Backend server started (PID: {})".format(process.pid))
        return process
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def start_frontend_server():
    """Start a simple HTTP server for frontend"""
    print("\n🌐 Starting Frontend Server...")
    frontend_path = Path(__file__).parent / "Frontend"
    
    if not (frontend_path / "index.html").exists():
        print("❌ Frontend index.html not found!")
        return None
    
    try:
        if platform.system() == "Windows":
            process = subprocess.Popen(
                [sys.executable, "-m", "http.server", "8000", "--directory", str(frontend_path)],
                creationflags=subprocess.CREATE_NEW_CONSOLE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        else:
            process = subprocess.Popen(
                [sys.executable, "-m", "http.server", "8000", "--directory", str(frontend_path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        print("✅ Frontend server started (PID: {})".format(process.pid))
        return process
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return None

def open_browser():
    """Open the web interface in default browser"""
    print("\n🌍 Opening Dashboard...")
    time.sleep(2)
    try:
        webbrowser.open("http://localhost:8000")
        print("✅ Dashboard opened in browser")
    except Exception as e:
        print(f"⚠️  Could not open browser automatically: {e}")
        print("📌 Manually visit: http://localhost:8000")

def print_info():
    """Print system information"""
    info = """
    ╔════════════════════════════════════════════════════════════╗
    ║                    System Information                       ║
    ╠════════════════════════════════════════════════════════════╣
    ║ Backend API:        http://localhost:5000                  ║
    ║ Frontend Dashboard: http://localhost:8000                  ║
    ║ API Documentation:  http://localhost:5000/api/             ║
    ║                                                              ║
    ║ Available Endpoints:                                        ║
    ║ • GET  /health                        - System health      ║
    ║ • GET  /api/intersections             - All intersections  ║
    ║ • POST /api/detection/image           - Detect vehicles    ║
    ║ • POST /api/intersection/<id>/signal/cycle                 ║
    ║ • POST /api/intersection/<id>/emergency/<dir>              ║
    ╠════════════════════════════════════════════════════════════╣
    ║ Features:                                                   ║
    ║ ✓ Real-time Vehicle Detection (YOLO)                      ║
    ║ ✓ Adaptive Traffic Signal Control                         ║
    ║ ✓ Emergency Vehicle Priority                              ║
    ║ ✓ Interactive Dashboard                                   ║
    ║ ✓ RESTful API                                             ║
    ║ ✓ Vehicle Tracking & Analytics                            ║
    ╚════════════════════════════════════════════════════════════╝
    """
    print(info)

def show_menu():
    """Show interactive menu"""
    menu = """
    ╔════════════════════════════════════════════════════════════╗
    ║           AI Traffic Management System Menu                ║
    ╠════════════════════════════════════════════════════════════╣
    ║ 1. Install Dependencies                                    ║
    ║ 2. Start Full System (Backend + Frontend)                 ║
    ║ 3. Start Backend Only                                      ║
    ║ 4. Start Frontend Only                                     ║
    ║ 5. View Documentation                                      ║
    ║ 6. Exit                                                     ║
    ╚════════════════════════════════════════════════════════════╝
    """
    return menu

def main():
    print_banner()
    print_info()
    
    backend_process = None
    frontend_process = None
    
    while True:
        print(show_menu())
        choice = input("📌 Select an option (1-6): ").strip()
        
        if choice == "1":
            install_dependencies()
        
        elif choice == "2":
            if not check_requirements():
                print("\n❓ Would you like to install dependencies? (y/n): ", end="")
                if input().lower() == "y":
                    if not install_dependencies():
                        continue
                else:
                    continue
            
            print("\n🔄 Starting full system...")
            backend_process = start_backend_server()
            frontend_process = start_frontend_server()
            
            if backend_process and frontend_process:
                print("\n✅ System Started Successfully!")
                open_browser()
                print("\n⏸️  Press Ctrl+C to stop the system...")
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("\n\n🛑 Shutting down system...")
                    backend_process.terminate()
                    frontend_process.terminate()
                    print("✅ System stopped")
            else:
                print("\n❌ Failed to start system")
        
        elif choice == "3":
            if not check_requirements():
                print("\n❓ Install dependencies first? (y/n): ", end="")
                if input().lower() == "y":
                    install_dependencies()
            backend_process = start_backend_server()
            if backend_process:
                print("\n⏸️  Press Ctrl+C to stop...")
                try:
                    backend_process.wait()
                except KeyboardInterrupt:
                    print("\n🛑 Stopping backend...")
                    backend_process.terminate()
        
        elif choice == "4":
            frontend_process = start_frontend_server()
            if frontend_process:
                open_browser()
                print("\n⏸️  Press Ctrl+C to stop...")
                try:
                    frontend_process.wait()
                except KeyboardInterrupt:
                    print("\n🛑 Stopping frontend...")
                    frontend_process.terminate()
        
        elif choice == "5":
            print("""
    📖 API Documentation:
    
    Authentication: None (Development Mode)
    
    Base URL: http://localhost:5000/api
    
    Endpoints:
    
    1. Health Check
       GET /health
       Response: {"status": "healthy"}
    
    2. Get All Intersections
       GET /intersections
       Response: [{"id": "INT_001", "name": "...", ...}]
    
    3. Get Intersection Status
       GET /intersection/{id}/status
       Response: {"signals": {...}, "vehicle_counts": {...}, ...}
    
    4. Detect Vehicles from Image
       POST /detection/image
       Params: image (file), intersection_id, direction
       Response: {"total_vehicles": 5, ...}
    
    5. Cycle Traffic Signal
       POST /intersection/{id}/signal/cycle
       Response: {"signals": {"north": "green", ...}}
    
    6. Emergency Mode
       POST /intersection/{id}/emergency/{direction}
       Response: {"signals": {"north": "green", ...}}
            """)
        
        elif choice == "6":
            print("\n👋 Thank you for using AI Traffic Management System!")
            sys.exit(0)
        
        else:
            print("❌ Invalid option. Please select 1-6.")
        
        print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 System terminated by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
