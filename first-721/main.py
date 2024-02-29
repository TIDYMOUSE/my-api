from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import requests
from typing import Union
from dotenv import load_dotenv
import os

app = FastAPI()
load_dotenv()
client_id = os.getenv("CLIENT_ID")

@app.get("/")
def read_root():
    return {"Hello": "World"}



@app.get("/nft-metadata")
def getTokenMetaDataWithoutCollections(
    name: str,
    description: str,
    # collections: Union[str, None],
):
    
    try:
        # params = {'client_id': client_id, "collections": collections}
        params = {'client_id': client_id}
        
        response = requests.get("https://api.unsplash.com/photos/random", params=params)
        response.raise_for_status()

        unsplash_data = response.json()
        image_uri = unsplash_data.get('urls', {}).get('regular')

        if not image_uri:
            raise HTTPException(status_code=500, detail="Invalid response from Unsplash API")

        
        metadata = {
            "title": "Asset Metadata",
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": name,
                },
                "description": {
                    "type": "string",
                    "description": description,
                },
                "image": {
                    "type": "string",
                    "description": image_uri
                }
            }
        }
        return JSONResponse(content=metadata, status_code=response.status_code)
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error calling Unsplash API: {str(e)}")
    
@app.get("nft-metadata/{collections}")
def getTokenMetaDataWithCollections(
    name: str,
    description: str,
    collections: str,
):
    
    try:
        params = {'client_id': client_id, "collections": collections}
        # params = {'client_id': client_id}
        
        response = requests.get("https://api.unsplash.com/photos/random", params=params)
        response.raise_for_status()

        unsplash_data = response.json()
        image_uri = unsplash_data.get('urls', {}).get('regular')

        if not image_uri:
            raise HTTPException(status_code=500, detail="Invalid response from Unsplash API")

        
        metadata = {
            "title": "Asset Metadata",
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": name,
                },
                "description": {
                    "type": "string",
                    "description": description,
                },
                "image": {
                    "type": "string",
                    "description": image_uri
                }
            }
        }
        return JSONResponse(content=metadata, status_code=response.status_code)
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error calling Unsplash API: {str(e)}")
