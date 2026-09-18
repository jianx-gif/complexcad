import cadquery as cq

# Parameters
outer_radius = 30.0
inner_radius = 10.0
block_height = 40.0
arc_control_offset = 5.0
chamfer_distance = 2.0
hole_diameter = 5.0
hole_depth = 15.0
hole_count = 6
hole_radius = outer_radius - 5.0

# Base profile for revolve (non‑trivial composite shape)
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, block_height)
    .threePointArc((outer_radius - arc_control_offset, block_height + arc_control_offset), (inner_radius, block_height))
    .lineTo(inner_radius, 0)
    .close()
)

# Revolve to create the arc block
solid = profile.revolve()

# Central through hole (cylindrical cut)
central_hole = cq.Workplane("XY").circle(inner_radius).extrude(block_height * 2)
solid = solid.cut(central_hole)

# Chamfer on the outer rim (top edge)
solid = solid.edges("|Z").chamfer(chamfer_distance)

# Patterned blind holes on the top face
result = (
    solid
    .faces(">Z")
    .workplane()
    .polarArray(radius=hole_radius, startAngle=0, angle=360, count=hole_count)
    .hole(hole_diameter, depth=hole_depth)
)
