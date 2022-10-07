from ast import keyword
import os
from selenium import webdriver
from datetime import datetime
from flask import Flask, request, render_template, make_response, send_from_directory
from flask_cors import CORS
from sgqlc.endpoint.http import HTTPEndpoint
from app.processes.citations import Citations
from app.processes.ecoli.gene import Gene_collection
from app.processes_HT.ht_process import HTprocess
from app.ht.dataset.datasets import DatasetsSearch
from app.processes.pdf_utils import CreatePDF
from app.processes.pdf_utils.sequence_format import SequenceFormat, fasta_format
from app.processes.web_services import get_RegulonDB_version


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
def ecoli_gene_list(collection_name):
    template = "no collection support"
    header_animation = True
    if collection_name == "gene":
        if request.method == 'POST':
            keyword = request.form['keyword']
            collection = Gene_collection(gql_service)
            results = collection.search(keyword)
            header_animation = False
            template =render_template('/ecoli/gene/index.html', data=results["data"], pagination=results["pagination"], search_result=keyword, header_animation=header_animation)
        else:
            collection = Gene_collection(gql_service)
            results = collection.search("RDBECOLI")
            template =render_template('/ecoli/gene/index.html', data=results["data"], pagination=results["pagination"], search_result="", header_animation=header_animation)
    return template

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
            sequence = sequence_format.get_genebank_format(False)
            product_sequence = SequenceFormat()
        except Exception as e:
            print("Error. load allCitations in gene"+str(e))
        now = datetime.now()
        date = now.strftime("%H:%M:%S %B %d, %Y")
        rendered = render_template(
            '/ecoli/gene/pdf.html', data=resp["data"][0], date=date, citations=citations, sequence=sequence, fasta_format=fasta_format)
        #pdf_n = pdfkit.from_string(rendered, css=css, options=pdf_options)
        regulonDB_version = get_RegulonDB_version(gql_service)
        pdf = CreatePDF(id,-1,rendered,regulonDB_version)
        pdf_file=open(pdf.file_path,'rb')
        response = make_response(pdf_file.read())
        pdf_file.close()
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=gene.pdf'
        return response
    return collection.getGeneById(id, format)

@app.route('/wdps/ecoli/dtt')
def dtt():
    url = "https://www.google.com/"
    driver = webdriver.Chrome(executable_path="app/static/drivers/chromedriver")
    driver.get(url)
    page = driver.page_source
    print(driver.page_source)
    driver.quit()
    return page

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