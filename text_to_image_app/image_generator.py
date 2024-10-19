from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
import io
import base64
import os

class ImageGenerator:
    def __init__(self, model_manager):
        # Set the device to GPU if available, otherwise use CPU
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.models = {}
        self.model_manager = model_manager  # Store the passed ModelManager instance

    def load_model(self, model_name):
        # Get model information using ModelManager
        model_info = self.model_manager.get_model_info(model_name)
        model_id = model_info.get('model_id')  # Fetch the correct model ID

        if not model_id:
            raise ValueError(f"Model ID for '{model_name}' not found.")

        # Load the model if it's not already cached
        if model_name not in self.models:
            try:
                self.models[model_name] = StableDiffusionPipeline.from_pretrained(
                    model_id,  # Use the correct model ID
                    torch_dtype=torch.float16,
                    use_auth_token=os.getenv("HUGGINGFACE_TOKEN")  # Pass Hugging Face token
                ).to(self.device)
            except Exception as e:
                raise RuntimeError(f"Failed to load model '{model_name}': {str(e)}")

        return self.models[model_name]

    def generate_image(self, prompt, model_name):
        model = self.load_model(model_name)
        try:
            with torch.autocast(self.device):
                output = model(prompt)

            if not output.images:
                raise ValueError("Model did not generate any images.")

            image = output.images[0]

            # Convert PIL Image to bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()

            # Encode to base64 for easier debugging
            base64_image = base64.b64encode(img_byte_arr).decode('utf-8')

            return {
                'image_bytes': img_byte_arr,
                'base64_image': base64_image
            }
        except Exception as e:
            raise RuntimeError(f"Error during image generation: {str(e)}")
