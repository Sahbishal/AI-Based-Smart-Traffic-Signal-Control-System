import math


class ObjectTracker:
    """
    ObjectTracker class is used to track multiple moving objects
    based on their center coordinates across frames.
    """

    def __init__(self):
        # Dictionary to hold object IDs and their center points
        self.tracked_objects = {}
        # Counter for assigning unique IDs to new objects
        self.next_id = 0

    def update(self, detections):
        """
        Updates the tracker with a list of detected object rectangles.

        Args:
            detections (list): List of bounding boxes in format [x, y, w, h]

        Returns:
            list: Updated list of bounding boxes with assigned IDs
        """
        updated_objects = []

        for (x, y, w, h) in detections:
            # Calculate center of the current detection
            center_x = x + w // 2
            center_y = y + h // 2

            # Assume this is a new object
            assigned_id = None

            # Compare with existing tracked objects to check if it's the same
            for obj_id, (prev_x, prev_y) in self.tracked_objects.items():
                distance = math.hypot(center_x - prev_x, center_y - prev_y)

                # If the object is close to a previous center, it's the same object
                if distance < 35:
                    self.tracked_objects[obj_id] = (center_x, center_y)
                    updated_objects.append([x, y, w, h, obj_id])
                    assigned_id = obj_id
                    break

            # If the object was not matched with any existing one, assign a new ID
            if assigned_id is None:
                self.tracked_objects[self.next_id] = (center_x, center_y)
                updated_objects.append([x, y, w, h, self.next_id])
                self.next_id += 1

        # Keep only active (recently updated) objects
        active_objects = {obj_id: self.tracked_objects[obj_id] for _, _, _, _, obj_id in updated_objects}
        self.tracked_objects = active_objects

        return updated_objects
