import requests
import pyaudio
import wave
import io


def play_audio_from_url(audio_url):

    response = requests.get(audio_url)

    audio_data = io.BytesIO(response.content)
    with wave.open(audio_data, 'rb') as wf:
        num_channels = wf.getnchannels()
        sample_width = wf.getsampwidth()
        frame_rate = wf.getframerate()
        num_frames = wf.getnframes()


        p = pyaudio.PyAudio()


        stream = p.open(format=pyaudio.paInt32,
                        channels=num_channels,
                        rate=frame_rate,
                        output=True)


        chunk_size = 1024
        for i in range(0, num_frames, chunk_size):
            chunk = wf.readframes(chunk_size)
            stream.write(chunk)


        stream.stop_stream()
        stream.close()
        p.terminate()



play_audio_from_url(
    'https://app.resemble.ai/rails/active_storage/blobs/redirect/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBCUHVPemc0PSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--ebfaa6573a1aa0c5190fee1ea0a86c4abbf11680/result.wav')
