import whisper
import warnings

# Ignore all warnings
warnings.filterwarnings("ignore")


def transcribe_audio_to_text(audio_path):
    # Load the Whisper model
    model = whisper.load_model("base")

    # Transcribe the audio
    result = model.transcribe(audio_path)

    # Return the transcribed text
    return result["text"]


# Example usage
audio_path = "C://Users//adhik//OneDrive//Desktop//AI voice assistant//output.wav"  # Replace with your audio file path
transcribed_text = transcribe_audio_to_text(audio_path)
print("Transcribed text:", transcribed_text)
