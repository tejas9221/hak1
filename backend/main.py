from model import predict_disease
import io

@app.post("/predict")
async def predict(
    image: UploadFile = File(...),
    text: str = Form("")
):
    contents = await image.read()

    result = predict_disease(io.BytesIO(contents), text)

    return result
