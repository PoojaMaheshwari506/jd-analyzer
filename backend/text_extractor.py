import pdfplumber
from PIL import Image
import pytesseract
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                 text += page.extract_text() + "\n"  
    return text.strip()

def extract_text_from_image(file):
    image = Image.open(file)
    text = pytesseract.image_to_string(image)
    return text.strip()