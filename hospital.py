from constant import paye_ouvrier_par_heure
import pandas as pd

def get_hospital_info(df: pd.DataFrame):
    id_bat_hospital = "".join(map(str, set(df[df['type_batiment']=='hôpital']['id_batiment'])))
    list_infra_hospital = list(df[df['id_batiment']==id_bat_hospital]['infra_id'])
    list_nb_ouvrier = [2,3,1]
    budjet_hopital = 0
    temps_hospital = 0
    for infra_nb in range(3):
        cout_ouvrier = paye_ouvrier_par_heure*df.loc[df['infra_id'] == list_infra_hospital[infra_nb], 'temps'].iloc[0]
        cout_materiel = df.loc[df['infra_id'] == list_infra_hospital[infra_nb], 'price'].iloc[0]
        budjet_hopital += cout_ouvrier + cout_materiel
        temps_infra = df.loc[df['infra_id'] == list_infra_hospital[infra_nb], 'temps'].iloc[0]/list_nb_ouvrier[infra_nb]
        temps_hospital = max(temps_hospital, temps_infra)
    return round(budjet_hopital, 2), round(temps_hospital,2)