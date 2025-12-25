
import random  
import time    
import tkinter as tk  
from tkinter import ttk  
import threading  


def cost(state):
    n, s, e, w, phase, tp = state
    return n + s + e + w

def heuristic(state):
    n, s, e, w, phase, tp = state   
    return max(n, s, e, w)

def transition_for_planning(state, action, min_green_time=3):
    n, s, e, w, phase, tp = state
    
    n = n + 1
    s = s + 1
    e = e + 1
    w = w + 1
    
    if action == "HOLD":
        new_phase = phase
        new_tp = tp + 1
    else:  
        if tp >= min_green_time:
            new_phase = "EW" if phase == "NS" else "NS"
            new_tp = 0
        else:
            new_phase = phase
            new_tp = tp + 1
    
    if new_phase == "NS":
        n = max(0, n - 2)  
        s = max(0, s - 2)
    else:  
        e = max(0, e - 2)
        w = max(0, w - 2)
    
    return (n, s, e, w, new_phase, new_tp)

def transition_for_simulation(state, action, min_green_time=3):
    n, s, e, w, phase, tp = state
    
    n = n + random.randint(0, 2)
    s = s + random.randint(0, 2)
    e = e + random.randint(0, 2)
    w = w + random.randint(0, 2)
    
    if action == "HOLD":
        new_phase = phase
        new_tp = tp + 1
    else: 
        if tp >= min_green_time:
            new_phase = "EW" if phase == "NS" else "NS"
            new_tp = 0
        else:
            new_phase = phase
            new_tp = tp + 1
    
    if new_phase == "NS":
        n = max(0, n - random.randint(1, 3))
        s = max(0, s - random.randint(1, 3))
    else:  
        e = max(0, e - random.randint(1, 3))
        w = max(0, w - random.randint(1, 3))
    
    return (n, s, e, w, new_phase, new_tp)


def bfs(start_state, horizon):
    visited = []
    queue = [[(start_state, None)]]  
    best_action = "HOLD"
    best_cost = float('inf')
    
    while queue:
        path = queue.pop(0)
        state, _ = path[-1]
        
        if state in visited:
            continue
        visited.append(state)
        
        if len(path) - 1 == horizon:
            state_cost = cost(state)
            if state_cost < best_cost:
                best_cost = state_cost
                best_action = path[1][1] if len(path) > 1 else "HOLD"
            continue  
        
        for action in ["HOLD", "SWITCH"]:
            next_state = transition_for_planning(state, action)
            new_path = path.copy()
            new_path.append((next_state, action))
            queue.append(new_path)
    
    return best_action


def dfs(start_state, horizon):
    visited = []
    stack = [[(start_state, None)]]
    
    best_action = "HOLD"
    best_cost = float('inf')
    
    while stack:
        path = stack.pop()
        state, _ = path[-1]
        
        if state in visited:
            continue
        visited.append(state)
        
        if len(path) - 1 == horizon:
            state_cost = cost(state)
            if state_cost < best_cost:
                best_cost = state_cost
                best_action = path[1][1] if len(path) > 1 else "HOLD"
            continue  
        
        for action in ["HOLD", "SWITCH"]:
            next_state = transition_for_planning(state, action)
            new_path = path.copy()
            new_path.append((next_state, action))
            stack.append(new_path)
    
    return best_action


def path_cost_ucs(path):
    total_cost = 0
    for (state, action) in path:
        total_cost += cost(state)
    return total_cost

def ucs(start_state, horizon):
    visited = []
    queue = [[(start_state, None)]]
    
    while queue:
        queue.sort(key=path_cost_ucs)
        path = queue.pop(0)
        state, _ = path[-1]
        
        if state in visited:
            continue
        visited.append(state)
        
        if len(path) - 1 == horizon:
            return path[1][1] if len(path) > 1 else "HOLD"
        
        for action in ["HOLD", "SWITCH"]:
            next_state = transition_for_planning(state, action)
            new_path = path.copy()
            new_path.append((next_state, action))
            queue.append(new_path)
    
    return "HOLD"


def a_star(start_state, horizon):
 
    open_list = [(start_state, [(start_state, None)], 0)]
    closed = []
    
    while open_list:
        min_f = float('inf')  
        best_index = 0  
        for i in range(len(open_list)):
            state, path, g = open_list[i]
            f = g + heuristic(state)
            if f < min_f:
                min_f = f
                best_index = i
        
        state, path, g = open_list.pop(best_index)
        closed.append(state)
        
        if len(path) - 1 == horizon:
            return path[1][1] if len(path) > 1 else "HOLD"
        
        for action in ["HOLD", "SWITCH"]:
            next_state = transition_for_planning(state, action)
            if next_state not in closed:
                new_g = g + cost(next_state)
                new_path = path + [(next_state, action)]
                open_list.append((next_state, new_path, new_g))
    
    return "HOLD"


def dfs_limited(start_state, depth_limit):
    visited = []
    stack = [[(start_state, None)]]
    
    best_action = "HOLD"
    best_cost = float('inf')
    
    while stack:
        path = stack.pop()
        state, _ = path[-1]
        
        if state in visited:
            continue
        visited.append(state)
        
        if len(path) - 1 == depth_limit:
            state_cost = cost(state)
            if state_cost < best_cost:
                best_cost = state_cost
                best_action = path[1][1] if len(path) > 1 else "HOLD"
            continue  
        
        for action in ["HOLD", "SWITCH"]:
            next_state = transition_for_planning(state, action)
            new_path = path.copy()
            new_path.append((next_state, action))
            stack.append(new_path)
    
    return best_action

def iddfs(start_state, horizon):
    best_action = "HOLD"
    for depth in range(1, horizon + 1):
        best_action = dfs_limited(start_state, depth)
    return best_action


def run_simulation(algorithm_func, algorithm_name, total_time=300, horizon=10, verbose=False):
    north = 0
    south = 0
    east = 0
    west = 0
    phase = "NS"
    time_in_phase = 0
    
    total_waiting = 0  
    switches = 0  
    step_times = []  
    
    if verbose:
        print(f"\n{'='*70}")
        print(f"Algorithm: {algorithm_name}")
        print(f"{'='*70}")
        print(f"{'Time':<8} {'N':<6} {'S':<6} {'E':<6} {'W':<6} {'Phase':<8} {'Action':<8} {'Total':<8}")
        print("-" * 70)
    
    for t in range(total_time):
        state = (north, south, east, west, phase, time_in_phase)
        
        start_time = time.time()
        action = algorithm_func(state, horizon)
        step_times.append(time.time() - start_time)
        
        north, south, east, west, phase, time_in_phase = transition_for_simulation(state, action)
        
        if action == "SWITCH":
            switches += 1
        
        cars_waiting = north + south + east + west
        total_waiting += cars_waiting
        
        if verbose and t % 10 == 0:
            print(f"{t:<8} {north:<6} {south:<6} {east:<6} {west:<6} {phase:<8} {action:<8} {cars_waiting:<8}")
    
    avg_waiting = total_waiting / total_time  
    avg_step_time = sum(step_times) / len(step_times)  
    
    return {
        'algorithm': algorithm_name,
        'total_waiting': total_waiting,
        'avg_waiting': avg_waiting,
        'switches': switches,
        'avg_step_time': avg_step_time
    }


def compare_algorithms(total_time=300, horizon=10):
    algorithms = [
        (a_star, "A*"),
        (bfs, "BFS"),
        (dfs, "DFS"),
        (ucs, "UCS"),
        (iddfs, "IDDFS")
    ]
    
    print("\n" + "="*80)
    print("AI-BASED INTELLIGENT TRAFFIC LIGHT CONTROL SYSTEM")
    print("ALGORITHM COMPARISON")
    print("="*80)
    print(f"\nSimulation Parameters:")
    print(f"  Total Time: {total_time} steps")
    print(f"  Planning Horizon: {horizon} steps")
    
    results = []
    
    for algo_func, algo_name in algorithms:
        print(f"\n{'='*80}")
        print(f"Running {algo_name}...")
        print(f"{'='*80}")
        
        result = run_simulation(algo_func, algo_name, total_time, horizon, verbose=True)
        results.append(result)
    
    print("\n" + "="*80)
    print("PERFORMANCE COMPARISON")
    print("="*80)
    print(f"{'Algorithm':<12} {'Total Wait':<15} {'Avg Wait':<15} {'Switches':<12} {'Avg Time(ms)':<15}")
    print("-"*80)
    
    for r in results:
        print(f"{r['algorithm']:<12} {r['total_waiting']:<15} {r['avg_waiting']:<15.2f} {r['switches']:<12} {r['avg_step_time']*1000:<15.3f}")
    
    best_waiting = min(results, key=lambda x: x['avg_waiting'])  
    best_speed = min(results, key=lambda x: x['avg_step_time'])  
    
    print("\n" + "="*80)
    print("BEST PERFORMERS")
    print("="*80)
    print(f"Best Average Waiting Time: {best_waiting['algorithm']} ({best_waiting['avg_waiting']:.2f} cars)")
    print(f"Fastest Execution: {best_speed['algorithm']} ({best_speed['avg_step_time']*1000:.3f} ms per step)")
    print("\n")
    
    return best_waiting['algorithm']


# ==================== GUI IMPLEMENTATION ====================

class TrafficLightGUI:
    def __init__(self, root, algorithm_func, algorithm_name):
        self.root = root
        self.root.title(f"AI Traffic Light Control System - {algorithm_name}")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        
        self.algorithm_func = algorithm_func
        self.algorithm_name = algorithm_name
        
        self.running = False  
        self.paused = False   
        self.north = 0        
        self.south = 0        
        self.east = 0         
        self.west = 0         
        self.phase = "NS"     
        self.time_in_phase = 0  
        self.current_step = 0   
        self.total_steps = 300  
        self.horizon = 10       
        self.total_waiting = 0  
        self.switches = 0       
        self.delay = 500        
        self.setup_gui()
        
        self.root.after(500, self.start_simulation)
        
    def setup_gui(self):
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        title_frame.pack(fill=tk.X)  
        title_label = tk.Label(title_frame, text=f"AI Traffic Light Control - {self.algorithm_name}", 
                              font=("Arial", 20, "bold"), bg="#2c3e50", fg="white")
        title_label.pack(pady=15)  
        
        self.canvas = tk.Canvas(self.root, width=600, height=450, bg="#34495e")
        self.canvas.pack(pady=10) 
        self.draw_intersection()
        
        info_frame = tk.Frame(self.root, bg="#ecf0f1")
        info_frame.pack(fill=tk.X, padx=20, pady=5)
        
        left_info = tk.Frame(info_frame, bg="#ecf0f1")
        left_info.pack(side=tk.LEFT, padx=10)
        
        self.step_label = tk.Label(left_info, text="Step: 0/300", 
                                   font=("Arial", 12, "bold"), bg="#ecf0f1")
        self.step_label.pack(anchor=tk.W) 
        
        self.phase_label = tk.Label(left_info, text="Phase: NS", 
                                    font=("Arial", 12), bg="#ecf0f1", fg="#27ae60")
        self.phase_label.pack(anchor=tk.W)
        
        self.action_label = tk.Label(left_info, text="Action: HOLD", 
                                     font=("Arial", 12), bg="#ecf0f1")
        self.action_label.pack(anchor=tk.W)
        
        right_info = tk.Frame(info_frame, bg="#ecf0f1")
        right_info.pack(side=tk.RIGHT, padx=10)
        
        self.total_cars_label = tk.Label(right_info, text="Total Waiting: 0", 
                                         font=("Arial", 12), bg="#ecf0f1")
        self.total_cars_label.pack(anchor=tk.E) 
        
        self.avg_waiting_label = tk.Label(right_info, text="Avg Waiting: 0.00", 
                                         font=("Arial", 12), bg="#ecf0f1")
        self.avg_waiting_label.pack(anchor=tk.E)
        
        self.switches_label = tk.Label(right_info, text="Switches: 0", 
                                      font=("Arial", 12), bg="#ecf0f1")
        self.switches_label.pack(anchor=tk.E)
        
        button_frame = tk.Frame(self.root, bg="#ecf0f1")
        button_frame.pack(pady=10)
        
        self.pause_btn = tk.Button(button_frame, text="Pause", 
                                   command=self.toggle_pause,  
                                   font=("Arial", 12, "bold"), bg="#f39c12", 
                                   fg="white", width=15, height=2)
        self.pause_btn.pack(side=tk.LEFT, padx=5)

        self.reset_btn = tk.Button(button_frame, text="Reset", 
                                   command=self.reset_simulation,  
                                   font=("Arial", 12, "bold"), bg="#e74c3c", 
                                   fg="white", width=15, height=2)
        self.reset_btn.pack(side=tk.LEFT, padx=5)
        
        speed_frame = tk.Frame(self.root, bg="#ecf0f1")
        speed_frame.pack(pady=5)
        
        tk.Label(speed_frame, text="Speed:", font=("Arial", 10), bg="#ecf0f1").pack(side=tk.LEFT, padx=5)
        
        self.speed_scale = tk.Scale(speed_frame, from_=100, to=2000, 
                                    orient=tk.HORIZONTAL, length=200,
                                    command=self.update_speed, bg="#ecf0f1")  
        self.speed_scale.set(500) 
        self.speed_scale.pack(side=tk.LEFT)
        
        tk.Label(speed_frame, text="(Lower = Faster)", 
                font=("Arial", 9, "italic"), bg="#ecf0f1", fg="gray").pack(side=tk.LEFT, padx=5)
        
    def draw_intersection(self):
        self.canvas.create_rectangle(250, 0, 350, 450, fill="#7f8c8d", outline="")
        self.canvas.create_rectangle(0, 175, 600, 275, fill="#7f8c8d", outline="")
        
        self.canvas.create_rectangle(250, 175, 350, 275, fill="#95a5a6", outline="")
        
        for i in range(0, 450, 30):  
            self.canvas.create_rectangle(295, i, 305, i+15, fill="white", outline="")
        for i in range(0, 600, 30):  
            self.canvas.create_rectangle(i, 220, i+15, 230, fill="white", outline="")
        
        self.north_light = self.canvas.create_oval(285, 150, 315, 180, fill="red", outline="black", width=2)
        self.south_light = self.canvas.create_oval(285, 270, 315, 300, fill="red", outline="black", width=2)
        self.east_light = self.canvas.create_oval(355, 210, 385, 240, fill="red", outline="black", width=2)
        self.west_light = self.canvas.create_oval(215, 210, 245, 240, fill="red", outline="black", width=2)
        
        self.canvas.create_rectangle(270, 60, 330, 95, fill="#2c3e50", outline="white", width=2)
        self.north_text = self.canvas.create_text(300, 77, text="N: 0", 
                                                 font=("Arial", 18, "bold"), fill="#f39c12")
        
        self.canvas.create_rectangle(270, 355, 330, 390, fill="#2c3e50", outline="white", width=2)
        self.south_text = self.canvas.create_text(300, 372, text="S: 0", 
                                                 font=("Arial", 18, "bold"), fill="#f39c12")
        
        self.canvas.create_rectangle(470, 205, 530, 240, fill="#2c3e50", outline="white", width=2)
        self.east_text = self.canvas.create_text(500, 222, text="E: 0", 
                                                font=("Arial", 18, "bold"), fill="#f39c12")
        
        self.canvas.create_rectangle(70, 205, 130, 240, fill="#2c3e50", outline="white", width=2)
        self.west_text = self.canvas.create_text(100, 222, text="W: 0", 
                                                font=("Arial", 18, "bold"), fill="#f39c12")
        
    def update_lights(self):
        if self.phase == "NS":
            self.canvas.itemconfig(self.north_light, fill="#2ecc71")
            self.canvas.itemconfig(self.south_light, fill="#2ecc71")
            self.canvas.itemconfig(self.east_light, fill="#e74c3c")
            self.canvas.itemconfig(self.west_light, fill="#e74c3c")
        else:  
            self.canvas.itemconfig(self.north_light, fill="#e74c3c")
            self.canvas.itemconfig(self.south_light, fill="#e74c3c")
            self.canvas.itemconfig(self.east_light, fill="#2ecc71")
            self.canvas.itemconfig(self.west_light, fill="#2ecc71")
    
    def update_display(self, action="HOLD"):
        self.canvas.itemconfig(self.north_text, text=f"N: {self.north}")
        self.canvas.itemconfig(self.south_text, text=f"S: {self.south}")
        self.canvas.itemconfig(self.east_text, text=f"E: {self.east}")
        self.canvas.itemconfig(self.west_text, text=f"W: {self.west}")
        
        self.step_label.config(text=f"Step: {self.current_step}/{self.total_steps}")
        self.phase_label.config(text=f"Phase: {self.phase} (t={self.time_in_phase})")
        self.action_label.config(text=f"Action: {action}")
        
        cars_waiting = self.north + self.south + self.east + self.west
        avg_waiting = self.total_waiting / self.current_step if self.current_step > 0 else 0
        
        self.total_cars_label.config(text=f"Total Waiting: {cars_waiting}")
        self.avg_waiting_label.config(text=f"Avg Waiting: {avg_waiting:.2f}")
        self.switches_label.config(text=f"Switches: {self.switches}")
        
        self.update_lights()
    
    def start_simulation(self):
        if not self.running:
            self.running = True  
            self.paused = False  
            
            sim_thread = threading.Thread(target=self.run_simulation_loop, daemon=True)
            sim_thread.start()
    
    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.pause_btn.config(text="Resume", bg="#3498db")  
        else:
            self.pause_btn.config(text="Pause", bg="#f39c12")  
    
    def reset_simulation(self):
        self.running = False
        self.paused = False
        self.north = 0
        self.south = 0
        self.east = 0
        self.west = 0
        self.phase = "NS"  
        self.time_in_phase = 0
        self.current_step = 0
        self.total_waiting = 0
        self.switches = 0
        
        self.update_display()
        self.pause_btn.config(text="Pause", bg="#f39c12")
        
        self.root.after(500, self.start_simulation)
    
    def update_speed(self, value):
        self.delay = int(value)
    
    def run_simulation_loop(self):
        print("\n" + "="*70)
        print(f"Algorithm: {self.algorithm_name}")
        print("="*70)
        print(f"{'Time':<8} {'N':<6} {'S':<6} {'E':<6} {'W':<6} {'Phase':<8} {'Action':<8} {'Total':<8}")
        print("-" * 70)
        
        for t in range(self.total_steps):
            if not self.running:
                break
                
            while self.paused:
                time.sleep(0.1)  
                if not self.running:
                    break
            
            self.current_step = t + 1
            
            state = (self.north, self.south, self.east, self.west, self.phase, self.time_in_phase)
            action = self.algorithm_func(state, self.horizon)
            
            self.north, self.south, self.east, self.west, self.phase, self.time_in_phase = \
                transition_for_simulation(state, action)
            
            if action == "SWITCH":
                self.switches += 1
            
            cars_waiting = self.north + self.south + self.east + self.west
            self.total_waiting += cars_waiting
            
            if t % 10 == 0:
                print(f"{t:<8} {self.north:<6} {self.south:<6} {self.east:<6} {self.west:<6} {self.phase:<8} {action:<8} {cars_waiting:<8}")
            
            self.root.after(0, lambda a=action: self.update_display(a))
            
            time.sleep(self.delay / 1000.0)
        
        if self.running:
            avg_waiting = self.total_waiting / self.total_steps if self.total_steps > 0 else 0
            print("\n" + "="*70)
            print("SIMULATION COMPLETE")
            print("="*70)
            print(f"Total Waiting: {self.total_waiting} cars")
            print(f"Average Waiting: {avg_waiting:.2f} cars")
            print(f"Switches: {self.switches}")
            print("\n")
        
        self.running = False


def run_gui_with_best_algorithm():
    algo_map = {
        "A*": a_star,
        "BFS": bfs,
        "DFS": dfs,
        "UCS": ucs,
        "IDDFS": iddfs
    }
    
    print("\nRunning algorithm comparison to find best average waiting time...")
    best_algo_name = compare_algorithms(total_time=300, horizon=10)
    
    print("\n" + "="*80)
    print(f"LAUNCHING GUI WITH BEST ALGORITHM: {best_algo_name}")
    print("="*80)
    print("\nGUI will now visualize the simulation in real-time.")
    print("All output will continue to appear in this terminal.\n")
    
    best_algo_func = algo_map[best_algo_name]
    
    root = tk.Tk()
    app = TrafficLightGUI(root, best_algo_func, best_algo_name)
    root.mainloop()


if __name__ == "__main__":
    
    
  
    print("\n" + "="*80)
    print("NOW RUNNING FULL COMPARISON (300 steps, all 5 algorithms)")
    print("="*80)
    
    run_gui_with_best_algorithm()