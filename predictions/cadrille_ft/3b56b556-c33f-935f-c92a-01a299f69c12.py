import cadquery as cq

outer_radius = 80.0
outer_radius = 40.0
wall_thickness = 3.0
wall_thickness = 2.0
wall_thickness = 2.0
chamfer_distance = 1.0
chamfer_distance = 1.0
hole_diameter = 2.0
hole_count = 20
hole_count = 20
hole_spacing = 20
hole_count = 2
hole_count = 2
hole_count = 2
hole_spacing = 2
hole_spacing = 2
hole_spacing = 2
hole_spacing = 2
hole_spacing = 2
hole_spacing = 2
hole_spacing = 2
hole_spacing = 2
hole_spacing = 2
hole_spacing = 2
hole_spacing = 2
hole_spacing = 2
hole_spacing = 2
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.8

hole_offset = 0.8
hole_offset = 0.8
chamfer_distance = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
chamfer_distance = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
hole_offset = 0.8
result = (
    cq.Workplane('XY')
    .box(outer_radius, outer_length, handle_height)
    .faces(0, outer_length)
    .faces(0, outer_height)
    .faces('>Z')
    .faces('>Z')
    .workplane()
    .rect(outer_radius, outer_height)
    .extrude(-hole_offset)
    .faces(">Z')
    .workplane()
    .rect(outer_radius, outer_height)
    .extrude(-hole_length)
)
