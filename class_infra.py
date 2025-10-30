##Creating infra class

class Infra:
    """
    Represents an infrastructure element.
    The 'longueur' attribute has been replaced by 'price' and 'temps'.
    """
    def __init__(self, infra_id, infra_type, infra_state, price, temps, nb_maisons):
        self.infra_id = infra_id
        self.infra_type = infra_type
        self.infra_state = infra_state
        # New attributes replacing longueur
        self.price = float(price)
        self.temps = float(temps)
        # This nb_maisons is the AGGREGATE sum of houses served by this infrastructure.
        self.nb_maisons = int(nb_maisons)
        self.is_fixed = False # NEW: Status flag for fixing

    def __repr__(self):
        fixed_status = " (FIXED)" if self.is_fixed else ""
        return (f"Infra(ID: '{self.infra_id}', Type: '{self.infra_type}', "
                f"Price: {self.price:.2f}, Time: {self.temps:.2f}, Served Houses: {self.nb_maisons}, Difficulty: {self.calculate_difficulty():.2f}{fixed_status})")

    def is_operational(self):
        return self.infra_state.lower() == 'infra_intacte'

    def calculate_difficulty(self):
        """
        Calculates difficulty as the combined price and time cost per house served.
        Returns 0.0 if the infrastructure is marked as fixed.
        """
        if self.is_fixed:
            return 0.0

        if self.nb_maisons == 0:
            return 0.0
        # New difficulty formula: (Price + Time) / Total Houses Served
        return (self.price * self.temps) / self.nb_maisons
