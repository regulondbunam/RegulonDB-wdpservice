import sys, os
from datetime import datetime
from flask import render_template, make_response
from app.controllers.citations import Citations
from app.controllers.pdf_utils.sequence_format import SequenceFormat, fasta_format
from app.controllers.pdf_utils import CreatePDF
from app.controllers.web_services import get_RegulonDB_version
from app.controllers.scrap.dtt import DrawingTraceScrap
from app.utiles import errorRegister

def format_pdf_gene(id,gene,gql_service,browser_url):
    file_path = "./cache/" + id + "_pdf_v" + str(1) + ".pdf.cache"
    if not os.path.exists(file_path):
        return createPDf(id,gene,gql_service,browser_url)
    else:
        pdf_file=open(file_path,'rb')
        response = make_response(pdf_file.read())
        pdf_file.close()
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=gene.pdf'
        return response
        

def createPDf(id,gene,gql_service,browser_url):
    citations = None
    sequence = None
    dtt_gene = ""
    #dtt_regulation = ""
    now = datetime.now()
    date = now.strftime("%H:%M:%S %B %d, %Y")
    regulonDB_version = get_RegulonDB_version(gql_service)
    #sequence and allCitations process
    try:
        citations = Citations(gene["data"][0]["allCitations"])
        sequence_format = SequenceFormat(gene["data"][0]["gene"]["sequence"],"")
        sequence = sequence_format.get_genebank_format(False)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        error = f"""on {str(fname)} def createPDF create Citations and Sequence format [{str(exc_tb.tb_lineno)}];{str(e)};type={str(exc_type)}"""
        errorRegister(error)
        print("Error. load allCitations asn format sequence in gene"+str(e))
    #canvas process
    try:
        scrap = DrawingTraceScrap("gene"+id,browser_url,200,800,gene["data"][0]["gene"]["leftEndPosition"]-1000,gene["data"][0]["gene"]["rightEndPosition"]+1000)
        dtt_gene = scrap.get_dtt_svg()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        error = f"""on {str(fname)} def createPDF crate scrap [{str(exc_tb.tb_lineno)}];{str(e)};type={str(exc_type)}"""
        errorRegister(error)
        print("create Canvas"+str(e))
    #pdf rendered
    try:
        rendered = render_template(
                '/ecoli/gene/pdf.html', data=gene["data"][0], date=date, citations=citations, sequence=sequence, fasta_format=fasta_format)
        try:
            pdf = CreatePDF(id,1,rendered,regulonDB_version,dtt_gene)
            pdf_file=open(pdf.file_path,'rb')
            response = make_response(pdf_file.read())
            pdf_file.close()
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = 'inline; filename=gene.pdf'
            return response
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            error = f"""on {str(fname)} def createPDF build pdf [{str(exc_tb.tb_lineno)}];{str(e)};type={str(exc_type)}"""
            errorRegister(error)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        error = f"""on {str(fname)} def createPDF render genePdfTemplate [{str(exc_tb.tb_lineno)}];{str(e)};type={str(exc_type)}"""
        errorRegister(error)
        print("crate Gene Template error: "+str(e))
    return "Internal Error 500 PDF generator"
    