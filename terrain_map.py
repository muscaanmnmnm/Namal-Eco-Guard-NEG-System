import heapq  # Used for priority queue in Dijkstra's algorithm

class TerrainMap:
    def __init__(self):
        # Stores graph: { "NodeA": [("NodeB", weight), ...] }
        self.adj_list = {}

    def add_location(self, location):
        """Adds a specific Namal Department/Spot as a node."""
        if location not in self.adj_list:
            self.adj_list[location] = []

    def add_road(self, u, v, distance_km, slope_difficulty):
        """
        Calculates 'Effort Weight' combining distance and terrain slope.
        Weight = Distance + (Slope Factor * 2)
        """
        weight = distance_km + (slope_difficulty * 2)
        
        if u not in self.adj_list: self.add_location(u)
        if v not in self.adj_list: self.add_location(v)
        
        # Add undirected edge (Road goes both ways)
        self.adj_list[u].append((v, weight))
        self.adj_list[v].append((u, weight))

    def get_shortest_path(self, start_node, end_node):
        """
        Custom Dijkstra Implementation (No external libraries).
        Finds the path of least resistance from Truck Garage to Waste Bin.
        """
        # 1. Initialize Distances
        distances = {node: float('inf') for node in self.adj_list}
        previous_nodes = {node: None for node in self.adj_list}
        distances[start_node] = 0
        
        # 2. Priority Queue Simulator (List of tuples: (current_dist, node))
        pq = [(0, start_node)]
        visited = set()

        while pq:
            # MANUAL EXTRACT-MIN: Sort to find smallest distance (Replacing heapq)
            pq.sort(key=lambda x: x[0])
            current_dist, current_node = pq.pop(0)

            if current_node in visited:
                continue
            visited.add(current_node)

            if current_node == end_node:
                break

            # Explore neighbors (Roads connecting Departments)
            for neighbor, weight in self.adj_list.get(current_node, []):
                if neighbor not in visited:
                    new_dist = current_dist + weight
                    
                    if new_dist < distances[neighbor]:
                        distances[neighbor] = new_dist
                        previous_nodes[neighbor] = current_node
                        pq.append((new_dist, neighbor))

        # 3. Reconstruct Path
        path = []
        current = end_node
        if distances[end_node] == float('inf'):
            return float('inf'), [] # Path blocked or impossible

        while current is not None:
            path.insert(0, current)
            current = previous_nodes[current]

        return distances[end_node], path

    def display_map(self):
        print("\n--- Namal Terrain Connectivity ---")
        for node, edges in self.adj_list.items():
            print(f"{node} connects to:")
            for neighbor, weight in edges:
                print(f"  -> {neighbor} (Effort Cost: {weight})")