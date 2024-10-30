from flask import Flask, request, jsonify, render_template, send_file
from PIL import Image
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_images():
    if 'images' not in request.files:
        return jsonify({"error": "No files uploaded"}), 400

    files = request.files.getlist('images')
    results = []

    for file in files:
        image = Image.open(file.stream)
        text = pytesseract.image_to_string(image).lower()
        words = text.split()
        results.append({
            "words": words,
            "text": text
        })

    return jsonify(results)

# Novo endpoint para download
@app.route('/download', methods=['POST'])
def download_sorted_words():
    data = request.get_json()
    sorted_words = data.get("sortedWords")

    # Cria um arquivo temporário com as palavras ordenadas
    file_path = "sorted_words.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("\n".join(sorted_words))

    # Retorna o arquivo para download
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
