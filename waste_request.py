import time

class WasteRequest:
    # --- NAMAL SPECIFIC LOCATIONS ---
    LOC_AGRITECH = "Agritech Center"
    LOC_BIG_DATA = "Center for Big Data & AI"
    LOC_LIBRARY_MAIN = "Main Library"
    LOC_LIBRARY_SCI = "Science Library"
    LOC_ACADEMIC = "Academic Block"
    LOC_PRINTING = "Printing Block"
    LOC_MESS = "Mess & Kitchen Hall"
    LOC_TUCK = "Tuck Shop"
    LOC_ITSC = "ITSC Department"
    LOC_LAB_CIRCUITS = "Circuits Lab"
    LOC_LAB_DIGITAL = "Digital Lab"
    LOC_LAB_POWER = "Power Lab"
    LOC_LAB_MACHINES = "Machines Lab"
    LOC_RIKHI_VILLAGE = "Rikhi Village"

    # --- WASTE TYPES & BASE URGENCY ---
    # Tech waste is critical (hazardous materials). Organic is high (sanitation). Paper is low.
    TYPE_TECH = "Tech Waste (Wires/Burnt Instruments)"
    TYPE_ORGANIC = "Organic/Food Waste"
    TYPE_PAPER = "Paper Waste"
    TYPE_HAZARDOUS = "Hazardous/Chemical"

    def __init__(self, request_id, location, waste_type):
        self.request_id = request_id
        self.location = location
        self.waste_type = waste_type
        self.creation_time = time.time()  # Real-time timestamp
        self.urgency_score = self._calculate_urgency()

    def _calculate_urgency(self):
        """
        Auto-calculates urgency based on the real-world nature of Namal waste.
        """
        score = 0
        
        # 1. Base Score by Waste Type
        if self.waste_type == self.TYPE_HAZARDOUS:
            score = 100
        elif self.waste_type == self.TYPE_TECH:
            score = 90  # E-waste needs careful handling
        elif self.waste_type == self.TYPE_ORGANIC:
            score = 75  # Rotting food attracts animals/pests
        elif self.waste_type == self.TYPE_PAPER:
            score = 30  # Low urgency, non-toxic

        # 2. Location Multipliers (Research Centers are VIP areas)
        if self.location in [self.LOC_BIG_DATA, self.LOC_AGRITECH]:
            score += 10
        
        # 3. Special Case: Labs often have sensitive waste
        if "Lab" in self.location:
            score += 5

        return min(score, 100)  # Cap at 100

    def __repr__(self):
        # Shows a formatted time string for real-time feel
        time_str = time.strftime('%H:%M:%S', time.localtime(self.creation_time))
        return f"[{time_str}] Priority:{self.urgency_score} | {self.waste_type} @ {self.location}"