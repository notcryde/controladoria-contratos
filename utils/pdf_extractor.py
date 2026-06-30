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


# import os

# AUTHORIZATION_ITEMS = {
#     'material_code': r'^\d+\s+([\d.]+)',
#     'qquantity': r'^\d+\s+[\d.]+\s+([\d.,]+)',
#     'description': r'^\d+\s+[\d.]+\s+[\d.,]+\s+[A-Za-z]+\s+(.*?)\s+[\d.,]+\s+(?:.*?\s+)?[\d.,]+\s*$',
#     'unitary_value': r'([\d.,]+)\s+[\d.,]+\s*$',
# }


# def output_test(opt=1):
#     file_name = 'af.pdf'
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     root_dir = os.path.dirname(current_dir)
#     file_path = os.path.join(root_dir, 'samples', file_name)

#     raw_text = extract_text_from_pdf(file_path)

#     items = extract_items(raw_text, AUTHORIZATION_ITEMS)

#     if opt == 1:
#         print(f'{'Código':<15} | {'Qtd':<10} | {'Valor Unit.':<12} | {'Descrição'}')
#         print('-' * 80)

#         for item in items:
#             print(f'{item.get('material_code') or '':<15} | '
#                 f'{item.get('qquantity') or '':<10} | '
#                 f'{item.get('unitary_value') or '':<12} | '
#                 f'{item.get('description') or ''}')
#     else:
#         print(raw_text)

# output_test(1)