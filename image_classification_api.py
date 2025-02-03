from fastapi import FastAPI, HTTPException
import requests
from io import BytesIO
from PIL import Image

app = FastAPI()

@app.get("/")
async def root():
    """ Verifica si la API está corriendo correctamente. """
    return {"message": "API de clasificación de ropa funcionando 🚀"}

@app.post("/classify")
async def classify(image_url: str):
    """
    Recibe la URL de una imagen, la descarga y la procesa para clasificarla.
    """
    try:
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
