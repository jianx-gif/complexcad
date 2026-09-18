import cadquery as cq

# Parameters
clip_length = 80.0
clip_width = 30.0
clip_thickness = 2.0
tab_width = 12.0
tab_height = 15.0
tab_offset = 5.0
slot_width = 6.0
slot_length = 20.0
slot_offset = 10.0
hole_diameter = 4.0
hole_spacing = 20.0
hole_offset = 15.0
fillet_radius = 1.5
chamfer_distance = 0.8

# Base plate
base = (
    cq.Workplane("XY")
    .rect(clip_length, clip_width)
    .extrude(clip_thickness)
)

# Tab protrusion
tab = (
    cq.Workplane("XY")
    .center(-clip_length/2 + tab_offset, 0)
    .rect(tab_width, tab_height)
    .extrude(clip_thickness)
)

# Combine base and tab
combined = base.union(tab)

# Slot cutout
slot = (
    cq.Workplane("XY")
    .center(-clip_length/2 + slot_offset, 0)
    .rect(slot_width, slot_length)
    .extrude(clip_thickness + 0.1)
)
combined = combined.cut(slot)

# Mounting holes (two holes)
hole1 = (
    cq.Workplane("XY")
    .center(-clip_length/2 + hole_offset, -hole_spacing/2)
    .circle(hole_diameter/2)
    .extrude(clip_thickness + 0.1)
)
hole2 = (
    cq.Workplane("XY")
    .center(-clip_length/2 + hole_offset, hole_spacing/2)
    .circle(hole_diameter/2)
    .extrude(clip_thickness + 0.1)
)
combined = combined.cut(hole1).cut(hole2)

# Fillet outer vertical edges
combined = combined.edges("|Z").fillet(fillet_radius)

# Chamfer top edges for safety
combined = combined.edges(">Z").chamfer(chamfer_distance)

result = combined