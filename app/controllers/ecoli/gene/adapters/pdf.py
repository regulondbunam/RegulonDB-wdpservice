from datetime import datetime
from flask import Flask, request, render_template, make_response
from app.controllers.citations import Citations
from app.controllers.pdf_utils.sequence_format import SequenceFormat, fasta_format
from app.controllers.pdf_utils import CreatePDF
from app.controllers.web_services import get_RegulonDB_version

def format_pdf_gene(id,gene,gql_service):
    citations = None
    sequence = None
    svg_gene = ""
    svg_regulation = ""
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
        rendered = render_template(
                '/ecoli/gene/pdf.html', data=gene["data"][0], date=date, citations=citations, sequence=sequence, fasta_format=fasta_format)
        try:
            print(rendered)
            pdf = CreatePDF(id,1,rendered,regulonDB_version)
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
    