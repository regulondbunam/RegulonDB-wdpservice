from flask import Blueprint, jsonify, render_template, send_from_directory, abort, request
import os

meme_bp = Blueprint('meme', __name__, url_prefix='/wdps/meme')

MEME_DOCS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'docs', 'meme'))

def is_path_safe(base_directory, target_path):
    return os.path.commonpath([base_directory]) == os.path.commonpath([base_directory, target_path])

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

# Ruta única para ver o descargar un archivo específico
@meme_bp.route('/<category>/<tfbs>/<filename>')
def handle_file(category, tfbs, filename):
    tfbs_path = os.path.join(MEME_DOCS_PATH, category, tfbs)
    file_path = os.path.abspath(os.path.join(tfbs_path, filename))
    
    if not os.path.exists(file_path) or not is_path_safe(MEME_DOCS_PATH, file_path):
        abort(404)

    # Determinar si la solicitud debe ver o descargar el archivo
    if request.args.get('download') == 'true':
        return send_from_directory(tfbs_path, filename, as_attachment=True)
    else:
        return send_from_directory(tfbs_path, filename)

# Nueva ruta para devolver el contenido del directorio del proyecto en formato JSON
@meme_bp.route('/directory_content', methods=['GET'])
def directory_content():
    content = {}
    for category in ['all_tfbs', 'confirmed_strong_tfbs']:
        category_path = os.path.join(MEME_DOCS_PATH, category)
        if os.path.exists(category_path):
            content[category] = os.listdir(category_path)
    return jsonify(content)

# Nueva ruta para acceder al README.md
@meme_bp.route('/readme', methods=['GET'])
def readme():
    readme_path = os.path.join(MEME_DOCS_PATH, 'README.md')
    if not os.path.exists(readme_path):
        abort(404)
    
    return send_from_directory(MEME_DOCS_PATH, 'README.md')