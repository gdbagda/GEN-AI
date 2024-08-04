from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

## Function to load Gemini Pro-Model and get responses
model = genai.GenerativeModel("gemini-pro")
def get_gemini_response(question) -> None:
    response = model.generate_content(question)
    return response.text

## Initialize our streamlit application
st.set_page_config(page_title="Summer Internship Poornima")
st.header("Puch ky puchega")
input = st.text_input("Input: " , key = "input")
submit = st.button("idher dekh:")

## When user submit is clicked
if submit :
    response = get_gemini_response(input)
    st.subheader("The response is ")
    st.write(response)


    import cv2
import numpy as np

def detect_image(image_path):
    # Load the image
    img = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to segment out the objects from the background
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Find the contours of the objects
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterate through the contours and draw a bounding box around each object
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Return the image with the detected objects
    return img

def lambda_handler(event, context):
    # ... (rest of your code remains the same)

    # Add image detection
    image_path = event["image_path"]
    detected_image = detect_image(image_path)

    # ... (rest of your code remains the same)

    return {
        'statusCode': 200,
        'body': json.dumps({
            "answer": answer.get("answer").strip(),
            "sources": sources,
            "detected_image": detected_image
        })
    }