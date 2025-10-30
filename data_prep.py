import pandas as pd
from constant import prix_aerien,prix_fourreau,prix_semi_aerien
from constant import temps_aerien,temps_fourreau,temps_semi_aerien

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
        return prix_aerien
    elif infra_type == 'semi-aerien':
        return prix_semi_aerien
    else:
        return prix_fourreau

def get_right_time(infra_type):
    if infra_type == 'aerien':
        return temps_aerien
    elif infra_type == 'semi-aerien':
        return temps_semi_aerien
    else:
        return temps_fourreau

