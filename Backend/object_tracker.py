import math
from typing import List, Dict, Tuple
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class TrackedObject:
    id: int
    class_name: str
    center: Tuple[int, int]
    bbox: Tuple[int, int, int, int]
    last_seen: datetime = field(default_factory=datetime.now)
    frames_since_seen: int = 0
    confidence: float = 0.9
    
    def update(self, center: Tuple[int, int], bbox: Tuple[int, int, int, int]) -> None:
        self.center = center
        self.bbox = bbox
        self.last_seen = datetime.now()
        self.frames_since_seen = 0


class ObjectTracker:
    def __init__(self, max_distance: int = 50, max_frames_lost: int = 30):
        self.tracked_objects: Dict[int, TrackedObject] = {}
        self.next_id = 0
        self.max_distance = max_distance
        self.max_frames_lost = max_frames_lost
    
    def calculate_distance(
        self, 
        point1: Tuple[int, int], 
        point2: Tuple[int, int]
    ) -> float:
        """Calculate Euclidean distance between two points."""
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    
    def update(self, detections: List[Dict]) -> List[Dict]:
        """
        Update tracker with new detections.
        
        Args:
            detections: List of detection dicts with keys: 
                       center, bbox, class_name, confidence
        
        Returns:
            List of tracked objects with assigned IDs
        """
        matched_ids = set()
        updated_detections = []
        
        for detection in detections:
            center = detection["center"]
            bbox = detection["bbox"]
            class_name = detection["class_name"]
            confidence = detection.get("confidence", 0.9)
            
            best_match_id = None
            best_distance = self.max_distance
            
            for obj_id, tracked_obj in self.tracked_objects.items():
                if obj_id in matched_ids:
                    continue
                
                distance = self.calculate_distance(center, tracked_obj.center)
                
                if distance < best_distance:
                    best_distance = distance
                    best_match_id = obj_id
            
            if best_match_id is not None:
                self.tracked_objects[best_match_id].update(center, bbox)
                matched_ids.add(best_match_id)
                updated_detections.append({
                    "id": best_match_id,
                    "center": center,
                    "bbox": bbox,
                    "class_name": class_name,
                    "confidence": confidence
                })
            else:
                new_id = self.next_id
                self.next_id += 1
                
                self.tracked_objects[new_id] = TrackedObject(
                    id=new_id,
                    class_name=class_name,
                    center=center,
                    bbox=bbox,
                    confidence=confidence
                )
                matched_ids.add(new_id)
                updated_detections.append({
                    "id": new_id,
                    "center": center,
                    "bbox": bbox,
                    "class_name": class_name,
                    "confidence": confidence
                })
        
        for obj_id in list(self.tracked_objects.keys()):
            if obj_id not in matched_ids:
                self.tracked_objects[obj_id].frames_since_seen += 1
                
                if self.tracked_objects[obj_id].frames_since_seen > self.max_frames_lost:
                    del self.tracked_objects[obj_id]
        
        return updated_detections
    
    def get_active_objects(self) -> List[TrackedObject]:
        """Get list of currently tracked objects."""
        return list(self.tracked_objects.values())
    
    def reset(self) -> None:
        """Reset tracker state."""
        self.tracked_objects.clear()
        self.next_id = 0
