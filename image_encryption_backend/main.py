from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware


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

@app.post("image/encrypt")
def encrypt_image(image: UploadFile = File(...)):
    
    return {"filename": image.filename}

@app.post("image/decrypt")
def decrypt_image(image: UploadFile = File(...), key: str = None):
    
    
    
    return {"filename": image.filename}