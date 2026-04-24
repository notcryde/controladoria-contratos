import pandas as pd
from dateutil.relativedelta import relativedelta

def calcular_prazo(inicio, fim):
    if not inicio or not fim or pd.isna(inicio) or pd.isna(fim):
        return 'Data não informada'
    try:
        data_inicial = pd.to_datetime(inicio, format='%d/%m/%Y')
        data_final = pd.to_datetime(fim, format='%d/%m/%Y')
        
        if data_final < data_inicial:
            return 'Datas invertidas'
        elif data_final == data_inicial:
            return '1 dia'
            
        rd = relativedelta(data_final, data_inicial)
        meses = rd.years * 12 + rd.months
        dias_restantes = rd.days
        
        partes = []
        if meses > 0:
            partes.append(f'{meses} meses' if meses > 1 else f'{meses} mês')
        if dias_restantes > 0:
            partes.append(f'{dias_restantes} dias' if dias_restantes > 1 else f'{dias_restantes} dia')
            
        return ' e '.join(partes) if partes else '0 dias'
    except Exception:
        return 'Data inválida'