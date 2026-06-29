import re
import pdfplumber
import logging
from typing import Dict, List, Any

def extract_text_from_pdf(pdf_file) -> str:
    full_text = ''
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    full_text += extracted + '\n'
        return full_text
    except Exception as e:
        logging.error(f'Erro ao processar PDF: {e}')
        return ''

def extract_data(text: str, patterns: Dict[str, str]) -> Dict[str, Any]:
    extracted_data = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            extracted_data[key] = match.group(1).strip()
        else:
            extracted_data[key] = None
    return extracted_data

def extract_items(text: str, item_patterns: Dict[str, str]) -> List[Dict[str, Any]]:
    items_list = []
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        item_data = {}
        all_matched = True
        
        for key, pattern in item_patterns.items():
            match = re.search(pattern, line)
            if match:
                item_data[key] = match.group(1).strip()
            else:
                all_matched = False
                break
                
        if all_matched:
            items_list.append(item_data)
            
    return items_list