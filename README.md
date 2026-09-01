# Smart Traffic Signal Optimization 🚥

A dynamic, real-time traffic signal optimization system that uses camera sensor inputs, a **Max-Heap data structure**, and a **Greedy allocation algorithm** to reduce traffic congestion at 4-way intersections.

---

## 📌 Problem Overview
Traditional traffic light systems in Sri Lanka operate on rigid **Fixed-Time Control** (90–180s cycle times split equally regardless of real vehicle demand). 
* **Blind to Demand:** Gives green lights to empty roads while major lanes experience heavy queues.
* **National Economic Impact:** Traffic congestion costs the Sri Lankan economy over **Rs. 1 Billion every single day** in wasted fuel, lost productivity, and increased emissions.
* **System Breakdown:** Peak hour traffic often forces traffic police officers to turn off automatic signals and step in to manage traffic manually.

---

## 💡 Proposed Solution
1. **Real-time Sensing:** Low-cost cameras on signal poles count waiting vehicles (cars, buses, three-wheelers, bikes) per lane in real time.
2. **Max-Heap Ranking:** Pushes real-time counts into a Max-Heap to instantly identify the busiest lane.
3. **Safety Minimum Guarantee:** Guarantees a mandatory 10-second green light to every lane to prevent lane starvation.
4. **Proportional Greedy Allocation:** Dynamically distributes the remaining green time pool in direct proportion to real traffic demand.

---

## ⚙️ How the Algorithm Works (90s Cycle Example)

1. **Reserve Minimum Safety Green Time:**
   $$\text{Reserved Time} = 4 \text{ lanes} \times 10\text{s} = 40\text{s}$$
   $$\text{Remaining Time Pool} = 90\text{s} - 40\text{s} = 50\text{s}$$

2. **Heapify Queues (O(n)):** 
   Arranges lane queue counts into a Max-Heap where the most congested lane rises to the top.

3. **Extract-Max & Proportional Split (O(nlog n)):**
   Distributes the remaining 50 seconds based on demand percentage. If the North lane holds 60% of all vehicles, it receives $60\% \times 50\text{s} = 30\text{s}$ extra green time (totaling 40s).

---

## 📊 Simulation Results

| Metric | Fixed-Timer (Baseline) | Greedy + Max-Heap (Proposed) | Improvement |
| :--- | :--- | :--- | :--- |
| **North Lane Queue (Avg)** | 206.20 vehicles | 15.21 vehicles | **13.5× Faster Clearance** |
| **South Lane Queue (Avg)** | 76.12 vehicles | 10.73 vehicles | **7.1× Reduction** |
| **East Lane Queue (Avg)** | 1.45 vehicles | 1.83 vehicles | Stable |
| **West Lane Queue (Avg)** | 1.17 vehicles | 1.62 vehicles | Stable |
| **Overall Intersection Avg** | **71.24 vehicles** | **7.35 vehicles** | **89.7% Reduction** |

---

## 📈 Time Complexity Analysis

* **Fixed-Timer:** $O(n)$ — Extremely fast, but zero awareness of real-time demand.
* **Greedy + Max-Heap:** $O(n \log n)$ — Efficient and scalable. Requires only 33 operations for a 10-lane intersection.
* **Brute-Force Optimal:** $O(n!)$ — Factorial growth. Requires ~3.6 million operations per decision at $n=10$, making it computationally infeasible.

---

## 📁 Repository Structure

```text
├── traffic_algorithm.py      # Core simulation script for Fixed vs. Greedy Max-Heap
├── complexity_growth.png     # O(n) vs O(n log n) vs O(n!) comparison graph
└── waiting_time_comparison.png # Queue length comparison chart per lane
