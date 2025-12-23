import os
import re
import opensim as osim

# -----------------------------
# EDIT THESE PATHS
# -----------------------------
MODEL_FILE   = "/app/output/scaled_model.osim"     # output from scaling
MARKER_TRC   = "/app/opensim/4.5/Models/Gait2392_Simbody/subject01_walk1.trc"             # your trial markers
IK_XML_IN    = "/app/opensim/4.5/Models/Gait2392_Simbody/subject01_Setup_IK.xml"
OUTPUT_DIR   = "/app/output/ik_walk01"

# Optional time range override (set to None to keep whatever is in XML)
TIME_RANGE = (0.0, 1.0)  # e.g., (start, end)

# -----------------------------
# Helpers
# -----------------------------
def must_exist(path: str):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File not found: {path}")

def replace_all_tags(xml_text: str, tag: str, value: str) -> str:
    pattern = rf"<{tag}>\s*.*?\s*</{tag}>"
    repl = f"<{tag}>{value}</{tag}>"
    if re.search(pattern, xml_text, flags=re.DOTALL):
        return re.sub(pattern, repl, xml_text, flags=re.DOTALL)
    raise RuntimeError(f"Tag <{tag}> not found in XML: {IK_XML_IN}")

# -----------------------------
# Main
# -----------------------------
os.makedirs(OUTPUT_DIR, exist_ok=True)

must_exist(MODEL_FILE)
must_exist(MARKER_TRC)
must_exist(IK_XML_IN)

# Run from OUTPUT_DIR so relative outputs land here
os.chdir(OUTPUT_DIR)

# For IK, absolute paths usually work fine, but if your build prefixes weirdly,
# switch to relative paths like we did for Scale:
model_path = os.path.abspath(MODEL_FILE)
marker_path = os.path.abspath(MARKER_TRC)

patched_xml = os.path.join(OUTPUT_DIR, "ik_setup_patched.xml")

with open(IK_XML_IN, "r", encoding="utf-8") as f:
    xml = f.read()

xml = replace_all_tags(xml, "model_file", model_path)
xml = replace_all_tags(xml, "marker_file", marker_path)

# Output in OUTPUT_DIR
xml = replace_all_tags(xml, "output_motion_file", "ik.mot")

if TIME_RANGE is not None:
    xml = replace_all_tags(xml, "time_range", f"{TIME_RANGE[0]} {TIME_RANGE[1]}")

with open(patched_xml, "w", encoding="utf-8") as f:
    f.write(xml)

print("[info] Loading InverseKinematicsTool with patched XML")
ik_tool = osim.InverseKinematicsTool(patched_xml)

print("[info] Running IK...")
ik_tool.run()

print("[info] Done.")
print("[info] IK motion:", os.path.join(OUTPUT_DIR, "ik.mot"))
