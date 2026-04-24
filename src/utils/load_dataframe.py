import pandas as pd

def load_dataframe(columns, data_table, load_data_function):
    dataframe = load_data_function(data_table)

    if dataframe.empty:
        return pd.DataFrame(columns=columns)
    
    return dataframe.reindex(columns=columns)