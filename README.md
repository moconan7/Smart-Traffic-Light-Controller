# 🚦 AI-Based Intelligent Traffic Light Control System

An intelligent traffic light control system that uses **classical AI search algorithms** to dynamically manage traffic signals at a four-way intersection, aiming to **minimize vehicle waiting time**.

This project simulates real-world traffic conditions and compares multiple AI algorithms to determine the most efficient control strategy.

---

## 📌 Project Overview

Traditional traffic lights operate on fixed timers, often causing unnecessary congestion.
This project introduces an **AI-driven decision-making system** that:

* Observes current traffic conditions
* Predicts future congestion
* Decides whether to **HOLD** or **SWITCH** the traffic signal
* Continuously adapts to changing traffic patterns

The system supports **visual simulation** using a GUI and **performance comparison** between multiple AI algorithms.

---

## 🧠 AI Algorithms Implemented

The project applies the following **state-space search algorithms**:

| Algorithm                           | Description                                          |
| ----------------------------------- | ---------------------------------------------------- |
| **BFS (Breadth-First Search)**      | Explores all possible states level by level          |
| **DFS (Depth-First Search)**        | Explores deep paths first (not always optimal)       |
| **UCS (Uniform Cost Search)**       | Expands states based on cumulative waiting cost      |
| **A***                              | Uses cost + heuristic to make intelligent decisions  |
| **IDDFS (Iterative Deepening DFS)** | Combines DFS memory efficiency with BFS completeness |

➡ Each algorithm plans decisions over a fixed **planning horizon** and returns the best immediate action.

---

## 🧩 Problem Representation

### State Definition

Each system state is represented as:

```
(north_cars, south_cars, east_cars, west_cars, current_phase, time_in_phase)
```

| Parameter       | Description                        |
| --------------- | ---------------------------------- |
| `north_cars`    | Vehicles waiting from the north    |
| `south_cars`    | Vehicles waiting from the south    |
| `east_cars`     | Vehicles waiting from the east     |
| `west_cars`     | Vehicles waiting from the west     |
| `current_phase` | Active green signal (`NS` or `EW`) |
| `time_in_phase` | Duration of the current phase      |

---

## 🎯 Objective Function

The system minimizes:

```python
cost = north + south + east + west
```

This represents the **total number of waiting vehicles** at any given moment.

---

## 🔮 Heuristic Function (A*)

The heuristic estimates future congestion:

```python
heuristic = max(north, south, east, west)
```

✔ Admissible
✔ Efficient
✔ Guides the search toward the most congested direction

---

## 🔁 State Transitions

Two transition models are used:

### 1️⃣ Planning Transition (Deterministic)

Used by AI algorithms for consistent decision-making.

* Fixed vehicle arrivals
* Predictable departures
* Enforced minimum green time

### 2️⃣ Simulation Transition (Stochastic)

Used during execution to mimic real-world traffic.

* Random vehicle arrivals
* Random vehicle departures
* More realistic behavior

---

## 🚥 Traffic Signal Actions

| Action     | Effect                                                    |
| ---------- | --------------------------------------------------------- |
| **HOLD**   | Maintain the current traffic phase                        |
| **SWITCH** | Change traffic phase (if minimum green time is satisfied) |

---

## 🖥️ Graphical User Interface (GUI)

The project includes a **Tkinter-based GUI** that visualizes:

* Real-time traffic flow
* Traffic light states
* Vehicle counts per direction
* Algorithm decisions
* Performance metrics

### GUI Features:

* Pause / Resume simulation
* Reset simulation
* Adjustable simulation speed
* Live statistics display

---

## 📊 Performance Evaluation

Each algorithm is evaluated based on:

* **Total waiting vehicles**
* **Average waiting time**
* **Number of signal switches**
* **Execution time per decision**

A full comparison is automatically performed to identify the **best-performing algorithm**, which is then used to drive the GUI simulation.

---

## ▶️ How to Run the Project

### Requirements

* Python 3.8+
* Tkinter (usually included with Python)

### Run the system

```bash
python main.py
```

The program will:

1. Test all algorithms
2. Run a full performance comparison
3. Automatically launch the GUI using the best algorithm

---

## 🧪 Example Scenario

**Initial State:**

```
North = 10, South = 8
East = 2, West = 1
Current Phase = NS
```

**Expected Behavior:**

* The system keeps the NS signal active
* Heavy traffic is cleared first
* Unnecessary switching is avoided

---

## ⚙️ Key Parameters

| Parameter        | Description                       |
| ---------------- | --------------------------------- |
| `horizon`        | Number of future steps considered |
| `min_green_time` | Minimum duration before switching |
| `total_time`     | Simulation length                 |
| `delay`          | GUI animation speed               |

---

## 🚀 Future Improvements

* Multi-lane intersections
* Left/right turn modeling
* Reinforcement Learning (Q-Learning / DQN)
* Multiple connected intersections
* Real traffic data integration

---

## 🎓 Academic Relevance

This project demonstrates practical applications of:

* State-space search
* Heuristic design
* AI planning
* Real-time decision-making
* Simulation vs planning models

Suitable for:

* Artificial Intelligence courses
* Intelligent Systems
* AI Planning & Search assignments

---

## 👨‍💻 Author

**Mohamed Kamel**
Computer Science Student
AI & Intelligent Systems Enthusiast

---

## 📄 License

This project is intended for **educational and academic use**.

--
