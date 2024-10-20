import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from model_manager import ModelManager
from image_generator import ImageGenerator

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Text-to-Image Generation API",
    description="An API for generating images from text prompts using various AI models.",
    version="1.0.0",
    docs_url="http://127.0.0.1:8000/docs",
    redoc_url="http://127.0.0.1:8000/redoc",
    openapi_url="/openapi.json"
)

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Streamlit default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ModelManager and ImageGenerator
try:
    model_manager = ModelManager()
    image_generator = ImageGenerator(model_manager)
except ValueError as e:
    print(f"Error initializing ModelManager: {str(e)}")
    print(f"HUGGINGFACE_TOKEN: {os.getenv('HUGGINGFACE_TOKEN')}")
    raise

class GenerateRequest(BaseModel):
    prompt: str
    model_name: str

@app.get("/models")
async def get_models():
    return {"models": model_manager.get_model_list()}

@app.get("/model/{model_name}")
async def get_model_info(model_name: str):
    model_info = model_manager.get_model_info(model_name)
    if model_info:
        return model_info
    raise HTTPException(status_code=404, detail="Model not found")

@app.post("/generate")
async def generate_image(request: GenerateRequest):
    try:
        result = image_generator.generate_image(request.prompt, request.model_name)
        return {"image": result['base64_image']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)