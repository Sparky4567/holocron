import subprocess
import sounddevice as sd
import numpy as np

class Speaking_Module:
    def __init__(self, MODEL):
        self.model = MODEL

    def speak(self, text):
        try:
            proc = subprocess.Popen(
                ["piper", "--model", self.model, "--output_raw"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                bufsize=0
            )
            audio_bytes, _ = proc.communicate(input=text.encode("utf-8"))
            audio_np = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
            sd.play(audio_np, samplerate=18000)
            sd.wait()
        except Exception as e:
            print(e)