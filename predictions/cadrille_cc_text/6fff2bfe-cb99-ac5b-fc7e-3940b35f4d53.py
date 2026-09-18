import cadquery as cq
base_outer_radius = 30.0
base_inner_radius = 20.0
wall_thickness = 2.0
notch_width = 8.0
notch_height = 10.0
notch_depth = 2.0
notch_start_radius = (base_outer_radius - wall_thickness) / 2.0
notch_end_radius = 15.0
vent_hole_radius = 2.0
vent_hole_count = 6
vent_hole_radius = 3.0
chamfer_size = 1.0
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(base_outer_radius, 0)
    .lineTo(base_outer_radius, height)
    .lineTo(base_outer_radius + wall_thickness, height)
    .lineTo(base_outer_radius + wall_thickness, 0)
    .lineTo(base_outer_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.shell(-wall_thickness)
vent_hole = (
    cq.Workplane("XY")
    .circle(vent_hole_radius)
    .extrude(vent_hole_radius * 2.0)
    .translate((0, 0, wall_thickness))
)
solid = solid.cut(vent_hole)
solid = solid.faces(">Z").edges().chamfer(chamfer_size)
result = solid
