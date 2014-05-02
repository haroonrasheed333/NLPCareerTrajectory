# import os
#
#
# filename = 'Resume_HaroonRasheedPaulMohamed.pdf'
# # os.system("pdftotext -layout " + filename)
# # raw_input("Finished")
#
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

def convert_pdf_to_txt(filename):
    resource_manager = PDFResourceManager()
    return_string = StringIO()
    la_params = LAParams()
    device = TextConverter(resource_manager, return_string, codec='utf-8', laparams=la_params)
    fp = file(filename, 'rb')
    interpreter = PDFPageInterpreter(resource_manager, device)
    page_nos=set()
    for page in PDFPage.get_pages(fp, page_nos):
        interpreter.process_page(page)
    fp.close()
    device.close()
    text = return_string.getvalue()
    return_string.close()
    return text

strr =  convert_pdf_to_txt('HaroonRasheed_Resume.pdf')
with open('test_save.txt', 'wb') as outfile:
    outfile.write(strr)

