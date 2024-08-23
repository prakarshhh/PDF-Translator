# app/translator.py
from transformers import MarianMTModel, MarianTokenizer
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from googletrans import Translator
def load_translation_model(source_lang="en", target_lang="fr"):
    model_name = f"Helsinki-NLP/opus-mt-{source_lang}-{target_lang}"
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    return tokenizer, model

def translate_text_chunk(chunk, tokenizer, model):
    inputs = tokenizer(chunk, return_tensors="pt", padding=True, truncation=True)
    translated_tokens = model.generate(**inputs)
    return tokenizer.decode(translated_tokens.squeeze(), skip_special_tokens=True)

def translate_chunks(chunks, tokenizer, model):
    with ThreadPoolExecutor(max_workers=4) as executor:
        translated_chunks = list(executor.map(lambda chunk: translate_text_chunk(chunk, tokenizer, model), chunks))
    return ''.join(translated_chunks)

def split_text(content, chunk_size=1000):
    """Splits text into chunks of specified size"""
    return [content[i:i + chunk_size] for i in range(0, len(content), chunk_size)]

def translate_markdown(content, target_language):
    source_lang = "en"  # Assuming the source language is English
    tokenizer, model = load_translation_model(source_lang, target_language)
    
    chunks = split_text(content, chunk_size=1000)  # Adjust chunk size as needed
    translated_content = translate_chunks(chunks, tokenizer, model)
    return translated_content
def parse_pdf_with_formatting(file):
    # Open the PDF file
    doc = fitz.open(stream=file.read(), filetype="pdf")
    content = ""

    # Iterate through the pages and extract text as HTML
    for page in doc:
        text = page.get_text("html")  # Extract text as HTML to retain formatting
        content += text
    
    return content
