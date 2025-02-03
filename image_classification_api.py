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
    """ Verifica si la API está corriendo correctamente. """
    return {"message": "API de clasificación de ropa funcionando 🚀"}

@app.post("/classify")
async def classify(request: ImageRequest):
    """
    Recibe la URL de una imagen en formato JSON, la descarga y la procesa.
    """
    try:
        # Obtener la URL de la imagen desde el JSON
        image_url = request.image_url

        # Descargar la imagen desde la URL proporcionada
        response = requests.get(image_url)

        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="No se pudo descargar la imagen")

        # Convertir la imagen a un objeto PIL para su procesamiento
        image_bytes = BytesIO(response.content)
        image = Image.open(image_bytes)

        # Simulación de clasificación (reemplazar con el modelo de IA real)
        labels = mock_classify_image(image)

        return {"labels": labels}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la imagen: {str(e)}")

def mock_classify_image(image):
    """
    Simula la clasificación de la imagen. 
    En la implementación real, conectar con un modelo de Machine Learning.
    """
    return ["Camiseta", "Jeans", "Camisa"]  # Respuesta de prueba