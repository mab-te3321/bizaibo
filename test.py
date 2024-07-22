# from tika import parser # pip install tika

# raw = parser.from_file(r'C:\Users\MAB\Downloads\518368 PL.pdf')
# print(raw['content'])
from pypdf import PdfReader

reader = PdfReader(r'C:\Users\MAB\Downloads\518368 PL.pdf')
text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"
print(text)
