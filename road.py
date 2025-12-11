import database
import numpy as np
import time
import detection


class Road:
    def __init__(self, name, initial_count, max_capacity, cycle_time, arrival_rate, file_path=None):
        """
        Create a Road object and store its initial info into the database.
        Green time is computed based on traffic load.
        """
        self.next = Road  # Placeholder for linking road nodes (optional)
        
        # Compute first green signal duration proportional to traffic load
        initial_green = (initial_count / max_capacity) * cycle_time

        # Insert this road into the database
        self.id = database.add_road(
            name,
            initial_green,
            initial_count,
            max_capacity,
            cycle_time,
            False,
            file_path
        )

        self.arrival_rate = arrival_rate
        self.is_green = False
        self.emergency_start_time = None

    # ---- Basic Getters ----
    def get_vehicle_count(self):
        return database.get_vehicle_count(self.id)

    def get_name(self):
        return database.get_name(self.id)

    def get_green_time(self):
        return database.get_green_time(self.id)

    def has_emergency_vehicle(self):
        return database.get_hasEmergencyVehicle(self.id)

    # ---- Signal Light Controllers ----
    def set_red(self):
        self.is_green = False

    def set_green(self):
        self.is_green = True

    # ---- Automatic Updating System ----
    def update(self):
        """
        Refresh the traffic state on this road:
        - Modify vehicle count depending on the signal
        - Adjust green duration
        - Randomly simulate emergency vehicles
        """
        count = database.get_vehicle_count(self.id)
        capacity = database.get_capacity(self.id)
        cycle_time = database.get_total_time(self.id)

        # Traffic movement simulation
        if self.is_green:
            # Vehicles moving out (random efficiency factor)
            discharge = int((capacity / 3600) * (1 + np.random.uniform(-0.1, 0.1)))
            count -= discharge
        else:
            # Vehicles arriving (random arrival rate)
            arrival = int(self.arrival_rate * (1 + np.random.uniform(-0.2, 0.2)))
            count += arrival

        # Update count in database
        database.update_vehicle_count(self.id, count)

        # Recompute green time based on congestion
        new_green = (count / capacity) * cycle_time
        database.update_green_time(self.id, new_green)

        # Random emergency simulation
        if np.random.rand() < 0.005 and self.emergency_start_time is None:
            print(f"⚠️ Emergency vehicle detected on {self.get_name()}.")
            database.update_hasEmergencyVehicle(self.id, True)
            self.emergency_start_time = time.time()

        # Clear emergency signal after 5 seconds
        if self.emergency_start_time:
            if time.time() - self.emergency_start_time > 5:
                print(f"✅ Emergency vehicle cleared on {self.get_name()}.")
                database.update_hasEmergencyVehicle(self.id, False)
                self.emergency_start_time = None

    # ---- Camera-Based Real-Time Update ----
    def cam_update(self):
        """
        Use live camera input to update vehicle count and emergency status.
        """
        file_path = database.get_file_path(self.id)
        count, emergency_detected = detection.get_vehicle_condition(file_path)

        database.update_vehicle_count(self.id, count)
        database.update_hasEmergencyVehicle(self.id, emergency_detected)
