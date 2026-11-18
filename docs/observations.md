# Observations & Analysis

## 1. CPU Scheduling Comparison
| Algorithm | Avg TAT | Avg WT | Avg RT | CPU Utilization |
| :--- | :---: | :---: | :---: | :---: |
| FCFS | 6.25 | 2.50 | 2.50 | 75.00% |
| SJF (Non-Preemptive) | 6.25 | 2.50 | 2.50 | 75.00% |
| **SRTF (Preemptive)** | **6.00** | **2.25** | 1.50 | 75.00% |
| **Round Robin (q=2)** | 7.50 | 3.75 | **0.75** | 75.00% |
| Priority (Non-Preemptive) | 6.25 | 2.50 | 2.50 | 75.00% |

### Key Takeaways
1. **Optimal Average Waiting & Turnaround Time:** **SRTF** achieved the lowest average waiting time (`2.25`) and turnaround time (`6.00`) because it preempted the longer job `P1` when shorter job `P2` arrived at `t = 4`.
2. **Best Responsiveness:** **Round Robin (`q = 2`)** delivered the lowest average response time (`0.75`) by giving every ready process an immediate time slice, at the cost of higher average waiting time (`3.75`) and more context switches.
3. **Idle Interval Impact:** All algorithms experienced the same `5` units of idle time (`[0->2]` before `P1` arrived and `[15->18]` before `P4` arrived), capping CPU utilization at `75.00%` regardless of scheduling policy.
4. **Data Preservation:** Deep-copying (`copy.deepcopy`) inside `validate_processes()` ensured the original process list remained completely unaltered across all five algorithm executions.

## 2. Input Validation & Error Handling
- Validating negative arrival times, zero/negative burst times, duplicate PIDs, invalid time quanta, and non-integer types up front prevents silent logic bugs and infinite loops (especially in Round Robin and SRTF).

## 3. Process Creation, Threads, and IPC Observations
- **Processes (`multiprocessing.Process`):** Each child receives an isolated address space and distinct OS PID while sharing the parent's PPID.
- **Threads (`threading.Thread` + `threading.Lock`):** Threads share the same process memory space; using `Lock` prevented race conditions on the shared counter (`4000/4000` exact increments).
- **IPC Mechanisms:** `os.pipe()` and `multiprocessing.Pipe()` provide fast byte/message streams, `multiprocessing.Queue` offers thread/process-safe FIFO messaging, and `multiprocessing.Value` with `Lock` enables synchronized shared-memory state updates.
