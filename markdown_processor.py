# app/markdown_processor.py
import fitz  # PyMuPDF

def display_markdown(content):
    """Display Markdown content in Streamlit"""
    import streamlit as st
    st.markdown(content)

def parse_markdown(file):
    """Extract text from a Markdown file or PDF"""
    if file.type == "application/pdf":
        return extract_text_from_pdf(file)
    elif file.type in ["text/markdown", "text/plain"]:
        return file.read().decode("utf-8")
    else:
        raise ValueError("Unsupported file type")

def extract_text_from_pdf(file):
    """Extract text from a PDF file, processing in manageable chunks"""
    import io
    text = ""
    with io.BytesIO(file.read()) as pdf_file:
        pdf_document = fitz.open(stream=pdf_file, filetype="pdf")
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
    return text