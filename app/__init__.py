import os
import ssl
from flask import Flask, Response, send_file, request, render_template, make_response, jsonify
from flask_cors import CORS
from sgqlc.endpoint.http import HTTPEndpoint
from app.controllers.ecoli.gene import Gene_collection
from app.processes_HT.ht_process import HTprocess
from app.ht.dataset.datasets import DatasetsSearch
from app.controllers.ecoli import collection_list


app = Flask(__name__)
CORS(app)
gql_url = os.environ.get("GQL_SERVICE")
browser_url = os.environ.get("REGULONDB_BROWSER")

gql_service = HTTPEndpoint(gql_url)
ssl._create_default_https_context = ssl._create_unverified_context

UPLOAD_FOLDER = '/cache'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/wdps')
def index():
    return render_template('/home/index.html')

# MEME collection
# @app.route('/wdps/meme', defaults={'collection': None, 'tf': None, 'file_name': None})


@app.route('/wdps/meme/')
def meme_dir():
    route_script = __file__
    abs = os.path.dirname(os.path.abspath(route_script))
    dir = abs.replace("app", "docs")+'/meme/'
    try:
        fileList = os.listdir(dir)
        return render_template('dir.html', list=fileList, url="/wdps/meme/")
    except Exception as e:
        return "file no found"

@app.route('/wdps/metadata/meme/')
def meme_metadata_dir():
    route_script = __file__
    abs = os.path.dirname(os.path.abspath(route_script))
    dir = abs.replace("app", "docs")+'/meme/'
    try:
        fileList = os.listdir(dir)
        dirData = []
        url="/wdps/metadata/meme/"
        for file in fileList:
            dirData.append({
               "label": file,
               "url": url+file 
            })
        return jsonify(dirData)
    except Exception as e:
        print(e)
        return "file no found"


@app.route('/wdps/meme/<collection>')
def meme_collection(collection):
    route_script = __file__
    abs = os.path.dirname(os.path.abspath(route_script))
    dir = abs.replace("app", "docs")+'/meme/'+collection
    try:
        fileList = os.listdir(dir)
        return render_template('dir.html', list=fileList, url="/wdps/meme/"+collection+'/')
    except Exception as e:
        return "file no found"

@app.route('/wdps/metadata/meme/<collection>')
def meme_metadata_collection(collection):
    route_script = __file__
    abs = os.path.dirname(os.path.abspath(route_script))
    dir = abs.replace("app", "docs")+'/meme/'
    try: 
        url_file = os.path.join(dir, collection)
        if os.path.isfile(url_file):
            with open(url_file, 'r') as file:
                content = file.read()
                return content
        elif os.path.isdir(url_file):
            url="/wdps/metadata/meme/"+collection+"/"
            fileList = os.listdir(url_file)
            dirData = []
            
            for file in fileList:
                dirData.append({
                "label": file,
                "url": url+file 
                })
            
            return jsonify(dirData)
        else:
            return f"{collection} no existe."
    except Exception as e:
        print(e)
        return "file no found"


@app.route('/wdps/meme/<collection>/<tf>')
def meme_collection_tf(collection, tf):
    route_script = __file__
    abs = os.path.dirname(os.path.abspath(route_script))
    dir = abs.replace("app", "docs")+'/meme/'+collection+'/'+tf
    try:
        fileList = os.listdir(dir)
        return render_template('dir.html', list=fileList, url="/wdps/meme/"+collection+'/'+tf+'/')
    except Exception as e:
        return "file no found"

@app.route('/wdps/metadata/meme/<collection>/<tf>')
def meme_metadata_tf(collection, tf):
    route_script = __file__
    abs = os.path.dirname(os.path.abspath(route_script))
    dir = abs.replace("app", "docs")+'/meme/'+collection
    try:
        url_file = os.path.join(dir, tf)
        if os.path.isfile(url_file):
            with open(url_file, 'r') as file:
                content = file.read()
                return content
        elif os.path.isdir(url_file):
            url="/wdps/meme/"+collection+"/"+tf+"/"
            fileList = os.listdir(url_file)
            dirData = []
            
            for file in fileList:
                dirData.append({
                "label": file,
                "url": url+file 
                })
            
            return jsonify(dirData)
        else:
            return f"{collection} no existe."
    except Exception as e:
        print(e)
        return "file no found"

@app.route('/wdps/meme/<collection>/<tf>/<file_name>')
def meme_file(collection, tf, file_name):
    route_script = __file__
    abs = os.path.dirname(os.path.abspath(route_script))
    dir = abs.replace("app", "docs")+'/meme/'+collection+'/'+tf+'/'
    file_index = os.path.join(dir, file_name)
    try:
        if os.path.exists(file_index):
            extension = os.path.splitext(file_name)[1]
            with open(file_index, 'r') as file:
                content = file.read()
                print(extension)
                if extension == ".html":
                    return content
                elif extension == ".xml":
                    return Response(
                        content, content_type='application/xml')
                else:
                    return f'<html><body><pre>{content}</pre></body></html>'
        else:
            return "file no found"
    except Exception as e:
        print(e)
        return "file no found"


# FLASK styles
@app.route('/wdps/static/<type>/<file_name>')
def static_file(type, file_name):
    ruta_script = __file__
    dir_absoluto = os.path.dirname(os.path.abspath(ruta_script))
    dir = dir_absoluto+'/static/'+type+'/'
    path = os.path.join(dir, file_name)
    print(path)
    if os.path.exists(path):
        return send_file(path, as_attachment=True, download_name=file_name)
    else:
        return "file no found"

# Ecoli routes and apps


@app.route('/wdps/ecoli')
def ecoli_page():
    return render_template('/ecoli/index.html')


@app.route('/wdps/ecoli/<collection_name>', methods=["GET", "POST"])
def ecoli_collection_list(collection_name):
    return collection_list(collection_name, gql_service, browser_url)


@app.route('/wdps/ecoli/gene/<id>/<format>')
def ecoli_gene_id(id, format):
    collection = Gene_collection(gql_service, browser_url)
    return collection.getGeneById(id, format)


@app.route('/wdps/ecoli/dtt/<format>/<variables>')
def dtt(format, variables):

    return "image"

# HT routes and apps


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/wdps/<file_format>', methods=['GET', 'POST'])
def ht_datasets(file_format):
    file_format = file_format.lower()
    if request.method == 'POST':
        data_json = request.get_json()
        print(data_json)
        dataset_search = DatasetsSearch(
            data_json['advancedSearch'], False, gql_service)
        dataset_search.get_data(file_format)
        return dataset_search.response
    return '''
        what?
        '''


@app.route('/wdps/<id_dataset>/<data_type>/<file_format>')
def process_ht(id_dataset, data_type, file_format):
    data_type = data_type.lower()
    ht_process = HTprocess(id_dataset, gql_service)
    response = 'error a'
    valid_types = ["sites", "peaks", "tus", "tts", "tss", "ge"]
    if data_type == 'authordata':
        ht_process.author_data(file_format)
        return ht_process.get_response()
    elif data_type in valid_types:
        ht_process.get_data(file_format, data_type)
        return ht_process.get_response()
    return response


'''
@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)
'''
