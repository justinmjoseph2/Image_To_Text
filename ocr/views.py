from django.shortcuts import render, redirect
import cv2
import pytesseract
import numpy as np
from .forms import ImageUploadForm
from .models import UploadedImage

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def enhance_image(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply a bilateral filter to remove noise while keeping edges sharp
    filtered = cv2.bilateralFilter(gray, 11, 17, 17)
    # Apply adaptive thresholding
    binary_image = cv2.adaptiveThreshold(
        filtered, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return binary_image

def extract_text(image_path):
    try:
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Image not loaded. Please check the path.")

        processed_image = enhance_image(image)
        custom_config = r'--oem 3 --psm 6'
        extracted_text = pytesseract.image_to_string(processed_image, config=custom_config)
        return extracted_text
    except Exception as e:
        print(f"Error during text extraction: {e}")
        return "Error during text extraction"

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()
            image_path = uploaded_image.image.path
            extracted_text = extract_text(image_path)
            uploaded_image.extracted_text = extracted_text
            uploaded_image.save()
            return redirect('ocr:result', pk=uploaded_image.pk)
    else:
        form = ImageUploadForm()
    return render(request, 'ocr/upload.html', {'form': form})

def result(request, pk):
    uploaded_image = UploadedImage.objects.get(pk=pk)
    return render(request, 'ocr/result.html', {'uploaded_image': uploaded_image})
