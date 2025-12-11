import os
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple


class TrafficLightState(Enum):
    RED = "red"
    YELLOW = "yellow"
    GREEN = "green"


@dataclass
class SignalTiming:
    min_duration: int = 10
    max_duration: int = 60
    yellow_duration: int = 3


@dataclass
class IntersectionConfig:
    intersection_id: str
    name: str
    latitude: float
    longitude: float
    camera_urls: dict
    signal_timings: SignalTiming = None
    
    def __post_init__(self):
        if self.signal_timings is None:
            self.signal_timings = SignalTiming()


class Config:
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    DEBUG = ENVIRONMENT == "development"
    
    YOLO_MODEL = "yolo11n.pt"
    CONFIDENCE_THRESHOLD = 0.5
    
    VEHICLE_CLASSES = ["car", "truck", "bus", "motorcycle", "bicycle"]
    EMERGENCY_CLASSES = ["ambulance", "fire_truck", "police"]
    
    MAX_TRACKING_DISTANCE = 50
    
    SIGNAL_MIN_TIME = 10
    SIGNAL_MAX_TIME = 60
    SIGNAL_YELLOW_TIME = 3
    
    DB_URL = os.getenv("DATABASE_URL", "sqlite:///traffic.db")
    
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", 5000))
    
    INTERSECTIONS: List[IntersectionConfig] = [
        IntersectionConfig(
            intersection_id="INT_001",
            name="Main Street & 5th Avenue",
            latitude=40.7128,
            longitude=-74.0060,
            camera_urls={
                "north": "0",
                "south": "1",
                "east": "2",
                "west": "3"
            }
        ),
    ]
    
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "traffic_system.log")


class DevelopmentConfig(Config):
    DEBUG = True
    YOLO_MODEL = "yolo11n.pt"


class ProductionConfig(Config):
    DEBUG = False
    YOLO_MODEL = "yolo11.pt"


def get_config():
    config_map = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
    }
    return config_map.get(Config.ENVIRONMENT, DevelopmentConfig)()
