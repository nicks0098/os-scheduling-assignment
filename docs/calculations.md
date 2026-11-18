# Scheduling Calculations

## Input Dataset (Preserved Across All Runs)
| PID | Arrival Time (AT) | Burst Time (BT) | Priority |
| :--- | :---: | :---: | :---: |
| P1 | 2 | 6 | 2 |
| P2 | 4 | 3 | 1 |
| P3 | 5 | 4 | 3 |
| P4 | 18 | 2 | 1 |

## Formulas Used
- **Turnaround Time (TAT)** = `Completion Time (CT) - Arrival Time (AT)`
- **Waiting Time (WT)** = `Turnaround Time (TAT) - Burst Time (BT)`
- **Response Time (RT)** = `First Start Time (ST) - Arrival Time (AT)`
- **CPU Utilization** = `((Total Time - Total Idle Time) / Total Time) * 100%`
- **Throughput** = `Number of Processes / Total Time`

---

## 1. FCFS, SJF (Non-Preemptive), and Priority (Non-Preemptive)
For this dataset, P1 arrives first at `t = 2` and runs uninterrupted until `t = 8` (in non-preemptive modes), by which time both P2 (`BT=3, Prio=1`) and P3 (`BT=4, Prio=3`) are ready. Both SJF and Priority select P2 next, then P3, leaving an idle gap `[15 -> 18]` before P4 arrives.

- **Timeline:** `[0->2] IDLE | [2->8] P1 | [8->11] P2 | [11->15] P3 | [15->18] IDLE | [18->20] P4`
- **Idle Intervals:** `[0 -> 2]` (2 units), `[15 -> 18]` (3 units) -> **Total Idle = 5 units**

| PID | AT | BT | Start | CT | TAT (`CT-AT`) | WT (`TAT-BT`) | RT (`ST-AT`) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| P1 | 2 | 6 | 2 | 8 | 6 | 0 | 0 |
| P2 | 4 | 3 | 8 | 11 | 7 | 4 | 4 |
| P3 | 5 | 4 | 11 | 15 | 10 | 6 | 6 |
| P4 | 18 | 2 | 18 | 20 | 2 | 0 | 0 |

- **Average TAT** = `(6 + 7 + 10 + 2) / 4 = 25 / 4 = 6.25`
- **Average WT** = `(0 + 4 + 6 + 0) / 4 = 10 / 4 = 2.50`
- **Average RT** = `(0 + 4 + 6 + 0) / 4 = 10 / 4 = 2.50`
- **CPU Utilization** = `((20 - 5) / 20) * 100% = 75.00%`
- **Throughput** = `4 / 20 = 0.2000 proc/unit`

---

## 2. SRTF (Shortest Remaining Time First - Preemptive)
At `t = 4`, P1 has 4 units remaining while P2 arrives with `BT = 3`. SRTF preempts P1 and runs P2 (`4->7`), then resumes P1 (`7->11`), then P3 (`11->15`), then idle (`15->18`), then P4 (`18->20`).

- **Timeline:** `[0->2] IDLE | [2->4] P1 | [4->7] P2 | [7->11] P1 | [11->15] P3 | [15->18] IDLE | [18->20] P4`
- **Average TAT** = `(9 + 3 + 10 + 2) / 4 = 24 / 4 = 6.00`
- **Average WT** = `(3 + 0 + 6 + 0) / 4 = 9 / 4 = 2.25`
- **Average RT** = `(0 + 0 + 6 + 0) / 4 = 6 / 4 = 1.50`

---

## 3. Round Robin (Time Quantum = 2)
- **Timeline:** `[0->2] IDLE | [2->4] P1 | [4->6] P2 | [6->8] P1 | [8->10] P3 | [10->11] P2 | [11->13] P1 | [13->15] P3 | [15->18] IDLE | [18->20] P4`
- **Average TAT** = `(11 + 7 + 10 + 2) / 4 = 30 / 4 = 7.50`
- **Average WT** = `(5 + 4 + 6 + 0) / 4 = 15 / 4 = 3.75`
- **Average RT** = `(0 + 0 + 3 + 0) / 4 = 3 / 4 = 0.75`
