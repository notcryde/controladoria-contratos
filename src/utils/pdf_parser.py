import pdfplumber
import re
from src.utils.database import save_items_notas_fiscais, save_autorizacoes_fornecimento_items, load_data

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

def extract_nf_items_from_text(pdf_text, regex_items, numero_nf):
    items = []
    for line in pdf_text.split('\n'):
        if not re.match(r'^\d+\s+', line.strip()):
            continue
            
        item_data = {'Nº NF': numero_nf}
        for key, pattern in regex_items.items():
            match = re.search(pattern, line)
            if match:
                item_data[key] = match.group(1).strip()
            else:
                item_data[key] = None
                
        if item_data.get('Cód. Material'):
            items.append(item_data)
            
    return items

def extract_af_items_from_text(pdf_text, regex_items, numero_af):
    items = []
    for line in pdf_text.split('\n'):
        line = line.strip()
        if not re.match(r'^\d+\s+[\d.]+', line):
            continue
            
        item_data = {'Nº AF': numero_af}
        for key, pattern in regex_items.items():
            match = re.search(pattern, line)
            if match:
                item_data[key] = match.group(1).strip()
            else:
                item_data[key] = None
                
        if item_data.get('Cód. Material'):
            items.append(item_data)
            
    return items

def process_files(uploaded_files, regex_patterns, save_document, table_name, extra_data=None, regex_items=None):
    if extra_data is None:
        extra_data = {}
        
    empenhos_df = None
    if table_name == 'autorizacoes':
        empenhos_df = load_data('empenhos')

    for pdf_file in uploaded_files:
        pdf_text = extract_text_from_pdf(pdf_file)
        
        extracted_data = extract_data_using_regex(pdf_text, regex_patterns)
        extracted_data.update(extra_data)
        
        if table_name == 'autorizacoes':
            num_empenho = extracted_data.get('Nº Empenho')
            if empenhos_df is not None and not empenhos_df.empty and num_empenho:
                emp_row = empenhos_df[empenhos_df['Nº Empenho'] == num_empenho]
                if not emp_row.empty:
                    extracted_data['Nº Processo'] = emp_row.iloc[0]['Nº Processo']                    
                    extracted_data['Valor Empenhado'] = emp_row.iloc[0]['Valor Empenhado']
                    extracted_data['Nome Fornecedor'] = emp_row.iloc[0]['Nome Fornecedor']
                    extracted_data['E-mail Fornecedor'] = emp_row.iloc[0]['E-mail Fornecedor']
        
        pk_map = {
            'solicitacoes_consumo': 'Nº Solicitação',
            'solicitacoes_compras': 'Nº Solicitação',
            'empenhos': 'Nº Empenho',
            'autorizacoes': 'Nº AF',
            'notas_fiscais': 'Nº NF'
        }
        pk_field = pk_map.get(table_name)
        
        if pk_field and not extracted_data.get(pk_field):
            raise ValueError(f"Não foi possível identificar o {pk_field} no arquivo {pdf_file.name}. Verifique se é o documento correto.")
        
        save_document(table_name, extracted_data)
        
        if table_name == 'notas_fiscais' and regex_items and extracted_data.get('Nº NF'):
            items_list = extract_nf_items_from_text(pdf_text, regex_items, extracted_data['Nº NF'])
            save_items_notas_fiscais(items_list)
            
        elif table_name == 'autorizacoes' and regex_items and extracted_data.get('Nº AF'):
            items_list = extract_af_items_from_text(pdf_text, regex_items, extracted_data['Nº AF'])
            save_autorizacoes_fornecimento_items(items_list)