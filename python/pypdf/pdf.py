import os

target_path = './pdfs'
pdf_lst = [f for f in os.listdir(target_path) if f.endswith('.pdf')]
pdf_lst = [os.path.join(target_path, filename) for filename in pdf_lst]
if(len(pdf_lst)<=1):
    exit()
print("wait...")

from PyPDF2 import PdfFileMerger

file_merger = PdfFileMerger()
for pdf in pdf_lst:
    file_merger.append(pdf)

if(os.path.isfile("./merge.pdf")==0):
    file_merger.write("./merge.pdf")
else:
    k=1
    while(os.path.isfile('./merge ('+str(k)+').pdf')):
        k+=1
    file_merger.write('./merge ('+str(k)+').pdf')
