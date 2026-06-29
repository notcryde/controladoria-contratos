import re

CONSUMPTION_REQUESTS = {
    'request_number': r'Solicitação Nº:\s*(\d+/\d+)',
    'requested_value': r'Valor Geral\s*:\s*([\d\.,]+)',
    'price_registration': r'Ata RP:\s*(.+?)(?:\n|$)',
    'start_date': r'Vigência Inicial:\s*(\d{2}/\d{2}/\d{4})',
    'end_date': r'Vigência Final:\s*(\d{2}/\d{2}/\d{4})',
    'requesting_unit': r'(?s)Unidade Solicitante:\s*(.*?)(?=\s*Ata RP:|\s*Status:|$)',
    'financial_department': r'Órgão Financeiro:\s*(.+?)(?:\n|$)',
    'notes': r'(?s)Observação:\s*(.*?)(?=\nFornecedor:|\nFicha\s*-|\nPrograma:|\nJustificativa:|\nPCR\d+|\nVersão|$)',
    'supplier_name': r'Fornecedor:\s*(.*?)(?=\s*,?\s*CNPJ:|$)',
    'supplier_cnpj': r'Fornecedor:.*?[,]?\s*CNPJ:\s*([\d\.\-/]+)',
}

PURCHASE_REQUESTS = {
    'request_number': r'Solicitação Nº:\s*(\d+/\d+)',
    'issue_date': r'Data de Emissão:\s*(\d{2}/\d{2}/\d{4})',
    'requested_value': r'Total\s+([\d\.,]+)',
    'object': r'(?s)Objeto:\s*(.*?)(?=\nJustificativa:|$)',
    'notes': r'(?s)Observação:\s*(.*?)(?=\nFicha\s*-|\nPrograma:|$)',
    'requesting_unit': r'(?s)Unidade Solicitante:\s*(.*?)(?=\s*Ata RP:|\s*Status:|$)',
    'financial_department': r'Órgão Financeiro:\s*(.+?)(?:\n|$)',
    'activity': r'Ação:\s*(.+?)(?:\n|$)',
    'designed_manager': r'Gestor Indicado:\s*(.*?)(?:\n|$)',
    'legislation': r'Legislação / Convenio / Contrato\s*:\s*(.+?)(?:\n|$)',
    'program': r'Programa:\s*(.+?)(?:\n|$)',
}

COMMITMENTS = {
    'commitment_number': r'Número:?\s*(\d+/\d+)',
    'commited_value': r'VALOR DESTE EMPENHO\s*\.+\s*([\d\.,]+)',
    'process_number': r'PROCESSO Nº\s*\.+\s*(\d+/\d+)',
    'source': r'FONTE DE RECURSO\s*:\s*\.+\s*(.+?)(?:\n|$)',
    'supplier_name': r'CREDOR\s*\.+\s*(.+?)(?=\s*CPF/CNPJ)',
    'supplier_cnpj': r'CPF/CNPJ:\s*([\d\.\-/]+)',
    'supplier_phone': r'ENDEREÇO\s*\.+.*?([\d]{4,5}-[\d]{4})(?=-[a-zA-Z0-9_.+-]+@)',
    'supplier_email': r'[\d]{4,5}-[\d]{4}[-\s]+([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)'
}

AUTHORIZATIONS = {    
    'authorization_number': r'A\.F\s*-\s*Nº\s*(\d+/\d+)',
    'process_number': r'Nº\s*Processo\s*(\d+)',
    'commitment_number': r'Empenho\s+(\d+/\d+)',
    'modality': r'Modalidade\s+(.+?)(?:\s{2,}|\n|$)',
    'contract': r'Contrato\s*/\s*Ano\s*(\d+/\d+)',
    'notes': r'Observações\s+([\s\S]+?)(?=\s*Solicitações|$)',
    'budget_sheet': r'Ficha\s+(\d+)',
    'budget_allocation': r'Dotação\s+([\d\.]+)',
}

AUTHORIZATION_ITEMS = {
    'material_code': r"^\d+\s+([\d.]+)",
    'qquantity': r"^\d+\s+[\d.]+\s+([\d.,]+)",
    'description': r"^\d+\s+[\d.]+\s+[\d.,]+\s+[A-Za-z]+\s+(.*?)\s+[\d.,]+\s+(?:.*?\s+)?[\d.,]+\s*$",
    'unitary_value': r"([\d.,]+)\s+(?:.*?\s+)?[\d.,]+\s*$", # B.O TÁ PEGANDO A COLUNA ITEM AO INVES DO VALOR UNITÁRIO
}

INVOICES = {
    'invoice_number': r'Número N\.F:\s*(\d+)',
    'issue_date': r'Data Emissão:\s*(\d{2}/\d{2}/\d{4})',
    'executed_value': r'Vlr\. Total:\s*([\d\.,]+)',
    'authorization_number': r'Autorização:\s*(\d+/\d+)',
}

INVOICE_ITEMS = {
    'material_code': r"^\d+\s+([\d.]+)",
    'descriptions': r"^\d+\s+[\d.]+\s+(.+?)\s+\d+,\d{3}",
    'quantity': r"(\d+,\d{3})",
    'unitary_value': r"\d+,\d{3}\s+([\d.]+,\d{2})",
}