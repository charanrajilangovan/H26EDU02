import json
import os


def build_connections(database):
    """
    Manually create electrical connections.
    """

    print("\n===== COMPONENTS =====\n")

    for comp in database:
        print(comp["id"], "(", comp["type"], ")")

    print("\nEnter connections.")
    print("Example: VS1 R1")
    print("Type 'done' to finish.\n")

    connections = []

    while True:

        entry = input("Connection : ")

        if entry.lower() == "done":
            break

        parts = entry.split()

        if len(parts) != 2:
            print("Invalid format. Example: VS1 R1")
            continue

        start = parts[0]
        end = parts[1]

        connections.append({
            "from": start,
            "to": end
        })

    os.makedirs("output", exist_ok=True)

    with open("output/connections.json", "w") as f:
        json.dump(connections, f, indent=4)

    return connections


# -------------------------
# Test
# -------------------------

if __name__ == "__main__":

    with open("output/component_database.json") as f:
        database = json.load(f)

    connections = build_connections(database)

    print("\nConnections Saved!\n")

    for c in connections:
        print(c)
