from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from crypt_image import image_encrypt, image_decrypt
from starlette.responses import FileResponse

import os

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

image_path: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/image/encrypt")
async def encrypt_image(image: UploadFile = File(...), extention: str = Form(...)):
    try:
        contents = await image.read()
        image_path = 'images/encrypt' + extention
        save_image_from_data(contents, image_path)
        
        image_path, key = image_encrypt(image_path)

        return FileResponse(image_path, key,)
    except Exception as e:
        return {"error": str(e)}
    finally:
        delete_file(image_path)

@app.post("/image/decrypt")
async def decrypt_image(image: UploadFile = File(...), key: str = None):
    
    image = image_decrypt.image_decrypt(image, key)
    return {"filename": image.filename}

def save_image_from_data(image_data, image_path):
    with open(image_path, "wb") as f:
        f.write(image_data)
    print("Image saved successfully.")

def delete_file(image_path):
    os.remove(image_path)
    print("File deleted successfully.")
