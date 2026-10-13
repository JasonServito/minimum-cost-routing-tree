import subprocess
import sys
import threading
import time

from generate_topology import TOPOLOGIES, generate

NODE_IDS = range(1, 8)
RUN_SECONDS = 15  # long enough for ANNOUNCE, JOIN, and DATA phases to finish


def stream_output(proc):
    # Relay each node's output to this terminal as it arrives
    for line in proc.stdout:
        print(line, end="", flush=True)


def main():
    topology_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    if topology_id not in TOPOLOGIES:
        sys.exit(f"Unknown topology {topology_id}; choose one of {sorted(TOPOLOGIES)}")
    generate(topology_id)

    # Start all 7 nodes; -u keeps their output unbuffered so lines appear in order
    procs = [
        subprocess.Popen([sys.executable, "-u", "node.py", f"config{n}.json"],
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for n in NODE_IDS
    ]
    for proc in procs:
        threading.Thread(target=stream_output, args=(proc,), daemon=True).start()

    try:
        time.sleep(RUN_SECONDS)
    except KeyboardInterrupt:
        pass
    finally:
        for proc in procs:
            proc.terminate()
        for proc in procs:
            proc.wait()
        print(f"\nStopped all nodes (topology {topology_id}).")


if __name__ == "__main__":
    main()
