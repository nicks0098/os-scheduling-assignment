"""
Comprehensive Test Suite: Valid, Boundary, and Invalid Test Cases
for CPU Scheduling Algorithms & Input Validation.
"""

import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from scheduler import (
    fcfs,
    sjf_non_preemptive,
    srtf_preemptive,
    round_robin,
    priority_non_preemptive,
    validate_processes,
)


class TestCPUScheduler(unittest.TestCase):
    # ---------------- VALID TEST CASES ----------------
    def test_valid_mixed_arrivals_and_idle_gap(self):
        procs = [
            {"pid": "P1", "arrival_time": 2, "burst_time": 6, "priority": 2},
            {"pid": "P2", "arrival_time": 4, "burst_time": 3, "priority": 1},
            {"pid": "P3", "arrival_time": 5, "burst_time": 4, "priority": 3},
            {"pid": "P4", "arrival_time": 18, "burst_time": 2, "priority": 1},
        ]
        orig = copy.deepcopy(procs)

        res_fcfs = fcfs(procs)
        self.assertEqual(res_fcfs["idle_intervals"], [(0, 2), (15, 18)])
        self.assertEqual(res_fcfs["total_idle_time"], 5)
        self.assertEqual(res_fcfs["avg_turnaround_time"], 6.25)
        self.assertEqual(res_fcfs["avg_waiting_time"], 2.5)

        res_sjf = sjf_non_preemptive(procs)
        self.assertEqual(res_sjf["idle_intervals"], [(0, 2), (15, 18)])

        res_srtf = srtf_preemptive(procs)
        self.assertEqual(res_srtf["total_idle_time"], 5)
        self.assertEqual(res_srtf["avg_turnaround_time"], 6.0)
        self.assertEqual(res_srtf["avg_waiting_time"], 2.25)

        res_rr = round_robin(procs, quantum=2)
        self.assertEqual(res_rr["total_idle_time"], 5)
        self.assertEqual(res_rr["avg_response_time"], 0.75)

        res_prio = priority_non_preemptive(procs)
        self.assertEqual(res_prio["total_idle_time"], 5)

        # Verify original data preserved
        self.assertEqual(procs, orig)

    # ---------------- BOUNDARY TEST CASES ----------------
    def test_boundary_single_process(self):
        procs = [{"pid": "P1", "arrival_time": 0, "burst_time": 1, "priority": 1}]
        res = fcfs(procs)
        self.assertEqual(res["idle_intervals"], [])
        self.assertEqual(res["avg_turnaround_time"], 1.0)
        self.assertEqual(res["avg_waiting_time"], 0.0)
        self.assertEqual(res["cpu_utilization"], 100.0)

    def test_boundary_quantum_one_and_large_quantum(self):
        procs = [
            {"pid": "P1", "arrival_time": 0, "burst_time": 4, "priority": 1},
            {"pid": "P2", "arrival_time": 0, "burst_time": 3, "priority": 2},
        ]
        rr_q1 = round_robin(procs, quantum=1)
        rr_q100 = round_robin(procs, quantum=100)
        self.assertEqual(len(rr_q1["timeline"]), 7)
        self.assertEqual(rr_q100["timeline"], [("P1", 0, 4), ("P2", 4, 7)])

    def test_boundary_late_first_arrival(self):
        procs = [{"pid": "P1", "arrival_time": 10, "burst_time": 5, "priority": 1}]
        res = sjf_non_preemptive(procs)
        self.assertEqual(res["idle_intervals"], [(0, 10)])
        self.assertEqual(res["total_idle_time"], 10)

    # ---------------- INVALID TEST CASES ----------------
    def test_invalid_empty_process_list(self):
        with self.assertRaises(ValueError):
            validate_processes([])

    def test_invalid_negative_arrival_time(self):
        with self.assertRaises(ValueError):
            fcfs([{"pid": "P1", "arrival_time": -1, "burst_time": 4}])

    def test_invalid_zero_or_negative_burst_time(self):
        with self.assertRaises(ValueError):
            sjf_non_preemptive([{"pid": "P1", "arrival_time": 0, "burst_time": 0}])
        with self.assertRaises(ValueError):
            srtf_preemptive([{"pid": "P1", "arrival_time": 0, "burst_time": -3}])

    def test_invalid_duplicate_pid(self):
        with self.assertRaises(ValueError):
            fcfs([
                {"pid": "P1", "arrival_time": 0, "burst_time": 2},
                {"pid": "P1", "arrival_time": 1, "burst_time": 3},
            ])

    def test_invalid_quantum(self):
        procs = [{"pid": "P1", "arrival_time": 0, "burst_time": 3}]
        with self.assertRaises(ValueError):
            round_robin(procs, quantum=0)
        with self.assertRaises(ValueError):
            round_robin(procs, quantum=-2)

    def test_invalid_type_errors(self):
        with self.assertRaises(TypeError):
            fcfs([{"pid": "P1", "arrival_time": "zero", "burst_time": 3}])


if __name__ == "__main__":
    unittest.main(verbosity=2)
