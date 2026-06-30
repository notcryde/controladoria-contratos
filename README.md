# Sistema de Controladoria de Contratos

Aplicação desenvolvida para gerenciar, auditar e automatizar o ciclo de vida de contratos e fornecimentos. O sistema controla o fluxo completo de aquisições, desde a solicitação inicial até o faturamento via Notas Fiscais, garantindo a integridade dos saldos, o acompanhamento de prazos e a rastreabilidade dos documentos.

## Objetivo do Projeto

O sistema visa substituir controles manuais por uma plataforma centralizada que realiza a extração automatizada de dados de documentos em PDF e gerencia as relações entre Solicitações, Empenhos, Autorizações de Fornecimento (AF) e Notas Fiscais (NF). O foco principal é evitar inconsistências financeiras, bloqueando faturamentos que excedam os saldos autorizados.

## Funcionalidades Principais

- **Extração Automatizada:** Leitura de arquivos PDF (Solicitações, Empenhos, AFs e NFs) utilizando `pdfplumber` e expressões regulares (`re`) para extração estruturada de dados.
- **Gestão de Documentos (CRUD):** Visualização, edição e acompanhamento de todos os documentos processados através de interfaces interativas.
- **Controle de Saldos em Tempo Real:** Cálculo automático do saldo financeiro e quantitativo. O sistema impede o lançamento de Notas Fiscais cujos valores ultrapassem o limite estabelecido na Autorização de Fornecimento.
- **Monitoramento de Prazos:** Acompanhamento dinâmico da vigência de contratos e autorizações, calculando os dias restantes com base na data atual.


## Tecnologias Utilizadas

- **Linguagem:** Python 3
- **Interface Gráfica (Frontend):** Streamlit
- **Banco de Dados:** SQLite (com Foreign Keys e integridade referencial)
- **Manipulação de Dados:** Pandas
- **Extração de PDFs:** pdfplumber

---

## Arquitetura e Estrutura do Projeto

O projeto adota uma arquitetura modular para separar a interface de usuário, as regras de negócio, o acesso a dados e os utilitários.

```text
controladoria-contratos/
├── app.py                  # Ponto de entrada da aplicação (Streamlit)
├── requirements.txt        # Dependências do projeto
├── README.md               # Documentação do projeto
├── core/                   # Regras de negócio e operações de banco (CRUD)
│   ├── authorizations.py
│   ├── authorization_items.py
│   ├── commitments.py
│   ├── invoices.py
│   ├── invoice_items.py
│   └── requests.py
├── database/               # Configuração e esquemas do banco de dados
│   ├── connection.py       # Gerenciador de conexão SQLite
│   └── schema.sql          # DDL do banco de dados
├── ui/                     # Componentes visuais e abas do Streamlit
│   ├── tab_authorizations.py
│   ├── tab_balances.py
│   ├── tab_commitments.py
│   ├── tab_invoices.py
│   └── tab_requests.py
└── utils/                  # Utilitários globais
    ├── formatters.py       # Formatação de datas e moedas (BRL)
    ├── headers.py          # Dicionários de cabeçalhos para DataFrames
    ├── pdf_extractor.py    # Lógica base do pdfplumber
    └── regex_patterns.py   # Padrões de expressões regulares para extração

```


## Modelo de Dados e Relacionamentos

O banco de dados relacional foi estruturado para refletir a hierarquia documental do processo de compras públicas/corporativas:

### **1. Solicitações (`requests`):** Entidade mestre.

- **Compras (`purchase_requests`):** Entidade filha (1:1).
- **Consumo (`consumption_requests`):** Entidade filha (1:1).

### **2. Empenhos (`commitments`):** Possui relação 1:1 com uma Solicitação. O vínculo é estabelecido manualmente pelo usuário durante o processamento do PDF.

### **3. Autorizações de Fornecimento (`authorizations`):** Possui relação 1:1 com um Empenho. Exige a definição manual de vigência (Data Inicial e Final).

- **Itens da AF (`authorization_items`):** Relação 1:N com a AF. Armazena os produtos/serviços autorizados e compõe o **saldo inicial** (imutável para fins de auditoria).

### **4. Notas Fiscais (`invoices`):** Possui relação 1:N com uma AF (várias NFs podem abater o saldo de uma mesma AF).

- **Itens da NF (`invoice_items`):** Relação 1:N com a NF. Representa o consumo efetivo do saldo autorizado.

## Regras de Negócio e Restrições

- **Geração de Chaves Primárias (Itens):** Devido à possibilidade de códigos de materiais duplicados com especificações diferentes nos PDFs, o sistema utiliza um campo `id` autoincremental genérico como Chave Primária (PK) para as tabelas de itens.
- **Integridade de Saldo:** O sistema avalia a equação `Saldo Atual = Saldo Inicial (AF) - Saldo Executado (NFs)`. Nenhuma NF é processada se o valor executado for maior que o saldo atual disponível.
- **Vínculos Manuais:** Devido a limitações na padronização dos PDFs de origem, os vínculos entre *Solicitação -> Empenho* e as *Vigências de Contrato* devem ser informados pelo usuário na interface no momento do upload.

## Instalação e Execução

Para executar o projeto localmente, siga os passos abaixo:

1. **Clone o repositório:**

```bash
git clone <url-do-repositorio>
cd controladoria-contratos
```

2. **Crie e ative um ambiente virtual (recomendado):**

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/MacOS
source .venv/bin/activate
```

3. **Instale as dependências:**

```bash
pip install -r requirements.txt
```


4. **Execute a aplicação:**

```bash
streamlit run app.py
```

*Nota: O banco de dados (`database.db`) e as tabelas serão inicializados automaticamente na primeira execução, com base no arquivo `schema.sql`.*

## Glossário

- **AF:** Autorização de Fornecimento. Documento que autoriza o fornecedor a entregar os itens empenhados.
- **NF:** Nota Fiscal. Documento fiscal que comprova a entrega/execução e consome o saldo da AF.
- **RP:** Registro de Preços.
- **PK:** *Primary Key* (Chave Primária do banco de dados).
