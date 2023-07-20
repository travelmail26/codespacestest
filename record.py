import sounddevice as sd
import numpy as np
import webbrowser
import time

# Set the URL to the desired web page
url = "https://www.example.com"

# Open the URL in a new Chrome browser window
webbrowser.get("google-chrome").open(url)

# Wait for the web page to load
time.sleep(5)  # Adjust the delay as needed

# Get the default output device index
default_output_device = sd.default.device[0]

# Set the input device to the VB-Audio Virtual Cable output
input_device = "CABLE Input (VB-Audio Virtual Cable)"

# Set the desired sample rate and duration for recording
sample_rate = 44100
duration = 10  # seconds

# Start recording audio from the specified input device
recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype=np.float32, device=(input_device, default_output_device))
sd.wait()

# Save the recorded audio to a WAV file
output_file = "output.wav"
sd.write(output_file, recording, sample_rate)

print("Audio recording complete. Saved to:", output_file)
