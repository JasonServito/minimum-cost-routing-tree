import json
import sys

# Shared 7-node graph: node -> list of (neighbor, link cost)
LINKS = {
    1: [(2, 2), (3, 5)],
    2: [(1, 2), (3, 6), (4, 4), (5, 5)],
    3: [(1, 5), (2, 6), (5, 2), (6, 2), (7, 5)],
    4: [(2, 4), (5, 5), (7, 4)],
    5: [(2, 5), (3, 2), (4, 5), (7, 2)],
    6: [(3, 2), (7, 5)],
    7: [(3, 5), (4, 4), (5, 2), (6, 5)],
}

# Role assignments to test: S = Source, F = Forwarder, R = Receiver
TOPOLOGIES = {
    1: {1: "S", 2: "F", 3: "F", 4: "R", 5: "F", 6: "R", 7: "R"},
    2: {1: "R", 2: "R", 3: "F", 4: "F", 5: "F", 6: "F", 7: "S"},
    3: {1: "F", 2: "R", 3: "S", 4: "R", 5: "F", 6: "F", 7: "R"},
}

BASE_PORT = 65000


def generate(topology_id):
    roles = TOPOLOGIES[topology_id]
    for node_id, neighbors in LINKS.items():
        config = {
            "id": node_id,
            "role": roles[node_id],
            "port": BASE_PORT + node_id,
            "neighbors": [{"id": n, "port": BASE_PORT + n, "cost": cost} for n, cost in neighbors]
        }
        with open(f"config{node_id}.json", "w") as f:
            json.dump(config, f, indent=4)
    print(f"Generated topology {topology_id} into config1.json through config7.json")


if __name__ == "__main__":
    topology_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    if topology_id not in TOPOLOGIES:
        sys.exit(f"Unknown topology {topology_id}; choose one of {sorted(TOPOLOGIES)}")
    generate(topology_id)
