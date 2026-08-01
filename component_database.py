import json
import os

def create_component_database(components):
    """
    Convert YOLO detections into a standard component database.
    """

    database = []

    counters = {
        "battery": 1,
        "resistor": 1,
        "capacitor": 1,
        "inductor": 1,
        "diode": 1,
        "led": 1,
        "ground": 1,
        "ammeter": 1,
        "voltmeter": 1,
        "supplyvoltage": 1
    }

    for comp in components:

        ctype = comp["name"].lower()

        # Remove spaces
        ctype = ctype.replace(" ", "")

        # If new component type
        if ctype not in counters:
            counters[ctype] = 1

        # Create ID
        if ctype == "resistor":
            cid = f"R{counters[ctype]}"

        elif ctype == "capacitor":
            cid = f"C{counters[ctype]}"

        elif ctype == "inductor":
            cid = f"L{counters[ctype]}"

        elif ctype == "battery":
            cid = f"B{counters[ctype]}"

        elif ctype == "ground":
            cid = f"GND{counters[ctype]}"

        elif ctype == "led":
            cid = f"LED{counters[ctype]}"

        elif ctype == "diode":
            cid = f"D{counters[ctype]}"

        elif ctype == "ammeter":
            cid = f"A{counters[ctype]}"

        elif ctype == "voltmeter":
            cid = f"V{counters[ctype]}"

        elif ctype == "supplyvoltage":
            cid = f"VS{counters[ctype]}"

        else:
            cid = f"{ctype.upper()}{counters[ctype]}"

        counters[ctype] += 1

        database.append({

            "id": cid,

            "type": ctype,

            "x": comp["x"],

            "y": comp["y"],

            "confidence": comp["confidence"]

        })

    os.makedirs("output", exist_ok=True)

    with open("output/component_database.json", "w") as f:

        json.dump(database, f, indent=4)

    return database


# ----------------------------
# Test
# ----------------------------

if __name__ == "__main__":

    with open("output/components.json") as f:

        components = json.load(f)

    db = create_component_database(components)

    print("\nComponent Database\n")

    for item in db:

        print(item)
