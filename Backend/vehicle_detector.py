import cv2
import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from ultralytics import YOLO
from config import Config
from logger import setup_logger


logger = setup_logger(__name__)


@dataclass
class Detection:
    class_id: int
    class_name: str
    confidence: float
    bbox: Tuple[int, int, int, int]
    center: Tuple[int, int]
    is_emergency: bool


@dataclass
class FrameAnalysis:
    total_vehicles: int
    vehicle_breakdown: Dict[str, int]
    emergency_vehicles: int
    emergency_types: List[str]
    detections: List[Detection]
    frame_timestamp: float


class VehicleDetector:
    def __init__(self, model_name: str = Config.YOLO_MODEL):
        try:
            self.model = YOLO(model_name)
            logger.info(f"Loaded YOLO model: {model_name}")
        except Exception as e:
            logger.error(f"Failed to load YOLO model: {e}")
            raise
        
        self.confidence_threshold = Config.CONFIDENCE_THRESHOLD
        self.vehicle_classes = set(Config.VEHICLE_CLASSES)
        self.emergency_classes = set(Config.EMERGENCY_CLASSES)
    
    def detect_vehicles(self, frame: np.ndarray) -> FrameAnalysis:
        """
        Detect vehicles in a frame using YOLO.
        
        Args:
            frame: Input video frame
            
        Returns:
            FrameAnalysis object with detection results
        """
        if frame is None or frame.size == 0:
            logger.warning("Invalid frame received")
            return self._empty_analysis()
        
        try:
            results = self.model(frame, conf=self.confidence_threshold, verbose=False)
            
            detections = []
            vehicle_breakdown = {class_name: 0 for class_name in self.vehicle_classes}
            emergency_types = []
            emergency_count = 0
            
            for result in results:
                if result.boxes is None:
                    continue
                
                for box in result.boxes:
                    class_id = int(box.cls[0])
                    class_name = self.model.names[class_id]
                    confidence = float(box.conf[0])
                    
                    x1, y1, x2, y2 = box.xyxy[0]
                    bbox = (int(x1), int(y1), int(x2), int(y2))
                    center = (
                        (int(x1) + int(x2)) // 2,
                        (int(y1) + int(y2)) // 2
                    )
                    
                    is_emergency = class_name in self.emergency_classes
                    
                    detection = Detection(
                        class_id=class_id,
                        class_name=class_name,
                        confidence=confidence,
                        bbox=bbox,
                        center=center,
                        is_emergency=is_emergency
                    )
                    detections.append(detection)
                    
                    if is_emergency:
                        emergency_count += 1
                        emergency_types.append(class_name)
                    elif class_name in self.vehicle_classes:
                        vehicle_breakdown[class_name] += 1
            
            total_vehicles = sum(vehicle_breakdown.values())
            
            analysis = FrameAnalysis(
                total_vehicles=total_vehicles,
                vehicle_breakdown=vehicle_breakdown,
                emergency_vehicles=emergency_count,
                emergency_types=list(set(emergency_types)),
                detections=detections,
                frame_timestamp=cv2.getTickCount() / cv2.getTickFrequency()
            )
            
            return analysis
        
        except Exception as e:
            logger.error(f"Error during vehicle detection: {e}")
            return self._empty_analysis()
    
    def _empty_analysis(self) -> FrameAnalysis:
        return FrameAnalysis(
            total_vehicles=0,
            vehicle_breakdown={class_name: 0 for class_name in self.vehicle_classes},
            emergency_vehicles=0,
            emergency_types=[],
            detections=[],
            frame_timestamp=cv2.getTickCount() / cv2.getTickFrequency()
        )
    
    def draw_detections(
        self, 
        frame: np.ndarray, 
        analysis: FrameAnalysis,
        draw_labels: bool = True
    ) -> np.ndarray:
        """
        Draw bounding boxes and labels on the frame.
        
        Args:
            frame: Input frame
            analysis: FrameAnalysis object with detections
            draw_labels: Whether to draw class labels
            
        Returns:
            Frame with drawn detections
        """
        output_frame = frame.copy()
        
        for detection in analysis.detections:
            x1, y1, x2, y2 = detection.bbox
            
            color = (0, 0, 255) if detection.is_emergency else (0, 255, 0)
            thickness = 3 if detection.is_emergency else 2
            
            cv2.rectangle(output_frame, (x1, y1), (x2, y2), color, thickness)
            
            if draw_labels:
                label = f"{detection.class_name}: {detection.confidence:.2f}"
                label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
                
                cv2.rectangle(
                    output_frame,
                    (x1, y1 - label_size[1] - 4),
                    (x1 + label_size[0], y1),
                    color,
                    -1
                )
                cv2.putText(
                    output_frame,
                    label,
                    (x1, y1 - 2),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    1
                )
        
        return output_frame
