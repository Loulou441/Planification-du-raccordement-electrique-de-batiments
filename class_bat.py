##creating building class
from class_infra import Infrastructure
from typing import List

class Building:
    """
    Represents a building or a complex of houses.
    """

    def __init__(self, building_id: int, building_type: str, num_houses: int,
                 infrastructure_list: List[Infrastructure] = None):
        self.building_id = building_id
        self.building_type = building_type
        self.num_houses = num_houses
        self.infrastructure_list = infrastructure_list if infrastructure_list else []

    def __repr__(self):
        return (f"Building(ID: {self.building_id}, Type: '{self.building_type}', "
                f"Houses: {self.num_houses}, Infra Count: {len(self.infrastructure_list)}, "
                f"Total Difficulty: {self.calculate_difficulty():.2f})")
    @property
    def total_cost(self) -> float:
        """Total cost of unfixed infrastructures in this building."""
        return sum(infra.total_cost for infra in self.infrastructure_list if not infra.is_fixed)

    @property
    def total_time(self) -> float:
        """Total repair time of unfixed infrastructures in this building."""
        return sum(infra.repair_time_hours for infra in self.infrastructure_list if not infra.is_fixed)
        
    def calculate_difficulty(self) -> float:
        """Calculates the total difficulty of all linked infrastructures."""
        return sum(self.infrastructure_list)

    def remove_infrastructure(self, infrastructure_id: str) -> bool:
        """
        Removes a specified Infrastructure object (by ID).
        Returns True if an infrastructure was removed.
        """
        original_len = len(self.infrastructure_list)
        self.infrastructure_list = [
            infra for infra in self.infrastructure_list if infra.infrastructure_id != infrastructure_id
        ]
        return original_len != len(self.infrastructure_list)