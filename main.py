from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
from vertexai.preview.generative_models import GenerativeModel, Part
import vertexai

# Initialize FastAPI
app = FastAPI()

# Your Google Cloud Project ID and Region
PROJECT_ID = os.getenv("GCP_PROJECT")
LOCATION = os.getenv("GCP_REGION")

# Initialize Vertex AI with your project and location
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Load the Gemini Pro Vision model (assuming it's a synchronous operation)
def load_model():
    return GenerativeModel("gemini-pro-vision")

multimodal_model = load_model()

class VideoAnalysisRequest(BaseModel):
    gcs_uri: str
    analysis_type: Optional[str] = 'description'  # default to 'description'

def create_part_from_uri(gcs_uri: str):
    if gcs_uri:
        return Part.from_uri(gcs_uri, mime_type="video/mp4")
    return None

def generate_content(model, prompt, video_part):
    if video_part:
        response = model.generate_content([prompt, video_part], generation_config={"temperature": 0.1, "max_output_tokens": 2048}, stream=True)
        final_response = " ".join([resp.text for resp in response if resp.text])
        return final_response
    return "No video part provided."
    
@app.get("/")
def read_root():
    return {"message": "Welcome to paigeon video analyzer"}    
    
@app.post("/analyze-video/")
async def analyze_video(request: VideoAnalysisRequest):
    video_part = create_part_from_uri(request.gcs_uri)

    if request.analysis_type == 'description':
        prompt = "Describe what is happening in this video."
    elif request.analysis_type == 'tags':
        prompt = "Generate tags for this video followed by '#'"
    elif request.analysis_type == 'highlights':
        prompt = "Summarize the key highlights of this video."
    elif request.analysis_type == 'shopping':
        prompt = "Identify the objects present in this video which can be used for online shopping"
    else:
        raise HTTPException(status_code=400, detail="Invalid analysis type")

    result = generate_content(multimodal_model, prompt, video_part)
    return {"result": result}


