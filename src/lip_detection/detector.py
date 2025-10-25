"""
Lip Movement Detector using Computer Vision
Uses MediaPipe and OpenCV for real-time lip tracking and movement analysis
"""

import cv2
import numpy as np
try:
    import mediapipe as mp
except ImportError:
    print("Warning: MediaPipe not installed. Install with: pip install mediapipe")
    mp = None


class LipDetector:
    """
    Real-time lip movement detector using facial landmarks
    """
    
    def __init__(self, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        """
        Initialize the lip detector
        
        Args:
            min_detection_confidence: Minimum confidence for face detection
            min_tracking_confidence: Minimum confidence for face tracking
        """
        if mp is None:
            raise ImportError("MediaPipe is required for lip detection")
            
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        
        # Lip landmark indices (MediaPipe Face Mesh)
        self.UPPER_LIP_INDICES = [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291]
        self.LOWER_LIP_INDICES = [146, 91, 181, 84, 17, 314, 405, 321, 375, 291]
        self.LIP_INDICES = self.UPPER_LIP_INDICES + self.LOWER_LIP_INDICES
        
        self.previous_lip_distance = None
        self.movement_history = []
        self.max_history = 30  # frames
        
    def detect_lip_landmarks(self, frame):
        """
        Detect facial landmarks and extract lip positions
        
        Args:
            frame: RGB image frame
            
        Returns:
            lip_landmarks: List of (x, y) coordinates for lip landmarks
            annotated_frame: Frame with landmarks drawn
        """
        # Convert BGR to RGB if needed
        if len(frame.shape) == 3 and frame.shape[2] == 3:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        else:
            rgb_frame = frame
            
        results = self.face_mesh.process(rgb_frame)
        
        lip_landmarks = []
        annotated_frame = frame.copy()
        
        if results.multi_face_landmarks:
            face_landmarks = results.multi_face_landmarks[0]
            
            # Extract lip landmarks
            h, w = frame.shape[:2]
            for idx in self.LIP_INDICES:
                landmark = face_landmarks.landmark[idx]
                x = int(landmark.x * w)
                y = int(landmark.y * h)
                lip_landmarks.append((x, y))
                
                # Draw landmark on frame
                cv2.circle(annotated_frame, (x, y), 2, (0, 255, 0), -1)
            
            # Draw lip contour
            if len(lip_landmarks) > 0:
                pts = np.array(lip_landmarks, np.int32)
                cv2.polylines(annotated_frame, [pts], True, (0, 255, 255), 2)
        
        return lip_landmarks, annotated_frame
    
    def calculate_lip_distance(self, lip_landmarks):
        """
        Calculate the vertical distance between upper and lower lips
        
        Args:
            lip_landmarks: List of (x, y) lip coordinates
            
        Returns:
            distance: Vertical lip distance (mouth openness)
        """
        if len(lip_landmarks) < len(self.LIP_INDICES):
            return 0.0
            
        # Calculate center points of upper and lower lips
        upper_lip_y = np.mean([lip_landmarks[i][1] for i in range(len(self.UPPER_LIP_INDICES))])
        lower_lip_y = np.mean([lip_landmarks[i][1] for i in range(len(self.UPPER_LIP_INDICES), len(lip_landmarks))])
        
        distance = abs(lower_lip_y - upper_lip_y)
        return distance
    
    def detect_movement(self, frame):
        """
        Detect lip movement in the current frame
        
        Args:
            frame: Input video frame
            
        Returns:
            movement_detected: Boolean indicating if significant movement detected
            movement_magnitude: Float indicating strength of movement
            annotated_frame: Frame with visualization
        """
        lip_landmarks, annotated_frame = self.detect_lip_landmarks(frame)
        
        if len(lip_landmarks) == 0:
            return False, 0.0, annotated_frame
        
        current_distance = self.calculate_lip_distance(lip_landmarks)
        
        movement_detected = False
        movement_magnitude = 0.0
        
        if self.previous_lip_distance is not None:
            movement_magnitude = abs(current_distance - self.previous_lip_distance)
            
            # Threshold for detecting significant movement
            if movement_magnitude > 2.0:  # Adjustable threshold
                movement_detected = True
        
        self.previous_lip_distance = current_distance
        self.movement_history.append(movement_magnitude)
        
        # Keep only recent history
        if len(self.movement_history) > self.max_history:
            self.movement_history.pop(0)
        
        # Add movement info to frame
        cv2.putText(annotated_frame, f"Movement: {movement_magnitude:.2f}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(annotated_frame, f"Detected: {movement_detected}", 
                   (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        return movement_detected, movement_magnitude, annotated_frame
    
    def get_movement_pattern(self):
        """
        Get recent movement pattern for analysis
        
        Returns:
            pattern: List of recent movement magnitudes
        """
        return self.movement_history.copy()
    
    def reset(self):
        """Reset detector state"""
        self.previous_lip_distance = None
        self.movement_history = []
    
    def close(self):
        """Clean up resources"""
        if hasattr(self, 'face_mesh'):
            self.face_mesh.close()
