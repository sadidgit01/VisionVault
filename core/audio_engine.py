import webrtcvad
from utils.logger import VaultLogger

class AudioEngine:
    def __init__(self, config):
        self.sample_rate = config['sample_rate']
        self.vad = webrtcvad.Vad()
        # Mode 3 is the most aggressive/strict for filtering out non-speech
        self.vad.set_mode(config['vad_mode'])

    def is_human_speaking(self, audio_frame):
        """
        Listens to a tiny slice of audio (usually 30 milliseconds).
        Returns True if human speech is detected, False otherwise.
        audio_frame must be 16-bit mono PCM format.
        """
        try:
            return self.vad.is_speech(audio_frame, self.sample_rate)
        except Exception as e:
            VaultLogger.error(f"Audio processing error: {str(e)}")
            return False