##creating building class

class Batiment:
  def __init__(self, id, list_infra):
    self.id = id
    self.list_infra = list_infra

    #Instances attibutes to be define with self
  def get_building_difficulty(self):
      return 0
  
  def __lt__(self):
     return 0