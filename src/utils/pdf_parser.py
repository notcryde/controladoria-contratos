import pdfplumber
import re

def extract_text_from_pdf(pdf_file):
    extracted_text = ''
    with pdfplumber.open(pdf_file) as pdf_document:
        for pdf_page in pdf_document.pages:
            page_text = pdf_page.extract_text()
            if page_text:
                extracted_text += page_text + '\n'
    return extracted_text

def extract_data_using_regex(pdf_text, regex_patterns):
    extracted_data = {}
    for key, pattern in regex_patterns.items():
        regex_match = re.search(pattern, pdf_text)
        if regex_match:
            extracted_value = regex_match.group(1).strip()
            if key == 'Unidade Solicitante':
                extracted_value = re.sub(r'\s+', ' ', extracted_value)
            extracted_data[key] = extracted_value
        else:
            extracted_data[key] = None
    return extracted_data

def process_files(uploaded_files, regex_patterns, save_document, table_name, extra_data=None):
    if extra_data is None:
        extra_data = {}
        
    for pdf_file in uploaded_files:
        pdf_text = extract_text_from_pdf(pdf_file)
        extracted_data = extract_data_using_regex(pdf_text, regex_patterns)
        
        extracted_data.update(extra_data)
        save_document(table_name, extracted_data)