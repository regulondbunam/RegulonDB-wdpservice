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

    def __init__(self, id: str, version, rendered):
        self.file_path = "./cache/" + id + "_pdf_v" + str(version) + ".pdf.cache"
        if os.path.exists(self.file_path) and version != -1:
            self.add_header()
        else:
            pdfkit.from_string(rendered, self.file_path, css=self.css, options=self.pdf_options)
            self.add_header()
            

    def add_header(self):
        header_text = "RegulonDB encabezado XD"
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
            # Draw footer
            canvas.saveState()
            canvas.setFont('Times-Roman', 17)

            # add text in the x,y coordinates of interest
            canvas.drawString(50, 820, header_text)
            canvas.restoreState()
            canvas.showPage()
        canvas.save()

    def add_pdf_footer(self):
        footer_text = "Pie de pagina ajskndajsnhdajnsd"
        # Get pages
        reader = PdfReader(self.pdf)
        pages = [pagexobj(p) for p in reader.pages]
        # Compose new pdf
        canvas = Canvas(self.pdf)
        for page_num, page in enumerate(pages, start=1):
            # Add page
            canvas.setPageSize((page.BBox[2], page.BBox[3]))
            canvas.doForm(makerl(canvas, page))
            canvas.saveState()
            canvas.setStrokeColorRGB(0, 0, 0)

            # draw a footer line
            canvas.setLineWidth(0.5)
            canvas.line(66, 78, page.BBox[2] - 66, 78)
            canvas.setFont('Times-Roman', 8)

            # add footer text using x,y coordinates
            canvas.drawString(0, 0, footer_text)
            canvas.restoreState()
            canvas.showPage()
        canvas.save()
        return self.pdf
