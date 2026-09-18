
import cadquery as cq

# Parameters
total_length = 80.0
base_width = 20.0
plate_thickness = 10.0
fillet_radius = base_width / 2.0
hole_diameter = 5.0
hole_offset_from_tip = 15.0
rib_count = 3
rib_width = 5.0
rib_extra_height = 6.0
rib_clearance = 2.0
pocket_length = 30.0
pocket_width = 12.0
pocket_depth = 4.0
chamfer_distance = 1.0

# Base rectangular portion (leaving space for fillet tip)
rect_length = total_length - fillet_radius
base_plate = (
    cq.Workplane("XY")
    .box(rect_length, base_width, plate_thickness, centered=(False, False, False))
)

# Filleted tip created by a half‑cylinder (cylinder intersected with plate)
fillet_tip = (
    cq.Workplane("XY")
    .center(rect_length, base_width / 2.0)
    .cylinder(plate_thickness, fillet_radius, centered=(True, True, False))
)

# Combine base and tip
lever_body = base_plate.union(fillet_tip)

# Through hole for bolt (placed relative to tip)
hole_center_x = total_length - hole_offset_from_tip
lever_body = (
    lever_body
    .faces(">Z")
    .workplane()
    .center(hole_center_x, base_width / 2.0)
    .hole(hole_diameter)
)

# Ribs for stiffness (arrayed along length on top face)
rib_pitch = (total_length - fillet_radius - rib_width) / (rib_count + 1)
lever_body = (
    lever_body
    .faces(">Z")
    .workplane()
    .rarray(rib_pitch, 0, rib_count, 1)
    .rect(rib_width, base_width - 2 * rib_clearance)
    .extrude(rib_extra_height)
)

# Central pocket for weight reduction (cut from top surface)
pocket_center_x = (total_length - fillet_radius) / 2.0
lever_body = (
    lever_body
    .faces(">Z")
    .workplane()
    .center(pocket_center_x, base_width / 2.0)
    .rect(pocket_width, pocket_length)
    .cutBlind(-pocket_depth)
)

# Chamfer outer vertical edges for safety
lever_body = (
    lever_body
    .edges("|Z")
    .chamfer(chamfer_distance)
)

result = lever_body
