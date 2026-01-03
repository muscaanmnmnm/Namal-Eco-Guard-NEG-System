import time
import random

# Import Custom Data Structures
from urgency_heap import UrgencyHeap           # Module A
from waste_request import WasteRequest
from bin_registry import BinRegistry, BinInfo  # Module B
from terrain_map import TerrainMap             # Module C
from daily_log import DailyLog                 # Module D

def run_namal_eco_guard():
    print("=========================================================")
    print("   NAMAL ECO-GUARD (NEG) - WASTE MANAGEMENT SYSTEM       ")
    print("   Target Area: Namal University & Rikhi Village         ")
    print("=========================================================")

    # ---------------------------------------------------------
    # 1. INITIALIZATION: Building the Digital Twin
    # ---------------------------------------------------------
    
    # --- A. Setup The Rapid Registry (Hash Table) ---
    print("\n[Init] Loading Bin Registry for Campus & Rikhi...")
    registry = BinRegistry(size=20)
    
    # Research Centers
    registry.add_bin(BinInfo("AGRI-01", "Agritech Center", 100, "Organic/Chemical"))
    registry.add_bin(BinInfo("AI-01", "Center for Big Data & AI", 50, "Paper/General"))
    
    # Libraries & Academic
    registry.add_bin(BinInfo("LIB-MAIN", "Main Library", 80, "Paper Waste"))
    registry.add_bin(BinInfo("LIB-SCI", "Science Library", 60, "Paper Waste"))
    registry.add_bin(BinInfo("ACAD-MAIN", "Academic Block", 200, "General Waste"))
    registry.add_bin(BinInfo("PRINT-01", "Printing Block", 150, "Paper/Chemical"))
    
    # Labs (Circuits, Digital, Power, Machines) & ITSC
    registry.add_bin(BinInfo("ITSC-MAIN", "ITSC Department", 100, "Tech Waste (Wires)"))
    registry.add_bin(BinInfo("LAB-CIRC", "Circuits Lab", 40, "Tech Waste"))
    registry.add_bin(BinInfo("LAB-DIGI", "Digital Lab", 40, "Tech Waste"))
    registry.add_bin(BinInfo("LAB-POWR", "Power Lab", 50, "Hazardous/Tech"))
    registry.add_bin(BinInfo("LAB-MACH", "Machines Lab", 60, "Metal/Oil"))
    
    # Services (Mess, Tuck Shop)
    registry.add_bin(BinInfo("MESS-HALL", "Mess & Kitchen Hall", 300, "Organic/Food"))
    registry.add_bin(BinInfo("TUCK-SHOP", "Tuck Shop", 100, "Plastic/Wrapper"))
    
    # External Area
    registry.add_bin(BinInfo("RIKHI-CEN", "Rikhi Village", 500, "General/Agricultural"))
    
    registry.display_registry()

    # --- B. Setup The Terrain Map (Weighted Graph) ---
    print("\n[Init] Mapping Mountainous Terrain (Graph)...")
    namal_map = TerrainMap()
    
    # Truck starts here
    truck_garage = "Transport Office (Garage)"
    
    # Defining Roads: (Start, End, Distance_KM, Slope_Difficulty_0-10)
    
    # 1. The Climb from Rikhi to Namal (Steep!)
    namal_map.add_road("Rikhi Village", "Main Gate", 5.0, 8) 
    namal_map.add_road("Main Gate", truck_garage, 0.5, 1)
    
    # 2. Campus Core (Relatively Flat)
    namal_map.add_road(truck_garage, "Academic Block", 1.0, 2)
    namal_map.add_road("Academic Block", "Center for Big Data & AI", 0.3, 0)
    namal_map.add_road("Academic Block", "Main Library", 0.2, 0)
    namal_map.add_road("Main Library", "Science Library", 0.4, 0)
    namal_map.add_road("Academic Block", "Printing Block", 0.2, 0)
    
    # 3. Lab Cluster (Short distance, flat)
    namal_map.add_road("Academic Block", "ITSC Department", 0.5, 1)
    namal_map.add_road("ITSC Department", "Circuits Lab", 0.1, 0)
    namal_map.add_road("ITSC Department", "Digital Lab", 0.1, 0)
    namal_map.add_road("ITSC Department", "Power Lab", 0.2, 0) # Near high voltage area
    namal_map.add_road("ITSC Department", "Machines Lab", 0.2, 0)
    
    # 4. Remote/Steep Areas
    namal_map.add_road("Academic Block", "Agritech Center", 1.5, 4) # Slightly uphill
    namal_map.add_road("Main Gate", "Mess & Kitchen Hall", 0.8, 2)
    namal_map.add_road("Mess & Kitchen Hall", "Tuck Shop", 0.1, 0)
    
    namal_map.display_map()

    # --- C. Setup Modules A (Heap) & D (BST) ---
    priority_queue = UrgencyHeap()
    daily_log = DailyLog()

    # ---------------------------------------------------------
    # 2. REAL-TIME EVENT SIMULATION
    # ---------------------------------------------------------
    print("\n[Simulation] 08:00 AM - Shift Starts. Receiving Alerts...")

    # Generating Waste Requests based on your scenario
    # Request(ID, Location, Type) -> Urgency is auto-calculated inside class
    incoming_requests = [
        WasteRequest("REQ-01", "Main Library", "Paper Waste"),           # Low Urgency
        WasteRequest("REQ-02", "Mess & Kitchen Hall", "Organic/Food Waste"), # High Urgency (Smell)
        WasteRequest("REQ-03", "ITSC Department", "Tech Waste (Wires/Burnt Instruments)"), # Critical
        WasteRequest("REQ-04", "Rikhi Village", "General Waste"),        # Medium
        WasteRequest("REQ-05", "Power Lab", "Hazardous/Chemical"),       # MAX Urgency!
        WasteRequest("REQ-06", "Agritech Center", "Organic/Chemical")    # High
    ]

    for req in incoming_requests:
        print(f" -> Alert Received: {req}")
        priority_queue.insert(req)

    # ---------------------------------------------------------
    # 3. TRUCK DISPATCH LOOP
    # ---------------------------------------------------------
    print("\n[Operations] Dispatching Truck (Optimizing for Urgency & Terrain)...")
    
    current_truck_location = truck_garage
    mission_time_minutes = 480 # Start at 8:00 AM (480 mins from midnight)

    while not priority_queue.is_empty():
        # 1. Identify Critical Job (Heap)
        job = priority_queue.extract_max()
        print(f"\n>>> MISSION START: {job.waste_type} at {job.location} (Priority: {job.urgency_score})")

        # 2. Validate Bin (Hash Table)
        # Mapping Location Name to Bin ID for lookup
        target_bin_id = None
        # Simple lookup mapper for simulation
        if "ITSC" in job.location: target_bin_id = "ITSC-MAIN"
        elif "Power" in job.location: target_bin_id = "LAB-POWR"
        elif "Mess" in job.location: target_bin_id = "MESS-HALL"
        elif "Rikhi" in job.location: target_bin_id = "RIKHI-CEN"
        elif "Agritech" in job.location: target_bin_id = "AGRI-01"
        elif "Library" in job.location: target_bin_id = "LIB-MAIN"
        
        if target_bin_id:
            bin_data = registry.get_bin(target_bin_id)
            if bin_data:
                print(f"    [Registry] Confirmed Bin {bin_data.bin_id} accepts {bin_data.allowed_waste_type}")

        # 3. Navigate Terrain (Dijkstra)
        print(f"    [Nav] Calculating route from '{current_truck_location}'...")
        effort_cost, path = namal_map.get_shortest_path(current_truck_location, job.location)
        
        if effort_cost == float('inf'):
            print(f"    [Error] Destination {job.location} is unreachable!")
            continue

        print(f"    [Path] {' -> '.join(path)}")
        print(f"    [Effort] Total Terrain Resistance: {effort_cost:.2f}")

        # 4. Execute Pickup & Log (BST)
        current_truck_location = job.location # Move truck
        
        # Simulate Time Passing based on effort
        travel_time = int(effort_cost * 2) # Rough est: 1 unit effort = 2 mins
        mission_time_minutes += travel_time
        
        # Format time for log (HH:MM)
        hours = mission_time_minutes // 60
        mins = mission_time_minutes % 60
        time_str = f"{hours:02d}:{mins:02d}"
        
        collected_kg = random.randint(20, 100)
        daily_log.add_entry(time_str, job.location, job.waste_type, collected_kg)
        print(f"    [Complete] Picked up {collected_kg}kg at {time_str}.")

    # ---------------------------------------------------------
    # 4. END OF DAY REPORT
    # ---------------------------------------------------------
    print("\n[System] All requests processed. Truck returning to Garage.")
    daily_log.generate_report()

if __name__ == "__main__":
    run_namal_eco_guard()