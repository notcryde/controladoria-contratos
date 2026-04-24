def convert_dataframe_to_csv(dataframe):
    '''Converte o dataframe para CSV no padrão PT-BR.'''
    return dataframe.to_csv(index=False, sep=';', decimal=',', encoding='utf-8-sig')