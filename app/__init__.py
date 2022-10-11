import os

from flask import Flask, request, render_template, make_response
from flask_cors import CORS
from sgqlc.endpoint.http import HTTPEndpoint
from app.processes.citations import Citations
from app.controllers.ecoli.gene import Gene_collection
from app.processes_HT.ht_process import HTprocess
from app.ht.dataset.datasets import DatasetsSearch
from app.controllers.ecoli import collection_list


app = Flask(__name__)
CORS(app)
gql_url = os.environ.get("GQL_SERVICE")
browser_url = os.environ.get("REGULONDB_BROWSER")

gql_service = HTTPEndpoint(gql_url)

UPLOAD_FOLDER = '/cache'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/wdps')
def index():
    return render_template('/home/index.html')

#Ecoli routes and apps
@app.route('/wdps/ecoli')
def ecoli_page():
    return render_template('/ecoli/index.html')

@app.route('/wdps/ecoli/<collection_name>', methods=["GET", "POST"])
def ecoli_collection_list(collection_name):
    return collection_list(collection_name, gql_service)

@app.route('/wdps/ecoli/gene/<id>/<format>')
def ecoli_gene_id(id, format):
    collection = Gene_collection(gql_service,browser_url)
    return collection.getGeneById(id, format)
  
@app.route('/wdps/ecoli/dtt/<format>/<variables>')
def dtt(format,variables):
    
    return "image"

#HT routes and apps

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