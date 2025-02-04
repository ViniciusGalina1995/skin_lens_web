import streamlit as st
import requests
from PIL import Image

API_URL = "https://skinlens-1019856209529.europe-west1.run.app/predict"

st.markdown("""
    <style>
        /* Set background color for the main content */
        .main {
            background-color: #e3e6f3; /* Solid light blue-gray */
        }

        /* Customize buttons */
        .stButton>button {
            background-color: #2E7D32; /* Darker Green */
            color: white;
            padding: 14px 20px;
            margin: 8px 0;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            width: 100%;
            font-weight: bold;
            transition: background 0.3s ease;
        }

        .stButton>button:hover {
            background-color: #1b5e20; /* Even darker green */
        }

        /* Header with a stronger gradient effect */
        .header {
            background: linear-gradient(90deg, #2E7D32 0%, #1b5e20 100%);
            color: white;
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            text-align: center;
            font-size: 1.8em;
            font-weight: bold;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
        }

        /* Feature card with stronger color contrast */
        .feature-card {
            padding: 1.8rem;
            background: #ffffff;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            margin-bottom: 1rem;
            text-align: center;
            border: 2px solid #2E7D32;
        }

        /* Analysis result section */
        .analysis-result {
            margin-top: 20px;
            padding: 1.2rem;
            border: 3px solid #2E7D32;
            border-radius: 12px;
            background: #F1F8E9; /* Light green background */
            font-weight: bold;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }

        /* Highlight condition text */
        .condition {
            font-size: 1.6em;
            font-weight: bold;
            color: #2C6B2F; /* Darker and more solid green */
            background-color: #A5D6A7; /* Soft light green background */
            padding: 8px 12px;
            border-radius: 6px;
            text-shadow: none; /* No shadow for clearer text */
        }

        /* Confidence score styling */
        .confidence {
            font-size: 1.3em;
            color: #222;
            background: #C8E6C9; /* Darker Green */
            padding: 6px 12px;
            border-radius: 6px;
            display: inline-block;
            font-weight: bold;
        }

        /* Detailed probabilities section */
        .detailed-probabilities {
            margin-top: 12px;
            background: #C8E6C9; /* Solid light green background */
            padding: 12px;
            border-radius: 8px;
            border: 2px solid #2E7D32; /* Dark green border */
            color: #333333; /* Dark color for text for better contrast */
            font-size: 1em; /* Slightly larger font for better readability */
        }

    </style>

""", unsafe_allow_html=True)

PAGES = {
    "Home": "home",
    "Skin Analysis": "analysis",
    "Technology": "technology"
}

def main():
    if "page" not in st.session_state:
        st.session_state["page"] = "Home"

    page_list = list(PAGES.keys())

    selected_page = st.sidebar.radio("Go to", page_list, index=page_list.index(st.session_state["page"]))

    if selected_page != st.session_state["page"]:
        st.session_state["page"] = selected_page
        st.rerun()

    if st.session_state["page"] == "Home":
        show_home_page()
    elif st.session_state["page"] == "Skin Analysis":
        show_analysis_page()
    elif st.session_state["page"] == "Technology":
        show_technology_page()

def show_home_page():
    st.markdown('<div class="header"><h1>Welcome to Skin Lens</h1></div>', unsafe_allow_html=True)
    st.markdown("""
        ### Early Detection for Better Skin Health
        Upload a photo of your skin concern and get instant AI-powered analysis. Our advanced algorithms help identify potential skin conditions with clinical-grade accuracy.
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            **Why Choose Us?**
            - 🩺 **Accuracy:** Trusted by experts
            - ⚡ **Instant Results:** Get analysis in seconds
            - 🔒 **Privacy Ensured:** Your data is safe with us

            **Get Started**
            Don't wait! Early detection can make a huge difference. Click the button below to analyze your skin now.
        """)

        if st.button("Go to Skin Analysis →", key="skin_analysis_button"):
            st.session_state["page"] = "Skin Analysis"
            st.rerun()

    with col2:
        try:
            img = Image.open("images/skin_image.jpg")
            st.image(img, use_container_width=True)
        except FileNotFoundError:
            st.warning("Homepage image not found. Using placeholder.")
            st.image(Image.new("RGB", (400, 300), color="#45a049"), use_container_width=True)

def show_analysis_page():
    st.title("Skin Analysis")
    uploaded_file = st.file_uploader("Upload skin lesion image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        col1, col2 = st.columns(2)
        with col1:
            st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

        with st.spinner("Analyzing image..."):
            try:
                response = requests.post(API_URL, files={"file": uploaded_file}, timeout=30)
                response.raise_for_status()

                prediction = response.json()

                if "prediction" not in prediction or "all_class_probabilities" not in prediction:
                    st.error("Invalid API response structure.")
                    return

                with col2:
                    st.markdown(f"""
                    <div class="analysis-result" style="background: rgba(255, 255, 255, 0.6); padding: 20px; border-radius: 10px;">
                        <p class="condition" style="font-size: 1.5em; font-weight: bold; color: #4CAF50;">
                            🩺Condition: {prediction['prediction']['class']}
                        </p>
                        <p class="confidence" style="font-size: 1.2em; color: #333333;">
                            📊Confidence: {prediction['prediction']['probability']:.1f}%
                        </p>
                    </div>
                """, unsafe_allow_html=True)

                    # Expander for detailed probabilities
                    with st.expander("🔎 **Show Detailed Probabilities**"):
                        st.markdown(f"""
                        <div style="background: rgba(0, 255, 0, 0.1); padding: 20px; border-radius: 10px; border: 2px solid #4CAF50;">
                            {format_probabilities(prediction["all_class_probabilities"])}
                        </div>
                        """, unsafe_allow_html=True)


            except requests.exceptions.RequestException as e:
                st.error(f"API Connection Error: {str(e)}")
                st.write("Please check your internet connection and try again.")
            except ValueError as ve:
                st.error(f"Data Parsing Error: {str(ve)}")
                st.json(response.json())
            except Exception as e:
                st.error(f"Unexpected Error: {str(e)}")

def format_probabilities(probabilities):
    return "\n".join([f"<p>- {k}: {v:.1f}%</p>" for k, v in probabilities.items()])

def show_technology_page():
    st.markdown("<h1 style='text-align: center;'>Our Technology</h1>", unsafe_allow_html=True)

    st.markdown("""
        <div style="background-color: #f0f4f8; padding: 2rem; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
            <h2 style="color: #4CAF50; font-size: 2.5rem; font-weight: bold;">Revolutionizing with AI</h2>
            <p style="font-size: 1.2rem; color: #333;">Our system combines cutting-edge deep learning with clinical expertise to offer real-time, highly accurate skin condition analysis. We empower dermatologists and patients with clinical-grade precision.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### How It Works")
    st.write("""
        Our AI solution utilizes state-of-the-art deep neural networks trained on over 200,000 dermatoscopic images. The system is continuously updated with new data to stay at the forefront of skin health research.

        - **Deep Neural Networks**: Powerful models that learn to identify skin conditions with exceptional accuracy.
        - **Clinical Validation**: Developed in partnership with certified dermatologists to ensure real-world accuracy.
        - **Continuous Learning**: Our model improves over time, as it is retrained with new and diverse data.
    """)

    st.markdown("### Key Features")
    st.write("""
        - **AI-Driven Analysis**: Accurate, fast predictions based on a vast dataset.
        - **Real-Time Results**: Get immediate, actionable insights for better decision-making.
        - **Security & Privacy**: Your data is encrypted and processed in compliance with the highest medical standards.
    """)

    st.markdown("### Our Technical Architecture")
    st.write("AI Model: EfficientNet-B5, trained on the ISIC 2020 dataset for robust skin lesion classification.")

    st.markdown("## Model Performance on Test Set")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Confusion Matrix")
        st.image("images/confusion_matrix.png", caption="Confusion Matrix", use_container_width=True)

    with col2:
        st.markdown("### Classification Report")
        st.image("images/classification_metrics.png", caption="Classification Report", use_container_width=True)

    st.markdown("### Learning Curve")
    st.image("images/learning_curves.png", caption="Learning Curve", use_container_width=True)

    st.markdown("""
        <div style="background-color: #e8f5e9; padding: 2rem; border-radius: 10px; margin-top: 40px;">
            <h3 style="color: #388e3c; font-size: 2rem; font-weight: bold; text-align: center;">Privacy & Security</h3>
            <p style="font-size: 1.2rem; color: #333; text-align: center;">We prioritize your privacy with HIPAA-compliant data handling, end-to-end encryption, and automatic image deletion. Your security is our top concern.</p>
        </div>
    """, unsafe_allow_html=True)
    # st.markdown("""
    #     <div style="margin-top: 30px; text-align: center;">
    #         <a href="#privacy-policy" style="padding: 10px 20px; background-color: #388e3c; color: white; border-radius: 5px; text-decoration: none; font-size: 1.2rem;">Read Our Privacy Policy →</a>
    #     </div>
    # """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
    st.markdown("---")
