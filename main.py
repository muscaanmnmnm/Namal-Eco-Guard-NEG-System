import time

# Import our Custom "Big Four" Modules
from urgency_heap import UrgencyHeap           # Module A
from waste_request import WasteRequest
from bin_registry import BinRegistry, BinInfo  # Module B
from terrain_map import TerrainMap             # Module C
from daily_log import DailyLog                 # Module D

def run_namal_eco_guard():
    print("=====================================================")
    print("      NAMAL ECO-GUARD (NEG) SYSTEM STARTUP           ")
    print("=====================================================")

    # ---------------------------------------------------------
    # 1. SETUP PHASE: Initialize the World
    # ---------------------------------------------------------
    
    # --- Setup Module B: The Rapid Registry ---
    print("\n[System] Initializing Bin Registry (Hash Table)...")
    registry = BinRegistry(size=10)
    
    # Registering bins at Namal and Rikhi
    # ID, Location, Capacity
    registry.add_bin(BinInfo("NML-01", "Academic Block", 100))
    registry.add_bin(BinInfo("NML-02", "Student Center", 200))
    registry.add_bin(BinInfo("LAKE-01", "Dry Lake Bed", 50))
    registry.add_bin(BinInfo("RIK-01", "Rikhi Main Sq", 150))
    registry.add_bin(BinInfo("RIK-02", "Rikhi Clinic", 80))
    
    registry.display_registry()

    # --- Setup Module C: The Terrain Map ---
    print("\n[System] Mapping Terrain (Weighted Graph)...")
    namal_map = TerrainMap()
    
    # Add locations and road weights (Effort = Distance + Slope Difficulty)
    # The truck starts at "Main Garage"
    namal_map.add_road("Main Garage", "Academic Block", 5)
    namal_map.add_road("Academic Block", "Student Center", 2)
    namal_map.add_road("Student Center", "Library", 3)
    
    # Mountain roads (High weight due to slope)
    namal_map.add_road("Main Garage", "Rikhi Main Sq", 20) 
    namal_map.add_road("Rikhi Main Sq", "Rikhi Clinic", 4)
    namal_map.add_road("Rikhi Main Sq", "LAKE-01", 15)  # Hard path to lake
    namal_map.add_road("Academic Block", "LAKE-01", 25) # Steep shortcut
    
    namal_map.display_map()

    # --- Setup Module D: Daily Log Archive ---
    daily_log = DailyLog()

    # --- Setup Module A: Priority Processor ---
    priority_queue = UrgencyHeap()

    # ---------------------------------------------------------
    # 2. EVENT GENERATION: Incoming Waste Requests
    # ---------------------------------------------------------
    print("\n[Events] Incoming Waste Collection Requests...")

    # Format: ID, Location, Type, Urgency (1-100)
    requests = [
        WasteRequest("REQ-1", "Academic Block", "Paper/Plastic", 10),
        WasteRequest("REQ-2", "Rikhi Clinic", "Medical/Hazardous", 95), # HIGH PRIORITY
        WasteRequest("REQ-3", "LAKE-01", "Chemical Spill", 100),        # CRITICAL
        WasteRequest("REQ-4", "Student Center", "Food Waste", 50),
        WasteRequest("REQ-5", "Rikhi Main Sq", "General Waste", 20)
    ]

    for req in requests:
        print(f" -> Received: {req}")
        priority_queue.insert(req)

    # ---------------------------------------------------------
    # 3. PROCESSING PHASE: The Truck Route
    # ---------------------------------------------------------
    print("\n[Operations] Dispatching Truck based on Urgency...")
    
    current_location = "Main Garage"

    while not priority_queue.is_empty():
        # 1. Get the most urgent job (Max-Heap Extract)
        job = priority_queue.extract_max()
        print(f"\n>>> PROCESSING URGENT JOB: {job.waste_type} at {job.location} (Score: {job.urgency_score})")

        # 2. Check Bin Status (Hash Table Lookup O(1))
        # (For this sim, we map Location names to Bin IDs roughly)
        bin_id = None
        if job.location == "Academic Block": bin_id = "NML-01"
        elif job.location == "Rikhi Clinic": bin_id = "RIK-02"
        elif job.location == "LAKE-01": bin_id = "LAKE-01"
        elif job.location == "Student Center": bin_id = "NML-02"
        elif job.location == "Rikhi Main Sq": bin_id = "RIK-01"

        if bin_id:
            bin_data = registry.get_bin(bin_id)
            print(f"    [Registry Check] Bin {bin_id} Found. Capacity: {bin_data.capacity_liters}L")
        
        # 3. Find Best Route (Dijkstra)
        print(f"    [Navigation] Calculating path from {current_location} to {job.location}...")
        cost, path = namal_map.get_shortest_path(current_location, job.location)
        
        if cost == float('inf'):
            print("    [Error] No path found!")
        else:
            print(f"    [Route] Path: {' -> '.join(path)} (Total Effort Cost: {cost})")
            
            # Simulate travel and collection
            current_location = job.location # Truck moves there
            
            # 4. Archive the Event (BST Insertion)
            # We simulate a timestamp (e.g., 0900 + cost)
            # For simplicity, we just use a counter or random time for the demo
            import random
            sim_time = random.randint(800, 1800) # Random time between 08:00 and 18:00
            collected_amount = random.randint(10, 50)
            
            daily_log.add_entry(sim_time, job.location, collected_amount)
            print("    [Log] Job Complete & Archived.")

    # ---------------------------------------------------------
    # 4. REPORTING PHASE: End of Day
    # ---------------------------------------------------------
    daily_log.generate_report()
    print("\n[System] Simulation Complete.")

if __name__ == "__main__":
    run_namal_eco_guard()