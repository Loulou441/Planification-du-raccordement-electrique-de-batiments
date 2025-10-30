##creating building class
class Batiment:
    """
    Represents a building or a complex of houses.
    """
    def __init__(self, id_batiment, type_batiment, nb_maisons, list_infra=None):
        self.id_batiment = id_batiment
        self.type_batiment = type_batiment
        self.nb_maisons = int(nb_maisons)
        self.list_infra = list_infra if list_infra is not None else []

    def __repr__(self):
        return (f"Batiment(ID: {self.id_batiment}, Type: '{self.type_batiment}', "
                f"Houses: {self.nb_maisons}, Infra Count: {len(self.list_infra)}, Total Difficulty: {self.calculate_difficulty():.2f})")

    def get_details(self):
        return f"Building ID: {self.id_batiment}, Type: {self.type_batiment}, Number of Units: {self.nb_maisons}"

    def calculate_difficulty(self):
        total_difficulty = 0.0
        for infra in self.list_infra:
            total_difficulty += infra.calculate_difficulty()
        return total_difficulty

    def remove_infra(self, infra_id):
        """
        Removes a specified Infra object (by ID) from this Batiment's list.
        Returns True if an infra object was successfully removed.
        """
        original_len = len(self.list_infra)
        self.list_infra = [infra for infra in self.list_infra if infra.infra_id != infra_id]
        return original_len != len(self.list_infra)