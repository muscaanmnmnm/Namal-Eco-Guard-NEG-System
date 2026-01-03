class WasteRequest:
    def __init__(self, request_id, location, waste_type, urgency_score):
        """
        Args:
            request_id (str): Unique ID (e.g., "REQ-001")
            location (str): Where the waste is (e.g., "Lake Side")
            waste_type (str): Type (e.g., "Medical", "Paper")
            urgency_score (int): 1-100 (Higher = More Urgent)
        """
        self.request_id = request_id
        self.location = location
        self.waste_type = waste_type
        self.urgency_score = urgency_score

    def __repr__(self):
        return f"[{self.urgency_score}] {self.waste_type} at {self.location}"