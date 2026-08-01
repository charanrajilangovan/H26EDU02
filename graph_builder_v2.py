import json
import math
import os

# ----------------------------
# Load Terminals
# ----------------------------
with open("output/terminals.json") as f:
    terminals = json.load(f)

connections = []

MAX_DISTANCE = 70

# ----------------------------
# Compare Every Component
# ----------------------------
for i in range(len(terminals)):

    for j in range(i + 1, len(terminals)):

        comp1 = terminals[i]
        comp2 = terminals[j]

        for p1 in comp1["pins"]:

            for p2 in comp2["pins"]:

                d = math.sqrt(
                    (p1[0]-p2[0])**2 +
                    (p1[1]-p2[1])**2
                )

                if d < MAX_DISTANCE:

                    connections.append({

                        "from": comp1["name"],

                        "to": comp2["name"],

                        "distance": round(d,2)

                    })

# ----------------------------
# Remove Duplicate
# ----------------------------
unique = []

seen = set()

for c in connections:

    key = tuple(sorted((c["from"], c["to"])))

    if key not in seen:

        seen.add(key)

        unique.append(c)

# ----------------------------
# Save
# ----------------------------
os.makedirs("output",exist_ok=True)

with open(
    "output/connections.json",
    "w"
) as f:

    json.dump(unique,f,indent=4)

print()

print("Connections Found :",len(unique))

print()

for c in unique:

    print(
        c["from"],
        " --> ",
        c["to"]
    )
