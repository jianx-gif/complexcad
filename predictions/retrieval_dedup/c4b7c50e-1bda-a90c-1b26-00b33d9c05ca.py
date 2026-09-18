import cadquery as cq

# Parameters
outer_width = 60.0
outer_height = 60.0
conduit_length = 100.0
wall_thickness = 1.5
hole_diameter = 5.0
hole_depth = 12.0
hole_spacing = 30.0
rib_height = 5.0
rib_thickness = 2.0
chamfer_distance = 0.75
notch_width = 20.0
notch_height = 5.0
notch_depth = 5.0

# Base conduit with thin walls
base = (
    cq.Workplane('XY')
    .rect(outer_width, outer_height)
    .extrude(conduit_length)
    .shell(-wall_thickness)
    # top entry notch
    .faces('>Z')
    .workplane()
    .center(0, outer_width/2 - 10)
    .rect(notch_width, notch_height)
    .cutBlind(notch_depth)
)
# Ribs on opposite side walls
left_rib = (
    base
    .faces('>Z')
    .workplane()
    .center(-outer_width/2 + wall_thickness + rib_thickness/2, 0)
    .rect(rib_thickness, rib_height)
    .extrude(rib_height)
)
right_rib = (
    base
    .faces('>Z')
    .workplane()
    .center(outer_width/2 - wall_thickness - rib_thickness/2, 0)
    .rect(rib_thickness, rib_height)
    .extrude(rib_height)
)
# Combine base and ribs
combined = base.union(left_rib).union(right_rib)
# Chamfer outer edges
chamfered = combined.edges('|Z').chamfer(chamfer_distance)
# Blind holes on bottom face
result = (
    chamfered
    .faces('<Z')
    .workplane()
    .pushPoints([
        (-hole_spacing/2, -hole_spacing/2),
        (hole_spacing/2, -hole_spacing/2),
        (-hole_spacing/2, hole_spacing/2),
        (hole_spacing/2, hole_spacing/2)
    ])
    .hole(hole_diameter, depth=hole_depth)
)
