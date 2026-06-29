PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS requests (
    request_number TEXT PRIMARY KEY,
    request_type TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS consumption_requests (
    request_number TEXT PRIMARY KEY,
    requested_value REAL,
    price_registration TEXT,
    start_date DATE,
    end_date DATE,
    requesting_unit TEXT,
    financial_department TEXT,
    notes TEXT,
    supplier_name TEXT,
    supplier_cnpj TEXT,
    FOREIGN KEY (request_number) REFERENCES requests(request_number) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS purchase_requests (
    request_number TEXT PRIMARY KEY,
    issue_date DATE,
    requested_value REAL,
    object TEXT,
    notes TEXT,
    requesting_unit TEXT,
    financial_department TEXT,
    activity TEXT,
    designed_manager TEXT,
    legislation TEXT,
    program TEXT,
    FOREIGN KEY (request_number) REFERENCES requests(request_number) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS commitments (
    commitment_number TEXT PRIMARY KEY,
    request_number TEXT NOT NULL UNIQUE,
    commited_value REAL,
    process_number TEXT,
    source TEXT,
    supplier_name TEXT,
    supplier_cnpj TEXT,
    supplier_phone TEXT,
    supplier_email TEXT,
    FOREIGN KEY (request_number) REFERENCES requests(request_number) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS authorizations (
    authorization_number TEXT PRIMARY KEY,
    commitment_number TEXT NOT NULL UNIQUE,
    process_number TEXT,
    modality TEXT,
    contract TEXT,
    notes TEXT,
    budget_sheet TEXT,
    budget_allocation TEXT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    FOREIGN KEY (commitment_number) REFERENCES commitments(commitment_number) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS authorization_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    authorization_number TEXT NOT NULL,
    material_code TEXT,
    description TEXT,
    quantity REAL,
    unitary_value REAL,
    FOREIGN KEY (authorization_number) REFERENCES authorizations(authorization_number) ON DELETE CASCADE
);

-- 7. Tabela: Notas Fiscais (Relação 1-N com AF)
CREATE TABLE IF NOT EXISTS invoices (
    invoice_number TEXT PRIMARY KEY,
    authorization_number TEXT NOT NULL,
    issue_date DATE,
    executed_value REAL,
    FOREIGN KEY (authorization_number) REFERENCES authorizations(authorization_number) ON DELETE CASCADE
);

-- 8. Tabela: Itens da Nota Fiscal (Relação 1-N com NF)
CREATE TABLE IF NOT EXISTS invoice_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_number TEXT NOT NULL,
    material_code TEXT,
    description TEXT,
    quantity REAL,
    unitary_value REAL,
    FOREIGN KEY (invoice_number) REFERENCES invoices(invoice_number) ON DELETE CASCADE
);