
import streamlit as st
import requests
from PIL import Image, ExifTags
import io

# Face++ API credentials
API_KEY = "A8Nk1CllaBmRcHFLEGSU0az1RwYm5uyH"
API_SECRET = "ry51vlFv6ZX2idnDwKSTcrgRv5tFcH"
API_URL = "https://api-us.faceplusplus.com/facepp/v3/detect"

# Auto-orient function using EXIF
def auto_orient_image(image):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = image._getexif()
        if exif is not None:
            orientation_value = exif.get(orientation, None)
            if orientation_value == 3:
                image = image.rotate(180, expand=True)
            elif orientation_value == 6:
                image = image.rotate(270, expand=True)
            elif orientation_value == 8:
                image = image.rotate(90, expand=True)
    except Exception as e:
        st.warning("Image orientation correction skipped.")
    return image

st.title("AI Facial Mapping - Powered by Face++")

uploaded_file = st.file_uploader("Upload a front-facing image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    image = auto_orient_image(image)
    st.image(image, caption="Corrected Image", use_container_width=True)

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
            st.json(landmarks)
        else:
            st.error("No face detected. Try a different image.")
