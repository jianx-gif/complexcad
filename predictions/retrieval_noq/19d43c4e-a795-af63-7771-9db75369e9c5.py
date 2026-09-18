import cadquery as cq

cover_length = 80
cover_width = 60
cover_thickness = 8
protrusion_height = 10
protrusion_diameter = 15
switch_hole_diameter = 8
chamfer_size = 1
rib_width = 3
rib_height = 2
rib_overlap = 0.5
mount_hole_diameter = 4
mount_hole_spacing = 30

# Base solid plate
result = (
    cq.Workplane("XY")
    .rect(cover_length, cover_width)
    .extrude(cover_thickness)
)
# Central protrusion
result = result.union(
    cq.Workplane("XY")
    .center(0, 0)
    .circle(protrusion_diameter/2)
    .extrude(protrusion_height)
)
# Switch clearance hole
result = result.cut(
    cq.Workplane("XY")
    .center(0, 0)
    .circle(switch_hole_diameter/2)
    .extrude(cover_thickness + protrusion_height + 2)
)
# Reinforcing ribs as separate solids intersecting base
rib_span = cover_width - 10
rib1 = (
    cq.Workplane("XY")
    .center(-cover_length/2 + 5, 0)
    .rect(rib_width, rib_span)
    .extrude(rib_height)
    .translate((0, 0, cover_thickness - rib_overlap))
)
rib2 = (
    cq.Workplane("XY")
    .center(cover_length/2 - 5, 0)
    .rect(rib_width, rib_span)
    .extrude(rib_height)
    .translate((0, 0, cover_thickness - rib_overlap))
)
result = result.union(rib1).union(rib2)
# Mounting holes pattern on the front face
result = (
    result
    .faces("<Y")
    .workplane()
    .center(0, 0)
    .rarray(mount_hole_spacing, 0, 2, 1)
    .circle(mount_hole_diameter/2)
    .cutBlind(-cover_thickness)
)
# Ensure single solid
result = result.combine()
# Chamfer top edges
result = result.faces(">Z").chamfer(chamfer_size)
