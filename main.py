##Main project file

##Import all necessary functions
import pandas as pd
from data_prep import broken_network
from modelisation import LinearGraph
from simulation import ProjectManager

##Import dataframe
network_df = pd.read_excel('cas pratique _ planification de raccordement/reseau_en_arbre.xlsx')
info_infra = pd.read_csv('cas pratique _ planification de raccordement/infra.csv')
info_infra = info_infra.rename(columns={'id_infra': 'infra_id'})
info_batiment = pd.read_csv('cas pratique _ planification de raccordement/batiments.csv')
info_prix = pd.read_excel('cas pratique _ planification de raccordement/prix_infra.xlsx')

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

## Joining table to get all extra info on buildings and infras including prices
broken_network_df_2 = broken_network_df_no_houses.merge(info_batiment, on='id_batiment', how = "left")
broken_network_df_3 = broken_network_df_2.merge(info_infra, on='infra_id', how = "left")
broken_network_df_4 = broken_network_df_3.merge(info_prix, on='type_infra', how = "left")
broken_network_df_4['price'] = broken_network_df_4['price']*broken_network_df_4['longueur']
broken_network_df_4['temps'] = broken_network_df_4['temps']*broken_network_df_4['longueur']
final_network = broken_network_df_4
final_network.to_excel('modelisation_files/network_remastered.xlsx')

##Create files for QGIS
state_df=pd.DataFrame({"id_batiment": list_id_batiment, "state_batiment" : state_batiment})
state_df.to_excel('modelisation_files/etat_batiment.xlsx', index=False)

##Modelisation
graph = LinearGraph()
graph.build_from_csv("modelisation_files/network_remastered.xlsx")

##Exploration et résultat
pm = ProjectManager.from_dataframe(final_network)
ranked_buildings = pm.simulate_fixing(verbose=True)
ranked_buildings