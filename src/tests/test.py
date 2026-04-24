from document_processor import process_af, process_empenho, process_solicitacao, process_af_tables, process_nf
from utils import raw_text
from paths import NF_SAMPLES

if __name__ == '__main__':
    print('1 - Empenho')
    print('2 - AF')
    print('3 - Solicitação')
    print('4 - Nota Fiscal')
    print('5 - Texto Bruto\n')

    opt = int(input('Selecione uma opção:'))

    if opt == 1:
        process_empenho()
    elif opt == 2:
        process_af()
    elif opt == 3:
        process_solicitacao()
    elif opt == 4:
        process_nf()
    elif opt == 5:
        raw_text(f'{NF_SAMPLES}/BAIXA NF 5891698 COMEVAP.pdf')
    elif opt == 6:
        process_af_tables()
    else:
        print('Tipo de documento não implementado.')