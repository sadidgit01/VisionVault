import argparse
import os
import yaml
import cv2
import subprocess
from core.downloader import Downloader
from core.processor import VisionEngine
from core.audio_engine import AudioEngine
from utils.metadata import MetadataVault
from utils.logger import VaultLogger

def load_config():
    with open("config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def extract_audio_chunk(video_path):
    """Extracts audio to a temporary WAV file for the AudioEngine to analyze."""
    temp_audio = "temp_audio.wav"
    command = [
        "ffmpeg", "-y", "-i", video_path, 
        "-vn", "-acodec", "pcm_s16le", "-ar", "32000", "-ac", "1", 
        temp_audio
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return temp_audio

def extract_clip(input_vid, start_time, duration, output_path):
    command = [
        "ffmpeg", "-y", "-ss", str(start_time), "-t", str(duration), 
        "-i", input_vid, "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
        "-c:a", "aac", "-b:a", "128k", output_path
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def process_video(video_path, url, config, vision, audio):
    VaultLogger.info(f"Processing: {os.path.basename(video_path)}")
    
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps
    
    current_time = config['timing']['intro_skip']
    clips_saved = 0
    prev_face = None

    # THE PROGRESS BAR START
    while current_time < (duration - config['timing']['end_skip']):
        # Update the UI
        VaultLogger.progress(current_time, duration, label="Mining")
        
        cap.set(cv2.CAP_PROP_POS_MSEC, current_time * 1000)
        ret, frame = cap.read()
        if not ret: break

        # Vision Check
        is_valid, face_roi, reason = vision.analyze_frame(frame, prev_face)
        prev_face = face_roi

        if is_valid:
            # We found a face! Now slice and save.
            clip_filename = f"Vault_{int(current_time)}.mp4"
            clip_path = os.path.join(config['paths']['clips_dir'], clip_filename)
            
            extract_clip(video_path, current_time, config['timing']['clip_duration'], clip_path)
            MetadataVault.generate_sidecar(clip_path, url, current_time, 0.9, 100)
            clips_saved += 1
            current_time += config['timing']['clip_duration']
        else:
            current_time += 1.0

    cap.release()
    print("\n") # Break the progress bar line
    VaultLogger.success(f"Extracted {clips_saved} clips. Cleaning up raw files...")
    
    # THE CLEANUP: Delete the big raw video to save space
    if os.path.exists(video_path):
        os.remove(video_path)
        VaultLogger.info("Raw video deleted.")

def main():
    parser = argparse.ArgumentParser(description="VisionVault Pro")
    parser.add_argument("--url", required=True)
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--batch", type=int, default=1)
    parser.add_argument("--res", default="1080") # Set default to 1080p

    args = parser.parse_args()
    config = load_config()

    downloader = Downloader(config, args.res)
    vision = VisionEngine(config)
    audio = AudioEngine(config['audio'])

    is_playlist, title = downloader.get_info(args.url)
    
    if not is_playlist:
        path = downloader.download(args.url)
        if path: process_video(path, args.url, config, vision, audio)
    else:
        for i in range(args.start, args.start + args.batch):
            path = downloader.download(args.url, index=i)
            if path: process_video(path, args.url, config, vision, audio)

if __name__ == "__main__":
    main()