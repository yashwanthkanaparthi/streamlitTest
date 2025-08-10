import streamlit as st
import pdfplumber
from groq import Groq

st.write("Upload your pdf")
file = st.file_uploader("Pick a file",type=["pdf"])

reader=pdfplumber.open(file)
pdf_text=""
for i in range(3):
    pdf_text += reader.pages[i].extract_text()

client = Groq(api_key="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")
model = "llama-3.3-70b-versatile"

prompt = "Summarize the research findings from this academic paper:\n\n" + pdf_text
response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": "You are a research assistant."},
        {"role": "user", "content": prompt}
    ]
)

st.write(response.choices[0].message.content)

if st.button("Extract Title"):
    title_prompt= "Show the title of this research paper:\n\n " + pdf_text
    title_response=client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": "You are a research assistant."},
        {"role": "user", "content": title_prompt}
    ])
    st.write(title_response.choices[0].message.content)

elif st.button("Extract Authors"):
    author_prompt="Show the author information of this research paper:\n\n " + pdf_text
    author_response=client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": "You are a research assistant."},
        {"role": "user", "content": author_prompt}
    ])

    st.write(author_response.choices[0].message.content)

elif st.button("Extract abstract"):
    abstract_prompt="Show the abstract information of this research paper:\n\n " + pdf_text
    abstract_response=client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": "You are a research assistant."},
        {"role": "user", "content": abstract_prompt}
    ])
    st.write(abstract_response.choices[0].message.content)
else:
    pass