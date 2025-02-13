import streamlit as st
import requests
import speech_recognition as sr
from gtts import gTTS
import tempfile
import os
from googletrans import Translator
from transformers import pipeline

# Hugging Face API details
HF_API_TOKEN = "YOUR_HUGGINGFACE_TOKEN"
API_URL = "https://api-inference.huggingface.co/models/thrishala/mental_health_chatbot"
HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}

# Load NLP Model (Fallback for local processing)
try:
    chatbot_pipeline = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.2")
except:
    chatbot_pipeline = None

translator = Translator()

# Supported Indian Languages
languages = {
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
    "Tamil": "ta",
    "Telugu": "te",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Malayalam": "ml",
    "Kannada": "kn",
    "Odia": "or",
    "Urdu": "ur"
}

# Function to get chatbot response using Hugging Face API
def query_hf(payload):
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response_json = response.json()
        if isinstance(response_json, list):
            return response_json[0]["generated_text"]
        return "Sorry, I couldn't process that."
    except Exception as e:
        return f"Error: {str(e)}"

# NLP-based local fallback
def generate_response(text):
    if chatbot_pipeline:
        response = chatbot_pipeline(text, max_length=100, num_return_sequences=1)
        return response[0]["generated_text"]
    else:
        return "AI model unavailable. Please check your internet connection."

# Speech-to-text conversion
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand your speech."
        except sr.RequestError:
            return "Could not process audio. Please check your connection."

# Translate text
def translate_text(text, target_lang):
    try:
        return translator.translate(text, dest=target_lang).text
    except:
        return text  # Return original text if translation fails

# Streamlit UI
st.title("🧠 EMpathiAI - Multilingual Mental Health Chatbot")
st.write("A chatbot that understands your emotions and responds with care.")

# Language selection
selected_lang = st.selectbox("Select Language", list(languages.keys()))

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.text_input("Type your message here")
if st.button("🎤 Speak"):
    user_input = recognize_speech()
    st.write("Recognized Text: ", user_input)

if user_input:
    # Translate input to English for processing
    user_input_translated = translate_text(user_input, "en")
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get chatbot response (either from HF API or local NLP model)
    response_text = query_hf({"inputs": user_input_translated})
    if "Error" in response_text:
        response_text = generate_response(user_input_translated)  # Fallback to local model if API fails

    # Translate response back to selected language
    bot_response_translated = translate_text(response_text, languages[selected_lang])

    # Append chatbot response to chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_response_translated})

    # Display chatbot response
    with st.chat_message("assistant"):
        st.markdown(bot_response_translated)

    # Convert response to speech
    tts = gTTS(bot_response_translated, lang=languages[selected_lang])
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts.save(fp.name)
        st.audio(fp.name, format='audio/mp3')
