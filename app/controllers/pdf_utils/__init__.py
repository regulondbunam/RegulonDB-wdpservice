import io
import os
import pdfkit
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4


class CreatePDF:

    pdf_options = {
        'page-size': 'A4',
        'margin-top': '1in',
        'margin-right': '0in',
        'margin-bottom': '1in',
        'margin-left': '0in',
        'encoding': "UTF-8",
        'no-outline': None
    }
    
    css = "app/static/css/pdf.css"
    ccg_logo = "app/static/img/ccg_logo.jpg"
    regulondb_logo = "app/static/img/regulondb_logo.jpg"
    

    def __init__(self, id: str, version, rendered, rdb_version, dtt_gene):
        self.rdb_version = rdb_version
        self.path_dtt_gene = dtt_gene
        self.fileTemp_path = "./cache/_temp_" + id + "_pdf_v" + str(version) + ".pdf.cache"
        self.file_path = "./cache/" + id + "_pdf_v" + str(version) + ".pdf.cache"
        if not os.path.exists(self.file_path) or version == -1:
            pdfkit.from_string(rendered, self.fileTemp_path, css=self.css, options=self.pdf_options)
            self.addLayout()
            
    
    def addLayout(self):
        packet = io.BytesIO()
        canvas = Canvas(packet, pagesize=A4)
        
        canvas.setFont('Times-Roman', 14)
        # add text in the x,y coordinates of interest
        canvas.drawCentredString(297, 800, "RegulonDB Database")
        canvas.drawCentredString(297, 786, "Escherichia coli")
        
        # Draw logos 
        canvas.drawImage(self.ccg_logo,450,770,100,50,preserveAspectRatio=True)
        canvas.drawImage(self.regulondb_logo,40,770,100,50,preserveAspectRatio=True)
        canvas.drawImage(self.path_dtt_gene,0,600,400,200,preserveAspectRatio=True)
        
        #Add footer
        canvas.setFont('Times-Roman', 8)
        canvas.drawCentredString(297, 50, "Data and graphics is available under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0);")
        canvas.drawCentredString(297, 42, "additional terms may apply. By using this site, you agree to our terms of use and privacy policy. RegulonDB® is a registered trademark of CCG-UNAM.")
        canvas.drawCentredString(297, 34, "RegulonDB Release"+self.rdb_version)
        
        canvas.save()
        packet.seek(0)
        pdf_layout = PdfFileReader(packet)
        pdf_info = PdfFileReader(open(self.fileTemp_path, "rb"))
        output = PdfFileWriter()
        
        num_pages = pdf_info.getNumPages()
        for num_page in range(0,num_pages):
            page = pdf_info.getPage(num_page)
            page.mergePage(pdf_layout.getPage(0))
            output.addPage(page)
        outputStream = open(self.file_path,'wb')
        output.write(outputStream)
        outputStream.close()
        os.remove(self.fileTemp_path)
        os.remove(self.path_dtt_gene)
        

