"""
CPU Scheduling Algorithms Simulator
Demonstrates FCFS, SJF (Non-Preemptive), SRTF (Preemptive), Round Robin,
and Priority (Non-Preemptive) scheduling while preserving original process data.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Dict, List, Tuple, Any


@dataclass(frozen=True)
class Process:
    pid: str
    arrival_time: int
    burst_time: int
    priority: int = 1


def validate_processes(processes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Validate process list and return a clean deep copy."""
    if not isinstance(processes, list) or len(processes) == 0:
        raise ValueError("Process list must be a non-empty list.")

    seen_pids = set()
    validated: List[Dict[str, Any]] = []

    for idx, proc in enumerate(processes):
        if not isinstance(proc, dict):
            raise TypeError(f"Process at index {idx} must be a dictionary.")

        for field in ("pid", "arrival_time", "burst_time"):
            if field not in proc:
                raise ValueError(f"Process at index {idx} is missing required field '{field}'.")

        pid = str(proc["pid"]).strip()
        if not pid:
            raise ValueError(f"Process at index {idx} has an empty PID.")
        if pid in seen_pids:
            raise ValueError(f"Duplicate PID detected: '{pid}'.")
        seen_pids.add(pid)

        at = proc["arrival_time"]
        bt = proc["burst_time"]
        prio = proc.get("priority", 1)

        if not isinstance(at, int) or isinstance(at, bool):
            raise TypeError(f"Arrival time for '{pid}' must be an integer.")
        if not isinstance(bt, int) or isinstance(bt, bool):
            raise TypeError(f"Burst time for '{pid}' must be an integer.")
        if not isinstance(prio, int) or isinstance(prio, bool):
            raise TypeError(f"Priority for '{pid}' must be an integer.")

        if at < 0:
            raise ValueError(f"Arrival time for '{pid}' cannot be negative (got {at}).")
        if bt <= 0:
            raise ValueError(f"Burst time for '{pid}' must be greater than 0 (got {bt}).")
        if prio < 0:
            raise ValueError(f"Priority for '{pid}' cannot be negative (got {prio}).")

        validated.append({
            "pid": pid,
            "arrival_time": at,
            "burst_time": bt,
            "priority": prio,
        })

    return copy.deepcopy(validated)


def _compute_metrics(
    timeline: List[Tuple[str, int, int]],
    original_processes: List[Dict[str, Any]],
    completion_times: Dict[str, int],
    start_times: Dict[str, int],
) -> Dict[str, Any]:
    """Compute per-process and aggregate scheduling metrics."""
    rows = []
    total_tat = 0
    total_wt = 0
    total_rt = 0
    total_bt = 0

    for p in original_processes:
        pid = p["pid"]
        at = p["arrival_time"]
        bt = p["burst_time"]
        ct = completion_times[pid]
        st = start_times[pid]
        tat = ct - at
        wt = tat - bt
        rt = st - at

        total_tat += tat
        total_wt += wt
        total_rt += rt
        total_bt += bt

        rows.append({
            "pid": pid,
            "arrival_time": at,
            "burst_time": bt,
            "priority": p["priority"],
            "start_time": st,
            "completion_time": ct,
            "turnaround_time": tat,
            "waiting_time": wt,
            "response_time": rt,
        })

    idle_intervals = [(s, e) for label, s, e in timeline if label == "IDLE"]
    total_idle = sum(e - s for s, e in idle_intervals)
    total_time = timeline[-1][2] - timeline[0][1] if timeline else 0
    cpu_util = ((total_time - total_idle) / total_time * 100.0) if total_time > 0 else 0.0
    throughput = len(original_processes) / total_time if total_time > 0 else 0.0
    n = len(original_processes)

    return {
        "timeline": timeline,
        "idle_intervals": idle_intervals,
        "total_idle_time": total_idle,
        "total_time": total_time,
        "cpu_utilization": round(cpu_util, 2),
        "throughput": round(throughput, 4),
        "avg_turnaround_time": round(total_tat / n, 2),
        "avg_waiting_time": round(total_wt / n, 2),
        "avg_response_time": round(total_rt / n, 2),
        "process_metrics": rows,
    }


def _merge_timeline(segments: List[Tuple[str, int, int]]) -> List[Tuple[str, int, int]]:
    """Merge consecutive timeline segments with the same label."""
    if not segments:
        return []
    merged = [segments[0]]
    for label, start, end in segments[1:]:
        prev_label, prev_start, prev_end = merged[-1]
        if label == prev_label and start == prev_end:
            merged[-1] = (prev_label, prev_start, end)
        else:
            merged.append((label, start, end))
    return merged


def fcfs(processes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """First-Come, First-Served (Non-Preemptive)."""
    work = validate_processes(processes)
    work.sort(key=lambda p: (p["arrival_time"], p["pid"]))

    time = 0
    timeline: List[Tuple[str, int, int]] = []
    completion_times: Dict[str, int] = {}
    start_times: Dict[str, int] = {}

    for p in work:
        if time < p["arrival_time"]:
            timeline.append(("IDLE", time, p["arrival_time"]))
            time = p["arrival_time"]
        start_times[p["pid"]] = time
        end_time = time + p["burst_time"]
        timeline.append((p["pid"], time, end_time))
        completion_times[p["pid"]] = end_time
        time = end_time

    return _compute_metrics(_merge_timeline(timeline), processes, completion_times, start_times)


def sjf_non_preemptive(processes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Shortest Job First (Non-Preemptive)."""
    work = validate_processes(processes)
    remaining = copy.deepcopy(work)

    time = 0
    timeline: List[Tuple[str, int, int]] = []
    completion_times: Dict[str, int] = {}
    start_times: Dict[str, int] = {}

    while remaining:
        ready = [p for p in remaining if p["arrival_time"] <= time]
        if not ready:
            next_arrival = min(p["arrival_time"] for p in remaining)
            timeline.append(("IDLE", time, next_arrival))
            time = next_arrival
            continue

        chosen = min(ready, key=lambda p: (p["burst_time"], p["arrival_time"], p["pid"]))
        remaining.remove(chosen)
        start_times[chosen["pid"]] = time
        end_time = time + chosen["burst_time"]
        timeline.append((chosen["pid"], time, end_time))
        completion_times[chosen["pid"]] = end_time
        time = end_time

    return _compute_metrics(_merge_timeline(timeline), processes, completion_times, start_times)


def srtf_preemptive(processes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Shortest Remaining Time First (Preemptive SJF)."""
    work = validate_processes(processes)
    rem_bt = {p["pid"]: p["burst_time"] for p in work}
    start_times: Dict[str, int] = {}
    completion_times: Dict[str, int] = {}
    timeline: List[Tuple[str, int, int]] = []

    completed = 0
    n = len(work)
    time = 0

    while completed < n:
        ready = [p for p in work if p["arrival_time"] <= time and rem_bt[p["pid"]] > 0]
        if not ready:
            future = [p["arrival_time"] for p in work if rem_bt[p["pid"]] > 0]
            next_arrival = min(future)
            timeline.append(("IDLE", time, next_arrival))
            time = next_arrival
            continue

        chosen = min(ready, key=lambda p: (rem_bt[p["pid"]], p["arrival_time"], p["pid"]))
        pid = chosen["pid"]
        if pid not in start_times:
            start_times[pid] = time

        timeline.append((pid, time, time + 1))
        rem_bt[pid] -= 1
        time += 1

        if rem_bt[pid] == 0:
            completion_times[pid] = time
            completed += 1

    return _compute_metrics(_merge_timeline(timeline), processes, completion_times, start_times)


def round_robin(processes: List[Dict[str, Any]], quantum: int = 2) -> Dict[str, Any]:
    """Round Robin Scheduling."""
    if not isinstance(quantum, int) or isinstance(quantum, bool) or quantum <= 0:
        raise ValueError(f"Time quantum must be a positive integer (got {quantum}).")

    work = validate_processes(processes)
    work.sort(key=lambda p: (p["arrival_time"], p["pid"]))
    rem_bt = {p["pid"]: p["burst_time"] for p in work}

    time = 0
    idx = 0
    n = len(work)
    queue: List[Dict[str, Any]] = []
    timeline: List[Tuple[str, int, int]] = []
    start_times: Dict[str, int] = {}
    completion_times: Dict[str, int] = {}

    while idx < n or queue:
        if not queue:
            if time < work[idx]["arrival_time"]:
                timeline.append(("IDLE", time, work[idx]["arrival_time"]))
                time = work[idx]["arrival_time"]
            while idx < n and work[idx]["arrival_time"] <= time:
                queue.append(work[idx])
                idx += 1

        current = queue.pop(0)
        pid = current["pid"]
        if pid not in start_times:
            start_times[pid] = time

        exec_slice = min(quantum, rem_bt[pid])
        timeline.append((pid, time, time + exec_slice))
        time += exec_slice
        rem_bt[pid] -= exec_slice

        while idx < n and work[idx]["arrival_time"] <= time:
            queue.append(work[idx])
            idx += 1

        if rem_bt[pid] > 0:
            queue.append(current)
        else:
            completion_times[pid] = time

    return _compute_metrics(_merge_timeline(timeline), processes, completion_times, start_times)


def priority_non_preemptive(processes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Priority Scheduling (Non-Preemptive, lower number = higher priority)."""
    work = validate_processes(processes)
    remaining = copy.deepcopy(work)

    time = 0
    timeline: List[Tuple[str, int, int]] = []
    completion_times: Dict[str, int] = {}
    start_times: Dict[str, int] = {}

    while remaining:
        ready = [p for p in remaining if p["arrival_time"] <= time]
        if not ready:
            next_arrival = min(p["arrival_time"] for p in remaining)
            timeline.append(("IDLE", time, next_arrival))
            time = next_arrival
            continue

        chosen = min(ready, key=lambda p: (p["priority"], p["arrival_time"], p["pid"]))
        remaining.remove(chosen)
        start_times[chosen["pid"]] = time
        end_time = time + chosen["burst_time"]
        timeline.append((chosen["pid"], time, end_time))
        completion_times[chosen["pid"]] = end_time
        time = end_time

    return _compute_metrics(_merge_timeline(timeline), processes, completion_times, start_times)


def print_result(name: str, result: Dict[str, Any]) -> None:
    """Pretty-print labelled scheduling output."""
    print(f"\n{'=' * 74}")
    print(f"ALGORITHM: {name}")
    print(f"{'=' * 74}")

    gantt_str = " | ".join(f"[{s}->{e}] {lbl}" for lbl, s, e in result["timeline"])
    print(f"Execution Order : {gantt_str}")

    if result["idle_intervals"]:
        idle_str = ", ".join(f"[{s} -> {e}] (len={e-s})" for s, e in result["idle_intervals"])
    else:
        idle_str = "None"
    print(f"Idle Intervals  : {idle_str}")
    print(f"Total Idle Time : {result['total_idle_time']} units")

    print("\nPID   AT   BT   Prio   Start   CT   TAT   WT   RT")
    print("-" * 52)
    for r in result["process_metrics"]:
        print(
            f"{r['pid']:<5} {r['arrival_time']:<4} {r['burst_time']:<4} "
            f"{r['priority']:<6} {r['start_time']:<7} {r['completion_time']:<4} "
            f"{r['turnaround_time']:<5} {r['waiting_time']:<4} {r['response_time']:<4}"
        )

    print(
        f"\nSummary Metrics -> Avg TAT: {result['avg_turnaround_time']} | "
        f"Avg WT: {result['avg_waiting_time']} | "
        f"Avg RT: {result['avg_response_time']} | "
        f"CPU Util: {result['cpu_utilization']}% | "
        f"Throughput: {result['throughput']} proc/unit"
    )


def main() -> None:
    original_processes = [
        {"pid": "P1", "arrival_time": 2, "burst_time": 6, "priority": 2},
        {"pid": "P2", "arrival_time": 4, "burst_time": 3, "priority": 1},
        {"pid": "P3", "arrival_time": 5, "burst_time": 4, "priority": 3},
        {"pid": "P4", "arrival_time": 18, "burst_time": 2, "priority": 1},
    ]

    snapshot_before = copy.deepcopy(original_processes)
    print("ORIGINAL PROCESS DATA (Before Scheduling):")
    for p in original_processes:
        print(f"  {p}")

    algorithms = [
        ("FCFS (First-Come, First-Served)", fcfs(original_processes)),
        ("SJF (Shortest Job First - Non-Preemptive)", sjf_non_preemptive(original_processes)),
        ("SRTF (Shortest Remaining Time First)", srtf_preemptive(original_processes)),
        ("Round Robin (Quantum = 2)", round_robin(original_processes, quantum=2)),
        ("Priority (Non-Preemptive)", priority_non_preemptive(original_processes)),
    ]

    for name, res in algorithms:
        print_result(name, res)

    print(f"\n{'=' * 74}")
    print("COMPARISON SUMMARY")
    print(f"{'=' * 74}")
    print(f"{'Algorithm':<42} {'Avg TAT':>8} {'Avg WT':>8} {'Avg RT':>8} {'CPU %':>8}")
    print("-" * 74)
    for name, res in algorithms:
        print(
            f"{name:<42} {res['avg_turnaround_time']:>8.2f} "
            f"{res['avg_waiting_time']:>8.2f} {res['avg_response_time']:>8.2f} "
            f"{res['cpu_utilization']:>7.2f}%"
        )

    assert original_processes == snapshot_before, "Original process data was mutated!"
    print("\n[VERIFIED] Original process data preserved intact after all algorithm runs.")


if __name__ == "__main__":
    main()
