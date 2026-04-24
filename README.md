# Controladoria de Contratos - SEDIS

O projeto Controladoria de Contratos - SEDIS é uma plataforma de gestão e acompanhamento de fluxos administrativos públicos, desenvolvida para centralizar o processamento de documentos fundamentais como Solicitações de Compra/Consumo, Notas de Empenho, Autorizações de Fornecimento (AF) e Notas Fiscais.

O sistema utiliza técnicas de extração de dados via Processamento de Linguagem Natural (Regex) em documentos PDF, automatizando a inserção de informações em uma base de dados estruturada e permitindo o acompanhamento financeiro em tempo real da execução contratual.

## Principais Funcionalidades

### 1. Processamento Inteligente de Documentos

Extração automatizada de metadados de arquivos PDF utilizando expressões regulares customizadas. O sistema identifica automaticamente:
- Dados de fornecedores (CNPJ, Razão Social, Contato).
- Valores empenhados, executados e saldos remanescentes.
- Prazos de vigência e datas de emissão.
- Itens detalhados de Notas Fiscais e Autorizações de Fornecimento.

### 2. Gestão Documental Estruturada
Visualização centralizada de todos os documentos processados, organizada por abas interativas:
- Filtros avançados e ordenação via AgGrid.
- Detalhamento de itens por modal (pop-up) sem recarregamento de página.
- Exportação de dados para formato CSV (padrão PT-BR).

### 3. Acompanhamento de Execução Financeira
Módulo dedicado para análise de saúde financeira dos contratos:
- Cálculo automático de saldo atual (Empenhado vs. Executado).
- Monitoramento de prazos de vigência remanescentes.
- Detalhamento técnico por item de material/serviço, permitindo rastrear o que já foi entregue e o que resta a executar.

---

## Arquitetura Técnica

O projeto foi construído seguindo princípios de modularização e separação de preocupações (SoC):

- **Frontend:** Streamlit (v1.55.0) para interface reativa.
- **Processamento de Dados:** Pandas para manipulação de dataframes e NumPy para cálculos vetoriais.
- **Extração de PDF:** Pdfplumber para análise de texto e tabelas em documentos PDF.
- **Persistência:** SQLite3 para armazenamento local com suporte a integridade referencial (Foreign Keys).
- **Interface de Tabelas:** Streamlit-AgGrid para componentes de grade de alta performance.

---

## Estrutura do Projeto

```text
sedis-controladoria/
├── src/
│   ├── utils/            # Lógica de negócio, banco de dados e processamento
│   │   ├── database.py   # Operações CRUD e persistência SQLite
│   │   ├── pdf_parser.py # Motor de extração de texto e lógica de processamento
│   │   ├── regex_patterns.py # Padrões de extração para cada tipo de documento
│   │   └── render_table.py   # Configurações globais das grades AgGrid
│   ├── views/            # Páginas da aplicação Streamlit
│   │   ├── uploads.py    # Interface de entrada de novos documentos
│   │   ├── gestao_documental.py # Visualização geral da base de dados
│   │   └── execucao_notas_fiscais.py # Relatórios de execução financeira
│   └── tests/            # Amostras e scripts de validação de parsers
├── controladoria.db      # Banco de dados SQLite
├── requirements.txt      # Dependências do projeto
└── streamlit_app.py      # Ponto de entrada da aplicação
```

---

## Instalação e Execução

### Pré-requisitos
- Python 3.10 ou superior.
- Ambiente virtual (recomendado).

### Passo a passo

1.  **Clonar o repositório:**

    ```bash
    git clone <url-do-repositorio>
    cd sedis-controladoria
    ```

2.  **Criar e ativar o ambiente virtual:**

    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    ```

3.  **Instalar dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Executar a aplicação:**

    ```bash
    streamlit run
    ```

## Fluxo de Utilização Recomendado

Para manter a integridade referencial do banco de dados, os documentos devem ser carregados preferencialmente na seguinte ordem:

1.  **Solicitações (Compra/Consumo):** Define a demanda inicial e o número do processo.
2.  **Empenhos:** Vincula o recurso financeiro à solicitação.
3.  **Autorizações de Fornecimento (AF):** Documento que formaliza o pedido ao fornecedor.
4.  **Notas Fiscais:** Registra a execução e consome o o valor empenhado.

---

## Segurança e Acesso

A aplicação conta com uma camada básica de autenticação gerenciada via `st.session_state`. O acesso às páginas de gestão e upload é restrito a usuários logados, garantindo que as operações de escrita no banco de dados sejam controladas.

---

## Manutenção e Contribuição

O motor de extração de dados é baseado em `regex_patterns.py`. Caso o layout de algum documento oficial da prefeitura mude, as expressões regulares neste arquivo devem ser atualizadas para garantir a continuidade da extração correta dos dados.