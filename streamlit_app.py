
import streamlit as st
import requests
from PIL import Image
import io

API_KEY = "A8Nk1CllaBmRcHFLEGSU0az1RwYm5uyH"
API_SECRET = "ry51vlFv6ZX2idnDwKSTcrgRv5tFcH"
API_URL = "https://api-us.faceplusplus.com/facepp/v3/detect"

st.title("AI Facial Mapping - Powered by Face++")

uploaded_file = st.file_uploader("Upload a front-facing image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_bytes = buffered.getvalue()

    with st.spinner("Analyzing face with Face++..."):
        response = requests.post(
            API_URL,
            files={"image_file": img_bytes},
            data={
                "api_key": API_KEY,
                "api_secret": API_SECRET,
                "return_landmark": 1
            }
        )

        result = response.json()

        if "faces" in result and len(result["faces"]) > 0:
            landmarks = result["faces"][0]["landmark"]
            st.success("Face detected and landmarks extracted.")
            st.markdown("Facial landmark analysis complete. Overlay processing coming next.")
            st.json(landmarks)
        else:
            st.error("No face detected. Please try another image.")
