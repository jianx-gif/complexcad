import cadquery as cq

outer_radius = 80.0
outer_radius = 20.0
wall_thickness = 8.0
wall_thickness = 4.0
wall_thickness = 2.0
chamfer_distance = 1.0
hole_diameter = 2.0
hole_spacing = 20.0
hole_spacing = 12.0
hole_spacing = 20.0
hole_spacing = 20.0
hole_spacing = 12.0
hole_spacing = 20.0
hole_spacing = 20.0
hole_spacing = 20.0
hole_spacing = 20.0
hole_spacing = 20.0
hole_spacing = 20.0
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

hole_offset = 0.5

result = (
    cq.Workplane('XY')
    .box(outer_length, outer_height, outer_height)
    .faces('>Z')
    .workplane()
    .rect(outer_length, outer_height)
    .extrude(outer_height)
)
