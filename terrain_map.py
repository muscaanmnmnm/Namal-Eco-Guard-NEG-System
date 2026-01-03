class TerrainMap:
    def __init__(self):
        # Dictionary to store graph: { "LocationA": [("LocationB", weight), ...] }
        self.adj_list = {}

    def add_location(self, location):
        """Adds a new node (vertex) to the graph."""
        if location not in self.adj_list:
            self.adj_list[location] = []

    def add_road(self, u, v, weight):
        """
        Adds a weighted edge between two locations.
        Since roads are two-way, we add edges for both directions.
        """
        if u not in self.adj_list:
            self.add_location(u)
        if v not in self.adj_list:
            self.add_location(v)
        
        self.adj_list[u].append((v, weight))
        self.adj_list[v].append((u, weight))

    def get_shortest_path(self, start_node, end_node):
        """
        Implements Dijkstra's Algorithm to find the path of least resistance.
        Returns: (total_cost, path_list)
        """
        # Distances initialization: Infinite for all, 0 for start
        distances = {node: float('inf') for node in self.adj_list}
        distances[start_node] = 0
        
        # To reconstruct the path: keep track of where we came from
        previous_nodes = {node: None for node in self.adj_list}
        
        # Priority Queue simulation (List of tuples: (current_dist, node))
        # We start with the source node
        pq = [(0, start_node)]
        
        visited = set()

        while pq:
            # 1. Extract node with smallest distance (Manual Min-Heap behavior)
            # Sort to simulate priority queue extraction (O(N log N) for simplicity here)
            pq.sort(key=lambda x: x[0])
            current_dist, current_node = pq.pop(0)

            if current_node in visited:
                continue
            visited.add(current_node)

            # Stop early if we reached the destination
            if current_node == end_node:
                break

            # 2. Explore neighbors
            for neighbor, weight in self.adj_list[current_node]:
                if neighbor not in visited:
                    new_dist = current_dist + weight
                    
                    # Relaxation step: If we found a shorter path, update it
                    if new_dist < distances[neighbor]:
                        distances[neighbor] = new_dist
                        previous_nodes[neighbor] = current_node
                        pq.append((new_dist, neighbor))

        # 3. Reconstruct the path from end to start
        path = []
        current = end_node
        if distances[end_node] == float('inf'):
            return float('inf'), [] # No path exists

        while current is not None:
            path.insert(0, current)
            current = previous_nodes[current]

        return distances[end_node], path

    def display_map(self):
        print("\n--- Terrain Map Connections ---")
        for node, neighbors in self.adj_list.items():
            print(f"{node} connects to: {neighbors}")