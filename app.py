import streamlit as st
from PIL import Image
import os
import json
from ultralytics import YOLO

from detector import detect_components
from component_database import create_component_database

# -----------------------------------
# Streamlit Configuration
# -----------------------------------

st.set_page_config(
    page_title="CircuitSketch AI",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ CircuitSketch AI")
st.write("### Hand Drawn Circuit to Digital Schematic")

model = YOLO("best.pt")

uploaded = st.file_uploader(
    "Upload Circuit",
    type=["jpg","jpeg","png"]
)

if uploaded:

    image = Image.open(uploaded).convert("RGB")

    os.makedirs("temp",exist_ok=True)

    image_path = os.path.join(
        "temp",
        uploaded.name
    )

    image.save(image_path)

    # -----------------------------------
    # YOLO Detection
    # -----------------------------------

    with st.spinner("Detecting Components..."):

        results = model.predict(
            image_path,
            conf=0.40,
            save=False
        )

        annotated = results[0].plot()

        components = detect_components(image_path)

    create_component_database(components)

    # -----------------------------------
    # Layout
    # -----------------------------------

    col1,col2 = st.columns(2)

    with col1:

        st.subheader("Original Image")

        st.image(
            image,
            use_container_width=True
        )

    with col2:

        st.subheader("Detected Components")

        st.image(
            annotated,
            channels="BGR",
            use_container_width=True
        )

    st.divider()

    # -----------------------------------
    # Component List
    # -----------------------------------

    st.subheader("Detected Components")

    for c in components:

        st.success(
            f"{c['name']} ({c['confidence']:.2f})"
        )

    st.divider()

    # -----------------------------------
    # Wire Extraction
    # -----------------------------------

    st.subheader("Wire Extraction")

    if os.path.exists("output/wires_binary.png"):

        st.image(
            "output/wires_binary.png",
            use_container_width=True
        )

    else:

        st.warning("Run wire_analyzer.py")

    st.divider()

    # -----------------------------------
    # Terminal Detection
    # -----------------------------------

    st.subheader("Terminal Detection")

    if os.path.exists("output/terminals.png"):

        st.image(
            "output/terminals.png",
            use_container_width=True
        )

    else:

        st.warning("Run terminal_detector.py")

    st.divider()

    # -----------------------------------
    # Component Database
    # -----------------------------------

    st.subheader("Component Database")

    if os.path.exists("output/component_database.json"):

        with open("output/component_database.json") as f:

            db = json.load(f)

        st.json(db)

    st.divider()

    # -----------------------------------
    # Schematic
    # -----------------------------------

    st.subheader("Generated Schematic")

    if os.path.exists("output/final_schematic.png"):

        st.image(
            "output/final_schematic.png",
            use_container_width=True
        )

        with open(
            "output/final_schematic.png",
            "rb"
        ) as file:

            st.download_button(
                "Download Schematic",
                file,
                file_name="schematic.png"
            )

    else:

        st.warning("Schematic not generated")

    st.divider()

    # -----------------------------------
    # Connections
    # -----------------------------------

    st.subheader("Connections")

    if os.path.exists("output/connections.json"):

        with open("output/connections.json") as f:

            conn = json.load(f)

        st.json(conn)

    else:

        st.info("Connections not generated yet")

    st.divider()

    # -----------------------------------
    # Export
    # -----------------------------------

    st.subheader("KiCad Export")

    if st.button("Generate KiCad"):

        st.info("Coming in Version 2")
