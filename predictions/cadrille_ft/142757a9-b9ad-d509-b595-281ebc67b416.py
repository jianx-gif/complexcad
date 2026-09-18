import cadquery as cq
outer_diameter = 80.0
outer_diameter = 40.0
wall_thickness = 3.0
wall_thickness = 2.0
wall_thickness = 4.0
wall_thickness = 5.0
wall_thickness = 2.0
chamfer_distance = 2.0
hole_diameter = 4.0
hole_count = 2
hole_count = 30
hole_count = 2
hole_count = 2
hole_count = 2
hole_count = 2
hole_count = 2
hole_count = 2
hole_count = 2
hole_count = 2
hole_count = 2
hole_count = 2
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
result = (
    result = (
    result.faces(">Z").workplane(' (hole_offset, 0)
    .rect(outer_length, outer_length)
    .extrude(-wall_thickness)
    .faces(0, outer)
    .extrude(-wall_thickness)
)

result = (
    result.faces(">Z").workplane()
    .rect(outer_width, outer_height)
    .extrude(-wall_thickness)
    .faces(0, outer)
    .extrude(-wall_thickness)
    .faces(0, outer)
    .faces('>Z')
    .workplane()
    .rect(outer_width, outer_height)
    .extrude(-wall_thickness)
)
