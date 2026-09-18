import cadquery as cq

# Parameters
outer_diameter = 80.0
flange_thickness = 10.0
rib_width = 6.0
rib_height = 15.0
rib_length = 60.0
rib_angle = 30.0
hole_diameter = 4.0
hole_spacing = 20.0
hole_rows = 3
hole_cols = 3
chamfer_distance = 2.0
countersink_diameter = 8.0
countersink_depth = 2.0

# Base flange with outer chamfer
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(flange_thickness)
    .edges()
    .chamfer(chamfer_distance)
)

# Diagonal rib on back face
rib = (
    base.faces("<Z")
    .workplane()
    .center(-rib_length / 2, 0)
    .rect(rib_length, rib_width)
    .extrude(rib_height, taper=rib_angle)
)

# Combine base and rib
combined = base.union(rib)

# Pattern of nine through holes on front face
holes = (
    combined.faces(">Z")
    .workplane()
    .rarray(hole_spacing, hole_spacing, hole_cols, hole_rows, center=True)
    .hole(hole_diameter)
)

# Countersink on central hole
result = (
    holes.faces(">Z")
    .workplane()
    .center(0, 0)
    .cskHole(countersink_diameter, countersink_depth, hole_diameter)
)
