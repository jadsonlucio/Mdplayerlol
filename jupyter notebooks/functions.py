import numpy as np
from sklearn.preprocessing import MinMaxScaler

def add_atributos_relativos(match_dataframe,atributos):
    """
    Adiciona atributos relativos a cada time a um dataframe de uma partidas
    
    Parameters
    ----------
    match_dataframe : DataFrame
        Dataframe de uma partida onde cada linha representa um jogador
        e cada columa um atributo.
    atributos : list
        Lista dos atributos que serão relativizados de acordo com o
        time
    
    Returns
    --------
    dataframe : Dataframe com os atributos relativos adicionados.
    
    """
    for atributo in atributos:
        array_time_1=match_dataframe[atributo][:5]
        array_time_2=match_dataframe[atributo][5:]
        soma_array_time_1=sum(array_time_1)
        soma_array_time_2=sum(array_time_2)
        if(soma_array_time_1==0):
            rel_array_time_1=np.zeros(5)
        else:
            rel_array_time_1=[value/soma_array_time_1 for value in array_time_1]
            
        if(soma_array_time_2==0):
            rel_array_time_2=np.zeros(5)
        else:
            rel_array_time_2=[value/soma_array_time_2 for value in array_time_2]
        
        array_match=[]
        [array_match.append(value) for value in rel_array_time_1]
        [array_match.append(value) for value in rel_array_time_2]
        
        match_dataframe["rel_"+atributo]=np.array(array_match)

    return match_dataframe

#adiciona colunas de atributos relativos aos atributos de um dataframe

def add_atributos_normalizados(dataframe,atributos):
    for atributo in atributos:
        serie=dataframe.get(atributo)
        serie=(serie-min(serie))/(max(serie)-min(serie))
        dataframe["norm_"+atributo]=serie
    
    return dataframe
    
#função que recebe a role e a lane e retorna a posição do jogador (adc,sup,mid,jg,top)
def get_position(dict):
    if(dict["role"]=="DUO_CARRY"):
        return "adc"
    elif(dict["role"]=="DUO_SUPPORT"):
        return "sup"
    elif(dict["lane"]=="MIDDLE"):
        return "mid"
    elif(dict["lane"]=="JUNGLE"):
        return "jg"
    elif(dict["lane"]=="TOP"):
        return "top"
    else:
        return None 
    
    
