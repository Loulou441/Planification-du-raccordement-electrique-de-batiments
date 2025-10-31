##All simulation functions
import pandas as pd
from typing import List, Dict
from class_bat import Building
from class_infra import Infrastructure
from constant_values import PHASES

class BrokenBuildings:
    """
    Manages Buildings and Infrastructure instances, Reading the data from a dataframe.
    Provides simulation, ranking, and cost-phase allocation methods.
    """

    def __init__(self, buildings: List[Building]):
        self.buildings = buildings

    # ---------- Factory ----------
    @classmethod
    def from_dataframe(cls, df: pd.DataFrame) -> 'BrokenBuildings':
        required_cols = ['id_batiment', 'nb_maisons', 'infra_id', 'type_batiment', 'type_infra', 'longueur', 'infra_state']
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            raise ValueError(f"Missing columns: {missing}")

        df = df.copy()
        df['building_id'] = df['id_batiment'].astype(str)
        df['num_houses'] = df['nb_maisons'].astype(int)
        df['longueur'] = df['longueur'].astype(float)
        df['infrastructure_id'] = df['infra_id'].astype(str)

        infra_house_map = df.groupby('infrastructure_id')['num_houses'].sum().to_dict()

        infra_instances = {
            row['infrastructure_id']: Infrastructure(
                infrastructure_id=row['infrastructure_id'],
                infrastructure_type=row['type_infra'],
                infrastructure_state=row['infra_state'],
                length=row['longueur'],
                num_houses=infra_house_map[row['infrastructure_id']],
            )
            for _, row in df.drop_duplicates(subset=['infrastructure_id']).iterrows()
        }

        buildings = []
        for b_id, group in df.groupby('building_id'):
            linked = [infra_instances[iid] for iid in group['infrastructure_id'].unique()]
            buildings.append(
                Building(
                    building_id=b_id,
                    building_type=group['type_batiment'].iloc[0],
                    num_houses=group['num_houses'].iloc[0],
                    infrastructure_list=linked,
                )
            )

        return cls(buildings)

    # ---------- Fixing Mechanics ----------
    def fix_building(self, target_building: Building, verbose=False) -> List[str]:
        """Fix a building and remove its infrastructures from others."""
        fixed_ids = [infra.infrastructure_id for infra in target_building.infrastructure_list if not infra.is_fixed]
        for infra in target_building.infrastructure_list:
            infra.is_fixed = True

        if not fixed_ids:
            return []

        for building in self.buildings:
            if building is target_building:
                continue
            before = building.calculate_difficulty()
            building.infrastructure_list = [i for i in building.infrastructure_list if i.infrastructure_id not in fixed_ids]
            after = building.calculate_difficulty()
            if verbose and before != after:
                print(f"  Building {building.building_id}: difficulty {before:.2f} → {after:.2f}")

        return fixed_ids

    # ---------- Simulation ----------
    def simulate_fixing(self, verbose=True):
        """
        High-level orchestration: simulate the fixing process,
        compute total costs, assign phases, and summarize results.
        """
        if verbose:
            print("\n--- Fixing Simulation Started ---")

        # Step 1: Simulate dynamic fixing (returns order, costs, and times)
        fixed_order, building_costs, building_times = self._run_fixing_sequence(verbose=verbose)

        # Step 2: Compute total cost and phase thresholds
        total_cost = sum(building_costs.values())
        thresholds = self._compute_phase_thresholds(total_cost)

        # Step 3: Assign buildings to phases based on cumulative cost
        building_phase_map = self._assign_buildings_to_phases(fixed_order, building_costs, thresholds)

        # Step 4: Summarize cost/time per phase
        summary = self._summarize_phases(building_phase_map, building_costs, building_times, total_cost, verbose)

        return summary

    def _run_fixing_sequence(self, verbose=False):
        """Simulate the actual fixing process, updating buildings dynamically."""
        remaining = [b for b in self.buildings]
        fixed_order = []
        building_costs = {}
        building_times = {}
        rank = 1

        while remaining:
            remaining.sort(key=lambda b: b.calculate_difficulty())
            current = remaining[0]
            diff = current.calculate_difficulty()

            if diff == 0:
                if verbose:
                    print(f"Skipping Building {current.building_id} (already fixed)")
                remaining.pop(0)
                continue

            if verbose:
                print(f"\nStep {rank}: Fixing Building {current.building_id} (difficulty {diff:.2f})")

            building_costs[current.building_id] = current.total_cost
            building_times[current.building_id] = current.total_time

            self.fix_building(current, verbose=verbose)

            fixed_order.append(current)
            remaining.pop(0)
            rank += 1

        return fixed_order, building_costs, building_times

    def _compute_phase_thresholds(self, total_cost: float) -> List[float]:
        """Compute cumulative cost thresholds based on PHASES."""
        return [sum(PHASES[:i]) * total_cost for i in range(1, len(PHASES) + 1)]

    def _assign_buildings_to_phases(self, fixed_order: List[Building],
                                    building_costs: Dict[str, float],
                                    thresholds: List[float]) -> Dict[str, int]:
        """Assign buildings to phases dynamically based on cumulative cost."""
        cumulative = 0.0
        building_phase_map = {}
        num_phases = len(PHASES)

        for building in fixed_order:
            cumulative += building_costs[building.building_id]
            for i, threshold in enumerate(thresholds, start=1):
                if cumulative <= threshold:
                    phase = i
                    break
            else:
                phase = num_phases
            building_phase_map[building.building_id] = phase

        return building_phase_map

    def _summarize_phases(self, building_phase_map, building_costs, building_times, total_cost, verbose):
        """Aggregate cost/time per phase and print a summary."""
        num_phases = len(PHASES)
        phase_buildings = {i + 1: [] for i in range(num_phases)}
        phase_cost = {i + 1: 0.0 for i in range(num_phases)}
        phase_time = {i + 1: 0.0 for i in range(num_phases)}

        # Group buildings by phase
        for b_id, phase in building_phase_map.items():
            phase_buildings[phase].append(b_id)
            phase_cost[phase] += building_costs[b_id]

        # Compute time per phase as max(building_times)
        for phase in range(1, num_phases + 1):
            times = [building_times[b_id] for b_id in phase_buildings[phase]]
            phase_time[phase] = max(times) if times else 0.0

        if verbose:
            print("\n--- Simulation Complete ---")
            for ph in range(1, num_phases + 1):
                perc = (phase_cost[ph] / total_cost * 100) if total_cost else 0
                print(f"Phase {ph}: Buildings {phase_buildings[ph]}, "
                      f"Cost: {phase_cost[ph]:.2f} ({perc:.2f}%), Time: {phase_time[ph]:.2f}h")

        return {
            "phase_buildings": phase_buildings,
            "phase_cost": phase_cost,
            "phase_time": phase_time,
            "building_phase_map": building_phase_map,
            "total_project_cost": total_cost
        }