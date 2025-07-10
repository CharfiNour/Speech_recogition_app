import cv2
import streamlit as st
import numpy as np

face_cascade = cv2.CascadeClassifier(
    r'C:\Users\Lumiere\Desktop\Data projects\face detection\haarcascade_frontalface_default.xml'
)

def app():
    st.title("Face Detection App")
    st.markdown("""
    **Instructions:**
    1. Choose the rectangle color and adjust detection parameters as desired.
    2. Click **Detect Faces** to capture an image from your webcam and detect faces.
    3. Click **Save Image** to download the image with detected faces.
    4. Click **Stop** to stop detection.
    """)

    # Rectangle color picker
    rect_color = st.color_picker("Pick rectangle color for faces", "#00FF00")
    # Convert hex color to BGR tuple
    rect_color_bgr = tuple(int(rect_color.lstrip('#')[i:i+2], 16) for i in (4, 2, 0))

    # Detection parameter sliders
    scale_factor = st.slider("Scale Factor", min_value=1.01, max_value=2.0, value=1.3, step=0.01)
    min_neighbors = st.slider("minNeighbors", min_value=1, max_value=10, value=5, step=1)

    if "run" not in st.session_state:
        st.session_state.run = False
    if "last_frame" not in st.session_state:
        st.session_state.last_frame = None

    col1, col2, col3 = st.columns(3)
    if col1.button("Detect Faces"):
        st.session_state.run = True
    if col2.button("Stop"):
        st.session_state.run = False
    save_image = col3.button("Save Image")

    FRAME_WINDOW = st.image([])

    if st.session_state.run:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if not ret:
            st.write("Failed to grab frame")
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(
                gray, scaleFactor=scale_factor, minNeighbors=min_neighbors
            )
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), rect_color_bgr, 2)
            st.session_state.last_frame = frame.copy()
            FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        cap.release()

    # Save image feature
    if save_image and st.session_state.last_frame is not None:
        result, buf = cv2.imencode('.jpg', st.session_state.last_frame)
        if result:
            st.download_button(
                label="Download Image",
                data=buf.tobytes(),
                file_name="detected_faces.jpg",
                mime="image/jpeg"
            )
        else:
            st.error("Failed to encode image for download.")

if __name__ == "__main__":
    app()    