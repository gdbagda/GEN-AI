from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai
import cv2
import pytesseract
from PIL import Image
import pyttsx3

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
    input_text = st.text_input("Input:", key="input_text")
    submit_button = st.button("Generate Response")

    if submit_button:
        if input_text:
            response = get_gemini_response(input_text)
            st.subheader("The response is:")
            st.write(response)
        else:
            st.warning("Please enter a question.")

elif option == 'Image to Text':
    st.subheader("Upload an image:")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', use_column_width=True)
        st.write("")
        st.subheader("Extracted Text:")
        text = image_to_text(image)
        st.write(text)

elif option == 'Voice to Speech':
    st.subheader("Enter text for speech synthesis:")
    input_text = st.text_area("Input:", key="input_text")
    submit_button = st.button("Convert to Speech")

    if submit_button:
        if input_text:
            voice_to_speech(input_text)
            st.success("Speech synthesis complete.")
        else:
            st.warning("Please enter text for speech synthesis.")
