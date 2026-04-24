import io
import pandas as pd

def convert_dataframe_to_excel(dataframe):
    memory_buffer = io.BytesIO()
    with pd.ExcelWriter(memory_buffer, engine='xlsxwriter') as excel_writer:
        dataframe.to_excel(excel_writer, index=False, sheet_name='Relatório')
    return memory_buffer.getvalue()