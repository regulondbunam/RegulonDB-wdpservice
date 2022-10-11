from datetime import datetime
from logging import exception
from flask import Flask, request, render_template, make_response
from app.controllers.citations import Citations
from app.controllers.pdf_utils.sequence_format import SequenceFormat, fasta_format
from app.controllers.pdf_utils import CreatePDF
from app.controllers.web_services import get_RegulonDB_version
from app.controllers.scrap.dtt import DrawingTraceScrap

def format_pdf_gene(id,gene,gql_service,browser_url):
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
        print("Error. load allCitations asn format sequence in gene"+str(e))
    #canvas process
    try:
        scrap = DrawingTraceScrap("gene"+id,browser_url,200,800,gene["data"][0]["gene"]["leftEndPosition"]-1000,gene["data"][0]["gene"]["rightEndPosition"]+1000)
        dtt_gene = scrap.get_dtt_svg()
    except Exception as e:
            print("create Canvas"+str(e))
    #pdf rendered
    try:
        rendered = render_template(
                '/ecoli/gene/pdf.html', data=gene["data"][0], date=date, citations=citations, sequence=sequence, fasta_format=fasta_format)
        try:
            pdf = CreatePDF(id,-1,rendered,regulonDB_version,dtt_gene)
            pdf_file=open(pdf.file_path,'rb')
            response = make_response(pdf_file.read())
            pdf_file.close()
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = 'inline; filename=gene.pdf'
            return response
        except Exception as e:
            print("PDF compile "+str(e))
    except Exception as e:
        print("crate Gene Template error: "+str(e))
    return "Internal Error 500 PDF generator"
    