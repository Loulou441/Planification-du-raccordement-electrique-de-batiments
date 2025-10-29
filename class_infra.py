##Creating infra class
class Infra :
    def __init__(self, infra_id, lengh, infra_etat, nb_maisons, infra_type) :
        self.infra_id = infra_id
        self.lengh = lengh
        self.infra_etat = infra_etat
        self.nb_maisons = nb_maisons
        self.infra_type = infra_type
        
    def repair_infra(self):
        self.infra_etat = "infra_intacte"
    
    def get_infra_difficulty(self):
        difficulty = self.lengh / self.nb_maisons
        return difficulty
    
    def __radd__ (self): 
        return 0
        

