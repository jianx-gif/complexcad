import cadquery as cq
base_radius = 15.0
top_radius = 12.0
wall_thickness = 2.0
flange_outer_radius = 22.0
flange_thickness = 4.0
chamfer_len = 1.5
slot_width = 3.0
slot_height = 12.0
slot_depth = wall_thickness + 2.0
groove_dia = 20.0
groove_depth = 5.0
groove_recess_dia = 10.0
groove_recess_depth = 5.0
outer_radius = base_radius + top_radius
inner_radius = base_radius + top_radius
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(base_radius, 0)
    .lineTo(base_radius, base_radius)
    .lineTo(0, base_radius)
    .close()
)
solid = profile.revolve()
solid = solid.shell(-wall_thickness)
solid = solid.faces(">Z").edges().chamfer(chamfer_len)
slot = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(slot_width)
    .extrude(slot_height)
    .translate((0, 0, wall_thickness))
)
solid = solid.cut(slot)
solid = solid.edges().chamfer(chamfer_len)
solid = solid.faces(">Z").edges().chamfer(chamfer_len)
result = solid
