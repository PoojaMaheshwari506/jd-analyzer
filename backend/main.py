from models import JDRequest, JDResponse
from analyzer import analyze_jd
from fastapi import FastAPI, UploadFile, File
from text_extractor import extract_text_from_pdf, extract_text_from_image

app = FastAPI(title="JD Analyzer API")
app = FastAPI()
@app.post("/analyze", response_model=JDResponse)
def analyze(request: JDRequest):
    return analyze_jd(request.jd_text)

@app.post("/analyze-file")
async def analyze_file(file: UploadFile = File(...)):
    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(file.file)
    elif file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
        text = extract_text_from_image(file.file)
    else:
        return {"error": "Unsupported file type"}

    return analyze_jd(text)
