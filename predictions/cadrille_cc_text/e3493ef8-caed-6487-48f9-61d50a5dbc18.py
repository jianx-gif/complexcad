import cadquery as cq
outer_width = 80.0
outer_depth = 60.0
outer_height = 20.0
wall_thickness = 2.0
hole_diameter = 3.0
fillet_radius = 1.0
chamfer_distance = 0.5
rib_width = 20.0
rib_height = outer_height - 2 * wall_thickness
rib_length = outer_width - 2 * wall_thickness
hole_spacing = (outer_width - 2 * wall_thickness - 1) * hole_spacing
hole_positions = [(hole_spacing, 0), (hole_spacing, 0)]
result = (
    cq.Workplane("XY")
    .rect(outer_width, outer_depth)
    .extrude(outer_height)
    .edges("|Z")
    .fillet(fillet_radius)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_length, rib_width)
    .extrude(rib_height)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_length, rib_width)
    .extrude(rib_height)
    .edges("|Z")
    .chamfer(chamfer_distance)
)
