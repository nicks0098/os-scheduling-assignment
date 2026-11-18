"""
Process Creation, Threads, Synchronization, and IPC Demonstration
Uses safe Python standard library and Linux/POSIX mechanisms.
"""

import os
import subprocess
import threading
import time
import multiprocessing as mp


def demo_linux_commands() -> None:
    """Safely run approved Linux inspection commands without shell=True."""
    print("\n" + "=" * 70)
    print("1. APPROVED LINUX ENVIRONMENT CHECKS")
    print("=" * 70)
    commands = [
        ["uname", "-a"],
        ["python3", "--version"],
        ["ps", "-o", "pid,ppid,comm", "-p", str(os.getpid())],
    ]
    for cmd in commands:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"$ {' '.join(cmd)}")
        print(res.stdout.strip())


def _child_worker(worker_id: int, queue: mp.Queue) -> None:
    """Worker function executed in a separate child process."""
    pid = os.getpid()
    ppid = os.getppid()
    msg = f"Child-{worker_id} (PID={pid}, PPID={ppid}) completed computation: {worker_id * 10}"
    queue.put(msg)


def demo_process_creation_and_queue_ipc() -> None:
    """Demonstrate safe process creation and Queue IPC."""
    print("\n" + "=" * 70)
    print("2. PROCESS CREATION & MULTIPROCESSING QUEUE IPC")
    print("=" * 70)
    print(f"Parent Process PID={os.getpid()}")

    q: mp.Queue = mp.Queue()
    processes = [mp.Process(target=_child_worker, args=(i, q)) for i in range(1, 4)]

    for p in processes:
        p.start()
        print(f"  Spawned child process PID={p.pid}")

    for p in processes:
        p.join()
        print(f"  Joined child process PID={p.pid} (exitcode={p.exitcode})")

    print("  Messages received via Queue IPC:")
    while not q.empty():
        print(f"    -> {q.get()}")


def _pipe_sender(conn) -> None:
    """Send structured data through an IPC pipe."""
    conn.send({"sender_pid": os.getpid(), "payload": "Hello from child via Pipe IPC!"})
    conn.close()


def demo_posix_and_mp_pipe_ipc() -> None:
    """Demonstrate OS-level os.pipe() and multiprocessing.Pipe() IPC."""
    print("\n" + "=" * 70)
    print("3. POSIX os.pipe() & multiprocessing.Pipe() IPC")
    print("=" * 70)

    # Low-level POSIX pipe
    read_fd, write_fd = os.pipe()
    os.write(write_fd, b"POSIX pipe message: CPU scheduling telemetry OK")
    os.close(write_fd)
    raw_bytes = os.read(read_fd, 1024)
    os.close(read_fd)
    print(f"  [os.pipe()] Received: {raw_bytes.decode('utf-8')}")

    # Multiprocessing Pipe between parent and child
    parent_conn, child_conn = mp.Pipe()
    p = mp.Process(target=_pipe_sender, args=(child_conn,))
    p.start()
    received = parent_conn.recv()
    p.join()
    print(f"  [mp.Pipe()] Received from PID {received['sender_pid']}: {received['payload']}")


def demo_threads_with_lock() -> None:
    """Demonstrate Python threading with Lock synchronization."""
    print("\n" + "=" * 70)
    print("4. MULTITHREADING WITH LOCK SYNCHRONIZATION")
    print("=" * 70)

    shared_state = {"counter": 0}
    lock = threading.Lock()

    def thread_task(tid: int, increments: int) -> None:
        for _ in range(increments):
            with lock:
                shared_state["counter"] += 1
        print(f"  Thread-{tid} (ident={threading.get_ident()}) finished {increments} safe increments.")

    threads = [threading.Thread(target=thread_task, args=(i, 1000)) for i in range(1, 5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"  Final synchronized shared counter = {shared_state['counter']} (expected: 4000)")


def _shared_mem_worker(shared_val: mp.Value, lock: mp.Lock) -> None:
    with lock:
        shared_val.value += 25


def demo_shared_memory_ipc() -> None:
    """Demonstrate synchronized shared memory Value IPC."""
    print("\n" + "=" * 70)
    print("5. SHARED MEMORY IPC (multiprocessing.Value + Lock)")
    print("=" * 70)
    shared_val = mp.Value("i", 100)
    lock = mp.Lock()
    workers = [mp.Process(target=_shared_mem_worker, args=(shared_val, lock)) for _ in range(4)]
    for w in workers:
        w.start()
    for w in workers:
        w.join()
    print(f"  Initial Value: 100 -> After 4 processes (+25 each): {shared_val.value}")


def main() -> None:
    demo_linux_commands()
    demo_process_creation_and_queue_ipc()
    demo_posix_and_mp_pipe_ipc()
    demo_threads_with_lock()
    demo_shared_memory_ipc()
    print("\n[DONE] All Process, Thread, and IPC demonstrations completed safely.")


if __name__ == "__main__":
    main()
