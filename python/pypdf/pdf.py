import os
from pypdf import PdfWriter

target_path = './input'
pdf_lst = [os.path.join(target_path, f) for f in os.listdir(target_path) if f.endswith('.pdf')]
if len(pdf_lst) <= 1:
    exit()

print("wait...")

pdf_writer = PdfWriter()
for pdf in pdf_lst:
    pdf_writer.append(pdf)

output_path = './output/merge.pdf'

if os.path.isfile(output_path):
    k = 1
    while os.path.isfile(f'./output/merge ({k}).pdf'):
        k += 1
    output_path = f'./output/merge ({k}).pdf'

with open(output_path, 'wb') as f:
    pdf_writer.write(f)

print('down!')
