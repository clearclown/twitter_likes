from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests
import os
import logging

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserID(BaseModel):
    screen_name: str

def get_twitter_likes(screen_name: str):
    bearer_token = os.getenv("BEARER_TOKEN")
    auth_token = os.getenv("AUTH_TOKEN")
    ct0 = os.getenv("CT0")
    cookie = os.getenv("COOKIE")

    logger.info(f"Bearer Token: {bearer_token}")
    logger.info(f"Auth Token: {auth_token}")
    logger.info(f"CT0 Token: {ct0}")
    logger.info(f"Cookie: {cookie}")

    if not bearer_token or not auth_token or not ct0 or not cookie:
        raise HTTPException(status_code=500, detail="Necessary tokens are not found")

    url = f"https://api.twitter.com/1.1/favorites/list.json?screen_name={screen_name}"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json",
        "Cookie": cookie,
        "x-csrf-token": ct0
    }

    response = requests.get(url, headers=headers)

    logger.info(f"Response Status Code: {response.status_code}")
    logger.info(f"Response Text: {response.text}")

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()

@app.post("/likes/")
def read_likes(user: UserID):
    try:
        likes = get_twitter_likes(user.screen_name)
        return JSONResponse(content=likes)
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
