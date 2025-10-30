##All simulation functions
import pandas as pd
from typing import List, Dict, Tuple
from class_bat import Batiment
from class_infra import Infra

class ProjectManager:
    """
    Manages Buildings and Infrastructure instances.
    Provides simulation and ranking methods.
    """

    def __init__(self, buildings: List['Batiment'], infrastructure: List['Infra']):
        self.buildings = buildings
        self.infrastructure = infrastructure

    # -----------------------------
    # 🏗️ Class Constructor
    # -----------------------------
    @classmethod
    def from_dataframe(cls, df: pd.DataFrame) -> 'ProjectManager':
        """
        Creates a ProjectManager instance from a pandas DataFrame.
        Expects columns: id_batiment, nb_maisons, price, temps, infra_id, type_batiment, infra_type.
        """
        required_cols = ['id_batiment', 'nb_maisons', 'price', 'temps', 'infra_id', 'type_batiment', 'infra_type']
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            raise ValueError(f"Missing columns: {missing}")

        # --- Data preparation ---
        df = df.copy()
        df['id_batiment'] = df['id_batiment'].astype(str)
        df['num_houses'] = df['nb_maisons'].astype(int)
        df['price'] = df['price'].astype(float)
        df['temps'] = df['temps'].astype(float)
        df['infra_id'] = df['infra_id'].astype(str)

        # Aggregate total houses per infrastructure
        infra_house_map = (
            df.groupby('infra_id')['num_houses'].sum().to_dict()
        )

        # Create unique Infrastructure instances
        infra_instances = {}
        for _, row in df.drop_duplicates(subset=['infra_id']).iterrows():
            infra_instances[row['infra_id']] = Infra(
                infra_id=row['infra_id'],
                infra_type=row['infra_type'],
                infra_state='Operational',
                price=row['price'],
                temps=row['temps'],
                nb_maisons=infra_house_map[row['infra_id']],
            )

        # Link infrastructures to buildings
        building_instances = []
        grouped = df.groupby('id_batiment')
        for b_id, group in grouped:
            linked_infras = [infra_instances[iid] for iid in group['infra_id'].unique()]
            building_instances.append(
                Batiment(
                    id_batiment=b_id,
                    type_batiment=group['type_batiment'].iloc[0],
                    nb_maisons=group['nb_maisons'].iloc[0],
                    list_infra=linked_infras,
                )
            )

        return cls(building_instances, list(infra_instances.values()))

    # -----------------------------
    # ⚙️ Core Methods
    # -----------------------------
    def rank_buildings(self) -> List['Batiment']:
        """Return buildings sorted by total difficulty (ascending)."""
        return sorted(self.buildings, key=lambda b: b.calculate_difficulty())

    def fix_building(self, building: 'Batiment', verbose: bool = False) -> List[str]:
        """
        Fix the given building and update shared infrastructures.
        Returns a list of infrastructure IDs that were fixed.
        """
        fixed_ids = [infra.infra_id for infra in building.list_infra if not infra.is_fixed]
        for infra in building.list_infra:
            infra.is_fixed = True

        if not fixed_ids:
            return []

        for b in self.buildings:
            if b is building:
                continue
            before = b.calculate_difficulty()
            # Remove fixed infrastructures from other buildings
            b.list_infra = [i for i in b.list_infra if i.infra_id not in fixed_ids]
            after = b.calculate_difficulty()

            if verbose and before != after:
                print(f"  Building {b.id_batiment}: difficulty {before:.2f} → {after:.2f}")

        return fixed_ids

    def simulate_fixing(self, verbose: bool = True) -> Dict[int, int]:
        """
        Iteratively fix buildings by ascending difficulty.
        Buildings with difficulty == 0 are skipped (already fixed),
        but do not stop the simulation.
        Logs the infrastructures fixed for each building.
        """
        results = {}
        rank = 1

        if verbose:
            print("\n--- Fixing Simulation Started ---")

        remaining = set(self.buildings)

        while remaining:
            # Sort by current difficulty
            ranked = sorted(remaining, key=lambda b: b.calculate_difficulty())
            current = ranked[0]
            diff = current.calculate_difficulty()

            # Skip buildings that are already effectively fixed
            if diff == 0:
                if verbose:
                    print(f"Skipping Building {current.id_batiment} (already fixed)")
                results[current.id_batiment] = rank
                remaining.remove(current)
                continue

            if verbose:
                print(f"\nStep {rank}: Fixing Building {current.id_batiment} (difficulty {diff:.2f})")

            # Fix the building and get list of fixed infrastructures
            fixed_infra_ids = self.fix_building(current, verbose=verbose)
            results[current.id_batiment] = rank
            remaining.remove(current)

            if verbose:
                infra_list_str = ", ".join(fixed_infra_ids) if fixed_infra_ids else "None"
                print(f"  → Fixed infrastructures: [{infra_list_str}]")

            rank += 1

        if verbose:
            print("\n--- Simulation Complete ---")
        return results