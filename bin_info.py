class BinInfo:
    def __init__(self, bin_id, location, capacity_liters, allowed_waste_type):
        """
        Args:
            bin_id (str): e.g., "ITSC-01"
            location (str): e.g., "ITSC Department"
            capacity_liters (int): Max volume
            allowed_waste_type (str): The specific category this bin accepts
        """
        self.bin_id = bin_id
        self.location = location
        self.capacity_liters = capacity_liters
        self.allowed_waste_type = allowed_waste_type
        self.current_load = 0 

    def update_load(self, amount):
        self.current_load = min(self.capacity_liters, self.current_load + amount)

    def is_full(self):
        return self.current_load >= self.capacity_liters

    def __repr__(self):
        return f"[{self.bin_id}] {self.location} ({self.current_load}/{self.capacity_liters}L) - {self.allowed_waste_type} Only"