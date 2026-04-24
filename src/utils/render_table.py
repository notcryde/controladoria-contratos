import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode

def render_table(dataframe, table_columns, enable_selection=False, key=None):
    if dataframe.empty:
        return pd.DataFrame(columns=table_columns), None

    grid_builder = GridOptionsBuilder.from_dataframe(dataframe)
    
    grid_builder.configure_default_column(
        resizable=True, 
        filter=True, 
        sortable=True, 
        minWidth=100, 
        wrapText=True, 
        autoHeight=True,
        headerClass='header-center'
    )
    
    grid_builder.configure_pagination(paginationPageSize=15) 
    
    monetary_keywords = ['Valor', 'Total', 'Liberação', 'Unitário', 'Saldo', 'Executado', 'Empenhado']
    
    for col in dataframe.columns:
        if any(word in col for word in monetary_keywords):
            grid_builder.configure_column(
                col, 
                valueFormatter="x != null ? Number(x).toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'}) : 'R$ 0,00'"
            )

    if enable_selection and 'Ações' in table_columns:
        grid_builder.configure_selection(selection_mode="single", use_checkbox=False)
        
        btn_cell_renderer = JsCode('''
            class BtnCellRenderer {
                init(params) {
                    this.params = params;
                    this.eGui = document.createElement('div');
                    this.eGui.style.display = 'flex';
                    this.eGui.style.justifyContent = 'center';
                    this.eGui.style.alignItems = 'center';
                    this.eGui.style.height = '100%';
                    this.eGui.style.width = '100%';
                    this.eGui.innerHTML = `
                        <button style="
                            background-color: #1f77b4; 
                            border: none; 
                            border-radius: 4px; 
                            color: white; 
                            cursor: pointer; 
                            padding: 6px 16px; 
                            min-width: 120px;
                            width: auto;
                            font-size: 13px;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            white-space: nowrap;
                        ">Ver Itens</button>
                    `;
                    this.eBtn = this.eGui.querySelector('button');
                    this.btnClickedHandler = this.btnClickedHandler.bind(this);
                    this.eBtn.addEventListener('click', this.btnClickedHandler);
                }
                btnClickedHandler(event) {
                    this.params.node.setSelected(true);
                }
                getGui() { return this.eGui; }
                destroy() { this.eBtn.removeEventListener('click', this.btnClickedHandler); }
            }
        ''')
        
        grid_builder.configure_column(
            'Ações', 
            cellRenderer=btn_cell_renderer,
            minWidth=160,
            maxWidth=200,
            suppressMenu=True,
            sortable=False,
            headerClass='header-center'
        )
    
    grid_options = grid_builder.build()
    
    grid_response = AgGrid(
        dataframe, 
        gridOptions=grid_options, 
        height=500,
        fit_columns_on_grid_load=True, 
        theme='streamlit',
        update_mode=GridUpdateMode.MODEL_CHANGED | GridUpdateMode.SELECTION_CHANGED,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        allow_unsafe_jscode=True,
        key=key
    )

    df_returned = pd.DataFrame(grid_response['data']) if grid_response['data'] is not None else pd.DataFrame(columns=table_columns)
    return df_returned, grid_response.get('selected_rows', None)