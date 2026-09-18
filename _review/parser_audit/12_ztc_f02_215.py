import cadquery as cq

# Parameters
length_base = 80.0
width_base = 60.0
thickness_base = 8.0
rib_length = 40.0
rib_height = 30.0
rib_thickness = 6.0
rib_offset = 10.0
gusset_length = 50.0
gusset_height = 35.0
gusset_thickness = 6.0
gusset_offset = 5.0
clearance_hole_diameter = 10.0
clearance_hole_offset_x = 0.0
clearance_hole_offset_y = 0.0
chamfer_size = 1.5

# Base plate
base = (
    cq.Workplane("XY")
    .rect(length_base, width_base)
    .extrude(thickness_base)
)

# Diagonal rib (triangular prism) on top face
rib = (
    base.faces(">Z").workplane()
    .center(-length_base/2 + rib_offset, 0)
    .polyline([(0, 0), (rib_length, 0), (0, rib_height)])
    .close()
    .extrude(rib_thickness)
)

# Welded gusset (larger triangular prism) on top face, adjacent to rib
gusset = (
    base.faces(">Z").workplane()
    .center(-length_base/2 + gusset_offset, 0)
    .polyline([(0, 0), (gusset_length, 0), (0, gusset_height)])
    .close()
    .extrude(gusset_thickness)
)

# Clearance hole through base plate
hole = (
    base.faces("<Z").workplane()
    .center(clearance_hole_offset_x, clearance_hole_offset_y)
    .hole(clearance_hole_diameter)
)

# Combine parts and apply chamfers
result = (
    base.union(rib).union(gusset).cut(hole)
    .edges("|Z")
    .chamfer(chamfer_size)
)
