class LogEntry:
    def __init__(self, timestamp, location, amount_kg):
        """
        Args:
            timestamp (int): Time in 24hr format (e.g., 1430 for 2:30 PM). 
                             This is the KEY for the BST.
            location (str): Where the pickup happened.
            amount_kg (float): Weight of waste collected.
        """
        self.timestamp = timestamp
        self.location = location
        self.amount_kg = amount_kg

    def __repr__(self):
        return f"[{self.timestamp}] Collected {self.amount_kg}kg from {self.location}"