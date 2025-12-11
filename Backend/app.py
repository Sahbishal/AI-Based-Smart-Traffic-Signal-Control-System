from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from datetime import datetime
import threading
import cv2
import numpy as np
from io import BytesIO
import time

from config import get_config, Config
from logger import setup_logger
from vehicle_detector import VehicleDetector
from signal_controller import TrafficSignalController
from object_tracker import ObjectTracker


app = Flask(__name__)
CORS(app)

config = get_config()
logger = setup_logger(__name__)

vehicle_detector = VehicleDetector()
signal_controller = TrafficSignalController()
object_tracker = ObjectTracker()

for intersection in config.INTERSECTIONS:
    signal_controller.initialize_intersection(intersection.intersection_id)

simulation_running = False
current_frame = None
current_analysis = None


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "environment": config.ENVIRONMENT
    }), 200


@app.route("/api/intersections", methods=["GET"])
def get_intersections():
    try:
        intersections_data = []
        for intersection in config.INTERSECTIONS:
            intersections_data.append({
                "id": intersection.intersection_id,
                "name": intersection.name,
                "latitude": intersection.latitude,
                "longitude": intersection.longitude,
                "cameras": intersection.camera_urls
            })
        return jsonify(intersections_data), 200
    except Exception as e:
        logger.error(f"Error getting intersections: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/intersection/<intersection_id>/status", methods=["GET"])
def get_intersection_status(intersection_id):
    try:
        status = signal_controller.get_intersection_status(intersection_id)
        if not status:
            return jsonify({"error": "Intersection not found"}), 404
        return jsonify(status), 200
    except Exception as e:
        logger.error(f"Error getting intersection status: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/intersection/<intersection_id>/signal/state", methods=["GET"])
def get_signal_state(intersection_id):
    try:
        state = signal_controller.get_signal_state(intersection_id)
        if not state:
            return jsonify({"error": "Intersection not found"}), 404
        return jsonify({
            "intersection_id": intersection_id,
            "signals": state,
            "timestamp": datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Error getting signal state: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/intersection/<intersection_id>/signal/cycle", methods=["POST"])
def cycle_signal(intersection_id):
    try:
        signals = signal_controller.cycle_signal(intersection_id)
        if not signals:
            return jsonify({"error": "Intersection not found"}), 404
        return jsonify({
            "intersection_id": intersection_id,
            "signals": signals,
            "timestamp": datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Error cycling signal: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/intersection/<intersection_id>/emergency/<direction>", methods=["POST"])
def trigger_emergency(intersection_id, direction):
    try:
        signals = signal_controller.handle_emergency(intersection_id, direction)
        if not signals:
            return jsonify({"error": "Intersection not found"}), 404
        return jsonify({
            "intersection_id": intersection_id,
            "emergency_direction": direction,
            "signals": signals,
            "timestamp": datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Error triggering emergency: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/intersection/<intersection_id>/vehicle-count", methods=["POST"])
def update_vehicle_count(intersection_id):
    try:
        data = request.get_json()
        direction = data.get("direction")
        vehicle_count = data.get("vehicle_count", 0)
        emergency_vehicles = data.get("emergency_vehicles", 0)
        
        if not direction:
            return jsonify({"error": "Direction required"}), 400
        
        signal_controller.update_vehicle_counts(
            intersection_id, 
            direction, 
            vehicle_count, 
            emergency_vehicles
        )
        
        return jsonify({
            "status": "updated",
            "intersection_id": intersection_id,
            "direction": direction,
            "vehicle_count": vehicle_count,
            "timestamp": datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Error updating vehicle count: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/video/process", methods=["POST"])
def process_video():
    try:
        if "video" not in request.files:
            return jsonify({"error": "No video file provided"}), 400
        
        video_file = request.files["video"]
        intersection_id = request.form.get("intersection_id", "INT_001")
        direction = request.form.get("direction", "north")
        
        stream = BytesIO(video_file.read())
        nparr = np.frombuffer(stream.getvalue(), np.uint8)
        
        cap = cv2.VideoCapture()
        retval = cap.open(cv2.CAP_FFMPEG)
        
        success, frame = cap.read()
        cap.release()
        
        if not success:
            return jsonify({"error": "Failed to read video"}), 400
        
        analysis = vehicle_detector.detect_vehicles(frame)
        
        signal_controller.update_vehicle_counts(
            intersection_id,
            direction,
            analysis.total_vehicles,
            analysis.emergency_vehicles
        )
        
        return jsonify({
            "intersection_id": intersection_id,
            "direction": direction,
            "total_vehicles": analysis.total_vehicles,
            "vehicle_breakdown": analysis.vehicle_breakdown,
            "emergency_vehicles": analysis.emergency_vehicles,
            "emergency_types": analysis.emergency_types,
            "timestamp": datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Error processing video: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/detection/image", methods=["POST"])
def detect_from_image():
    try:
        if "image" not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        image_file = request.files["image"]
        intersection_id = request.form.get("intersection_id", "INT_001")
        direction = request.form.get("direction", "north")
        
        nparr = np.frombuffer(image_file.read(), np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            return jsonify({"error": "Invalid image file"}), 400
        
        analysis = vehicle_detector.detect_vehicles(frame)
        
        signal_controller.update_vehicle_counts(
            intersection_id,
            direction,
            analysis.total_vehicles,
            analysis.emergency_vehicles
        )
        
        return jsonify({
            "intersection_id": intersection_id,
            "direction": direction,
            "total_vehicles": analysis.total_vehicles,
            "vehicle_breakdown": analysis.vehicle_breakdown,
            "emergency_vehicles": analysis.emergency_vehicles,
            "emergency_types": analysis.emergency_types,
            "detections": [
                {
                    "class": d.class_name,
                    "confidence": d.confidence,
                    "bbox": d.bbox,
                    "is_emergency": d.is_emergency
                }
                for d in analysis.detections
            ],
            "timestamp": datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Error detecting from image: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/detection/visualization", methods=["POST"])
def get_detection_visualization():
    try:
        if "image" not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        image_file = request.files["image"]
        nparr = np.frombuffer(image_file.read(), np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            return jsonify({"error": "Invalid image file"}), 400
        
        analysis = vehicle_detector.detect_vehicles(frame)
        output_frame = vehicle_detector.draw_detections(frame, analysis)
        
        _, buffer = cv2.imencode('.png', output_frame)
        img_io = BytesIO(buffer)
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/png')
    except Exception as e:
        logger.error(f"Error generating visualization: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/tracker/state", methods=["GET"])
def get_tracker_state():
    try:
        active_objects = object_tracker.get_active_objects()
        return jsonify({
            "active_objects": len(active_objects),
            "objects": [
                {
                    "id": obj.id,
                    "class": obj.class_name,
                    "center": obj.center,
                    "confidence": obj.confidence
                }
                for obj in active_objects
            ],
            "timestamp": datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Error getting tracker state: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/tracker/reset", methods=["POST"])
def reset_tracker():
    try:
        object_tracker.reset()
        return jsonify({
            "status": "tracker reset",
            "timestamp": datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Error resetting tracker: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/stats/overview", methods=["GET"])
def get_stats_overview():
    try:
        stats = {
            "intersections": len(config.INTERSECTIONS),
            "intersection_statuses": []
        }
        
        for intersection in config.INTERSECTIONS:
            status = signal_controller.get_intersection_status(intersection.intersection_id)
            stats["intersection_statuses"].append(status)
        
        stats["timestamp"] = datetime.now().isoformat()
        return jsonify(stats), 200
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        return jsonify({"error": str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    logger.info(f"Starting Traffic Management System API - {config.ENVIRONMENT} mode")
    app.run(
        host=config.API_HOST,
        port=config.API_PORT,
        debug=config.DEBUG
    )
