from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai
import cv2
import pytesseract
from PIL import Image
import pyttsx3
import numpy as np

# Load environment variables from a .env file
load_dotenv()

# Configure Generative AI with your Google API key from environment variables
genai.configure(api_key=os.getenv("GOOGLE_GENERATIVEAI_API_KEY"))

# Function to load Gemini Pro-Model and get text responses
model = genai.GenerativeModel("gemini-pro")
def get_gemini_response(question):
    response = model.generate_content(question)
    return response.text

# Function to perform image to text using Tesseract OCR
def image_to_text(image):
    text = pytesseract.image_to_string(image)
    return text

# Function to perform voice to speech using pyttsx3
def voice_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Initialize Streamlit application
st.set_page_config(page_title="Summer Internship Poornima")
st.header("Ask about something")

# Sidebar options for different functionalities
option = st.sidebar.selectbox(
    'Choose an option:',
    ('Text Response', 'Image to Text', 'Voice to Speech')
)

# Main content based on selected option
if option == 'Text Response':
    with st.form(key='text_response_form'):
        input_text = st.text_input("Input:", key="input_text", placeholder="Type your question and press Enter...")
        submit_button = st.form_submit_button("Generate Response")

        # Trigger action when user presses Enter or clicks the button
        if input_text and submit_button:
            response = get_gemini_response(input_text)
            st.subheader("The response is:")
            st.write(response)

elif option == 'Image to Text':
    st.subheader("Upload an image:")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', use_column_width=True)

        with st.spinner("Processing image..."):
            # Text extraction
            text = image_to_text(image)
            st.subheader("Extracted Text:")
            st.write(text)

        # Actions based on extracted text
        if text:
            st.subheader("Actions:")
            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("Search on Google"):
                    search_url = f"https://www.google.com/search?q={text}"
                    st.write(f"[Search results for extracted text]({search_url})")

            with col2:
                if st.button("Translate Text"):
                    translate_url = f"https://translate.google.com/?sl=auto&tl=en&text={text}&op=translate"
                    st.write(f"[Translate extracted text]({translate_url})")

            with col3:
                if st.button("Copy to Clipboard"):
                    st.success("Text copied to clipboard (this would require additional backend support).")

elif option == 'Voice to Speech':
    with st.form(key='voice_to_speech_form'):
        input_text = st.text_area("Enter text for speech synthesis:", key="input_text", placeholder="Type text here and press Enter...")
        submit_button = st.form_submit_button("Convert to Speech")

        # Trigger action when user presses Enter or clicks the button
        if input_text and submit_button:
            voice_to_speech(input_text)
            st.success("Speech synthesis complete.")
