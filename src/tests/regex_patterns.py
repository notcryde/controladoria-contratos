# Padrões de RegEx: Solicitações de Consumo

REGEX_SOLIC_CONS = {
    'Nº Solicitação': r'Solicitação Nº:\s*(\d+/\d+)',
    'Data Emissão': r'Data de Emissão:\s*(\d{2}/\d{2}/\d{4})',
    'Valor Solicitado': r'Valor Geral\s*:\s*([\d\.,]+)',
    'Ata RP': r'Ata RP:\s*(.+?)(?:\n|$)',
    'Vigência Inicial': r'Vigência Inicial:\s*(\d{2}/\d{2}/\d{4})',
    'Vigência Final': r'Vigência Final:\s*(\d{2}/\d{2}/\d{4})',
    'Status': r'Status:\s*(.+?)(?:\s+Vigência|$)',
    'Prazo Exec.': r'Prazo Cons\./Exec\.:\s*(.+?)(?:\n|$)',
    'Forma Exec.': r'Forma Entr\./Exec\.:\s*(.+?)(?:\n|$)',
    'Local Entrega': r'Local para Entrega:\s*(.+?)(?:\n|$)',
    'Funcionário': r'Funcionário:\s*(.+?)(?:\n|$)',
    'Unidade Solicitante': r'(?s)Unidade Solicitante:\s*(.*?)(?=\s*Ata RP:|\s*Status:|$)',
    'Órgão Financeiro': r'Órgão Financeiro:\s*(.+?)(?:\n|$)',
    'Unidade Financeira': r'Unidade Financeira:\s*(.+?)(?:\n|$)',
    'Observação': r'(?s)Observação:\s*(.*?)(?=\nFicha\s*-|\nPrograma:|$)',
    'Nome do Fornecedor': r'Fornecedor:\s*(.*?)(?=\s*,?\s*CNPJ:|$)',
    'CNPJ do Fornecedor': r'Fornecedor:.*?[,]?\s*CNPJ:\s*([\d\.\-/]+)',
}

# Padrões de RegEx: Solicitações de Compras

REGEX_SOLIC_COMPR = {
    'Nº Solicitação': r'Solicitação Nº:\s*(\d+/\d+)',
    'Data Emissão': r'Data de Emissão:\s*(\d{2}/\d{2}/\d{4})',
    'Valor Solicitado': r'Total\s+([\d\.,]+)',
    'Local Entrega': r'Local para Entrega:\s*(.+?)(?:\n|$)',
    'Objeto': r'(?s)Objeto:\s*(.*?)(?=\nJustificativa:|$)',
    'Observação': r'(?s)Observação:\s*(.*?)(?=\nFicha\s*-|\nPrograma:|$)',
    'Status': r'Status:\s*(.+?)(?:\n|$)',
    'Prazo Exec.': r'Prazo Cons\./Exec\.:\s*(.+?)(?:\n|$)',
    'Forma Exec.': r'Forma Entr\./Exec\.:\s*(.+?)(?:\n|$)',
    'Funcionário': r'Funcionário:\s*(.+?)(?:\n|$)',
    'Órgão Financeiro': r'Órgão Financeiro:\s*(.+?)(?:\n|$)',
    'Unidade Solicitante': r'(?s)Unidade Solicitante:\s*(.*?)(?=\s*Ata RP:|\s*Status:|$)',
    'Unidade Financeira': r'Unidade Financeira:\s*(.+?)(?:\n|$)',
    'Ação': r'Ação:\s*(.+?)(?:\n|$)',
    'Gestor Indicado': r'Gestor Indicado:\s*(.*?)(?:\n|$)',
    'Legislação': r'Legislação / Convenio / Contrato\s*:\s*(.+?)(?:\n|$)',
    'Programa': r'Programa:\s*(.+?)(?:\n|$)',
}

# Padrões de RegEx: Empenhos

REGEX_EMP = {
    'Nº Empenho': r'Número:\s*(\d+/\d+)',
    'Nº Processo': r'PROCESSO Nº\s*\.+\s*(\d+/\d+)',
    'Valor Empenhado': r'VALOR DESTE EMPENHO\s*\.+\s*([\d\.,]+)',
    'Órgão Solicitante': r'ÓRGÃO\s*:\s*\.+\s*(.+?)(?:\n|$)',
    'Unidade': r'UNIDADE\s*:\s*\.+\s*(.+?)(?:\n|$)',
    'Ação': r'AÇÃO\s*:\s*\.+\s*(.+?)(?:\n|$)',
    'Fonte': r'FONTE DE RECURSO\s*:\s*\.+\s*(.+?)(?:\n|$)',
    'Nome Fornecedor': r'CREDOR\s*\.+\s*(.+?)(?=\s*CPF/CNPJ)',
    'CNPJ Fornecedor': r'CPF/CNPJ:\s*([\d\.\-/]+)',
    'Tel. Fornecedor': r'ENDEREÇO\s*\.+.*?([\d]{4,5}-[\d]{4})(?=-[a-zA-Z0-9_.+-]+@)',
    'E-mail Fornecedor': r'[\d]{4,5}-[\d]{4}[-\s]+([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)'
}

# Padrões de RegEx: Autorizações de Fornecimento

REGEX_AF = {
    'Nº AF': r'A\.F\s*-\s*Nº\s*(\d+/\d+)',
    'Data': r'Data\s*(\d{2}/\d{2}/\d{4})',
    'Valor Empenhado': r'Empenho.*?valor:\s*([\d\.,]+)',
    'Nº Processo': r'Nº\s*Processo\s*(\d+)',
    'Nº Empenho': r'Empenho\s+(\d+/\d+)',
    'Fonte de Recurso': r'Fonte\s+de\s+Recurso\s+(.+?)(?:\n|$)',
    'Ano Processo': r'Ano\s*Processo\s*(\d{4})',
    'Nº Modalidade': r'Nº\s*Modalidade\s*(\d+)',
    'Ano Modalidade': r'Ano\s*Modalidade\s*(\d{4})',
    'Modalidade': r'Modalidade\s+(.+?)(?:\s{2,}|\n|$)',
    'Contrato/Ano': r'Contrato\s*/\s*Ano\s*(\d+/\d+)',
    'Valor Contrato': r'Valor\s+Contrato:\s*([\d\.,]+)',
    'Prazo de Entrega': r'Prazo\s+de\s+Entrega\s+(.+?)(?:\n|$)',
    'Local de Entrega': r'Local\s+de\s+Entrega\s+(.+?)(?:\n|$)',
    'Prazo de Pagamento': r'Prazo\s+de\s+Pagamento\s+(.+?)(?:\n|$)',
    'Objeto': r'(?s)Objeto\s*(.*?)\s*(?=Observações|Solicitações|$)',
    'Observacoes': r'Observações\s+([\s\S]+?)(?=\s*Solicitações|$)',
    'Total Liberação': r'Total\s+Liberação\s*:\s*([\d\.,]+)',
    'Solicitacoes de Compra': r'Solicitações\s+de\s+Compra\s*([\s\S]*?)(?=\s*Solicitações\s+de\s+Consumo|$)',
    'Solicitacoes de Consumo': r'Solicitações\s+de\s+Consumo\s*([\s\S]*?)(?=\s*Ata:|\s*Empenho|$)',
    'Órgão Solicitante': r'Órgão\s+Solicitante\s+(.+?)(?:\n|$)',
    'Ficha': r'Ficha\s+(\d+)',
    'Dotacao': r'Dotação\s+([\d\.]+)',
    'Nº Fornecedor': r'Fornecedor\s+(\d+)',
    'Nome Fornecedor': r'Fornecedor\s+\d+\s+(.+?)(?:\n|$)',
    'CNPJ': r'CNPJ\s+(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})',
    'Fone': r'Fone\s*([\d\s\(\)-]+)',
    'Email': r'E-mail\s+(.+?)(?:\n|$)',
    'Contas': r'Contas\s+(.+?)(?:\n|$)',
}

# Padrões de RegEx: Notas Fiscais

REGEX_NF = {
    'Nº NF': r'Número N\.F:\s*(\d+)',
    'Data Emissão': r'Data Emissão:\s*(\d{2}/\d{2}/\d{4})',
    'Valor Executado': r'Vlr\. Total:\s*([\d\.,]+)',
    'Fornecedor': r'Fornecedor:\s*(.*?)(?=\s*CNPJ:|$)',
    'Nº AF': r'Autorização:\s*(\d+/\d+)',
    'Nº Empenho': r'Empenho:\s*(\d+/\d+)',
}