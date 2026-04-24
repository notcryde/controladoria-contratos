import print_section
from src.utils.regex_patterns import REGEX_AF, REGEX_EMP, REGEX_NF, REGEX_SOLIC_COMPR, REGEX_SOLIC_CONS

def parse_af(text):
    all_labels = list(REGEX_AF.keys())
    label_width = max(len(label) for label in all_labels) + 2

    print_section("DADOS DA AF", REGEX_AF, text, label_width)

def parse_empenho(text):
    label_width = max(len(label) for label in REGEX_EMP.keys()) + 2
    print_section("DADOS DO EMPENHO", REGEX_EMP, text, label_width)

def parse_solic_consumo(text):
    all_labels = list(REGEX_SOLIC_CONS)
    label_width = max(len(label) for label in all_labels) + 2

    print_section('DADOS CONSUMO', REGEX_SOLIC_CONS, text, label_width)

def parse_solic_compras(text):
    all_labels = list(REGEX_SOLIC_COMPR.keys())
    label_width = max(len(label) for label in all_labels) + 2

    print_section('DADOS COMPRAS', REGEX_SOLIC_COMPR, text, label_width)

def parse_solicitacao(text):
    texto_upper = text.upper()
    
    if 'SOLICITAÇÃO DE COMPRA' in texto_upper:
        print('-> Identificado: Solicitação de Compras')
        parse_solic_compras(text)
    elif 'SOLICITAÇÃO DE CONSUMO' in texto_upper:
        print('-> Identificado: Solicitação de Consumo')
        parse_solic_consumo(text)
    else:
        print('-> Aviso: Tipo de solicitação (Compra/Consumo) não identificado no texto.')

def parse_nf(text):
    all_labels = list(REGEX_NF.keys())
    label_width = max(len(label) for label in all_labels) + 2
    print_section('DADOS DA NOTA FISCAL', REGEX_NF, text, label_width)