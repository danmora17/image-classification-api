from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from io import BytesIO
from PIL import Image

app = FastAPI()

class ImageRequest(BaseModel):
    image_url: str

@app.get("/")
async def root():
    return {"message": "API de clasificación de ropa funcionando 🚀"}

@app.post("/classify")
async def classify(request: ImageRequest):
    try:
        image_url = request.image_url
        headers = {"User-Agent": "Mozilla/5.0"}

        # Si la URL es de Imgur pero no tiene extensión, agregamos ".jpg"
        if "imgur.com" in image_url and not image_url.endswith((".jpg", ".png", ".jpeg")):
            image_url += ".jpg"

        response = requests.get(image_url, headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="No se pudo descargar la imagen")

        image_bytes = BytesIO(response.content)
        image = Image.open(image_bytes)

        labels = mock_classify_image(image)
        return {"labels": labels}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la imagen: {str(e)}")

def mock_classify_image(image):
    return ["Camiseta", "Jeans", "Camisa"]

    import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)