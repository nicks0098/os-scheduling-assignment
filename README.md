# OS Scheduling, Process, Thread & IPC Assignment

**Name:** Nikhil Dhandhi  
**Roll No:** 2401360026  

## Environment
- **OS:** Ubuntu 24.04 LTS (via WSL2)
- **Language:** Python 3.x
- **Editor:** Visual Studio Code
- **Approved Linux Commands:** `python3`, `uname`, `ps`, `ls`, `cat`, `git`

## Project Structure
```text
os_assignment/
├── src/
│   ├── scheduler.py            # FCFS, SJF, SRTF, Round Robin, Priority + validation
│   └── process_thread_ipc.py   # Process creation, Threads + Lock, Pipe/Queue/SharedMem IPC
├── tests/
│   └── test_suite.py           # Valid, Boundary, and Invalid test cases
├── docs/
│   ├── calculations.md         # Step-by-step manual scheduling calculations
│   └── observations.md         # Comparative analysis & OS mechanism observations
├── screenshots/                # Terminal execution evidence (PNG images)
└── README.md
```

## How to Run
```bash
# 1. Run CPU Scheduling Simulator
python3 src/scheduler.py

# 2. Run Valid, Boundary, and Invalid Test Suite
python3 -m unittest tests/test_suite.py -v

# 3. Run Process Creation, Threads, and IPC Demo
python3 src/process_thread_ipc.py
```

## ZOSIMA Submission Checklist
- [x] Source files (`src/scheduler.py`, `src/process_thread_ipc.py`, `tests/test_suite.py`)
- [x] Terminal evidence (`screenshots/*.png`)
- [x] Calculations (`docs/calculations.md`)
- [x] Observations (`docs/observations.md`)
- [x] GitHub repository link
