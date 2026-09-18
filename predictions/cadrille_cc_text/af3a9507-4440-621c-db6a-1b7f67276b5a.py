import cadquery as cq
conduit_length = 80.0
conduit_width = 30.0
conduit_height = 25.0
wall_thickness = 3.0
rib_width = 5.0
rib_thickness = 2.0
rib_spacing = 20.0
chamfer_depth = 1.5
fillet_radius = 1.0
profile = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (conduit_width, 0),
        (conduit_width, profile_height),
        (conduit_width - rib_thickness, profile_height),
        (conduit_width - rib_thickness, profile_height - rib_spacing),
        (0, profile_height),
    ])
    .close()
)
solid = profile.extrude(conduit_length)
solid = solid.edges("|Z").chamfer(chamfer_depth)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_thickness)
    .extrude(conduit_length)
)
solid = solid.union(rib)
solid = solid.edges("|Z").chamfer(chamfer_depth)
result = solid
