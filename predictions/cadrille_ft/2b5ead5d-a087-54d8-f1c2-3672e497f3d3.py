import cadquery as cq
outer_radius = 80.0
outer_radius = 30.0
wall_thickness = 40.0
wall_thickness = 2.0
wall_thickness = 4.0
wall_thickness = 4.0
wall_thickness = 1.0
wall_thickness = 2.0
chamfer_distance = 2.0
hole_count = 2.0
hole_spacing = 2.0
hole_count = 2.0
hole_count = 2.0
hole_count = 2.0
hole_count = 2.0
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5
hole_offset = cq.Workplane('XY')
        .box(outer_radius, outer_length, outer_height)
    .faces(0, outer_height)
    .faces(0, outer_height)
    .faces('>Z')
    .workplane()
    .rect(outer_radius, outer_height)
    .extrude(-outer_height)
    .faces(">Z')
    .workplane()
    .rect(outer_radius, outer_height)
    .extrude(-outer_height)
    .faces(">Z')
    .workplane()
    .rect(outer_radius, outer_height)
    .extrude(-outer_height)
    .translate((0, 0, 0), (0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, -hole_spacing))
    .translate((0, 0, -hole_offset), (0, 0, -hole_offset), (0, 0, -hole_offset), (0, -hole_offset), (0, -hole_offset), (0, -hole_offset), (0, -hole_offset), (0, -hole_offset), (0, -hole_offset), (0, -hole_offset), (0, -hole_offset), (0, -hole_offset), (0, -hole_offset), (0, -hole_offset), (0, -hole(offset=(0, -hole_offset), (0, -hole(offset=(0, -hole_offset),(-hole(offset=(0, -hole(offset=(0, -hole_offset),(-hole(offset=(0, -hole_offset),(-hole(offset=(0, -hole_offset),(-hole(offset=(0, -hole(offset=(0, -hole_offset),(-hole(offset=(0, -hole(offset=(0, -hole(offset=(0, -hole(offset=(0, -hole(offset=(0, -hole(offset=(0, -hole(offset=(0, -hole(offset=(0, -hole(offset=(0, -hole_offset),(-hole(offset=(0, -holehole_offset),(-holehole_offset, -hole_offset),(-holehole_offset, -hole_offset),(-holehole_offset, - hole_offset),(-holehole_offset, - hole_offset),(-holehole_offset, - hole_offset)
    .translate((0, -hole_offset),(-holehole_offset, - hole_offset),(-holehole_offset, - hole_offset)
    .translate((