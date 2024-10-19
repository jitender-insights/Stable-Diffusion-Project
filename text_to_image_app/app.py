import streamlit as st
from model_manager import ModelManager
from image_generator import ImageGenerator
import os
from dotenv import load_dotenv
from PIL import Image
import io
import base64

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(page_title="AI Image Generator", layout="wide")

# Custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("static/css/style.css")

# Initialize ModelManager and ImageGenerator
model_manager = ModelManager()
image_generator = ImageGenerator(model_manager)

# Main title
st.title("AI Image Generator")

# Create two columns
col1, col2 = st.columns([1, 1])

with col1:
    st.header("Generate Image")
    prompt = st.text_area("Enter your prompt:", height=100)
    model_name = st.selectbox("Select a model:", model_manager.get_model_list())
    
    if st.button("Generate Image"):
        if prompt:
            with st.spinner("Generating image..."):
                try:
                    result = image_generator.generate_image(prompt, model_name)
                    image_bytes = result['image_bytes']
                    base64_image = result['base64_image']
                    
                    try:
                        image = Image.open(io.BytesIO(image_bytes))
                        st.image(image, caption="Generated Image", use_column_width=True)
                    except Exception as e:
                        st.error(f"Error opening image: {str(e)}")
                        st.write("First 100 bytes of image data:", image_bytes[:100])
                        st.write("Base64 encoded image (first 100 characters):", base64_image[:100])
                        
                        # Try to display the image using base64
                        st.markdown(f"### Trying to display image using base64:")
                        st.markdown(f'<img src="data:image/png;base64,{base64_image}" alt="Generated Image">', unsafe_allow_html=True)
                        
                except Exception as e:
                    st.error(f"Error generating image: {str(e)}")
                    st.write("Error details:", str(e))
        else:
            st.warning("Please enter a prompt.")

with col2:
    st.header("Model Information")
    if model_name:
        model_info = model_manager.get_model_info(model_name)
        st.write(f"**Model:** {model_name}")
        st.write(f"**Description:** {model_info['description']}")
        st.write(f"**Provider:** {model_info['provider']}")

# Sidebar
st.sidebar.image("static/images/logo.png", use_column_width=True)
st.sidebar.header("About")
st.sidebar.info("This app uses state-of-the-art AI models to generate images from text prompts. Select a model and enter your prompt to create unique images!")

# Footer
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #0E1117;
        color: #FAFAFA;
        text-align: center;
        padding: 10px;
        font-size: 14px;
    }
    </style>
    <div class="footer">
        Created with ❤️ by DataSciLearn | <a href="https://github.com/jitender-insights" target="_blank">GitHub</a>
    </div>
    """,
    unsafe_allow_html=True
)