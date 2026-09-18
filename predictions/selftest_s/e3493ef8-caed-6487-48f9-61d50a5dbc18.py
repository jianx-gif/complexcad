import cadquery as cq

# Dimensions (max 100 units)
outer_width = 80.0
outer_depth = 60.0
outer_height = 20.0
wall_thickness = 2.0
inner_width = outer_width - 2 * wall_thickness
inner_depth = outer_depth - 2 * wall_thickness
rib_width = 20.0
rib_depth = outer_depth - 2 * wall_thickness
rib_extra = 1.0
rib_height = outer_height + rib_extra
hole_diameter = 3.0
hole_offset = wall_thickness + 10.0
fillet_radius = 1.0
chamfer_distance = 0.5

result = (
    cq.Workplane('XY')
    # Outer block
    .rect(outer_width, outer_depth)
    .extrude(outer_height)
    # Inner cavity (creates reinforcement rim)
    .faces('>Z')
    .workplane(offset=-outer_height)
    .rect(inner_width, inner_depth)
    .cutBlind(-outer_height)
    # Central reinforcement rib extending slightly above top
    .faces('<Z')
    .workplane()
    .rect(rib_width, rib_depth)
    .extrude(rib_height)
    # Mounting holes on top surface, positioned near corners inside the rim
    .faces('>Z')
    .workplane()
    .pushPoints([
        (-outer_width/2 + hole_offset, -outer_depth/2 + hole_offset),
        ( outer_width/2 - hole_offset, -outer_depth/2 + hole_offset),
        (-outer_width/2 + hole_offset,  outer_depth/2 - hole_offset),
        ( outer_width/2 - hole_offset,  outer_depth/2 - hole_offset)
    ])
    .hole(hole_diameter)
    # Fillet all external vertical edges for durability
    .edges('|Z')
    .fillet(fillet_radius)
    # Chamfer top edge to break sharpness
    .edges('>Z')
    .chamfer(chamfer_distance)
)
