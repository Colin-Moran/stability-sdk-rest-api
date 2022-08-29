from asyncio.windows_events import NULL
from tkinter import Image
from fastapi import FastAPI, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import Response

import io
import warnings
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from pydantic import BaseModel, ValidationError

# Uncomment this section for a basic token authentication
# api_keys = [ 
#     "whatever_you_want_your_key_to_be"
# ]  # Encrypt and store this somewhere
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# def api_key_auth(api_key: str = Depends(oauth2_scheme)):
#     if api_key not in api_keys:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Forbidden"
#         )
# app = FastAPI(dependencies=[Depends(api_key_auth)])

dreamStudioAPIKey = "YOUR_API_KEY"

app = FastAPI()

class ImageGenerationRequest(BaseModel):
    prompt:str
    height=512
    width=512
    cfg_scale=7.0
    sampler="SAMPLER_K_LMS" # SAMPLER_DDIM, SAMPLER_DDPM, SAMPLER_K_EULER, SAMPLER_K_EULER_ANCESTRAL, SAMPLER_K_HEUN, SAMPLER_K_DPM_2, SAMPLER_K_DPM_2_ANCESTRAL, SAMPLER_K_LMS
    steps=50
    num_samples=1
    seed=NULL # Integer value
    safety=False
    
stability_api = client.StabilityInference(
    key=dreamStudioAPIKey, 
    verbose=True,
)

@app.get("/")
async def root():
    return {"message": "Stability-SDK REST API is running!"}

@app.post("/generate")
async def generate(req: ImageGenerationRequest):
    image = getImage(req)
    if (isinstance(image, str)):
        return Response(content=image, status_code=500)
    imageAsBytes = imageToByteArray(image)
    return Response(imageAsBytes, media_type="image/png")

def getImage(params: ImageGenerationRequest):
    
    seed = NULL
    if (params.seed):
        seed = [int(x) for x in str(params.seed)]
    
    answers = stability_api.generate(
        prompt=params.prompt,
        height=params.height,
        width=params.width,
        cfg_scale=params.cfg_scale,
        sampler=params.sampler,
        steps=params.steps,
        seed=seed
    )
    
    image = NULL
    
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn(
                    "Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again.")
                return "Your request activated the API's safety filters and could not be processed."
            if artifact.type == generation.ARTIFACT_IMAGE:
                image = Image.open(io.BytesIO(artifact.binary))
    
    return image

def imageToByteArray(image: Image) -> bytes:
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format="png")
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr