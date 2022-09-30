import os
from datetime import datetime
from urllib import response
from flask import Flask, request, render_template, make_response
from flask_cors import CORS
from sgqlc.endpoint.http import HTTPEndpoint
from app.processes.citations import Citations
from app.processes.ecoli.gene import Gene_collection
from app.processes_HT.ht_process import HTprocess
from app.processes_HT.authorData import formatData_to_json_author_table
from app.ht.dataset.datasets import DatasetsSearch
from app.processes.pdf_utils import CreatePDF
from app.processes.pdf_utils.sequence_format import SequenceFormat


app = Flask(__name__)
CORS(app)
gql_url = os.environ.get("GQL_SERVICE")
gql_service = HTTPEndpoint(gql_url)

UPLOAD_FOLDER = '/cache'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    return render_template('/ecoli/gene/index.html', data=results["data"], pagination=results["pagination"])


@app.route('/wdps/ecoli/gene/<id>/<format>')
def ecoli_gene_id(id, format):
    collection = Gene_collection(gql_service)
    if format == "pdf":
        resp = collection.getGeneById(id, format)
        
        citations = None
        sequence = None
        try:
            citations = Citations(resp["data"][0]["allCitations"])
            sequence_format = SequenceFormat(resp["data"][0]["gene"]["sequence"],"")
            sequence = sequence_format.get_genebank_format(True)
        except Exception as e:
            print("Error. load allCitations in gene"+str(e))
        now = datetime.now()
        date = now.strftime("%H:%M:%S %B %d, %Y")
        rendered = render_template(
            '/ecoli/gene/pdf.html', data=resp["data"][0], date=date, citations=citations, sequence=sequence)
        #pdf_n = pdfkit.from_string(rendered, css=css, options=pdf_options)
        pdf = CreatePDF(id,-1,rendered)
        pdf_file=open(pdf.file_path,'rb')
        response = make_response(pdf_file.read())
        pdf_file.close()
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=gene.pdf'
        return response
    return collection.getGeneById(id, format)


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
