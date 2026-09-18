import cadquery as cq

outer_radius = 80.0
outer_radius = 30.0
wall_thickness = 1.0
wall_thickness = 2.0
chamfer_distance = 1.0
hole_diameter = 10.0
hole_spacing = 12.0
hole_spacing = 12.0
hole_count = 15
hole_count = 15
hole_count = 15
hole_count = 15
hole_count = 15
hole_count = 15
hole_count = 15
hole_count = 20
hole_count = 20
hole_count = 15
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
    cq.Workplane('XY')
    .rect(outer_length, outer_height)
    .extrude(outer_height)
    .faces('>Z')
    .workplane()
    .rect(outer_length - 2*hole_offset, 0)
    .extrude(outer_height)
    .faces(">Z')
    .workplane()
    .rect(outer_length - 2 * hole_spacing, hole_spacing)
    .cutBlind(-hole_offset)
    .faces(">Z')
    .workplane()
    .rect(outer_length - 2 * hole_count, hole_offset)
    .cutBlind(-hole_offset)
    .faces(">Z')
    .workplane()
    .rect(outer_length - 2 * hole_count, hole_offset)
    .cutBlind(-hole_offset)
    .faces(">Z')
    .workplane()
    .rarray(hole_spacing, hole_offset, hole_count, hole_offset)
    .hole(hole_diameter)
)
