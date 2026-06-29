def parse_currency(value_str: str) -> float:
    if not value_str:
        return 0.0
    cleaned_str = value_str.replace('.', '').replace(',', '.')
    try:
        return float(cleaned_str)
    except ValueError:
        return 0.0

def format_date_to_database(date_str: str) -> str:
    if not date_str or len(date_str) != 10:
        return date_str
    parts = date_str.split('/')
    if len(parts) == 3:
        return f'{parts[2]}-{parts[1]}-{parts[0]}'
    return date_str