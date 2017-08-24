import os
import subprocess
import wave
import struct
import csv
import sys
import numpy as np
import matplotlib.pyplot as plt

const_time_skip = 12500
const_time = 250

def read_wav(wav_file):
    """Returns two chunks of sound data from wave file."""
    w = wave.open(wav_file)
    frames = w.readframes(const_time_skip)
    wav_data_skip = np.fromstring(frames,dtype=np.int16)
    frames = w.readframes(const_time)
    wav_data = np.fromstring(frames,dtype=np.int16)
    framerate, nframes = w.getparams()[2:4]
    return wav_data, framerate, nframes

def convert_mp3(mp3_file):
    """Return feature vectors for two chunks of an MP3 file."""
    # Extract MP3 file to a mono, 10kHz WAV file
    mpg123_command = r'C:\Users\crazy\Desktop\Music\mpg123-1.25.6-x86-64-debug\mpg123.exe -w "%s" -r 10000 -m "%s"'
    out_file = 'temp.wav'
    cmd = mpg123_command % (out_file, mp3_file)
    temp = subprocess.call(cmd)
    # Read in chunks of data from WAV file
    # We'll cover how the features are computed in the next section!
    return read_wav(out_file)


# Main script starts here
# =======================
for path, dirs, files in os.walk(r'C:\Users\crazy\Desktop\Music'):
    for f in files:
        if not f.endswith('.mp3'):
            # Skip any non-MP3 files
            continue
        mp3_file = os.path.join(path, f)
        # Extract the track name (i.e. the file name) plus the names
        # of the two preceding directories. This will be useful
        # later for plotting.
        tail, track = os.path.split(mp3_file)
        tail, dir1 = os.path.split(tail)
        tail, dir2 = os.path.split(tail)
        # Compute features. feature_vec1 and feature_vec2 are lists of floating
        # point numbers representing the statistical features we have extracted
        # from the raw sound data.
        try:
            wav_data, framerate, nframes = convert_mp3(mp3_file)
            time = np.arange(0, const_time)*(1.0 / framerate)

            plt.plot(time,wav_data)
            plt.axis([0.0, const_time/10000 , max(wav_data), -max(wav_data)])
            plt.grid('on')

            plt.legend()

            plt.show()
        except Exception as e:
            print('Error:', e)
            continue