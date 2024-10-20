# AI Image Generator

This project is a Streamlit-based web application with a FastAPI backend for generating images using various AI models from Stability AI, RunwayML, and other providers available on Hugging Face.

## Features

- Select from multiple AI models for image generation
- Enter custom text prompts to generate images
- View model information and descriptions
- Attractive and responsive user interface
- FastAPI backend for scalability

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/jitender-insights/Stable-Diffusion-Project.git
   cd text_to_image_app
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up your Hugging Face token in the `.env` file.

## Usage

Run the application:

```
streamlit run app.py
```

Open your web browser and go to `http://localhost:8501` to use the app.

If you want to run main.py file please follow below steps:
Run the FastAPI server


```
uvicorn main:app --reload
```

Open your web browser and go to `http://127.0.0.1:8000/docs` to use the app.



## Deployment

This application is designed to be easily deployed on platforms like Render. Follow these steps:

1. Create a new Web Service on Render.
2. Connect your GitHub repository.
3. Set the build command to `pip install -r requirements.txt`.
4. Set the start command to `streamlit run app.py`.
5. Add your Hugging Face token as an environment variable named `HUGGINGFACE_TOKEN`.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
