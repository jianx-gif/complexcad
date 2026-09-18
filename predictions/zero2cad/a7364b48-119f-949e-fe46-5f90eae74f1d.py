import cadquery as cq

# Parameters
bracket_length = 80.0
bracket_width = 50.0
bracket_thickness = 8.0
cutout_length = 40.0
cutout_width = 30.0
hole_diameter = 6.0
hole_spacing = 30.0
hole_offset_y = -15.0
fillet_radius = 2.0
chamfer_distance = 0.8
rib_height = 4.0
rib_thickness = 3.0
rib_spacing = 10.0

# Base plate
base = (
    cq.Workplane("XY")
    .rect(bracket_length, bracket_width)
    .extrude(bracket_thickness)
)

# Rectangular cutout through the plate
cutout = (
    cq.Workplane("XY")
    .rect(cutout_length, cutout_width)
    .extrude(bracket_thickness + 1)
)
base = base.cut(cutout)

# Chamfer outer top edges for safety
base = base.faces(">Z").edges().chamfer(chamfer_distance)

# Fillet inner corners of the cutout (edges on top face)
base = base.faces(">Z").edges().fillet(fillet_radius)

# Add two through holes on the top face
hole_positions = [(-hole_spacing/2, hole_offset_y), (hole_spacing/2, hole_offset_y)]
base = (
    base.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)

# Add ribs on the back face for stiffness
rib_count = int((bracket_width - 2 * rib_spacing) // (rib_thickness + rib_spacing))
for i in range(rib_count):
    y_pos = -bracket_width/2 + rib_spacing + i * (rib_thickness + rib_spacing) + rib_thickness/2
    rib = (
        cq.Workplane("XY")
        .center(0, y_pos)
        .rect(bracket_length - 2 * rib_spacing, rib_thickness)
        .extrude(rib_height)
    )
    base = base.union(rib)

result = base