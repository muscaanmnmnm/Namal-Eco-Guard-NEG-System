# Namal Eco-Guard (NEG) System ♻️🚛
### A Digital Waste Logistics Simulation for Namal University Mianwali

**Course:** EE-253: Data Structures and Algorithms  
**Context:** Problem-Based Learning (PBL) Semester Project  
**Technology:** Python, SimPy, Matplotlib (Real-Time Visualization)

---

## 📖 Project Overview
The **Namal Eco-Guard (NEG)** is a specialized backend architecture designed to optimize waste collection in the challenging mountainous terrain of **Namal University** and **Rikhi Village**. 

Unlike standard systems, NEG does not treat all waste equally. It prioritizes hazardous chemical spills at research centers over general paper waste using a **Priority Queue**, navigates steep gradients using a **Weighted Graph**, and maintains instant inventory via a **Hash Table**.

## 🏗️ The "Big Four" Data Structures
This project implements four mandatory data structures **from scratch** (no pre-built libraries like `heapq` or `networkx` were used for the core logic), satisfying the project strict requirements:

| Module | Data Structure | Feature Implemented |
| :--- | :--- | :--- |
| **A. Priority Processor** | **Max-Heap** | **Smart Triage:** Prioritizes "Hazardous Waste" (Priority 100) over "Paper Waste" (Priority 10), ensuring critical spills at the *Power Lab* are handled first. |
| **B. Rapid Registry** | **Hash Table** | **Instant Lookup:** Maps Bin IDs (e.g., `AGRI-01`) to bin capacities and allowed waste types with $O(1)$ average time complexity. |
| **C. Terrain Network** | **Weighted Graph** | **Slope-Aware Navigation:** Uses **Dijkstra’s Algorithm** to calculate the path of "least resistance," accounting for the steep fuel cost of driving up from *Rikhi Village*. |
| **D. Organized Archive** | **Binary Search Tree** | **Compliance Logging:** Records every pickup event sorted by timestamp for chronological daily reporting. |

---

## 🚀 Installation & Usage

### 1. Prerequisites
You need Python installed along with `simpy` for the discrete-event simulation and `matplotlib` for the rendering.

```bash
pip install simpy matplotlib

#### 2. Clone the Repository

git clone [https://github.com/muscaanmnmnm/Namal-Eco-Guard-NEG-System.git](https://github.com/muscaanmnmnm/Namal-Eco-Guard-NEG-System.git)
cd Namal-Eco-Guard-NEG-System

#### 3. Run the Simulation
```bash
python sim_viz.py


🖥️ Simulation Interface
The dashboard is divided into three panels for real-time monitoring:

1. Digital Twin Map (Left):
2. Blue Nodes: Specific departments (e.g., Center for Big Data & AI, Circuits Lab).
3. Gray Lines: Roads. Thicker lines indicate steeper/harder terrain (e.g., the climb from Rikhi).
4. Red Square: The truck moving in real-time.
5. Priority Queue (Top Right): Live view of the Max-Heap. Watch as high-priority tasks bubble to the top.
7. Live Logs (Bottom Right): Scrolling terminal showing Dispatch, Arrival, and Collection events.


📂 Project Structure
1. main.py: CLI Driver code for text-only simulation.
2. sim_viz.py: Main GUI Application (SimPy + Matplotlib).
3. urgency_heap.py: Custom Max-Heap implementation.
4. bin_registry.py: Custom Hash Table with Chaining.
5. terrain_map.py: Custom Graph + Dijkstra's Algorithm.
6. daily_log.py: Custom BST for logging.
7. waste_request.py: Data object for waste events.


⚙️ Complexity Analysis
1, Pathfinding: O(E log V) using Dijkstra, essential for the sparse road network of Mianwali.
2. Bin Lookup: O(1)average case using Hash Table with Chaining for collision resolution.
3. Priority Management: O(log N) for inserting waste requests, ensuring the system scales even during campus emergencies.


🎓 Academic Integrity
This code was written to demonstrate the practical application of Data Structures in a localized Pakistani context (Namal/Mianwali region). All core data structures are custom implementations.



