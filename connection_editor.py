import streamlit as st
import json
import os

st.set_page_config(page_title="Connection Editor", layout="wide")

st.title("🔗 CircuitSketch AI - Connection Editor")

# -----------------------------
# Load Layout
# -----------------------------
layout_file = "output/layout.json"

if not os.path.exists(layout_file):
    st.error("layout.json not found.")
    st.stop()

with open(layout_file, "r") as f:
    components = json.load(f)

# -----------------------------
# Component List
# -----------------------------
names = []

for i, comp in enumerate(components):
    names.append(f"{i} - {comp['name']}")

st.subheader("Create a Connection")

comp1 = st.selectbox(
    "From",
    names,
    key="from"
)

comp2 = st.selectbox(
    "To",
    names,
    key="to"
)

# -----------------------------
# Save Connections
# -----------------------------
connections_file = "output/connections.json"

if os.path.exists(connections_file):

    with open(connections_file, "r") as f:
        connections = json.load(f)

else:

    connections = []

if st.button("➕ Add Connection"):

    if comp1 != comp2:

        connection = {
            "from": comp1,
            "to": comp2
        }

        if connection not in connections:
            connections.append(connection)

            with open(connections_file, "w") as f:
                json.dump(connections, f, indent=4)

            st.success("Connection Added!")

        else:
            st.warning("Connection already exists.")

# -----------------------------
# Display Connections
# -----------------------------
st.subheader("Current Connections")

if len(connections) == 0:

    st.info("No connections yet.")

else:

    for c in connections:

        st.write(f"🔹 {c['from']}  ➜  {c['to']}")

# -----------------------------
# Delete Connections
# -----------------------------
st.subheader("Delete Connection")

if len(connections) > 0:

    delete_item = st.selectbox(
        "Select Connection",
        [f"{c['from']} -> {c['to']}" for c in connections]
    )

    if st.button("❌ Delete"):

        idx = [f"{c['from']} -> {c['to']}" for c in connections].index(delete_item)

        connections.pop(idx)

        with open(connections_file, "w") as f:
            json.dump(connections, f, indent=4)

        st.success("Deleted Successfully!")

        st.rerun()
