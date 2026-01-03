import simpy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec
import random

# --- IMPORT BACKEND ---
from urgency_heap import UrgencyHeap
from waste_request import WasteRequest
from bin_registry import BinRegistry, BinInfo
from terrain_map import TerrainMap
from daily_log import DailyLog

# --- CONFIGURATION ---
# Coordinates (Science Library merged into Main Library)
LOCATIONS = {
    "Rikhi Village": (50, 50),
    "Main Gate": (250, 100),
    "Mess & Kitchen Hall": (150, 150),
    "Tuck Shop": (100, 120),
    "Transport Office (Garage)": (350, 250),
    "Academic Block": (400, 400),
    "Printing Block": (330, 370),
    "Main Library": (320, 480), # Moved up slightly for clarity
    "Center for Big Data & AI": (500, 450),
    "Agritech Center": (600, 550),
    "ITSC Department": (550, 300),
    "Circuits Lab": (650, 350),
    "Digital Lab": (650, 300),
    "Machines Lab": (650, 250),
    "Power Lab": (600, 200)
}

# --- SYSTEM STATE ---
env = simpy.Environment()
heap = UrgencyHeap()
registry = BinRegistry(size=20)
map_system = TerrainMap()
daily_log = DailyLog()

# Global Visual State
truck_visual_pos = LOCATIONS["Transport Office (Garage)"]
current_status = "Standby"
log_history = []  # Stores last 5 log messages

def init_backend():
    # Road Network (Science Library removed)
    roads = [
        ("Rikhi Village", "Main Gate", 5.0, 8),
        ("Main Gate", "Transport Office (Garage)", 0.5, 1),
        ("Main Gate", "Mess & Kitchen Hall", 0.8, 2),
        ("Mess & Kitchen Hall", "Tuck Shop", 0.1, 0),
        ("Transport Office (Garage)", "Academic Block", 1.0, 2),
        ("Academic Block", "Center for Big Data & AI", 0.3, 0),
        ("Academic Block", "Main Library", 0.2, 0),
        ("Academic Block", "Printing Block", 0.2, 0),
        ("Academic Block", "ITSC Department", 0.5, 1),
        ("ITSC Department", "Circuits Lab", 0.1, 0),
        ("ITSC Department", "Digital Lab", 0.1, 0),
        ("ITSC Department", "Power Lab", 0.2, 0),
        ("ITSC Department", "Machines Lab", 0.2, 0),
        ("Academic Block", "Agritech Center", 1.5, 4)
    ]
    for u, v, d, s in roads:
        map_system.add_road(u, v, d, s)

    # Initial Requests
    reqs = [
        WasteRequest("R1", "Power Lab", "Hazardous/Chemical"),
        WasteRequest("R2", "ITSC Department", "Tech Waste"),
        WasteRequest("R3", "Mess & Kitchen Hall", "Organic/Food Waste"),
        WasteRequest("R4", "Rikhi Village", "General Waste"),
        WasteRequest("R5", "Main Library", "Paper Waste")
    ]
    for r in reqs:
        heap.insert(r)

init_backend()

# --- SIMPY PROCESSES ---
def add_log(msg):
    """Adds a message to the scrolling log display"""
    global log_history
    log_history.append(f"[{env.now:.0f}] {msg}")
    if len(log_history) > 8: # Keep last 8 lines
        log_history.pop(0)

def waste_generator(env):
    """Generates random events"""
    while True:
        yield env.timeout(random.randint(60, 120))
        loc = random.choice(list(LOCATIONS.keys()))
        
        # Determine urgency based on location context
        w_type = "General"
        if "Lab" in loc: w_type = "Chemical"
        elif "Mess" in loc: w_type = "Organic"
        
        req = WasteRequest(f"AUTO-{int(env.now)}", loc, w_type)
        heap.insert(req)
        add_log(f"ALERT: {w_type} at {loc}")

def truck_process(env):
    global truck_visual_pos, current_status
    current_node = "Transport Office (Garage)"
    
    while True:
        if heap.is_empty():
            current_status = "IDLE - Waiting..."
            yield env.timeout(1)
            continue
            
        # 1. Get Job
        job = heap.extract_max()
        current_status = f"To: {job.location}"
        add_log(f"DISPATCH: {job.location}")
        
        # 2. Plan Route
        cost, path = map_system.get_shortest_path(current_node, job.location)
        if not path: continue
            
        # 3. Drive
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            start_pos, end_pos = LOCATIONS[u], LOCATIONS[v]
            
            # Animation steps
            steps = 15
            for step in range(steps):
                alpha = (step + 1) / steps
                lx = start_pos[0] + (end_pos[0] - start_pos[0]) * alpha
                ly = start_pos[1] + (end_pos[1] - start_pos[1]) * alpha
                truck_visual_pos = (lx, ly)
                yield env.timeout(0.2)
            
            current_node = v
            
        # 4. Collect
        current_status = "COLLECTING..."
        yield env.timeout(10)
        add_log(f"DONE: {job.location}")

# --- MATPLOTLIB VISUALIZATION SETUP ---

# Create a layout with 3 areas: Map, Heap, Logs
fig = plt.figure(figsize=(12, 7))
gs = GridSpec(2, 3, figure=fig)

# 1. Map Plot (Left Side - Takes 2/3 width)
ax_map = fig.add_subplot(gs[:, 0:2])
ax_map.set_title("Namal University Digital Twin", fontsize=14, fontweight='bold')
ax_map.set_xlim(0, 700)
ax_map.set_ylim(0, 600)
ax_map.set_aspect('equal')
ax_map.axis('off') # Hide axis numbers for cleaner look

# 2. Heap Panel (Top Right)
ax_heap = fig.add_subplot(gs[0, 2])
ax_heap.set_title("Priority Queue (Max-Heap)", fontsize=10, fontweight='bold', color='red')
ax_heap.axis('off')
heap_text = ax_heap.text(0, 1, "", va='top', fontsize=9, family='monospace')

# 3. Log Panel (Bottom Right)
ax_log = fig.add_subplot(gs[1, 2])
ax_log.set_title("Live Activity Log", fontsize=10, fontweight='bold', color='blue')
ax_log.axis('off')
log_text = ax_log.text(0, 1, "", va='top', fontsize=9, family='monospace')

# Draw Static Elements (Roads & Nodes)
for u, edges in map_system.adj_list.items():
    if u in LOCATIONS:
        for v, weight in edges:
            if v in LOCATIONS:
                x1, y1 = LOCATIONS[u]
                x2, y2 = LOCATIONS[v]
                lw = 2.5 if weight > 10 else 0.8
                color = '#7f8c8d' if weight > 10 else '#bdc3c7'
                ax_map.plot([x1, x2], [y1, y2], color=color, linewidth=lw, zorder=1)

for name, (x, y) in LOCATIONS.items():
    ax_map.plot(x, y, 'o', color='#3498db', markersize=8, zorder=2)
    # Offset text to avoid overlapping nodes
    ax_map.text(x, y+18, name, fontsize=8, ha='center', fontweight='bold', color='#2c3e50', zorder=3)

# Dynamic Elements
truck_marker, = ax_map.plot([], [], 's', color='#e74c3c', markersize=14, markeredgecolor='black', zorder=4)
status_label = ax_map.text(10, 580, "", fontsize=10, color='#c0392b', fontweight='bold')

# Initialize SimPy
env.process(truck_process(env))
env.process(waste_generator(env))

def update(frame):
    # Step simulation forward
    env.run(until=env.now + 0.5)
    
    # Update Truck Position
    tx, ty = truck_visual_pos
    truck_marker.set_data([tx], [ty])
    status_label.set_text(f"TIME: {env.now:.0f} | STATUS: {current_status}")
    
    # Update Priority Queue Panel
    sorted_heap = sorted(heap.heap, key=lambda x: x.urgency_score, reverse=True)
    heap_str = ""
    if not sorted_heap:
        heap_str = "(No Pending Tasks)"
    else:
        for r in sorted_heap[:6]: # Show top 6
            heap_str += f"[{r.urgency_score}] {r.location}\n   Type: {r.waste_type}\n\n"
    heap_text.set_text(heap_str)
    
    # Update Log Panel
    log_str = "\n".join(log_history)
    log_text.set_text(log_str)
    
    return truck_marker, status_label, heap_text, log_text

ani = animation.FuncAnimation(fig, update, interval=50, blit=False) # Blit=False for text updates
plt.tight_layout()
plt.show()