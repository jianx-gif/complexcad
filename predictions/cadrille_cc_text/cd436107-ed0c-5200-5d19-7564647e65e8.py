import cadquery as cq
horizontal_length = 80.0
vertical_length = horizontal_length
thickness = 10.0
inner_fillet_radius = 6.0
through_hole_diameter = 8.0
mount_hole_diameter = 5.0
mount_hole_pattern_spacing = 30.0
rib_width = 15.0
rib_height = 30.0
rib_count = 4
rib_start_z = vertical_length - 2 * rib_width
rib_end_z = vertical_length - 2 * rib_width
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (horizontal_length, 0),
        (horizontal_length, vertical_length),
        (0, vertical_length),
        (0, 0)
    ])
    .close()
    .extrude(thickness)
)
base = base.edges("|Z").fillet(inner_fillet_radius)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(through_hole_diameter)
)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_end_z)
)
base = base.union(rib)
base = base.edges("|Z").fillet(rib_end_z)
result = base
