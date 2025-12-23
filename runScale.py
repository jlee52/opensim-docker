import os
import re
import opensim as osim

SUBJECT_NAME = "subject01"

MODEL_FILE   = "/app/opensim/4.5/Models/Gait2392_Simbody/gait2392_simbody.osim"
STATIC_TRC   = "/app/opensim/4.5/Models/Gait2392_Simbody/subject01_static.trc"
SCALE_XML_IN = "/app/opensim/4.5/Models/Gait2392_Simbody/subject01_Setup_Scale.xml"
OUTPUT_DIR   = "/app/output"

MARKER_SET_FILE = "/app/opensim/4.5/Models/Gait2392_Simbody/gait2392_Scale_MarkerSet.xml"

def must_exist(path: str):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File not found: {path}")

def replace_all_tags(xml_text: str, tag: str, value: str) -> str:
    pattern = rf"<{tag}>\s*.*?\s*</{tag}>"
    repl = f"<{tag}>{value}</{tag}>"
    if re.search(pattern, xml_text, flags=re.DOTALL):
        return re.sub(pattern, repl, xml_text, flags=re.DOTALL)
    raise RuntimeError(f"Tag <{tag}> not found in XML: {SCALE_XML_IN}")

print(f"[info] Processing subject {SUBJECT_NAME}...")
os.makedirs(OUTPUT_DIR, exist_ok=True)

must_exist(MODEL_FILE)
must_exist(STATIC_TRC)
must_exist(SCALE_XML_IN)
must_exist(MARKER_SET_FILE)

# Run tool from OUTPUT_DIR
os.chdir(OUTPUT_DIR)

# Compute marker path RELATIVE to OUTPUT_DIR (prevents /app/output//app/... bug)
marker_file_rel = os.path.relpath(STATIC_TRC, start=OUTPUT_DIR)  # ex: ../static/subject01_static.trc

patched_xml = os.path.join(OUTPUT_DIR, "scale_setup_patched.xml")
out_model_name = "scaled_model.osim"

with open(SCALE_XML_IN, "r", encoding="utf-8") as f:
    xml = f.read()

xml = replace_all_tags(xml, "model_file", os.path.abspath(MODEL_FILE))
xml = replace_all_tags(xml, "marker_set_file", os.path.abspath(MARKER_SET_FILE))

# Critical: marker_file must be RELATIVE here for your OpenSim build
xml = replace_all_tags(xml, "marker_file", marker_file_rel)

# Output into OUTPUT_DIR by using filename only
xml = replace_all_tags(xml, "output_model_file", out_model_name)

with open(patched_xml, "w", encoding="utf-8") as f:
    f.write(xml)

print("[info] Loading ScaleTool with patched XML")
scale_tool = osim.ScaleTool(patched_xml)

print("[info] Running OpenSim Scale Tool...")
scale_tool.run()

print("[info] ScaleTool finished.")
print(f"[info] Scaled model: {os.path.join(OUTPUT_DIR, out_model_name)}")
