
import cadquery as cq

# Parameter definitions
base_radius = 15.0
top_radius = 12.0
cap_height = 60.0
wall_thickness = 2.0
chamfer_len = 1.5
washer_recess_dia = 20.0
washer_recess_depth = 5.0
groove_dia = 10.0
groove_depth = 2.0
flange_outer_radius = 22.0
flange_thickness = 4.0
slot_width = 3.0
slot_height = 12.0
slot_depth = wall_thickness + 1.0
mid_height = cap_height * 0.5

# Sweep path for outer solid (tapered)
offset = top_radius - base_radius  # negative for inward taper
path = (
    cq.Workplane("XZ")
    .lineTo(offset, cap_height)
    .wire()
)

# Profile: solid disc at base radius
profile = cq.Workplane("XY").circle(base_radius)

# Sweep to create solid cap
outer_cap = profile.sweep(path)

# Shell to create hollow interior
hollow_cap = outer_cap.shell(-wall_thickness)

# Add chamfer to tip edges
chamfered_cap = hollow_cap.faces(">Z").edges().chamfer(chamfer_len)

# Recessed pocket for washer (cut into interior near top)
washer_pocket = (
    chamfered_cap
    .faces(">Z")
    .workplane(invert=True)
    .center(0, 0)
    .circle(washer_recess_dia / 2)
    .cutBlind(washer_recess_depth)
)

# O-ring groove near bottom interior
groove = (
    washer_pocket
    .faces("<Z")
    .workplane(invert=True)
    .center(0, 0)
    .circle(groove_dia / 2)
    .cutBlind(groove_depth)
)

# External mounting flange at base
flange = (
    cq.Workplane("XY")
    .circle(flange_outer_radius)
    .extrude(flange_thickness)
)

# Position flange at bottom of cap (flush with Z=0)
flange = flange.translate((0, 0, -flange_thickness))

# Union flange with existing part
with_flange = groove.union(flange)

# Create slot cutter block
slot_cutter = (
    cq.Workplane("XY")
    .rect(slot_width, slot_height)
    .extrude(slot_depth)
)

# Place first slot cutter at side of cap
cutter1 = slot_cutter.translate((base_radius + slot_depth / 2, 0, mid_height))

# Cut first slot
part_after_slot1 = with_flange.cut(cutter1)

# Rotate cutter for opposite slot and cut
cutter2 = cutter1.rotate((0, 0, 0), (0, 0, 1), 180)
result = part_after_slot1.cut(cutter2)
