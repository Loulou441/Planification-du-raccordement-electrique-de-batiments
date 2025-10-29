##creating building class

class Batiment:
  def __init__(self, id, list_infra):
    self.id = id
    self.list_infra = list_infra

#Instances attibutes to be define with self
  def get_building_difficulty(self):
        """
        difficulté_batiment = somme des difficultés des infras liées à ce bâtiment
        """
        # Fusion des difficultés d'infra avec le réseau d’origine
        merged_df = self.df.merge(self.df_infra[['infra_id', 'difficulte_infra']], on='infra_id', how='left')

        # Agrégation par bâtiment
        batiment_df = (
            merged_df.groupby('id_batiment', as_index=False)
            .agg({
                'difficulte_infra': 'sum'
            })
        )

        batiment_df.rename(columns={'difficulte_infra': 'difficulte_batiment'}, inplace=True)
        self.df_batiment = batiment_df
        return self.df_batiment
  
  def __lt__(self):
     return 0