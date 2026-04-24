CONSUMO_PATTERNS = {
    'Nº Solicitação': r'Solicitação Nº:\s*(\d+/\d+)',
    'Unidade Solicitante': r'Unidade Solicitante:\s*(.+?)(?:\s+Status:|$)',
    'Data Emissão': r'Data de Emissão:\s*(\d{2}/\d{2}/\d{4})',
    'Status': r'Status:\s*(.+?)(?:\n|$)',
    'Prazo Cons./Exec.': r'Prazo Cons\./Exec\.:\s*(.+?)(?:\n|$)',
    'Forma Entr./Exec.': r'Forma Entr\./Exec\.:\s*(.+?)(?:\n|$)',
    'Local Entrega': r'Local para Entrega:\s*(.+?)(?:\n|$)',
    'Funcionário': r'Funcionário:\s*(.+?)(?:\n|$)',
    'Órgão Financeiro': r'Órgão Financeiro:\s*(.+?)(?:\n|$)',
    'Unidade Financeira': r'Unidade Financeira:\s*(.+?)(?:\n|$)',
    'Observação': r'(?s)Observação:\s*(.*?)(?=\nFicha\s*-|\nPrograma:|$)',
    'Ata RP': r'Ata RP:\s*(.+?)(?:\n|$)',
    'Vigência Inicial': r'Vigência Inicial:\s*(\d{2}/\d{2}/\d{4})',
    'Vigência Final': r'Vigência Final:\s*(\d{2}/\d{2}/\d{4})',
    'Nome do Fornecedor': r'Fornecedor:\s*(.*?)(?=\s*,?\s*CNPJ:|$)',
    'CNPJ do Fornecedor': r'Fornecedor:.*?[,]?\s*CNPJ:\s*([\d\.\-/]+)'
}

COMPRAS_PATTERNS = {
    'Nº Solicitação': r'Solicitação Nº:\s*(\d+/\d+)',
    'Unidade Solicitante': r'Unidade Solicitante:\s*(.+?)(?:\s+Status:|$)',
    'Data Emissão': r'Data de Emissão:\s*(\d{2}/\d{2}/\d{4})',
    'Status': r'Status:\s*(.+?)(?:\n|$)',
    'Prazo Cons./Exec.': r'Prazo Cons\./Exec\.:\s*(.+?)(?:\n|$)',
    'Forma Entr./Exec.': r'Forma Entr\./Exec\.:\s*(.+?)(?:\n|$)',
    'Local Entrega': r'Local para Entrega:\s*(.+?)(?:\n|$)',
    'Funcionário': r'Funcionário:\s*(.+?)(?:\n|$)',
    'Órgão Financeiro': r'Órgão Financeiro:\s*(.+?)(?:\n|$)',
    'Unidade Financeira': r'Unidade Financeira:\s*(.+?)(?:\n|$)',
    'Observação': r'(?s)Observação:\s*(.*?)(?=\nFicha\s*-|\nPrograma:|$)',
    'Gestor Indicado': r'Gestor Indicado:\s*(.*?)(?:\n|$)',
    'Legislação': r'Legislação / Convenio / Contrato\s*:\s*(.+?)(?:\n|$)',
    'Objeto': r'(?s)Objeto:\s*(.*?)(?=\nJustificativa:|$)',
    'Programa': r'Programa:\s*(.+?)(?:\n|$)',
    'Ação': r'Ação:\s*(.+?)(?:\n|$)'
}
