#!/usr/bin/env python3
import sys
import os

print("=" * 60)
print("[*] PROJECT VERIFICATION CHECK")
print("=" * 60)

print("\n[*] 1. Checking Dependencies...\n")

deps = {
    'flask': 'Flask',
    'cv2': 'OpenCV',
    'ultralytics': 'Ultralytics/YOLO',
    'torch': 'PyTorch',
    'numpy': 'NumPy',
    'flask_cors': 'Flask-CORS',
    'dotenv': 'python-dotenv',
    'requests': 'Requests'
}

missing = []
for module, name in deps.items():
    try:
        __import__(module)
        print(f'[OK] {name}')
    except ImportError:
        print(f'[X] {name} - NOT INSTALLED')
        missing.append(name)

if missing:
    print(f'\n[!] Missing: {", ".join(missing)}')
    print('Run: pip install -r requirements.txt')
else:
    print('\n[OK] All dependencies installed!')

print("\n" + "=" * 60)
print("[*] 2. Checking Backend Modules...\n")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Backend'))

modules = [
    ('config', 'Config'),
    ('logger', 'Logger'),
    ('vehicle_detector', 'VehicleDetector'),
    ('signal_controller', 'TrafficSignalController'),
    ('object_tracker', 'ObjectTracker'),
    ('app', 'Flask App')
]

backend_ok = True
for module_name, display_name in modules:
    try:
        __import__(module_name)
        print(f'[OK] {display_name} ({module_name}.py)')
    except Exception as e:
        print(f'[X] {display_name}: {str(e)[:50]}')
        backend_ok = False

print("\n" + "=" * 60)
print("[*] 3. Checking Frontend Files...\n")

frontend_files = ['index.html', 'app.js', 'styles.css']
for fname in frontend_files:
    fpath = os.path.join(os.path.dirname(__file__), 'Frontend', fname)
    if os.path.exists(fpath):
        size = os.path.getsize(fpath)
        print(f'[OK] {fname} ({size} bytes)')
    else:
        print(f'[X] {fname} - NOT FOUND')

print("\n" + "=" * 60)
print("[*] 4. Configuration Check...\n")

try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Backend'))
    from config import Config
    print(f'[OK] Environment: {Config.ENVIRONMENT}')
    print(f'[OK] YOLO Model: {Config.YOLO_MODEL}')
    print(f'[OK] Debug: {Config.DEBUG}')
    print(f'[OK] Intersections: {len(Config.INTERSECTIONS)}')
    print(f'[OK] API Port: {Config.API_PORT}')
    print(f'[OK] Vehicle Classes: {len(Config.VEHICLE_CLASSES)}')
    print(f'[OK] Emergency Classes: {len(Config.EMERGENCY_CLASSES)}')
except Exception as e:
    print(f'[X] Config Error: {e}')

print("\n" + "=" * 60)
print("[*] 5. File Structure...\n")

required_files = [
    'Backend/app.py',
    'Backend/config.py',
    'Backend/vehicle_detector.py',
    'Backend/signal_controller.py',
    'Backend/object_tracker.py',
    'Backend/logger.py',
    'Frontend/index.html',
    'Frontend/app.js',
    'Frontend/styles.css',
    'requirements.txt',
    '.env',
    'run_system.py'
]

missing_files = []
for fpath in required_files:
    full_path = os.path.join(os.path.dirname(__file__), fpath)
    if os.path.exists(full_path):
        print(f'[OK] {fpath}')
    else:
        print(f'[X] {fpath} - MISSING')
        missing_files.append(fpath)

print("\n" + "=" * 60)
if missing or not backend_ok or missing_files:
    print("[!] PROJECT STATUS: ISSUES FOUND")
    print("=" * 60)
else:
    print("[OK] PROJECT STATUS: READY TO RUN")
    print("=" * 60)
    print("\nTo start the system:")
    print("   python run_system.py")
    print("\nAccess points:")
    print("   Frontend: http://localhost:8000")
    print("   Backend:  http://localhost:5000")
    print("   API Docs: http://localhost:5000/api/")
