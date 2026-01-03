import tkinter as tk
import time
import threading

# Import your existing backend modules
from urgency_heap import UrgencyHeap
from waste_request import WasteRequest
from bin_registry import BinRegistry, BinInfo
from terrain_map import TerrainMap
from daily_log import DailyLog

# --- CONFIGURATION (These were missing!) ---
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 700
BG_COLOR = "#f0f0f0"
MAP_COLOR = "#ffffff"
NODE_COLOR = "#3498db"
TRUCK_COLOR = "#e74c3c"

# Coordinates for the "Digital Twin" Map (x, y)
LOCATIONS = {
    "Rikhi Village": (100, 600),
    "Main Gate": (300, 550),
    "Mess & Kitchen Hall": (200, 500),
    "Tuck Shop": (150, 520),
    "Transport Office (Garage)": (400, 400),
    "Academic Block": (450, 250),
    "Main Library": (380, 200),
    "Science Library": (320, 200),
    "Printing Block": (380, 280),
    "Center for Big Data & AI": (550, 200),
    "Agritech Center": (600, 100),
    "ITSC Department": (600, 300),
    "Circuits Lab": (680, 280),
    "Digital Lab": (680, 320),
    "Power Lab": (650, 360),
    "Machines Lab": (650, 240)
}

class NamalEcoGuardGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Namal Eco-Guard | Real-Time Waste Logistics Simulation")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=BG_COLOR)

        # Initialize Backend Systems
        self.init_backend()
        
        # 1. Initialize Simulation State FIRST
        # This fixes the "AttributeError: 'NamalEcoGuardGUI' object has no attribute 'truck_pos'"
        self.truck_pos = LOCATIONS["Transport Office (Garage)"]
        self.is_running = False

        # 2. Setup UI
        self.create_widgets()
        
        # 3. Draw Map (Now safe because truck_pos exists)
        self.draw_map()

    def init_backend(self):
        """Re-uses your existing Step 1-5 logic to setup the system"""
        # 1. Registry
        self.registry = BinRegistry(size=20)
        # (Add a few sample bins for demo)
        self.registry.add_bin(BinInfo("LAB-POWR", "Power Lab", 50, "Hazardous"))
        self.registry.add_bin(BinInfo("ITSC-MAIN", "ITSC Department", 100, "Tech"))
        self.registry.add_bin(BinInfo("MESS-HALL", "Mess & Kitchen Hall", 300, "Organic"))
        
        # 2. Graph
        self.map_system = TerrainMap()
        # Define connections matching LOCATIONS keys exactly
        roads = [
            ("Rikhi Village", "Main Gate", 5.0, 8),
            ("Main Gate", "Transport Office (Garage)", 0.5, 1),
            ("Main Gate", "Mess & Kitchen Hall", 0.8, 2),
            ("Mess & Kitchen Hall", "Tuck Shop", 0.1, 0),
            ("Transport Office (Garage)", "Academic Block", 1.0, 2),
            ("Academic Block", "Center for Big Data & AI", 0.3, 0),
            ("Academic Block", "Main Library", 0.2, 0),
            ("Main Library", "Science Library", 0.4, 0),
            ("Academic Block", "Printing Block", 0.2, 0),
            ("Academic Block", "ITSC Department", 0.5, 1),
            ("ITSC Department", "Circuits Lab", 0.1, 0),
            ("ITSC Department", "Digital Lab", 0.1, 0),
            ("ITSC Department", "Power Lab", 0.2, 0),
            ("ITSC Department", "Machines Lab", 0.2, 0),
            ("Academic Block", "Agritech Center", 1.5, 4)
        ]
        for u, v, d, s in roads:
            self.map_system.add_road(u, v, d, s)

        # 3. Heap & Logs
        self.heap = UrgencyHeap()
        self.logs = DailyLog()

        # Load Initial Requests
        reqs = [
            WasteRequest("R1", "Power Lab", "Hazardous/Chemical"),
            WasteRequest("R2", "ITSC Department", "Tech Waste (Wires/Burnt Instruments)"),
            WasteRequest("R3", "Mess & Kitchen Hall", "Organic/Food Waste"),
            WasteRequest("R4", "Rikhi Village", "General Waste"),
            WasteRequest("R5", "Main Library", "Paper Waste")
        ]
        for r in reqs:
            self.heap.insert(r)

    def create_widgets(self):
        # --- LEFT PANEL: CONTROLS & LOGS ---
        left_panel = tk.Frame(self.root, width=300, bg="#2c3e50")
        left_panel.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(left_panel, text="Control Center", font=("Arial", 16, "bold"), fg="white", bg="#2c3e50").pack(pady=10)
        
        self.btn_run = tk.Button(left_panel, text="Dispatch Truck (Next Job)", command=self.run_mission_step, bg="#27ae60", fg="white", font=("Arial", 12))
        self.btn_run.pack(pady=10, fill=tk.X, padx=20)

        tk.Label(left_panel, text="System Logs", font=("Arial", 12), fg="white", bg="#2c3e50").pack(pady=(20, 5))
        self.log_text = tk.Text(left_panel, height=20, width=35, font=("Consolas", 9))
        self.log_text.pack(padx=10)

        # --- CENTER: MAP CANVAS ---
        self.canvas = tk.Canvas(self.root, bg=MAP_COLOR)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # --- RIGHT PANEL: HEAP STATUS ---
        right_panel = tk.Frame(self.root, width=250, bg="#ecf0f1")
        right_panel.pack(side=tk.RIGHT, fill=tk.Y)
        
        tk.Label(right_panel, text="Priority Queue (Heap)", font=("Arial", 14), bg="#ecf0f1").pack(pady=10)
        self.heap_list = tk.Listbox(right_panel, font=("Arial", 10), height=30)
        self.heap_list.pack(fill=tk.BOTH, padx=10, pady=10)
        
        self.refresh_heap_view()

    def draw_map(self):
        self.canvas.delete("all")
        
        # Draw Edges (Roads)
        for node, edges in self.map_system.adj_list.items():
            if node in LOCATIONS:
                x1, y1 = LOCATIONS[node]
                for neighbor, weight in edges:
                    if neighbor in LOCATIONS:
                        x2, y2 = LOCATIONS[neighbor]
                        # Draw line with thickness based on "Effort Cost" (Thicker = Steeper)
                        width = 1
                        if weight > 10: width = 3 # Steep road indicator
                        self.canvas.create_line(x1, y1, x2, y2, fill="#95a5a6", width=width)

        # Draw Nodes (Locations)
        for name, (x, y) in LOCATIONS.items():
            self.canvas.create_oval(x-8, y-8, x+8, y+8, fill=NODE_COLOR, outline="white")
            self.canvas.create_text(x, y-15, text=name, font=("Arial", 8, "bold"), fill="#2c3e50")

        # Draw Truck
        tx, ty = self.truck_pos
        self.truck_id = self.canvas.create_rectangle(tx-10, ty-10, tx+10, ty+10, fill=TRUCK_COLOR)
        self.canvas.create_text(tx, ty-20, text="TRUCK", fill="red", font=("Arial", 8, "bold"), tags="truck_lbl")

    def refresh_heap_view(self):
        """Shows current state of the Heap in the sidebar"""
        self.heap_list.delete(0, tk.END)
        # Note: Accessing internal list for visualization only
        sorted_view = sorted(self.heap.heap, key=lambda x: x.urgency_score, reverse=True)
        for req in sorted_view:
            self.heap_list.insert(tk.END, f"[{req.urgency_score}] {req.location}")

    def log(self, message):
        self.log_text.insert(tk.END, f"> {message}\n")
        self.log_text.see(tk.END)

    def animate_truck(self, path):
        if not path: return
        
        # Go through each node in the path
        for i in range(len(path) - 1):
            start_node = path[i]
            end_node = path[i+1]
            
            start_coords = LOCATIONS[start_node]
            end_coords = LOCATIONS[end_node]
            
            # Interpolate movement (20 steps per road)
            steps = 20
            dx = (end_coords[0] - start_coords[0]) / steps
            dy = (end_coords[1] - start_coords[1]) / steps
            
            for _ in range(steps):
                self.canvas.move(self.truck_id, dx, dy)
                self.canvas.move("truck_lbl", dx, dy)
                self.root.update()
                time.sleep(0.02) # Speed of animation
            
            self.truck_pos = end_coords

    def run_mission_step(self):
        if self.heap.is_empty():
            self.log("All tasks complete. Heap empty.")
            return

        # 1. Extract Max Priority
        job = self.heap.extract_max()
        self.refresh_heap_view()
        self.log(f"DISPATCH: {job.waste_type}")
        self.log(f"Target: {job.location} (Priority {job.urgency_score})")

        # 2. Get Path from current location
        # Find current node name based on coordinates
        current_node_name = "Transport Office (Garage)" # Default start
        for name, coords in LOCATIONS.items():
            if coords == self.truck_pos:
                current_node_name = name
                break
        
        cost, path = self.map_system.get_shortest_path(current_node_name, job.location)
        
        if cost == float('inf'):
            self.log("ERROR: Path blocked!")
            return

        self.log(f"Path Found: {len(path)} stops.")
        
        # 3. Animate
        self.animate_truck(path)
        
        self.log(f"ARRIVED: {job.location}")
        self.log(f"Collected. returning to standby.\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = NamalEcoGuardGUI(root)
    root.mainloop()