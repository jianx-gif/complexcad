import cadquery as cq

# Parameters
total_length = 80.0
base_width = 40.0
top_width = 15.0
height = 20.0
wall_thickness = 3.0
fillet_radius = 1.0
pocket_width = 20.0
pocket_length = 30.0
pocket_depth = 5.0
hole_diameter = 5.0
hole_spacing = 25.0

# Outer lofted body
outer = (
    cq.Workplane("XY")
    .rect(base_width, height)
    .workplane(offset=total_length)
    .rect(top_width, height)
    .loft()
)

# Fillet outer edges before internal cut
outer = outer.edges().fillet(fillet_radius)

# Inner lofted cavity
inner = (
    cq.Workplane("XY")
    .rect(base_width - 2 * wall_thickness, height - 2 * wall_thickness)
    .workplane(offset=total_length)
    .rect(top_width - 2 * wall_thickness, height - 2 * wall_thickness)
    .loft()
)

# Subtract inner cavity
result = outer.cut(inner)

# Recessed pocket on top face
result = (
    result.faces(">Z")
    .workplane()
    .rect(pocket_width, pocket_length)
    .cutBlind(-pocket_depth)
)

# Mounting holes on side faces
result = (
    result.faces("<X")
    .workplane()
    .pushPoints([(-hole_spacing / 2, total_length / 2), (hole_spacing / 2, total_length / 2)])
    .hole(hole_diameter)
)
