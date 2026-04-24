import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode

def render_table(dataframe, table_columns):
    grid_builder = GridOptionsBuilder.from_dataframe(dataframe)
    
    grid_builder.configure_default_column(
        resizable=True, 
        filter=True, 
        sortable=True, 
        minWidth=150, 
        wrapText=True, 
        autoHeight=True
    )
    
    grid_builder.configure_pagination(paginationPageSize=10) 
    
    grid_options = grid_builder.build()
    
    grid_response = AgGrid(
        dataframe, 
        gridOptions=grid_options, 
        height=400,
        fit_columns_on_grid_load=False, 
        theme='streamlit',
        update_mode=GridUpdateMode.MODEL_CHANGED,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED
    )

    if 'data' in grid_response and grid_response['data'] is not None:
        return pd.DataFrame(grid_response['data'])

    return pd.DataFrame(columns=table_columns)