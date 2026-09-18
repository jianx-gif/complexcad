import cadquery as cq

outer_radius = 80.0
outer_radius = 30.0
wall_thickness = 20.0
wall_thickness = 12.0
wall_thickness = 2.0
wall_thickness = 4.0
wall_thickness = 1.0
wall_thickness = 2.0
hole_count = 20.0
hole_spacing = 20.0
hole_count = 15.0
hole_count = 15.0
hole_count = 20.0
hole_depth = 20.0
hole_positions = 12.0
hole_positions = 20.0
hole_positions = 20.0
hole_positions = 12.0
hole_positions = 20.0
hole_positions = 20.0
hole_positions = 20.0
hole_positions = 12.0
hole_positions = 20.0
hole_positions = 20.0
hole_positions = 20.0
hole_positions = 12.0
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

hole_offset = cq.Workplane('XY').circle(outer_radius).circle(hole_offset, hole_offset)
hole_offset = outer_hole_offset)
hole_offset = - (hole_offset, hole_offset)
hole_offset = - (hole_offset, hole_offset)
hole_offset = - (hole_offset, hole_offset)
hole_offset = - (hole_offset, hole_offset)
hole_offset = - (hole_offset, hole_offset)
hole_offset = - (hole_offset, hole_offset)
result = (
    cq.Workplane('XY')
    .circle(hole_offset)
    .extrude(hole_depth)
)
