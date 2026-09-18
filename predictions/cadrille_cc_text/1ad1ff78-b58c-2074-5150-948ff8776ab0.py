import cadquery as cq
outer_length = 80.0
outer_width = 50.0
outer_height = 20.0
wall_thickness = 2.0
rib_width = 4.0
rib_height = 3.0
rib_spacing = 10.0
fillet_radius = 2.0
chamfer_distance = 0.5
hole_diameter = 3.0
hole_offset_y = 12.0
hole_offset_x = 30.0
hole_offset_y = wall_thickness + rib_spacing
base = (
    cq.Workplane("XY")
    .box(outer_length, outer_width, outer_height, centered=(True, True, False))
    .faces(">Z")
    .shell(-wall_thickness)
    .faces(">Z")
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_height)
    .faces(">Z")
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_height)
    .faces(">Z")
    .workplane()
    .pushPoints(hole_offset_x, hole_offset_y)
    .hole(hole_diameter)
)
rib = (
    cq.Workplane("XY")
    .box(outer_length - 2 * wall_thickness, outer_width - 2 * wall_thickness, rib_height)
    .translate((0, 0, wall_thickness))
)
result = base.union(rib)
result = result.edges("|Z").fillet(fillet_radius)
result = result.edges("|Z").chamfer(chamfer_distance)
