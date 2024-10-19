import os
from huggingface_hub import login

class ModelManager:
    def __init__(self):
        self.models = {
            "stable-diffusion-v1-5": {
                "provider": "RunwayML",
                "model_id": "runwayml/stable-diffusion-v1-5",
                "description": "Stable Diffusion v1.5 model for general-purpose image generation.",
                
            },
            "stable-diffusion-2-1": {
                "provider": "Stability AI",
                "model_id": "stabilityai/stable-diffusion-2-1",
                "description": "Improved version of Stable Diffusion with better image quality and consistency."
            },
            "dall-e-mini": {
                "provider": "Open AI",
                 "model_id" : "dalle-mini/dalle-mini",
                "description": "Lightweight version of DALL-E for faster image generation."
            },
            # Add more models here
        }

        # Load the Hugging Face token from the environment
        hf_token = os.getenv("HUGGINGFACE_TOKEN")
        
        if hf_token:
            # Authenticate with Hugging Face
            login(hf_token)
        else:
            raise ValueError("Hugging Face token not found. Please set it in the .env file.")

    def get_model_list(self):
        return list(self.models.keys())

    def get_model_info(self, model_name):
        return self.models.get(model_name, {"provider": "Unknown", "description": "No information available."})
