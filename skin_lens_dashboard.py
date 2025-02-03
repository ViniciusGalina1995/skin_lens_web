import streamlit as st
import requests
spell = st.secrets['spell']
key = st.secrets.some_magic_api.key
#API_URL = "http://localhost:8000/predict"
API_URL = "https://skinlens-1019856209529.europe-west1.run.app/predict"
st.title("Skin Disease Prediction Dashboard")

uploaded_file = st.file_uploader("Upload an image of the skin lesion", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

    files = {"file": uploaded_file}

    try:
        response = requests.post(API_URL, files=files)

        if response.status_code == 200:
            prediction = response.json()

            st.write(f"Image scanned: The skin lesion is classified as {prediction['prediction']['class']} "
                     f"with a predicted probability of {prediction['prediction']['probability']:.2f}%")

            st.write("Class probabilities for all labels:")
            for class_name, prob in prediction["all_class_probabilities"].items():
                st.write(f"{class_name}: {prob}%")

        else:
            st.write(f"Error: {response.json().get('error', 'Unknown error occurred')}")

    except Exception as e:
        st.write(f"An error occurred while processing the request: {str(e)}")
