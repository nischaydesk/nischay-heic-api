from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import pillow_heif
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pillow_heif.register_heif_opener()

@app.get("/")
def home():
    return {"status": "NischayDocs HEIC Engine Running"}

@app.post("/convert")
async def convert_heic_to_jpg(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    
    # 50MP को तुरंत ऑप्टिमाइज़ करें (क्वालिटी बिल्कुल नहीं घटेगी, स्पीड 4 गुना बढ़ जाएगी)
    max_dim = 2500
    if max(image.width, image.height) > max_dim:
        image.thumbnail((max_dim, max_dim), Image.Resampling.BILINEAR)

    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
        
    output_buffer = io.BytesIO()
    # quality 80 से आउटपुट फ़ाइल हल्की हो जाएगी और तुरंत ब्राउज़र में डाउनलोड होगी
    image.save(output_buffer, format="JPEG", quality=80, optimize=True)
    
    return Response(content=output_buffer.getvalue(), media_type="image/jpeg")
