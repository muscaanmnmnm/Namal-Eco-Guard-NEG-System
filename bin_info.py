class BinInfo:
    def __init__(self, bin_id, location, capacity_liters):
        """
        Args:
            bin_id (str): Unique ID (e.g., "RIK-01", "NML-LIB")
            location (str): Physical location description
            capacity_liters (int): Total volume of the bin
        """
        self.bin_id = bin_id
        self.location = location
        self.capacity_liters = capacity_liters
        self.current_load = 0  # Starts empty

    def update_load(self, amount):
        """Updates current trash level, capping at capacity."""
        self.current_load = min(self.capacity_liters, self.current_load + amount)

    def is_full(self):
        return self.current_load >= self.capacity_liters

    def __repr__(self):
        return f"[Bin {self.bin_id}] {self.current_load}/{self.capacity_liters}L @ {self.location}"