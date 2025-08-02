from pypdf import PdfReader

def read_pdf_lines_pypdf2(pdf_path):
    with open(pdf_path, 'rb') as pdf_file_obj:
        pdf_reader = PdfReader(pdf_file_obj)
        for page_num in range(len(pdf_reader.pages)):
            page_obj = pdf_reader.get_page(page_num)
            text = page_obj.extract_text()
            if text:  # Ensure text was extracted


                lines = text.splitlines()
                for line in lines:
                    print("LINE START : ")
                    print(line)
                    print("LINE END : ")
            break

    # Example usage:


read_pdf_lines_pypdf2("../../../../docs/caffeine_on_health.pdf")

print("*********************************")
print("*************IRONMAN!************")
print("*********************************")

from unstructured.partition.auto import partition

import time
s = time.time()
elements = partition("../../../../docs/caffeine_on_health.pdf")

print("\n\n".join([str(el) for el in elements[:10]]))

print((time.time() - s) * 1000)
