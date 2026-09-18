import cadquery as cq

outer_diameter = 80.0
outer_diameter = 40.0
outer_diameter = 20.0
outer_diameter = 8.0
outer_diameter = 1.0
outer_diameter = 2.0
outer_diameter = 1.0
hole_diameter = 2.0
hole_count = 12
hole_count = 20.0
hole_count = 12
hole_count = 12
hole_count = 20.0
hole_spacing = 20.0
hole_spacing = 20.0
hole_spacing = 20.0
hole_spacing = 20.0
hole_spacing = 20.0
hole_spacing = 12.0
hole_spacing = 2.0
hole_spacing = 12.0
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.5

hole_offset = 0.5

hole_offset = 0.5

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
    (hole_offset, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, 0)
    .close()
    .revolve(outer_radius, 0)
    .extrude(outer_radius)
)

hole_offset = (outer_radius, 0, 0), (hole_offset, 0)])
    .hole(offset=(outer_radius, 0, 0), (hole_offset, 0)])
    .hole(offset=(outer_radius, 0, 0), (hole_offset, 0)])
    .hole(offset=(outer_radius, 0, 0), (hole_offset, 0)])
    .close()
)

result = (
    cq.Workplane('XY')
    .center(outer_radius, 0)
    .extrude(outer_radius)
    .translate((outer_radius, 0)
)
