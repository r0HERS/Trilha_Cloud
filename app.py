import os
from flask import Flask, request, redirect, url_for, render_template
from PIL import Image, ImageFilter
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESSED_FOLDER'] = 'static/processed'  # Alteração para garantir que processed esteja em static

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

# Mapeamento dos filtros
FILTERS = {
    'BLUR': ImageFilter.BLUR,
    'CONTOUR': ImageFilter.CONTOUR,
    'DETAIL': ImageFilter.DETAIL,
    'EDGE_ENHANCE': ImageFilter.EDGE_ENHANCE,
    'SHARPEN': ImageFilter.SHARPEN
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        # Salvar o arquivo enviado
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Obter o filtro selecionado
        filter_type = request.form.get('filter', 'BLUR')  # Filtro padrão é BLUR
        selected_filter = FILTERS.get(filter_type, ImageFilter.BLUR)

        # Carregar e aplicar o filtro na imagem
        img = Image.open(filepath)
        img = img.filter(selected_filter)

        # Salvar a imagem processada na pasta 'static/processed'
        processed_filename = 'processed_' + filename
        processed_path = os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)
        img.save(processed_path)

        # Gerar o URL para a imagem processada
        processed_image_url = url_for('static', filename='processed/' + processed_filename)

        return render_template('index.html', processed_image_url=processed_image_url)

if __name__ == '__main__':
    app.run(debug=True)
