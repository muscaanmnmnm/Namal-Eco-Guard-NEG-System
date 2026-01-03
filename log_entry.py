class LogEntry:
    def __init__(self, timestamp, location, waste_type, amount_kg):
        """
        Args:
            timestamp (str): Formatted time "HH:MM". This is the sorting KEY.
            location (str): e.g., "Circuits Lab"
            waste_type (str): e.g., "Tech Waste"
            amount_kg (float): Weight collected
        """
        self.timestamp = timestamp
        self.location = location
        self.waste_type = waste_type
        self.amount_kg = amount_kg

    def __repr__(self):
        return f"[{self.timestamp}] {self.location} | {self.waste_type} | {self.amount_kg}kg"