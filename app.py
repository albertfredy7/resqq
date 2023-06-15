import cv2
import numpy as np
import streamlit as st
import os
import tensorflow as tf
import keras
import requests
import geocoder

# Load the pre-trained model
model = keras.models.load_model('D:\projects\MainProject\Streamlit-Accident-Detection-\Accident detection\Accident_detection_model.h5')

# Function to preprocess a frame
def preprocess_frame(frame):
    # Resize the frame to the input size of the model
    resized_frame = cv2.resize(frame, (224, 224))

    # Normalize pixel values to the range [0, 1]
    normalized_frame = resized_frame / 255.0

    # Expand dimensions to match the model's input shape
    preprocessed_frame = np.expand_dims(normalized_frame, axis=0)

    return preprocessed_frame

# Function to perform accident detection on a preprocessed frame
def detect_accident(frame):
    # Perform accident detection using the pre-trained model
    prediction = model.predict(frame)[0]

    # Determine the predicted class based on the probability
    if np.max(prediction) > 3.15:
        return True
    else:
        return False

# Function to send the accident location to the Flutter server
def send_accident_location(latitude, longitude):
    url = "http://localhost:8000/receive-data"  # Replace with your Flutter server's endpoint
    data = {"latitude": latitude, "longitude": longitude}  # Send accident location data
    
    try:
        response = requests.post(url, json=data)
        st.success("Accident location sent successfully!")
    except requests.exceptions.RequestException as e:
        st.error(f"Error sending accident location: {e}")

def main():
    st.title("Accident Detection System")

    # File uploader
    uploaded_file = st.file_uploader("Upload a video file", type=["mp4"])

    # Check if a file was uploaded
    if uploaded_file is not None:
        # Save the uploaded file to a temporary location
        temp_file = "./temp.mp4"
        with open(temp_file, "wb") as file:
            file.write(uploaded_file.read())

        # Read the video using OpenCV
        video = cv2.VideoCapture(temp_file)

        # Check if the video was opened successfully
        if not video.isOpened():
            st.error("Failed to open the video file.")
        else:
            # Initialize variables
            frame_count = 0
            accident_count = 0
            alert_shown = False

            # Get the total number of frames in the video
            total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

            # Create a progress bar
            progress_bar = st.progress(0)

            # Read and process the video frames
            while True:
                ret, frame = video.read()
                if not ret:
                    break

                # Pre-process the input frame
                img = cv2.resize(frame, (224, 224))
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = img.astype(np.float32) / 255.0
                img = np.expand_dims(img, axis=0)

                # Detect accident
                is_accident = detect_accident(img)

                # Draw the label on the output frame
                label = 'Accident' if is_accident else 'Non-accident'
                cv2.putText(frame, label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                # Display the output frame
                cv2.imshow('frame', frame)

                # Increment frame count and reset accident count if non-accident frame
                if not is_accident:
                    frame_count += 1
                    accident_count = 0
                else:
                    frame_count += 1
                    accident_count += 1

                # Send accident location to Flutter server if accident count threshold is reached and alert not shown yet
                if accident_count >= 25 and not alert_shown:
                    latitude = 10.731485648591306
                    longitude = 76.28256349666859
                    send_accident_location(latitude, longitude)
                    st.warning("Accident Detected!")
                    alert_shown = True
                    # Hide the progress bar
                    progress_bar.empty()

                # Update the progress bar
                progress_bar.progress(int((frame_count / total_frames) * 100))

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        # Release the video capture object and delete the temporary file
        video.release()
        os.remove(temp_file)

    else:
        st.warning("Please upload a video file.")

if __name__ == "__main__":
    main()
