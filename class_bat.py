##creating building class
from class_infra import get_infra_difficulty

class Batiment:
  def __init__(self, id, list_infra):
    self.id = id
    self.list_infra = list_infra

  def get_building_difficulty(self):
        for infra in self.list_infra:
           difficulty = infra.get_infra_difficulty()
        return difficulty
  
  def __lt__(self, other_building):
    return self.get_building_difficulty() < other_building.get_building_difficulty()