from document_processor import process_af, process_empenho, process_solicitacao, process_af_tables, process_nf
from utils import raw_text
import config as cf

if __name__ == '__main__':
    print('1 - Empenho')
    print('2 - AF')
    print('3 - Solicitação')
    print('1 - Nota Fiscal')
    opt = int(input('Selecione uma opção:'))

    print('\n\n')

    if opt == 1:
        process_empenho()
    elif opt == 2:
        process_af()
    elif opt == 3:
        process_solicitacao()
    elif opt == 4:
        raw_text(cf.NF_SAMPLES / 'BAIXA NF 5891698 COMEVAP.pdf')
    elif opt == 5:
        process_af_tables()
    elif opt == 6:
        process_nf()
    else:
        print('Tipo de documento não implementado.')