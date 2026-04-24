from document_processor import process_af, process_empenho, process_solicitacao, process_af_tables, process_nf
from utils import raw_text
from paths import NF_SAMPLES

if __name__ == '__main__':
    print('1 - Empenho')
    print('2 - AF')
    print('3 - Solicitação')
    print('4 - Nota Fiscal')
    print('5 - Texto Bruto')
    print('6 - Tabelas de AF\n')

    try:
        opt = int(input('Selecione uma opção: '))
    except ValueError:
        print('Por favor, insira um número válido.')
        exit()

    if opt == 1:
        process_empenho()
    elif opt == 2:
        process_af()
    elif opt == 3:
        process_solicitacao()
    elif opt == 4:
        process_nf()
    elif opt == 5:
        pdf_file = NF_SAMPLES / 'BAIXA_AF_4290.pdf'
        raw_text(str(pdf_file))
    elif opt == 6:
        process_af_tables()
    else:
        print('Tipo de documento não implementado.')