import cv2
import numpy as np
from utils.logger import VaultLogger

class VisionEngine:
    def __init__(self, config):
        self.config = config['vision']
        # Load OpenCV's built-in fast face detector
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def analyze_frame(self, frame, prev_face_roi=None):
        """
        Analyzes a single frame for Quality, Face Count, and Motion (Anti-Static).
        Returns: (is_valid, face_roi, reason)
        """
        # Convert to grayscale for faster processing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 1. Blur Check (Variance of Laplacian)
        blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
        if blur_score < self.config['blur_threshold']:
            return False, None, f"Too blurry (Score: {blur_score:.1f})"

        # 2. Face Detection
        faces = self.face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.1, 
            minNeighbors=5, 
            minSize=(100, 100)
        )
        
        if len(faces) == 0:
            return False, None, "No face detected"
        
        if self.config['strict_single_face'] and len(faces) > 1:
            return False, None, f"Multiple faces ({len(faces)}) detected"

        # Extract face coordinates
        x, y, w, h = faces[0]
        face_area_ratio = (w * h) / (frame.shape[0] * frame.shape[1])
        
        # 3. Proximity Check (Is it a close-up?)
        if face_area_ratio < self.config['min_face_area']:
            return False, None, f"Face too small (Ratio: {face_area_ratio:.3f})"

        # Crop the face for motion tracking
        current_face_roi = gray[y:y+h, x:x+w]

        # 4. The Anti-Static Check (Comparing to previous frame)
        if prev_face_roi is not None:
            # Resize current face to match previous face size exactly
            current_face_resized = cv2.resize(current_face_roi, (prev_face_roi.shape[1], prev_face_roi.shape[0]))
            
            # Calculate pixel differences
            diff = cv2.absdiff(prev_face_roi, current_face_resized)
            motion_score = np.mean(diff)
            
            # If motion score is too low, it's a frozen picture
            if motion_score < self.config['entropy_threshold']:
                return False, current_face_roi, f"Static image detected (Motion: {motion_score:.2f})"

        return True, current_face_roi, "Pass"