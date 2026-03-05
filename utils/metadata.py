import json
import os
from utils.logger import VaultLogger

class MetadataVault:
    @staticmethod
    def generate_sidecar(clip_filename, original_url, timestamp, motion_score, blur_score):
        """
        Creates a JSON file with the exact same name as the video clip,
        storing all the AI scores and source data.
        """
        # Change file extension from .mp4 to .json
        json_filename = os.path.splitext(clip_filename)[0] + '.json'
        
        data = {
            "source_url": original_url,
            "extracted_at_second": timestamp,
            "quality_metrics": {
                "motion_entropy": round(motion_score, 2) if motion_score else None,
                "blur_score": round(blur_score, 2) if blur_score else None,
                "speech_detected": True
            },
            "engine_version": "VisionVault 1.0"
        }
        
        try:
            with open(json_filename, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            VaultLogger.error(f"Could not write metadata for {clip_filename}: {str(e)}")
            return False