from flask import Blueprint, jsonify, render_template, send_from_directory, abort
import os

meme_bp = Blueprint('meme', __name__, url_prefix='/meme')

MEME_DOCS_PATH = os.path.join(os.path.dirname(__file__), '../..', 'docs', 'meme')

# Ruta para listar las categorías principales
@meme_bp.route('/')
def list_main_categories():
    categories = ['all_tfbs', 'confirmed_strong_tfbs']
    return render_template('meme/main.html', categories=categories)

# Ruta para listar documentos en una categoría específica
@meme_bp.route('/<category>/')
def list_category(category):
    category_path = os.path.join(MEME_DOCS_PATH, category)
    if not os.path.exists(category_path):
        abort(404)
    
    directories = [d for d in os.listdir(category_path) if os.path.isdir(os.path.join(category_path, d))]
    return render_template('meme/category_list.html', category=category, directories=directories)

# Ruta para listar el contenido de un tfbs específico
@meme_bp.route('/<category>/<tfbs>/')
def list_tfbs_content(category, tfbs):
    tfbs_path = os.path.join(MEME_DOCS_PATH, category, tfbs)
    if not os.path.exists(tfbs_path):
        abort(404)

    files = os.listdir(tfbs_path)
    return render_template('meme/tfbs_list.html', category=category, tfbs=tfbs, files=files)

# Ruta para descargar un archivo específico
@meme_bp.route('/<category>/<tfbs>/<filename>')
def download_file(category, tfbs, filename):
    tfbs_path = os.path.join(MEME_DOCS_PATH, category, tfbs)
    if not os.path.exists(os.path.join(tfbs_path, filename)):
        abort(404)

    return send_from_directory(tfbs_path, filename, as_attachment=True)