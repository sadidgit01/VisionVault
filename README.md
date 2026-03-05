# VisionVault

## AI-Driven Media Mining and Dataset Extraction

VisionVault is a command-line utility designed for the automated extraction of high-quality video segments from YouTube.
The system integrates Computer Vision techniques and Voice Activity Detection (VAD) to filter low-quality data, static imagery, and non-vocal audio. The resulting output is optimized for machine learning datasets or structured media archival.

---

## Prerequisites

Before deployment, ensure the following software is installed:

- **Python 3.10 or higher** – primary runtime environment
- **FFmpeg** – required for video codec operations and audio stream processing

The `ffmpeg` executable must be available in the system `PATH`.

---

## Installation

Initialize the project environment and install dependencies using the following commands:

```bash
git clone https://github.com/sadidgit01/VisionVault
cd VisionVault

python -m venv .venv

# Windows
.\.venv\Scripts\activate

pip install -r requirements.txt
```

---

## Operation

VisionVault contains an automated URL detection mechanism that determines whether the provided link corresponds to:

- a single video
- a playlist

The internal processing pipeline adjusts accordingly.

### Basic Execution

```bash
python app.py --url "YOUR_YOUTUBE_LINK_HERE"
```

---

## Command Line Arguments

| Argument  | Description                                             | Default |
| --------- | ------------------------------------------------------- | ------- |
| `--url`   | YouTube video or playlist URL (required)                | —       |
| `--res`   | Target resolution (720, 1080, 1440, 2160)               | 1080    |
| `--batch` | Number of videos to process when a playlist is detected | 1       |
| `--start` | Starting index within the playlist                      | 1       |

---

## Usage Examples

### Process a single video

```bash
python app.py --url "https://www.youtube.com/watch?v=example_YOUR_YOUTUBE_LINK"
```

### Process a playlist

```bash
python app.py --url "https://www.youtube.com/playlist?list=example_YOUR_YOUTUBE_LINK" --res 2160 --start 5 --batch 10
```

---

## Core Features

### Motion-Entropy Filtering

The system analyzes pixel variance across sequential frames to identify static images or slideshow-style segments. Only dynamic video content is retained.

### Face Detection Constraint

Using OpenCV, VisionVault enforces subject validation to ensure a single human face is present and centrally positioned before extraction.

### Voice Activity Detection

The pipeline integrates Google WebRTC VAD to detect human speech frequencies and discard segments containing only background noise or silence.

### Storage Optimization

To prevent unnecessary disk usage, the original high-volume source video is automatically removed once the relevant clips are successfully extracted.

---

## Use Cases

VisionVault is intended for generating structured datasets suitable for:

- machine learning model training
- speech analysis datasets
- video analytics research
- curated media archives

---

## License

This project is distributed under the MIT License.
