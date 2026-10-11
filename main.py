from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import pillow_heif
import io

app = FastAPI()

# आपके NischayDocs डोमेन से कनेक्ट करने की अनुमति
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# HEIF/HEIC सपोर्ट रजिस्टर करें
pillow_heif.register_heif_opener()

@app.get("/")
def home():
    return {"status": "NischayDocs HEIC Engine Running"}

@app.post("/convert")
async def convert_heic_to_jpg(file: UploadFile = File(...)):
    # फ़ाइल डेटा पढ़ना
    contents = await file.read()
    
    # pillow-heif सीधे रॉ C बाइनरी से मोशन ट्रैक को अलग करके मुख्य फ़ोटो उठाता है
    image = Image.open(io.BytesIO(contents))
    
    # RGBA को RGB में बदलें ताकि साफ़ JPEG बने
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
        
    output_buffer = io.BytesIO()
    image.save(output_buffer, format="JPEG", quality=90)
    
    return Response(content=output_buffer.getvalue(), media_type="image/jpeg")
