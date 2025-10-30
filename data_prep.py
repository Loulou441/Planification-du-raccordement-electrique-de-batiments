import pandas as pd

##Drop not broken houses
def broken_network(network_df):
    broken_network_df = network_df[network_df['infra_type']=='a_remplacer']
    set_id_batiment = set(network_df["id_batiment"].values)
    set_id_broken_batiment = set(broken_network_df['id_batiment'].values)

    list_id_batiment, state_batiment = [],[]
    for id_batiment in set_id_batiment:
        list_id_batiment.append(id_batiment)
        if id_batiment in set_id_broken_batiment:
            state_batiment.append("to_repare")
        else:
            state_batiment.append("intact")

    return broken_network_df,list_id_batiment,state_batiment