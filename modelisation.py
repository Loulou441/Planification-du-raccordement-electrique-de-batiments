import pandas as pd
from collections import defaultdict, deque
from dataclasses import dataclass, field

@dataclass
class EdgeInfo:
    """Stores dynamic edge attributes as a dictionary."""
    attributes: dict = field(default_factory=dict)

class LinearGraph:
    def __init__(self):
        # adjacency: node_id -> dict(neighbor_id -> EdgeInfo)
        self.adjacency = defaultdict(dict)

    def add_edge(self, src: str, dst: str, **edge_data):
        """Add an undirected edge with dynamic attributes."""
        edge_info = EdgeInfo(attributes=edge_data)
        self.adjacency[src][dst] = edge_info
        self.adjacency[dst][src] = edge_info

    def build_from_csv(self, path: str, id_col="id_batiment", infra_col="infra_id"):
        """Build graph dynamically based on CSV content."""
        df = pd.read_excel(path)

        # Ensure IDs are strings
        df[id_col] = df[id_col].astype(str)
        df[infra_col] = df[infra_col].astype(str)

        # Columns to attach to edges (exclude node and infra IDs)
        edge_columns = [c for c in df.columns if c not in [id_col, infra_col]]

        # Group by infra_id and connect related buildings
        for _, group in df.groupby(infra_col):
            batiments = list(group[id_col].unique())

            for i in range(len(batiments) - 1):
                # Take first row’s values for this infra connection
                row = group.iloc[i]
                edge_data = {col: row[col] for col in edge_columns}
                edge_data[infra_col] = row[infra_col]
                self.add_edge(batiments[i], batiments[i + 1], **edge_data)

    # ---------------------------------------
    # DFS (Depth-First Search)
    # ---------------------------------------
    def dfs(self, start: str):
        visited = set()
        result = []

        def _dfs(node):
            visited.add(node)
            result.append(node)
            for neighbor in self.adjacency[node]:
                if neighbor not in visited:
                    _dfs(neighbor)

        if start in self.adjacency:
            _dfs(start)
        return result

    # ---------------------------------------
    # BFS (Breadth-First Search)
    # ---------------------------------------
    def bfs(self, start: str):
        visited = set()
        queue = deque([start])
        result = []

        while queue:
            node = queue.popleft()
            if node not in visited:
                visited.add(node)
                result.append(node)
                for neighbor in self.adjacency[node]:
                    if neighbor not in visited:
                        queue.append(neighbor)

        return result

    # ---------------------------------------
    # Utilities
    # ---------------------------------------
    def get_neighbors(self, node_id: str):
        return list(self.adjacency[node_id].keys())

    def get_edge_info(self, src: str, dst: str):
        return self.adjacency[src].get(dst)