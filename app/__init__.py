import os
from urllib import response
import pdfkit
from flask import Flask, request, render_template, make_response
from flask_cors import CORS
from sgqlc.endpoint.http import HTTPEndpoint
from app.processes.ecoli.gene import Gene_collection
from app.processes_HT.ht_process import HTprocess
from app.processes_HT.authorData import formatData_to_json_author_table
from app.ht.dataset.datasets import DatasetsSearch

app = Flask(__name__)
CORS(app)
gql_url = os.environ.get("GQL_SERVICE")
gql_service = HTTPEndpoint(gql_url)

UPLOAD_FOLDER = '/cache'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

license = """Data and graphics is available under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0);
additional terms may apply. By using this site, you agree to our terms of use and privacy policy. 
RegulonDB®️ is a registered trademark of CCG-UNAM.
RegulonDB Release 11.0"""

pdf_options = {
'page-size': 'A4',
'margin-top': '1in',
'margin-right': '0in',
'margin-bottom': '0.5in',
'margin-left': '0in',
'encoding': "UTF-8",
'header-html': 'app/templates/header.html',
'footer-font-size': '8',
'footer-center': license,
'custom-header' : [
    ('Accept-Encoding', 'gzip')
],
'no-outline':None
}


@app.route('/')
@app.route('/wdps')
def index():
    return render_template('/home/index.html')

@app.route('/wdps/ecoli')
def ecoli_page():
    return render_template('/ecoli/index.html')

@app.route('/wdps/ecoli/gene')
def ecoli_gene_list():
    collection = Gene_collection(gql_service)
    results = collection.search("RDBECOLI")
    return render_template('/ecoli/gene/index.html', data = results["data"], pagination = results["pagination"])


@app.route('/wdps/ecoli/gene/<id>/<format>')
def ecoli_gene_id(id,format):
    collection = Gene_collection(gql_service)
    if format == "pdf":
        resp = collection.getGeneById(id,format)
        css = "app/static/css/pdf.css"
        rendered = render_template('/ecoli/gene/pdf.html', data = resp["data"][0])
        pdf =  pdfkit.from_string(rendered,css=css, options=pdf_options)
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=gene.pdf'
        return response
    return collection.getGeneById(id,format)
    

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/wdps/<file_format>', methods=['GET', 'POST'])
def ht_datasets(file_format):
    file_format = file_format.lower()
    if request.method == 'POST':
        data_json = request.get_json()
        print(data_json)
        dataset_search = DatasetsSearch(data_json['advancedSearch'], False, gql_service)
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
