# stability-sdk-rest-api
This is a simple REST API for AI image generation using the Stable Diffusion model from DreamStudio. This API uses their stability-sdk client to access the DreamStudio API.

## Install

`pip install -r requirements.txt`

## Usage
Open the main.py file and set the `dreamStudioAPIKey` variable to your API key.

Start the server: `uvicorn main:app --host 0.0.0.0 --port 5000 --reload`

If everything goes as planned you will see an output in the console similar to this:

`
Uvicorn running on http://127.0.0.1:5000 (Press CTRL+C to quit) 
`

Your server is now running at that address. You can navigate to http://127.0.0.1:5000/docs to see and test the available endpoints. 

## Authentication
At the top of the main.py file there is a block of code that you can uncomment if you want to add a basic form of token authentication.

## Deployment

I have included a Procfile for easy deployment on Heroku.
