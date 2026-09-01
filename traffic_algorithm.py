"""
Smart Traffic Light Control - Simulation & Comparison
------------------------------------------------------
Compares two traffic-signal control algorithms over a simulated intersection:

  1. FIXED-TIMER (current real-world baseline)
     - Every lane always gets an equal share of the cycle time,
       regardless of how many vehicles are actually waiting.

  2. GREEDY / PRIORITY-QUEUE (developed solution)
     - A max-heap ranks the 4 lanes by vehicle count every cycle.
     - Green time is allocated proportionally to demand (busiest lane
       gets more green time, empty lanes get the safety minimum).

This script produces:
  - waiting_time_comparison.png  (avg & max queue length per lane)
  - complexity_growth.png        (O(k!) brute force vs O(k log k) greedy)
  
"""

import heapq
import math
import random
import matplotlib.pyplot as plt

random.seed(42)

# ----------------------------- CONFIG ---------------------------------
LANES = ["North", "South", "East", "West"]
K = len(LANES)

CYCLE_TIME = 90          # total seconds shared among all lanes each cycle
MIN_GREEN = 10            # safety minimum green time per lane (seconds)
SATURATION_FLOW = 0.5     # vehicles discharged per second of green (~1 car/2s)
SIM_SECONDS = 3600 * 2    # simulate 2 hours of traffic

# Average arrival rate (vehicles/second) per lane -> deliberately uneven,
# mimicking a real intersection where one road is a main road (busy)
# and the cross street is light.
ARRIVAL_RATES = {"North": 0.18, "South": 0.15, "East": 0.05, "West": 0.04}


# ----------------------- ALGORITHM 1: FIXED-TIMER -----------------------
def fixed_timer_green_times():
    """Equal split, ignores real demand. O(1)."""
    share = CYCLE_TIME / K
    return {lane: share for lane in LANES}


# ------------------- ALGORITHM 2: GREEDY / MAX-HEAP ---------------------
def greedy_green_times(queues):
    """
    Rank lanes by current queue length using a max-heap, then distribute
    the cycle time proportionally to demand (busiest lane gets the most
    green time). This is the classic GREEDY algorithm-design pattern
    (always service the largest need first) combined with a heap for
    O(k log k) ordering instead of brute-force search.
    """
    # Build max-heap of (-count, lane) -> O(k)
    heap = [(-queues[lane], lane) for lane in LANES]
    heapq.heapify(heap)                       # O(k)

    total_demand = sum(queues.values())
    green = {}

    if total_demand == 0:
        # nobody waiting -> equal minimum split
        return {lane: CYCLE_TIME / K for lane in LANES}

    remaining_time = CYCLE_TIME - MIN_GREEN * K
    # Extract-max repeatedly -> O(k log k) total
    while heap:
        neg_count, lane = heapq.heappop(heap)
        count = -neg_count
        proportional_extra = remaining_time * (count / total_demand)
        green[lane] = MIN_GREEN + proportional_extra

    return green


# --------------------- BRUTE FORCE (for complexity demo) ----------------
def brute_force_operations(k):
    """Number of permutations to check every possible servicing ORDER
    of k lanes to find the 'optimal' schedule = k! (factorial growth)."""
    return math.factorial(k)


def greedy_operations(k):
    """Heap build + extract-max operations ~ k log k."""
    return max(1, int(k * math.log2(k))) if k > 1 else 1


# --------------------------- SIMULATION LOOP ----------------------------
def simulate(algorithm):
    queues = {lane: 0 for lane in LANES}
    history = {lane: [] for lane in LANES}
    t = 0
    while t < SIM_SECONDS:
        # arrivals for this cycle (Poisson-like via random draws each second)
        # decide green split for this cycle using CURRENT queue snapshot
        if algorithm == "fixed":
            green_times = fixed_timer_green_times()
        else:
            green_times = greedy_green_times(queues)

        cycle_len = int(CYCLE_TIME)
        elapsed_in_cycle = {lane: 0 for lane in LANES}

        for _ in range(cycle_len):
            for lane in LANES:
                # arrival
                if random.random() < ARRIVAL_RATES[lane]:
                    queues[lane] += 1
                # service only if this lane currently has its green window
                if elapsed_in_cycle[lane] < green_times[lane]:
                    if random.random() < SATURATION_FLOW and queues[lane] > 0:
                        queues[lane] -= 1
                elapsed_in_cycle[lane] += 1
                history[lane].append(queues[lane])
            t += 1
            if t >= SIM_SECONDS:
                break
    return history


def summarize(history, label):
    print(f"\n--- {label} ---")
    stats = {}
    for lane in LANES:
        data = history[lane]
        avg_q = sum(data) / len(data)
        max_q = max(data)
        stats[lane] = (avg_q, max_q)
        print(f"{lane:6s}  avg queue={avg_q:6.2f}  max queue={max_q:3d}")
    overall_avg = sum(s[0] for s in stats.values()) / K
    print(f"Overall average queue length: {overall_avg:.2f} vehicles")
    return stats, overall_avg


if __name__ == "__main__":
    fixed_history = simulate("fixed")
    greedy_history = simulate("greedy")

    fixed_stats, fixed_avg = summarize(fixed_history, "FIXED-TIMER (baseline)")
    greedy_stats, greedy_avg = summarize(greedy_history, "GREEDY / HEAP (developed)")

    improvement = (fixed_avg - greedy_avg) / fixed_avg * 100
    print(f"\nAverage-queue reduction with greedy algorithm: {improvement:.1f}%")

    # ---------------- CHART 1: waiting/queue comparison ----------------
    fig, ax = plt.subplots(figsize=(8, 5))
    x = range(K)
    width = 0.35
    fixed_avgs = [fixed_stats[l][0] for l in LANES]
    greedy_avgs = [greedy_stats[l][0] for l in LANES]

    ax.bar([i - width/2 for i in x], fixed_avgs, width, label="Fixed-Timer (current)", color="#d9534f")
    ax.bar([i + width/2 for i in x], greedy_avgs, width, label="Greedy/Heap (developed)", color="#5cb85c")
    ax.set_xticks(list(x))
    ax.set_xticklabels(LANES)
    ax.set_ylabel("Average vehicles waiting (queue length)")
    ax.set_title("Average Queue Length per Lane: Fixed-Timer vs Greedy Algorithm")
    ax.legend()
    fig.tight_layout()
    fig.savefig("waiting_time_comparison.png", dpi=150)
    print("Saved waiting_time_comparison.png")

    # ---------------- CHART 2: complexity growth -----------------------
    ks = list(range(2, 11))
    brute = [brute_force_operations(k) for k in ks]
    greedy_ops = [greedy_operations(k) for k in ks]
    linear_ops = [k for k in ks]

    fig2, ax2 = plt.subplots(figsize=(8, 5))
    ax2.plot(ks, brute, marker="o", color="#d9534f", label="Brute-force optimal order  O(n!)")
    ax2.plot(ks, greedy_ops, marker="s", color="#5cb85c", label="Greedy + max-heap  O(n log n)")
    ax2.plot(ks, linear_ops, marker="^", color="#428bca", label="Fixed-timer decision  O(n)")
    ax2.set_yscale("log")
    ax2.set_xlabel("Number of lanes at the intersection (n)")
    ax2.set_ylabel("Operations needed per decision (log scale)")
    ax2.set_title("Time-Complexity Growth: Brute Force vs Greedy vs Fixed-Timer")
    ax2.legend()
    fig2.tight_layout()
    fig2.savefig("complexity_growth.png", dpi=150)
    print("Saved complexity_growth.png")
