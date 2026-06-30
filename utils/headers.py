CONSUMPTION_REQUESTS_HEADERS = {
    'request_number': 'Nº Solicitação',
    'requested_value': 'Valor Solicitado (R$)',
    'price_registration': 'Ata RP',
    'start_date': 'Data Inicial',
    'end_date': 'Data Final',
    'requesting_unit': 'Unidade Solicitante',
    'financial_department': 'Órgão Financeiro',
    'notes': 'Observações',
    'supplier_name': 'Fornecedor',
    'supplier_cnpj': 'CNPJ'
}

PURCHASE_REQUESTS_HEADERS = {
    'request_number': 'Nº Solicitação',
    'issue_date': 'Data de Emissão',
    'requested_value': 'Valor Solicitado (R$)',
    'object': 'Objeto',
    'notes': 'Observações',
    'requesting_unit': 'Unidade Solicitante',
    'financial_department': 'Órgão Financeiro',
    'activity': 'Ação',
    'designed_manager': 'Gestor Indicado',
    'legislation': 'Legislação / Convênio',
    'program': 'Programa'
}

COMMITMENTS_HEADERS = {
    'commitment_number': 'Nº Empenho',
    'request_number': 'Nº Solicitação',
    'commited_value': 'Valor Empenhado (R$)',
    'process_number': 'Nº Processo',
    'source': 'Fonte de Recurso',
    'supplier_name': 'Fornecedor',
    'supplier_cnpj': 'CNPJ',
    'supplier_phone': 'Telefone',
    'supplier_email': 'E-mail'
}

AUTHORIZATIONS_HEADERS = {
    'authorization_number': 'Nº AF',
    'commitment_number': 'Nº Empenho',
    'process_number': 'Nº Processo',
    'modality': 'Modalidade',
    'contract': 'Contrato',
    'notes': 'Observações',
    'budget_sheet': 'Ficha',
    'budget_allocation': 'Dotação',
    'start_date': 'Data Inicial',
    'end_date': 'Data Final'
}

AUTHORIZATION_ITEMS_HEADERS = {
    'id': 'ID',
    'authorization_number': 'Nº AF',
    'material_code': 'Cód. Material',
    'description': 'Descrição',
    'quantity': 'Quantidade',
    'unitary_value': 'Valor Unitário (R$)'
}

INVOICES_HEADERS = {
    'invoice_number': 'Nº NF',
    'authorization_number': 'Nº AF',
    'issue_date': 'Data de Emissão'
}

INVOICE_ITEMS_HEADERS = {
    'id': 'ID',
    'invoice_number': 'Nº NF',
    'material_code': 'Cód. Material',
    'description': 'Descrição',
    'quantity': 'Quantidade',
    'unitary_value': 'Valor Unitário (R$)',
    'executed_value': 'Valor Executado (R$)'
}

BALANCES_HEADERS = {
    'invoice_number': 'Nº NF',
    'material_code': 'Cód. Material',
    'initial_quantity': 'Qtde Inicial',
    'initial_value': 'Valor Inicial',
    'executed_quantity': 'Qtde Executada',
    'executed_value': 'Valor Executado',
    'balance_quantity': 'Saldo (Qtde)',
    'balance_value': 'Saldo (Valor)'
}