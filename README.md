## Dados Relevantes de Cada Documento

### 1. Solicitação de Consumo

```py
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
```

### 2. Solicitação de Compras

```py
PURCHASE_REQUESTS = {
    'request_number': r'Solicitação Nº:\s*(\d+/\d+)',
    'issue_': r'Data de Emissão:\s*(\d{2}/\d{2}/\d{4})',
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
```

### 3. Empenho

```py
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
```

### 4. Autorização de Fornecimento

```py
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

```

```py
AUTHORIZATION_ITEMS = {
    'material_code': r"^\d+\s+([\d.]+)",
    'qquantity': r"^\d+\s+[\d.]+\s+([\d.,]+)",
    'description': r"^\d+\s+[\d.]+\s+[\d.,]+\s+[A-Za-z]+\s+(.*?)\s+[\d.,]+\s+(?:.*?\s+)?[\d.,]+\s*$",
    'unitary_value': r"([\d.,]+)\s+(?:.*?\s+)?[\d.,]+\s*$",
}
```

### 5. Nota Fiscal

```py  
INVOICES = {
    'invoice_number': r'Número N\.F:\s*(\d+)',
    'issue_date': r'Data Emissão:\s*(\d{2}/\d{2}/\d{4})',
    'executed_value': r'Vlr\. Total:\s*([\d\.,]+)',
    'authorization_number': r'Autorização:\s*(\d+/\d+)',
}
```

```py
INVOICE_ITEMS = {
    'material_code': r"^\d+\s+([\d.]+)",
    'descriptions': r"^\d+\s+[\d.]+\s+(.+?)\s+\d+,\d{3}",
    'quantity': r"(\d+,\d{3})",
    'unitary_value': r"\d+,\d{3}\s+([\d.]+,\d{2})",
}
```

## Limitações Documentais

- O documento de empenho deve ter uma relação (1-1) com uma solicitação, mas não há o número da solicitação indicado em seu texto, sendo necessário informar de forma manual este vínculo
- Ocorre algo semelhante com autorização de fornecimento, sendo necessário estipular a data inicial de contrato e data final, também de forma manual (Obs: as vigências de uma Solicitação de Consumo vinculada ao seu Empenho não conta neste caso)
- Tanto no quesito de Itens de Notas Fiscais quanto nos Items de AFs, há códigos materiais duplicados com dados diferentes, portanto, a alternativa será tratar um campo genérico autoincremental chamado ID como PK

## Modelos de Dados

- Solicitações (requests) - Entidade pai
- Solicitações de Consumo (consumption_requests) - Entidade filha de Solicitações, ou seja, sua chave primária é ao mesmo tempo chave estrangeira de Solicitações
- Solicitações de Compras (purchase_requests) - Entidade filha de Solicitações, ou seja, sua chave primária é ao mesmo tempo chave estrangeira de Solicitações
- Empenhos (commitments) - Relação 1-1 com o número da solicitação indicado manualmente pelo usuário
- Autorizações de Fornecimento (authorizations) - Relação 1-1 com um número de empenho
- Itens de Autorização de Fornecimento (authorization_items) - Relação 1-N com com um número de autorização (vários itens contidos num mesmo documento de autorização de fornecimento)
- Notas Fiscais (invoices) - Relação 1-N com com um número de autorização (várias notas fiscais contidas num mesmo documento de autorização de fornecimento)
- Itens de Autorização de Fornecimento (invoice_items) - Relação 1-N com com um número de nota fiscal (vários itens contidos num mesmo documento de nota fiscal)

## Descrição do Fluxo

- O sistema deve considerar que uma autorização de fornecimento autoriza vários itens, representando o saldo inicial (somatório de valor unitário + somatório de quantidades)
- O sistema deve considerar que cada nota fiscal vinculada à autorização de fornecimento consome uma parte do saldo de quantidade e do saldo de valor. Obs: os valores do modelo de itens autorizados não podem ser alterados para garantir auditoria.
- O sistema deve sempre verificar o saldo atual (somatório das notas fiscais - saldo inicial) antes de lançar uma nota fiscal. 
- O sistema não deve permitir que uma nota fiscal seja lançada caso os valores dela sejam maiores que o saldo atual
- O sistema deve calcular o prazo final de uma autorização de fornecimento com a data atual (em tempo real)

## Interfaces de Usuário

### Uploads

- Tabs: Solicitações, Empenhos, Autorizações e Notas Fiscais

#### Solicitações

- Selectbox: 'Selecione o tipo de solicitação': ['Compras'. 'Consumo']
- Upload do documento (formato PDF)
- Botão 'Processar'

#### Empenhos

- Selectbox: 'Selecione o tipo de solicitação': ['Compras'. 'Consumo']
- Selectbox: 'Selecione o número de solicitação': 
  - Caso tenha solicitações cadastradas, retornar todas as solicitações do tipo selecionado nas opções
  - Caso contrário, retornar 'Não há solicitações cadastradas' e bloquear selectbox
- Upload do documento (formato PDF)
- Botão 'Processar'

#### Autorizações de Fornecimento

- Selectbox: 'Selecione a data inicial': `date_input`
- Selectbox: 'Selecione a data final': `date_input`
- Upload de documento (formato PDF)
- Botão 'Processar

#### Autorizações de Fornecimento

- Upload de documentos (formato PDF)
- Botão 'Processar

### Visualização Documental

- Tabs: Solicitações, Empenhos, Autorizações e Notas Fiscais

#### Solicitaçãões

- Dataframe de Solicitações de Consumo
- Dataframe de Solicitações de Compras

#### Empenhos

- Dataframe de Empenhos


#### Autorizações 

- Dataframe de Autorizações

#### Itens Notas Fiscais

- Selectbox 'Selecione o número da nota fiscal'
- Dataframe de Itens da Nota Fiscal (colunas: Nº AF, Cód. Material, Qtde, Valor Unitário, Valor Total)

### Acompanhamento de Saldos 

Selectbox 'Selecione o Nº da AF'

Exibir: Saldo Inicial, Saldo Executado e Saldo Atual
- Saldo Inicial: Somatório de Itens da AF (Qtde * Valor Unitário)
- Saldo Executado: Somatório de Itens de NFs vinculados à AF (Qtde * Valor Unitário)
- Saldo Atual: Saldo Inicial - Saldo Executado
 
Exibir: Data Inicial, Data Final, Prazo Restante
- Data Inicial: campo data_inicial digitado pelo usuário no momento do upload
- Data Final: campo data_final digitado pelo usuário no momento do upload
- Prazo Restante: Data Inicial - Data Atual (em tempo real)

Exibir: Dataframe de totalidade unitária de itens
- Colunas: Nº NF, Cód. Material, Qtde Inicial, Valor Inicial, Qtde Executada, Valor Executado, Saldo (Qtde), Saldo (Valor)

### Editar ou Remover Nota Fiscal

- Selectbox: 'Selecione o número da autorização de fornecimento': 
  - Caso tenha AFs cadastradas, retornar todas as solicitações do tipo selecionado nas opções
  - Caso contrário, retornar 'Não há AFs' e bloquear selectbox

- Caso o selectbox anterior tenha sido selecionado e que tenha AFs cadastradas:
  - Selectbox('Selecione uma nota fiscal)
  - Caso tenha NFs cadastradas, retornar todas as NFs vinculadas àquela AF

- Caso o selectbox anterior tenha sido selecionado e que tenha NFs cadastradas:
  - Formulário persistindo os campos do item da nota fiscal, podendo editá-los
  - Botão 'Editar' 

## Segurança e Integridade

- Adoção de boas práticas de desenvolvimento e modelagem de banco de dados
- Tendo tratamentos adequados para criação de tabelas, erros e sucessos nos CRUDs, bem como na integração com a interface de usuário
- Ter logs bem definidos para cada operação realizada

## Ambiente de Desenvolvimento

- Visar simplicidade e eficiência
- Boas práticas de desenvolvimento, mas sem complexar demais as coisas
- VS Code, Python, Streamlit, Pandas, PDFPlumber

## Script SQL

```sql

```

## Glossário

NF = Nota Fiscal

AF = Autorização de Fornecimento