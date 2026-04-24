from core.config import AF_SAMPLES, EMP_SAMPLES, SOLIC_SAMPLES, NF_SAMPLES
from tests.parsers import parse_af, parse_empenho, parse_solicitacao, parse_nf

def process_nf():
    if not NF_SAMPLES.exists():
        print(f'Pasta de Notas Fiscais não encontrada: {NF_SAMPLES}')
        return
    for pdf_path in NF_SAMPLES.glob('*.pdf'):
        print(f'\n{"="*60}')
        print(f' NOTA FISCAL: {pdf_path.name}'.center(60))
        print(f'{"="*60}')
        text = extract(pdf_path)
        parse_nf(text)

def process_af():
    if not AF_SAMPLES.exists():
        print(f'Pasta de AF não encontrada: {AF_SAMPLES}')
        return
    for pdf_path in AF_SAMPLES.glob('*.pdf'):
        print(f'\n{'='*60}')
        print(f' AF: {pdf_path.name}'.center(60))
        print(f'{'='*60}')
        text = extract(pdf_path)
        parse_af(text)

def process_empenho():
    if not EMP_SAMPLES.exists():
        print(f'Pasta de Empenhos não encontrada: {EMP_SAMPLES}')
        return
    for pdf_path in EMP_SAMPLES.glob('*.pdf'):
        print(f'\n{'='*60}')
        print(f' EMPENHO: {pdf_path.name}'.center(60))
        print(f'{'='*60}')
        text = extract(pdf_path)
        parse_empenho(text)

def process_solicitacao():
    if not SOLIC_SAMPLES.exists():
        print(f'Pasta de Solicitações não encontrada: {SOLIC_SAMPLES}')
        return
    for pdf_path in SOLIC_SAMPLES.glob('*.pdf'):
        print(f'\n{'='*60}')
        print(f' SOLICITAÇÃO: {pdf_path.name}'.center(60))
        print(f'{'='*60}')
        text = extract(pdf_path)
        parse_solicitacao(text)
        
def process_af_tables():
    if not AF_SAMPLES.exists():
        print(f'Pasta de AF nao encontrada: {AF_SAMPLES}')
        return
    
    target_cols = ['Item', 'Material', 'Qtd.', 'Valor Unit.', 'Valor Total']
    
    for pdf_path in AF_SAMPLES.glob('*.pdf'):
        tables = extract_tables_from_pdf(pdf_path)
        
        for table in tables:
            header = table[0]
            if len(header) > 0 and header[0] == 'Item':
                selected_indices = []
                for label in target_cols:
                    try:
                        idx = header.index(label)
                        selected_indices.append(idx)
                    except ValueError:
                        continue
                
                filtered_table = []
                for row in table:
                    filtered_row = [row[i] if i < len(row) else '' for i in selected_indices]
                    filtered_table.append(filtered_row)
                
                col_widths = [max(len(str(r[c])) for r in filtered_table) for c in range(len(selected_indices))]
                
                print(f'\nARQUIVO: {pdf_path.name}')
                for filtered_row in filtered_table:
                    line = '   '.join(str(val).ljust(width) for val, width in zip(filtered_row, col_widths))
                    print(line)