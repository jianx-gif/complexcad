import cadquery as cq
outer_radius = 35
inner_radius = 20
thickness = 30
wall_thickness = 2
chamfer_distance = 1
rib_width = 6
rib_height = 12
rib_thickness = 4
rib_spacing = 12
rib_count = 4
rib_count = 4
rib_count = 4
rib_count = 12
profile = (
    cq.Workplane("XZ")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, thickness)
    .lineTo(outer_radius, thickness)
    .lineTo(inner_radius, thickness)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_distance)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
rib_count = int((thickness - rib_width) // rib_count) + 1
rib_count = int((thickness - rib_width) // rib_count) + 1
rib_positions = [(-rib_count, 0), (rib_count, 0)]
solid = (
    solid.faces(">Z")
    .workplane()
    .pushPoints(rib_positions)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
solid = solid.union(rib_count)
solid = solid.edges("|Z").chamfer(chamfer_distance)
result = solid
