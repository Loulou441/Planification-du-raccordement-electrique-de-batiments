##Creating infra class
from config import EQUIPMENT_PRICE, TIME_TO_FIX, WORKER_PAY_PER_8H, MAX_WORKERS_PER_INFRA

class Infrastructure:
    """
    Represents a single infrastructure element .
    used length to assess the cost of the infrastructure.
    """
    def __init__(self, infrastructure_id: str, infrastructure_type: str, length: float,
                 infrastructure_state: str, num_houses: int):
        self.infrastructure_id = infrastructure_id
        self.infrastructure_type = infrastructure_type
        self.infrastructure_state = infrastructure_state
        self.length = length
        self.num_houses = num_houses
        self.is_fixed = False

    @property
    def equipement_cost(self) -> float:
        """Material cost based on equipment type and length."""
        return EQUIPMENT_PRICE.get(self.infrastructure_type, 0) * self.length

    @property
    def repair_time_hours(self) -> float:
        """Total repair time in hours."""
        return TIME_TO_FIX.get(self.infrastructure_type, 0) * self.length

    @property
    def labor_cost(self) -> float:
        """
        Computes labor cost based on repair time and workers assigned.
        - Up to 4 workers can work simultaneously.
        - Workers are paid per actual hour worked.
        """
        total_hours = self.repair_time_hours
        pay_per_hour = WORKER_PAY_PER_8H / 8

        # Each wave of work (with up to 4 workers) covers 8h * 4 = 32 worker-hours
        full_shifts = int(total_hours // (8 * MAX_WORKERS_PER_INFRA))
        remaining_hours = total_hours % (8 * MAX_WORKERS_PER_INFRA)

        # Cost for full 4-worker shifts
        cost = full_shifts * (MAX_WORKERS_PER_INFRA * 8 * pay_per_hour)

        # Remaining work may not fill a full shift
        # Calculate how many hours are left, spread across up to 4 workers
        if remaining_hours > 0:
            # Each remaining worker can work up to 8h
            full_workers = int(remaining_hours // 8)
            last_worker_hours = remaining_hours % 8

            cost += full_workers * 8 * pay_per_hour
            if last_worker_hours > 0:
                cost += last_worker_hours * pay_per_hour

        return cost

    @property
    def total_cost(self) -> float:
        """Total cost = equipment cost + labor cost."""
        return self.equipement_cost + self.labor_cost

    def calculate_difficulty(self) -> float:
        """
        Calculates difficulty as (equipment_price * time) / num_houses.
        Returns 0.0 if the infrastructure is fixed.
        """
        if self.is_fixed or self.num_houses == 0:
            return 0.0
        total_price = self.length * EQUIPMENT_PRICE[self.infrastructure_type]
        total_time = self.length * TIME_TO_FIX[self.infrastructure_type]
        return (total_price * total_time) / self.num_houses

    def __repr__(self):
        fixed_status = " (FIXED)" if self.is_fixed else ""
        return (
            f"Infrastructure(ID: '{self.infrastructure_id}', Type: '{self.infrastructure_type}', "
            f"Equip. Cost: {self.equipement_cost:.2f}, Labor: {self.labor_cost:.2f}, "
            f"Total: {self.total_cost:.2f}, Time: {self.repair_time_hours:.2f}h, "
            f"Houses: {self.num_houses}, Diff: {self.calculate_difficulty():.2f}{fixed_status})"
        )

    def __radd__(self, other):
        if isinstance(other, (int, float)):
            return other + self.calculate_difficulty()
        return self.calculate_difficulty()