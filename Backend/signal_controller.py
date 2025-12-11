import time
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from config import TrafficLightState, SignalTiming, Config
from logger import setup_logger


logger = setup_logger(__name__)


@dataclass
class SignalState:
    direction: str
    current_state: TrafficLightState
    duration: int
    elapsed_time: int = 0
    changed_at: datetime = field(default_factory=datetime.now)
    
    def is_expired(self) -> bool:
        elapsed = (datetime.now() - self.changed_at).total_seconds()
        return elapsed >= self.duration


@dataclass
class IntersectionState:
    intersection_id: str
    signals: Dict[str, SignalState]
    last_vehicle_counts: Dict[str, int] = field(default_factory=dict)
    has_emergency: bool = False
    optimization_enabled: bool = True


class TrafficSignalController:
    def __init__(self, signal_timing: SignalTiming = None):
        self.signal_timing = signal_timing or SignalTiming()
        self.intersections: Dict[str, IntersectionState] = {}
        self.emergency_mode = False
        logger.info("Traffic Signal Controller initialized")
    
    def initialize_intersection(
        self, 
        intersection_id: str, 
        directions: List[str] = None
    ) -> None:
        """Initialize signals for an intersection."""
        if directions is None:
            directions = ["north", "south", "east", "west"]
        
        signals = {}
        for i, direction in enumerate(directions):
            state = TrafficLightState.RED if i > 0 else TrafficLightState.GREEN
            signals[direction] = SignalState(
                direction=direction,
                current_state=state,
                duration=self.signal_timing.min_duration
            )
        
        self.intersections[intersection_id] = IntersectionState(
            intersection_id=intersection_id,
            signals=signals
        )
        logger.info(f"Initialized intersection {intersection_id} with {len(directions)} directions")
    
    def update_vehicle_counts(
        self, 
        intersection_id: str, 
        direction: str, 
        vehicle_count: int,
        emergency_vehicles: int = 0
    ) -> None:
        """Update vehicle counts for a specific direction."""
        if intersection_id not in self.intersections:
            logger.warning(f"Intersection {intersection_id} not initialized")
            return
        
        intersection = self.intersections[intersection_id]
        intersection.last_vehicle_counts[direction] = vehicle_count
        
        if emergency_vehicles > 0:
            intersection.has_emergency = True
            logger.warning(f"Emergency vehicle detected at {intersection_id} - {direction}")
    
    def optimize_signal_duration(
        self, 
        intersection_id: str, 
        direction: str, 
        vehicle_count: int
    ) -> int:
        """
        Calculate optimized signal duration based on vehicle count.
        
        Args:
            intersection_id: ID of the intersection
            direction: Direction of the signal
            vehicle_count: Number of vehicles detected
            
        Returns:
            Optimized duration in seconds
        """
        min_time = self.signal_timing.min_duration
        max_time = self.signal_timing.max_duration
        
        if vehicle_count == 0:
            return min_time
        
        density = min(vehicle_count / 50, 1.0)
        duration = min_time + int((max_time - min_time) * density)
        
        return duration
    
    def cycle_signal(self, intersection_id: str) -> Dict[str, TrafficLightState]:
        """
        Cycle traffic signals to the next state.
        
        Returns:
            Dictionary with current signal states
        """
        if intersection_id not in self.intersections:
            logger.warning(f"Intersection {intersection_id} not found")
            return {}
        
        intersection = self.intersections[intersection_id]
        directions = list(intersection.signals.keys())
        
        current_green_direction = None
        for direction, signal in intersection.signals.items():
            if signal.current_state == TrafficLightState.GREEN:
                current_green_direction = direction
                break
        
        if current_green_direction is None:
            directions[0]
        
        if current_green_direction and signal.is_expired():
            next_index = (directions.index(current_green_direction) + 1) % len(directions)
            
            intersection.signals[current_green_direction].current_state = TrafficLightState.RED
            
            for direction in directions:
                if direction != current_green_direction:
                    intersection.signals[direction].current_state = TrafficLightState.RED
            
            next_direction = directions[next_index]
            next_signal = intersection.signals[next_direction]
            next_signal.current_state = TrafficLightState.GREEN
            next_signal.changed_at = datetime.now()
            
            if intersection.optimization_enabled:
                vehicle_count = intersection.last_vehicle_counts.get(next_direction, 0)
                next_signal.duration = self.optimize_signal_duration(
                    intersection_id, 
                    next_direction, 
                    vehicle_count
                )
            
            logger.info(
                f"Signal cycled at {intersection_id}: "
                f"{current_green_direction} -> {next_direction} (duration: {next_signal.duration}s)"
            )
        
        return {
            direction: signal.current_state.value 
            for direction, signal in intersection.signals.items()
        }
    
    def handle_emergency(self, intersection_id: str, direction: str) -> Dict[str, str]:
        """
        Handle emergency vehicle by giving it priority.
        
        Args:
            intersection_id: ID of the intersection
            direction: Direction of emergency vehicle
            
        Returns:
            Updated signal states
        """
        if intersection_id not in self.intersections:
            logger.warning(f"Intersection {intersection_id} not found")
            return {}
        
        intersection = self.intersections[intersection_id]
        
        for direction_key, signal in intersection.signals.items():
            signal.current_state = TrafficLightState.RED if direction_key != direction else TrafficLightState.GREEN
            signal.changed_at = datetime.now()
            signal.duration = 30
        
        logger.warning(f"Emergency mode activated at {intersection_id} for direction {direction}")
        
        return {
            direction: signal.current_state.value 
            for direction, signal in intersection.signals.items()
        }
    
    def reset_emergency(self, intersection_id: str) -> None:
        """Reset emergency mode."""
        if intersection_id in self.intersections:
            self.intersections[intersection_id].has_emergency = False
            logger.info(f"Emergency mode reset for {intersection_id}")
    
    def get_signal_state(self, intersection_id: str) -> Dict[str, str]:
        """Get current signal states for an intersection."""
        if intersection_id not in self.intersections:
            return {}
        
        intersection = self.intersections[intersection_id]
        return {
            direction: signal.current_state.value 
            for direction, signal in intersection.signals.items()
        }
    
    def get_intersection_status(self, intersection_id: str) -> Dict:
        """Get comprehensive status of an intersection."""
        if intersection_id not in self.intersections:
            return {}
        
        intersection = self.intersections[intersection_id]
        
        return {
            "intersection_id": intersection_id,
            "signal_states": self.get_signal_state(intersection_id),
            "vehicle_counts": intersection.last_vehicle_counts,
            "emergency_mode": intersection.has_emergency,
            "optimization_enabled": intersection.optimization_enabled,
            "timestamp": datetime.now().isoformat()
        }
