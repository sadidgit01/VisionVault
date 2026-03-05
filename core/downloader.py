import yt_dlp
import os
from utils.logger import VaultLogger

class Downloader:
    def __init__(self, config, resolution="720"):
        self.config = config
        self.res = resolution

    def get_info(self, url):
        """Checks if the URL is a playlist or a single video."""
        ydl_opts = {'quiet': True, 'noplaylist': True, 'extract_flat': True}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                is_playlist = 'entries' in info
                return is_playlist, info.get('title', 'Unknown')
        except Exception as e:
            VaultLogger.error(f"Failed to fetch URL info: {str(e)}")
            return False, "Error"

    def download(self, url, index=None):
        """Downloads a specific video from a URL or playlist index."""
        output_template = os.path.join(self.config['paths']['raw_dir'], 'vid_%(id)s.%(ext)s')
        
        ydl_opts = {
            'format': f'bestvideo[height<={self.res}][ext=mp4]+bestaudio[ext=m4a]/best[height<={self.res}][ext=mp4]',
            'outtmpl': output_template,
            'quiet': True,
            'no_warnings': True,
        }

        if index:
            ydl_opts['playlist_items'] = str(index)
            VaultLogger.info(f"Fetching item #{index} from playlist...")
        else:
            VaultLogger.info(f"Fetching single video...")

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                # Handle playlist vs single video return structure
                if 'entries' in info:
                    video_data = info['entries'][0]
                else:
                    video_data = info
                
                filename = ydl.prepare_filename(video_data)
                VaultLogger.success(f"Downloaded: {os.path.basename(filename)}")
                return filename
        except Exception as e:
            VaultLogger.error(f"Download failed: {str(e)}")
            return None