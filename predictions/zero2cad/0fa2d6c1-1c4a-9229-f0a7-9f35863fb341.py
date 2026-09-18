import cadquery as cq

outer_radius = 45.0
inner_radius = 30.0
height = 60.0
wall_thickness = outer_radius - inner_radius
vent_width = 12.0
vent_height = 20.0
vent_depth = wall_thickness + 2.0
vent_center_z = height / 2.0
chamfer_size = 1.0

profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .threePointArc((outer_radius + 5, height / 2), (outer_radius, height))
    .lineTo(inner_radius, height)
    .threePointArc((inner_radius - 5, height / 2), (inner_radius, 0))
    .close()
)

shell = profile.revolve()

vent_cut = (
    cq.Workplane("XY")
    .box(vent_depth, vent_width, vent_height)
    .translate((outer_radius - vent_depth / 2, 0, vent_center_z))
)

result = (
    shell
    .cut(vent_cut)
    .edges("|Z")
    .chamfer(chamfer_size)
)
