@app.get("/")
def read_root():
    return {"message": "API de clasificación de ropa funcionando 🚀"}

from fastapi import FastAPI, UploadFile, File
import requests
import base64
import json
import uvicorn

app = FastAPI()

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
    image_bytes = await file.read()
    labels = classify_image(image_bytes)
    return {"labels": labels}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)