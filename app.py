from flask import Flask, render_template, request
import csv
import PyPDF2
import tabula
import pytesseract
from PIL import Image

app = Flask(__name__)

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(reader.pages)
        all_text = ""
        
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text = page.extract_text()
            all_text += text
        
        return all_text

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

def extract_key_value_pairs(text):
    key_value_pairs = {}
    
    # Define your own logic to extract key-value pairs from the text
    # For example, you can split the text by newlines and ':' character
    lines = text.split('\n')
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            key_value_pairs[key] = value
    
    return key_value_pairs

def save_to_csv(data, csv_path):
    with open(csv_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        
        # Write the header row
        writer.writerow(['Key', 'Value'])
        
        # Write the data rows
        for key, value in data.items():
            writer.writerow([key, value])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file.filename.lower().endswith('.pdf'):
        # Save the PDF file
        pdf_path = 'uploaded_file.pdf'
        file.save(pdf_path)

        # Extract text from PDF
        text = extract_text_from_pdf(pdf_path)
    else:
        # Save the image file
        image_path = 'uploaded_file.png'
        file.save(image_path)

        # Extract text from image
        text = extract_text_from_image(image_path)

    # Extract key-value pairs from the text
    data = extract_key_value_pairs(text)

    # Save the data to a CSV file
    csv_path = 'output.csv'
    save_to_csv(data, csv_path)

    return render_template('result.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
