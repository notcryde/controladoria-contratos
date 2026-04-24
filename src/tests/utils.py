import pdfplumber
import re

def extract(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return ' '.join([p.extract_text(x_tolerance=3) or '' for p in pdf.pages])

def raw_text(pdf_path):
    print(f'\n--- RAW TEXT: {pdf_path.name} ---\n')
    print(extract(pdf_path))

def print_section(title, patterns, text, width):
    print(f'\n--- {title} ---')
    for label, regex in patterns.items():
        match = re.search(regex, text)
        if match:
            value = match.group(1).strip().replace('\n', ' ')
            value = value if value else 'N/A'
            print(f'{label.ljust(width)}: {value}')
        else:
            print(f'{label.ljust(width)}: N/A')

def extract_tables_from_pdf(pdf_path):
    tables_data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            settings = {
                "vertical_strategy": "lines",
                "horizontal_strategy": "text",
                "intersection_y_tolerance": 15
            }
            tables = page.extract_tables(table_settings=settings)
            for table in tables:
                cleaned_table = []
                for row in table:
                    cleaned_row = [str(cell).replace('\n', ' ').strip() if cell is not None else '' for cell in row]
                    if any(cleaned_row):
                        cleaned_table.append(cleaned_row)
                if cleaned_table:
                    tables_data.append(cleaned_table)
    return tables_data