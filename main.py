##Main project file

##Import all necessary functions
import pandas as pd
from data_prep import broken_network
from modelisation import LinearGraph

##Import dataframe
network_df = pd.read_excel('cas pratique _ planification de raccordement/reseau_en_arbre.xlsx')

##Dataframe preparation
network_df['nb_maisons'] = network_df['nb_maisons'].astype(int)
network_df['id_batiment'] = network_df['id_batiment'].astype(str)
network_df['infra_id'] = network_df['infra_id'].astype(str)
network_df['infra_type'] = network_df['infra_type'].astype(str)
network_df['longueur'] = network_df['longueur'].astype(float)

##Cleaning Data
network_df_unique = network_df.drop_duplicates()
broken_network_df,list_id_batiment,state_batiment = broken_network(network_df_unique)
##Add potentially other preparation
final_network = broken_network_df
final_network.to_excel('modelisation_files/network_remastered.xlsx')

##Create files for QGIS
state_df=pd.DataFrame({"id_batiment": list_id_batiment, "state_batiment" : state_batiment})
state_df.to_excel('modelisation_files/etat_batiment.xlsx', index=False)

##Modelisation
graph = LinearGraph()
graph.build_from_csv("modelisation_files/network_remastered.xlsx")

##Exploration et résultat
list_bat_to_repare = final_network["id_batiment"].drop_duplicates()
print(list_bat_to_repare)