from fastapi import FastAPI, UploadFile, File
import requests
import base64
import json
import uvicorn

from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()

# Permitir compresión GZip para manejar archivos grandes
app.add_middleware(GZipMiddleware, minimum_size=500)

@app.get("/")
def read_root():
    return {"message": "API de clasificación de ropa funcionando 🚀"}

def classify_image(image_bytes):
    """
    Usa Google Vision AI para clasificar imágenes de ropa.
    """
    API_KEY = "TU_CLAVE_DE_API"
    url = f"https://vision.googleapis.com/v1/images:annotate?key={API_KEY}"
    
    img_base64 = base64.b64encode(image_bytes).decode("utf-8")
    
    payload = {
        "requests": [
            {
                "image": {"content": img_base64},
                "features": [{"type": "LABEL_DETECTION", "maxResults": 10}]
            }
        ]
    }
    
    response = requests.post(url, data=json.dumps(payload), headers={"Content-Type": "application/json"})
    
    if response.status_code == 200:
        labels = response.json()["responses"][0]["labelAnnotations"]
        return [label["description"] for label in labels]
    else:
        return f"Error: {response.text}"

@app.post("/classify")
async def classify(file: UploadFile = File(...)):
    # Limitar el tamaño del archivo 10MB

    max_file_size = 10 * 1024 * 1024 # 10MB
    contents = await file.read()
    if len (contents)>max_file_size:
        raise HTTPException(status_code=413, detail="El archivo es demasiado grande. Máximo permitido: 10MB")
    labels = classify_image(contents) #Procesar la imagen
    return {"labels": labels}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)