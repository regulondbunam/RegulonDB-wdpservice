from operator import is_not
import os
import pdfkit
from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from reportlab.pdfgen.canvas import Canvas


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

    def __init__(self, id: str, version, rendered):
        self.file_path = "./cache/" + id + "_pdf_v" + str(version) + ".pdf.cache"
        if os.path.exists(self.file_path) and version != -1:
            self.add_header()
        else:
            pdfkit.from_string(rendered, self.file_path, css=self.css, options=self.pdf_options)
            self.add_header()
            

    def add_header(self):
        # read pdf using pdfrw
        reader = PdfReader(self.file_path)
        pages = [pagexobj(p) for p in reader.pages]
        # Compose new pdf
        canvas = Canvas(self.file_path)
        for page_num, page in enumerate(pages, start=1):
            # Add page with the page size
            # Here BBox denotes a bounding box
            canvas.setPageSize((page.BBox[2], page.BBox[3]))

            # make a report lab object
            canvas.doForm(makerl(canvas, page))
            canvas.saveState()
            canvas.setFont('Times-Roman', 14)

            # add text in the x,y coordinates of interest
            canvas.drawCentredString(297, 820, "RegulonDB Database")
            canvas.drawCentredString(297, 806, "Escherichia coli")
            
            # Draw ccg logo 
            canvas.drawImage(self.ccg_logo,450,790,100,50,preserveAspectRatio=True)
            #Draw regulonDB Logo
            canvas.drawImage(self.regulondb_logo,40,790,100,50,preserveAspectRatio=True)
            
            #Add footer
            canvas.setFont('Times-Roman', 8)
            canvas.drawCentredString(297, 50, "Data and graphics is available under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0);")
            canvas.drawCentredString(297, 42, "additional terms may apply. By using this site, you agree to our terms of use and privacy policy. RegulonDB® is a registered trademark of CCG-UNAM.")
            canvas.drawCentredString(297, 34, "RegulonDB Release 11.0")
            
            canvas.restoreState()
            canvas.showPage()
        canvas.save()

