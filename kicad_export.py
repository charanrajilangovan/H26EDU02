import json
import uuid
import os

# -----------------------------
# Load Layout
# -----------------------------
with open("output/layout.json", "r") as f:
    components = json.load(f)

# -----------------------------
# KiCad Header
# -----------------------------
kicad = []

kicad.append('(kicad_sch')
kicad.append('  (version 20231120)')
kicad.append('  (generator CircuitSketchAI)')

# -----------------------------
# Convert Components
# -----------------------------
for comp in components:

    name = comp["name"]

    x = comp["layout_x"]
    y = comp["layout_y"]

    uid = str(uuid.uuid4())

    if "resistor" in name.lower():
        lib = "Device:R"

    elif "battery" in name.lower():
        lib = "Device:Battery"

    elif "capacitor" in name.lower():
        lib = "Device:C"

    elif "inductor" in name.lower():
        lib = "Device:L"

    elif "ground" in name.lower():
        lib = "power:GND"

    elif "led" in name.lower():
        lib = "Device:LED"

    else:
        lib = "Device:Generic"

    kicad.append(f'''
  (symbol
    (lib_id "{lib}")
    (at {x/10:.1f} {y/10:.1f} 0)
    (uuid "{uid}")
  )
''')

kicad.append(")")

# -----------------------------
# Save
# -----------------------------
os.makedirs("output", exist_ok=True)

with open("output/project.kicad_sch", "w") as f:

    f.write("\n".join(kicad))

print("KiCad schematic exported!")
