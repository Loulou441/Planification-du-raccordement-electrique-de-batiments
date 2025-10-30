##Main project file

##Import all necessary functions
import pandas as pd
from data_prep import broken_network, create_dico_temps, create_dico_price
from modelisation import LinearGraph
from simulation import ProjectManager
from hospital import get_hospital_info

##Import dataframe
network_df = pd.read_excel('cas pratique _ planification de raccordement/reseau_en_arbre.xlsx')
info_infra = pd.read_csv('cas pratique _ planification de raccordement/infra.csv')
info_infra = info_infra.rename(columns={'id_infra': 'infra_id'})
info_batiment = pd.read_csv('cas pratique _ planification de raccordement/batiments.csv')

##Dataframe preparation
network_df['nb_maisons'] = network_df['nb_maisons'].astype(int)
network_df['id_batiment'] = network_df['id_batiment'].astype(str)
network_df['infra_id'] = network_df['infra_id'].astype(str)
network_df['infra_type'] = network_df['infra_type'].astype(str)
network_df['longueur'] = network_df['longueur'].astype(float)

##Cleaning Data
network_df_unique = network_df.drop_duplicates()
broken_network_df,list_id_batiment,state_batiment = broken_network(network_df_unique)
broken_network_df_no_houses =  broken_network_df.drop('nb_maisons', axis=1)

## Get all extra info on buildings and infras including prices and time to repair
broken_network_df_2 = broken_network_df_no_houses.merge(info_batiment, on='id_batiment', how = "left")
broken_network_df_3 = broken_network_df_2.merge(info_infra, on='infra_id', how = "left")

dico_price = create_dico_price(broken_network_df_3)
dico_temps = create_dico_temps (broken_network_df_3)

broken_network_df_3['price'] = broken_network_df_3['infra_id'].map(dico_price)
broken_network_df_3['temps'] = broken_network_df_3['infra_id'].map(dico_temps)

broken_network_df_3['price'] = broken_network_df_3['price']*broken_network_df_3['longueur']
broken_network_df_3['temps'] = broken_network_df_3['temps']*broken_network_df_3['longueur']
network_with_hospital = broken_network_df_3
network_with_hospital.to_excel('modelisation_files/network_with_hospital.xlsx', index=False)

##Create files for QGIS
state_df=pd.DataFrame({"id_batiment": list_id_batiment, "state_batiment" : state_batiment})
state_df.to_excel('modelisation_files/etat_batiment.xlsx', index=False)

##Modelisation
graph = LinearGraph()
graph.build_from_csv("modelisation_files/network_with_hospital.xlsx")

##Exploration et results
##Dealing with the hospital
id_hospital, budjet_hospital, temps_hospital = get_hospital_info(network_with_hospital)
print("Le budjet total de réparation de l'hôpital est "+str(budjet_hospital)+"€ et prendra un total de "+str(temps_hospital)+" heures")

##Dealing with the rest
final_network = network_with_hospital[~network_with_hospital['id_batiment'].isin([id_hospital])]
pm = ProjectManager.from_dataframe(final_network)
ranked_buildings = pm.simulate_fixing(verbose=True)
ranked_buildings
