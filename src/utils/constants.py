# --  Cabeçalhos ---

PAGE_HEADERS = [
    'Upload de Documentos',
    'Gestão Documental',
    'Execução de Notas Fiscais',
]

SOLIC_COMP_HEADERS = [
    'Nº Solicitação',
    'Data Emissão',
    'Valor Solicitado',
    'Local Entrega',
    'Objeto',
    'Nº Processo',
    'Observação',
    'Status',
    'Forma Exec.',
    'Funcionário',
    'Órgão Financeiro', 
    'Unidade Solicitante',
    'Unidade Financeira',
    'Ação',
    'Gestor Indicado', 
    'Legislação',
    'Programa',
]

SOLIC_CONS_HEADERS = [
    'Nº Solicitação',
    'Data Emissão',
    'Valor Solicitado',
    'Ata RP',
    'Vigência Inicial',
    'Vigência Final',
    'Nº Processo',
    'Status',
    'Forma Exec.',
    'Local Entrega',
    'Funcionário',
    'Unidade Solicitante',
    'Órgão Financeiro',
    'Unidade Financeira',
    'Observação',
    'Nome do Fornecedor',
    'CNPJ do Fornecedor',
]

EMPENHOS_HEADERS = [
    'Nº Empenho',
    'Nº Processo',
    'Nº Solicitação',
    'Valor Empenhado',
    'Órgão Solicitante',
    'Unidade',
    'Ação',
    'Fonte',
    'Nome Fornecedor',
    'CNPJ Fornecedor',
    'Tel. Fornecedor',
    'E-mail Fornecedor',
]

AF_HEADERS = [
    'Nº Processo', 
    'Nº AF', 
    'Nº Empenho',
    'Data', 
    'Valor Empenhado',
    'Vigência Inicial',
    'Vigência Final',
    'Objeto',
    'Ano Processo', 
    'Modalidade',
    'Contrato/Ano',
    'Local de Entrega',
    'Nome Fornecedor',
    'E-mail Fornecedor'
]

NOTAS_FISCAIS_HEADERS = [
    'Nº AF',
    'Nº Empenho',
    'Nº NF',
    'Data Emissão',
    'Valor Executado',
    'Fornecedor',
    'Ações',
]

EXEC_NF_HEADERS = [
    'Nº AF',
    'Total Empenhado',
    'Total Executado',
    'Saldo Atual',
    'Prazo',
    'Ações'
]

MODAL_ACOMP_EXEC_HEADERS = [
    'Cód. Material', 
    'Descrição', 
    'Qtde Empenhado',
    'Valor Empenhado', 
    'Qtde Executado',
    'Valor Executado',
    'Saldo (Qtde)',
    'Saldo (Valor)'
]

# --- UI Constants ---

LABEL_TIPO_DOC = 'Selecione um tipo de documento:'
LABEL_NUM_PROC = 'Digite o número do processo:'
LABEL_UPLOAD_SECTION = 'Arraste os documentos em PDF aqui'
LABEL_SOLIC_VINC = 'Tem alguma solicitação vinculada?'
LABEL_TIPO_SOLIC = 'Selecione o tipo de solicitação:'
LABEL_SELEC_SOLIC = 'Selecione a solicitação:'
LABEL_VIG_INICIAL = 'Digite a vigência inicial:'
LABEL_VIG_FINAL = 'Digite a vigência final:'
LABEL_BTN_UPLOAD = 'Processar arquivos'
LABEL_BTN_EXPORTAR = 'Exportar tabela'

TIPOS_DOCS = [
    'Solicitação de Consumo',
    'Solicitação de Compras',
    'Empenho',
    'Autorização de Fornecimento',
    'Nota Fiscal', 
]

TIPOS_SOLIC = [
    'Consumo',
    'Compras',
]

TABS_TITLES = [
    'Solicitações',
    'Empenhos',
    'Autorizações de Fornecimento',
    'Notas Fiscais'
]

# --- Tabelas - Banco de Dados ---

SOLIC_CONS_TABLE = '''
    CREATE TABLE IF NOT EXISTS solicitacoes_consumo (
        "Nº Solicitação" TEXT PRIMARY KEY,
        "Nº Processo" TEXT,
        "Data Emissão" TEXT,
        "Valor Solicitado" REAL,
        "Ata RP" TEXT,
        "Vigência Inicial" TEXT,
        "Vigência Final" TEXT,
        "Status" TEXT,
        "Prazo Exec." TEXT,
        "Forma Exec." TEXT,
        "Local Entrega" TEXT,
        "Funcionário" TEXT,
        "Unidade Solicitante" TEXT,
        "Órgão Financeiro" TEXT,
        "Unidade Financeira" TEXT,
        "Observação" TEXT,
        "Nome do Fornecedor" TEXT,
        "CNPJ do Fornecedor" TEXT
    )
'''

SOLIC_COMP_TABLE = '''
    CREATE TABLE IF NOT EXISTS solicitacoes_compras (
        "Nº Solicitação" TEXT PRIMARY KEY,
        "Nº Processo" TEXT,
        "Data Emissão" TEXT,
        "Valor Solicitado" REAL,
        "Local Entrega" TEXT,
        "Objeto" TEXT,
        "Observação" TEXT,
        "Status" TEXT,
        "Prazo Exec." TEXT,
        "Forma Exec." TEXT,
        "Funcionário" TEXT,
        "Órgão Financeiro" TEXT,
        "Unidade Solicitante" TEXT,
        "Unidade Financeira" TEXT,
        "Ação" TEXT,
        "Gestor Indicado" TEXT,
        "Legislação" TEXT,
        "Programa" TEXT
    )
'''

EMPENHOS_TABLE = '''
    CREATE TABLE IF NOT EXISTS empenhos (
        "Nº Empenho" TEXT PRIMARY KEY,
        "Nº Processo" TEXT,
        "Nº Solicitação" TEXT,
        "Valor Empenhado" REAL,
        "Órgão Solicitante" TEXT,
        "Unidade" TEXT,
        "Ação" TEXT,
        "Fonte" TEXT,
        "Nome Fornecedor" TEXT,
        "CNPJ Fornecedor" TEXT,
        "Tel. Fornecedor" TEXT,
        "E-mail Fornecedor" TEXT
    )
'''

AF_TABLE = '''
    CREATE TABLE IF NOT EXISTS autorizacoes (
        "Nº AF" TEXT PRIMARY KEY,
        "Nº Empenho" TEXT,
        "Data" TEXT,
        "Valor Empenhado" REAL,
        "Vigência Inicial" TEXT,
        "Vigência Final" TEXT,
        "Nº Processo" TEXT,
        "Fonte de Recurso" TEXT,
        "Objeto" TEXT,
        "Ano Processo" TEXT,
        "Nº Modalidade" TEXT,
        "Ano Modalidade" TEXT,
        "Modalidade" TEXT,
        "Contrato/Ano" TEXT,
        "Valor Contrato" REAL,
        "Prazo de Entrega" TEXT,
        "Local de Entrega" TEXT,
        "Prazo de Pagamento" TEXT,
        "Observacoes" TEXT,
        "Total Liberação" REAL,
        "Solicitacoes de Compra" TEXT,
        "Solicitacoes de Consumo" TEXT,
        "Órgão Solicitante" TEXT,
        "Ficha" TEXT,
        "Dotacao" TEXT,
        "Nº Fornecedor" TEXT,
        "Nome Fornecedor" TEXT,
        "CNPJ" TEXT,
        "Fone" TEXT,
        "E-mail Fornecedor" TEXT,
        "Contas" TEXT,
        FOREIGN KEY ("Nº Empenho") REFERENCES empenhos ("Nº Empenho")
    )
'''

NF_TABLE = '''
    CREATE TABLE IF NOT EXISTS notas_fiscais (
        "Nº NF" TEXT PRIMARY KEY,
        "Nº AF" TEXT,
        "Nº Empenho" TEXT,
        "Data Emissão" TEXT,
        "Valor Executado" REAL,
        "Fornecedor" TEXT,
        FOREIGN KEY ("Nº AF") REFERENCES autorizacoes ("Nº AF"),
        FOREIGN KEY ("Nº Empenho") REFERENCES empenhos ("Nº Empenho")
    )
'''

NF_ITENS_TABLE = '''
    CREATE TABLE IF NOT EXISTS notas_fiscais_itens (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "Nº NF" TEXT,
        "Cód. Material" TEXT,
        "Descrição" TEXT,
        "Qtde" REAL,
        "Vlr. Unitário" REAL,
        "Valor Executado" REAL,
        FOREIGN KEY ("Nº NF") REFERENCES notas_fiscais ("Nº NF")
    )
'''

AF_ITENS_TABLE = '''
    CREATE TABLE IF NOT EXISTS autorizacoes_itens (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "Nº AF" TEXT,
        "Cód. Material" TEXT,
        "Descrição" TEXT,
        "Qtde" REAL,
        "Valor Unitário" REAL,
        "Valor Total" REAL,
        FOREIGN KEY ("Nº AF") REFERENCES autorizacoes ("Nº AF")
    )
'''