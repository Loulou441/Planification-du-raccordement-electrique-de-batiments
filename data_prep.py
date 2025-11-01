import pandas as pd
from config import AERIEN_PRICE,SEMI_AERIEN_PRICE,FOURREAU_PRICE
from config import AERIEN_TIME,SEMI_AERIEN_TIME,FOURREAU_TIME

##Drop not broken houses
def broken_network(df : pd.DataFrame):
    broken_network_df = df[df['infra_type']=='a_remplacer']
    set_id_batiment = set(df["id_batiment"].values)
    set_id_broken_batiment = set(broken_network_df['id_batiment'].values)

    list_id_batiment, state_batiment = [],[]
    for id_batiment in set_id_batiment:
        list_id_batiment.append(id_batiment)
        if id_batiment in set_id_broken_batiment:
            state_batiment.append("to_repare")
        else:
            state_batiment.append("intact")

    return broken_network_df,list_id_batiment,state_batiment

def get_right_price(infra_type):
    if infra_type == 'aerien':
        return AERIEN_PRICE
    elif infra_type == 'semi-aerien':
        return SEMI_AERIEN_PRICE
    else:
        return FOURREAU_PRICE

def get_right_time(infra_type):
    if infra_type == 'aerien':
        return AERIEN_TIME
    elif infra_type == 'semi-aerien':
        return SEMI_AERIEN_TIME
    else:
        return FOURREAU_TIME
    
def create_dico_price(df: pd.DataFrame):
    dico_price = {}
    list_infra_id = list(df['infra_id'])
    for infra in list_infra_id:
        dico_price[infra] = get_right_price(df.loc[df['infra_id'] == infra, 'type_infra'].iloc[0])
    return dico_price

def create_dico_temps(df: pd.DataFrame):
    dico_temps = {}
    list_infra_id = list(df['infra_id'])
    for infra in list_infra_id:
        dico_temps[infra] = get_right_time(df.loc[df['infra_id'] == infra, 'type_infra'].iloc[0])
    return dico_temps


