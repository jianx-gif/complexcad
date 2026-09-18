import cadquery as cq

outer_radius = 80.0
outer_radius = 30.0
wall_thickness = 2.0
wall_thickness = 4.0
wall_thickness = 3.0
wall_thickness = 2.0
hole_diameter = 2.0
hole_spacing = 20.0
hole_spacing = 20.0
hole_spacing = 2.0
hole_spacing = 2.0
hole_spacing = 2.0
hole_spacing = 2.0
hole_spacing = 2.0
hole_spacing = 2.0

hole_spacing = 2.0

hole_spacing = 0.5
hole_spacing = 0.5
hole_spacing = 0.5
hole_spacing = 0.5
hole_spacing = 0.5
hole_spacing = 0.5
hole_spacing = 0.5
hole_spacing = 0.5
hole_spacing = 0.5
hole_offset = 0.5

hole_offset = 0.5

result = (
    cq.Workplane('XY')
    .box(outer_radius, outer_height, handle_height)
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
    .translate((0, 0, 0), (0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0)
    .translate((0, 0, (0, 0, 0), 0, 0), 0, 0), 0, 0), 0, 0), (0, 0), (0, 0, 0), (0, 0, 0), (0, 0, (0, 0, 0