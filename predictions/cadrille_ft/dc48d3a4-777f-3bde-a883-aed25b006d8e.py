import cadquery as cq

outer_radius = 80.0
outer_radius = 30.0
wall_thickness = 40.0
wall_thickness = 5.0
wall_thickness = 3.0
hole_diameter = 4.0
hole_spacing = 20.0
hole_spacing = 20.0
chamfer_distance = 1.0
hole_depth = 15.0
hole_depth = 5.0
hole_depth = 1.0
chamfer_distance = 0.5

hole_count = 1.0

hole_count = 15
hole_spacing = 1.0

hole_spacing = 2.0

hole_spacing = 20.0
hole_spacing = 20.0
hole_spacing = 20.0
hole_spacing = 20.0
hole_spacing = 20.0
hole_spacing = 20.0
hole_spacing = 20.0
hole_spacing = 20.0
hole_offset = 0.5

hole_offset = 0.5

result = (
    cq.Workplane('XY')
    .box(outer_radius, outer_length, outer_height)
    .faces('>Z')
    .faces('>Z')
    .faces(">Z')
    .faces(">Z')
    .faces(">Z')
    .workplane()
    .rect(outer_radius, outer_height)
    .extrude(outer_height)
    .faces(">Z')
    .workplane()
    .rect(outer_radius, outer_height)
    .extrude(outer_height)
    .faces(">Z')
    .workplane()
    .rect(outer_radius, outer_height)
    .extrude(outer_height)
    .faces(">Z')
    .workplane()
    .rect(outer_radius, outer_height)
    .extrude(outer_height)
    .translate((outer_radius - 2 * wall_thickness, 0, 0))
    .cutBlind(-outer_radius)
)
