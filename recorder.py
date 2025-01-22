import pyaudio
import wave


def record_audio(output_filename, duration=5, rate=16000, channels=1, chunk_size=1024):
    # Initialize the PyAudio object
    p = pyaudio.PyAudio()

    # Open a stream for recording
    stream = p.open(format=pyaudio.paInt16,  # 16-bit audio
                    channels=channels,  # 1 for mono, 2 for stereo
                    rate=rate,  # Sample rate (e.g., 16000 or 44100)
                    input=True,  # Set as input stream
                    frames_per_buffer=chunk_size)  # Buffer size

    print(f"Recording audio for {duration} seconds...")

    frames = []  # List to hold the recorded audio frames

    # Record audio in chunks and append to frames list
    for _ in range(0, int(rate / chunk_size * duration)):
        data = stream.read(chunk_size)
        frames.append(data)

    # Stop and close the stream
    print("Recording complete.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded audio to a WAV file
    with wave.open(output_filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))  # Sample width in bytes
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))


# Example usage: Record for 5 seconds and save to 'output.wav'
record_audio("output.wav", duration=5)
