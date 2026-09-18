import cadquery as cq
outer_radius = 45.0
inner_radius = 20.0
total_height = 20.0
frame_thickness = 6.0
hex_flat_distance = 5.5
hex_depth = 2.5
hole_diameter = 5.5
hole_count = 8
hole_spacing = (hex_flat_distance + hex_flat_distance) / (hole_count - 1)
chamfer_dist = 0.8
pocket_width = 6.0
pocket_depth = 4.0
pocket_cut_depth = 3.0
pocket_depth = 3.0
outer_radius = outer_radius - frame_thickness
inner_radius = inner_radius
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, total_height - hex_depth)
    .lineTo(inner_radius, total_height - hex_depth)
    .lineTo(inner_radius, total_height)
    .lineTo(0, total_height)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_dist)
hex_cut = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(pocket_width, pocket_depth)
    .extrude(frame_thickness)
    .translate((0, 0, total_height - hex_depth))
)
solid = solid.cut(hex_cut)
solid = solid.edges().chamfer(chamfer_dist)
result = solid
