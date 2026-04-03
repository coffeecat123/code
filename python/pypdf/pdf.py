import os
from pypdf import PdfWriter

target_path = './input'
output_dir = './output'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

pdf_lst = sorted([os.path.join(target_path, f) for f in os.listdir(target_path) if f.endswith('.pdf')])

if len(pdf_lst) <= 1:
    print("PDF 數量不足，無需合併。")
    exit()

print("wait...")

merger = PdfWriter()
for pdf in pdf_lst:
    try:
        merger.append(pdf)
    except Exception as e:
        print(f"讀取 {pdf} 出錯: {e}")

output_path = os.path.join(output_dir, 'merge.pdf')

if os.path.exists(output_path):
    k = 1
    while os.path.exists(os.path.join(output_dir, f'merge ({k}).pdf')):
        k += 1
    output_path = os.path.join(output_dir, f'merge ({k}).pdf')

with open(output_path, "wb") as f_out:
    merger.write(f_out)

merger.close() 
print('down!')
