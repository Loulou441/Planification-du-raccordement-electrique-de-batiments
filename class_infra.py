##Creating infra class
class Infra :
    def __init__(self, infra_id, lengh, infra_type, nb_maisons, infra_type_construction) :
        self.infra_id = infra_id
        self.lengh = lengh
        self.infra_type = infra_type
        self.nb_maisons = nb_maisons
        self.infra_type_construction = 0 
        
    def repair_infra(self):
        self.infra_type = "infra_intacte"
    
    def get_infra_difficulty(self):
        difficulty = self.lengh / self.nb_maisons
        return difficulty
    
    def __radd__ (self): 
        return 0
    
    class Type_Infra :
        def __init__(self, nom, prix, duree):
            self.nom = nom
            self.prix = prix
            self.duree = duree

        def get_type_infra_prix(self):
            return self.prix
        
        

