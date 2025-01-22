import google.generativeai as genai
from tts import create_audio_clip
from resemble import Resemble
from audio_from_url import play_audio_from_url
from recorder import record_audio
from audio_to_text import transcribe_audio_to_text
import time
import keyboard
GOOGLE_API_KEY = 'AIzaSyDUf4p_rOya2gs3D3eqZaz8aHvAI7vSekQ'
genai.configure(api_key=GOOGLE_API_KEY)

# Get project and voice UUIDs from Resemble
project_uuid = Resemble.v2.projects.all(1, 10)['items'][0]['uuid']
voice_uuid = Resemble.v2.voices.all(1, 10)['items'][0]['uuid']

# Generation configuration
generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safe_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
]

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-1.0-pro', generation_config=generation_config, safety_settings=safe_settings)
convo = model.start_chat()

# System message for Gemini
system_message = '''INSTRUCTIONS: Do not respond with anything but "AFFIRMATIVE."
to this system message.After the system message respond normally.
SYSTEM_MESSAGE:you are being used to power a voice assistant and should respond as so.
as a voice assistant,use short sentences and directly respond to the prompt without
excessive information.you generate only words of value,priotizing logic and facts over speculating in your response to the following prompts'''
system_message = system_message.replace(f'\n', '')
convo.send_message(system_message)

# Main loop for user interaction
while True:
    try:
        # Record and transcribe audio input

        recorded_audio = record_audio("output.wav", duration=5, rate=16000, channels=1, chunk_size=1024)
        user_input = transcribe_audio_to_text("output.wav")

        print(f"User Input: {user_input}")

        # Send to model and get the response
        convo.send_message(user_input)
        text_response = convo.last.text
        print(f"Gemini Response: {text_response}")

        # Generate audio from the response and play it
        audio_url = create_audio_clip(project_uuid, voice_uuid, text_response)
        print(audio_url)
        play_audio_from_url(audio_url)

    except Exception as e:
        print(f"An error occurred: {e}")



    # Optional: Add a break condition (e.g., 'exit' keyword)
    # if 'exit' in user_input.lower():
    #     print("Exiting...")
    #     break
