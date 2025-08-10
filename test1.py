import requests
import os
import streamlit as st
import pandas as pd
import errno
import pdfplumber

st.write("Upload your pdf with links")
file = st.file_uploader("Pick a file",type=["csv","xlsx"])
if file is not None:
    if file.name.endswith(".csv"):
        df=pd.read_csv(file)
    elif file.name.endswith(".xlsx"):
        df=pd.read_excel(file)

try:
    os.makedirs(r"C:\Users\yashw\Onedrive\Desktop\downloaded_pdfs")
except OSError as e:
    if e.errno != errno.EEXIST:
        raise 
#os.mkdir(r"C:\Users\yashw\Onedrive\Desktop\downloaded_pdfs", exist_ok=True)

for i in range(len(df)):
    url = df.loc[i, 'PDF_URL']
    sn = df.loc[i, 'Sl.No']
    name = "file_" + str(sn) + ".pdf"
    path = r"C:\Users\yashw\Onedrive\Desktop\downloaded_pdfs/" + name

    print("Downloading:",name)
    r = requests.get(url)
    with open(path, "wb") as f:
      f.write(r.content)
#st.write(df.head())

try:
    os.makedirs(r"C:\Users\yashw\Onedrive\Desktop\extracted_texts")
except OSError as e:
    if e.errno != errno.EEXIST:
        raise 

page_counts = {}
char_counts = {}

if st.button("show analytics"):
    for i in os.listdir(r"C:\Users\yashw\Onedrive\Desktop\downloaded_pdfs/"):
        pdf_path = os.path.join(r"C:\Users\yashw\Onedrive\Desktop\downloaded_pdfs/", i)
        txt_path = os.path.join(r"C:\Users\yashw\Onedrive\Desktop\extracted_texts", i.replace(".pdf", ".txt"))

        reader = pdfplumber.open(pdf_path)
        num_pages = len(reader.pages)
        page_counts[i] = num_pages
        text = ""
        for page in reader.pages:
            text += page.extract_text()

        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)
            char_counts[i] = len(text)

        #print(i + " success")
    pages_series = pd.Series(page_counts, name="Pages").sort_values(ascending=False)
    st.bar_chart(pages_series, x_label="Number of Pages in Each PDF", y_label="Pages")

    chars_series= pd.Series(char_counts, name="Chars").sort_values(ascending=False)
    st.bar_chart(chars_series,x_label="Number of Text Characters in Each PDF",y_label="Characters")
else:
    st.write("Button not clicked yet")